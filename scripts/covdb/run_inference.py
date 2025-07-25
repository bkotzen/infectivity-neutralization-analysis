## Run MCMC
import argparse
import torch
import pandas as pd
from datetime import datetime as dt
from tqdm import tqdm

from sklearn.preprocessing import LabelEncoder

import pyro
from pyro.infer import MCMC, NUTS

from utils import load_plasma_lite, subset_plasma_lite, one_hot
from model import model_MCMC_specσβ as model


def save_results(traces, mcmc_data, args):
    date = args.date
    results = dict()
    results['traces'] = traces
    results['data'] = mcmc_data
    
    outfile = f'../../model_covdb/results.{date}.sb{args.sb}.pt'
    torch.save(results, outfile)
    return results

def load_data(args):
    plasma_lite = load_plasma_lite()
    X, features = one_hot(plasma_lite['Mutations'], args)
    Y = torch.tensor(plasma_lite['Log fold reduction'].values, dtype=args.dtype)
    assert X.shape[0], X.shape[1] == [len(plasma_lite), len(features)]
    assert Y.shape[0] == len(plasma_lite)
    
    serum_type_encoder = LabelEncoder()
    assay_type_encoder = LabelEncoder()
    exposures_encoder = LabelEncoder()
    months_encoder = LabelEncoder()
    pool_encoder = LabelEncoder()
    
    serum_type_data = serum_type_encoder.fit_transform(plasma_lite['Plasma'])
    assay_type_data = assay_type_encoder.fit_transform(plasma_lite['Assay'])
    exposures_data = exposures_encoder.fit_transform(plasma_lite['Exposures'])
    months_data = months_encoder.fit_transform(plasma_lite['Months'])
    pools = pool_encoder.fit_transform(plasma_lite['Most recent variant'])
    
    print(f'Loaded {X.shape[0]} experiments across {X.shape[1]} mutations')
    print(f'\t{X.unique(dim=0).shape[0]} unique mutation profiles')
    print(f'\t{X.unique(dim=1).shape[1]} colinear mutation blocks')
    print('\t{} experimental conditions'.format(len(pd.DataFrame({'Assay type':assay_type_data,
                                                                  'Serum type':serum_type_data,
                                                                  'Exposures':exposures_data,
                                                                  'Months':months_data,
                                                                  'Pool':pools}).drop_duplicates())))

    return {'X':X,
            'Y':Y,
            'features':features,
            'serum_type_data':serum_type_data,
            'serum_type_map':serum_type_encoder.inverse_transform([i for i in range(len(set(serum_type_data)))]),
            'assay_type_data':assay_type_data,
            'assay_type_map':assay_type_encoder.inverse_transform([i for i in range(len(set(assay_type_data)))]),
            'exposures_data':exposures_data,
            'exposures_map':exposures_encoder.inverse_transform([i for i in range(len(set(exposures_data)))]),
            'months_data':months_data,
            'months_map':months_encoder.inverse_transform([i for i in range(len(set(months_data)))]),
            'pools':pools,
            'pools_map':pool_encoder.inverse_transform([i for i in range(len(set(pools)))])
            }
    
def run_mcmc(mcmc_data, args):
    pyro.clear_param_store()
    
    nuts_kernel = NUTS(model)

    mcmc = MCMC(nuts_kernel, num_samples=args.num_samples, warmup_steps=args.warmup_steps, num_chains=8, mp_context="spawn")
    mcmc.run(mcmc_data['X'], 
             mcmc_data['Y'], 
             mcmc_data['serum_type_data'], 
             mcmc_data['assay_type_data'],
             mcmc_data['exposures_data'],
             mcmc_data['months_data'],
             mcmc_data['pools'],
             args.sb)
    
    posterior_samples = mcmc.get_samples()
    
    # Save 
    results = save_results(posterior_samples, mcmc_data, args)
    
    return results

    
def main(args):
    torch.set_default_dtype(args.dtype)
    pyro.set_rng_seed(0)
    pyro.clear_param_store()
    
    # Load data
    mcmc_data = load_data(args)
    
    # Run mcmc
    results = run_mcmc(mcmc_data, args)
    

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--dtype", default="float32")
    parser.add_argument("--num-samples", type=int, default=500)
    parser.add_argument("--warmup-steps", type=int, default=500)
    parser.add_argument("-sb", type=float, default=.1, help="σ_β")
    args = parser.parse_args()
    args.dtype = eval('torch.'+args.dtype)
    args.date = dt.today().strftime('%Y-%m-%d')
    
    main(args)