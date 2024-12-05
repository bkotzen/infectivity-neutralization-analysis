## Utility functions
import pandas as pd
import re
import numpy as np
import torch

def one_hot(mutations: pd.Series, args):
    features = sorted(list(set(' + '.join(filter(None, mutations.tolist())).split(' + '))))
    onehot = [[1 if mut.strip() in str(muts) else 0 for mut in features] for muts in mutations]
    
    return torch.tensor(onehot, dtype=args.dtype), features

def expand_indels(mutations):
    mutations = mutations.split(' + ')
    expanded_mutations = []
    for i, mut in enumerate(mutations):
        match = re.match(r'Δ(\d+)-(\d+)', mut)
        if match:
            mutations.pop(i)
            x, z = int(match.group(1)), int(match.group(2))
            indels = [f'Δ{i}' for i in range(x, z + 1)]
            expanded_mutations += indels
        else:
            expanded_mutations.append(mut)
    return ' + '.join(expanded_mutations)

def extract_basevoc(varmut):
    greek_letters = ['alpha', 'beta', 'gamma', 'delta', 'epsilon', 'zeta', 'eta', 
                     'theta', 'iota', 'kappa', 'lambda', 'mu', 'nu', 'xi', 'omicron', 
                     'pi', 'rho', 'sigma', 'tau', 'upsilon', 'phi', 'chi', 'psi', 'omega',
                     'None', 'NaN']
    # Should find a way to parse common pango lineages to greek letters (e.g. B.1.617, B.1.117, etc.)
    varmut = 'None' if varmut=='' else varmut
    match = next((letter.capitalize() for letter in greek_letters if letter in varmut.lower()), 'Unknown')
    if match in ['NaN', 'None']:
        match = 'Wild Type'
    return match


def load_plasma_lite():
    vp = pd.concat([pd.read_csv('../../data/CoVDB/datasheet_vp.csv').rename(columns={'Mutation':'Mutations'}), 
                    pd.read_csv('../../data/CoVDB/datasheet_vp_varmut.csv').rename(columns={'Variant: Mutations':'Mutations', 'Variant: Pos':'Mutation: Pos'})])

    cp = pd.concat([pd.read_csv('../../data/CoVDB/datasheet_cp.csv').rename(columns={'Mutation':'Mutations'}), 
                    pd.read_csv('../../data/CoVDB/datasheet_cp_varmut.csv').rename(columns={'Variant: Mutations':'Mutations', 'Variant: Pos':'Mutation: Pos'})])

    # Create a super-df for all plasma types
    vp['Plasma'] = 'Vaccine'; vp['Infection (CP)'] = ''
    cp['Plasma'] = 'Convalescent'; cp['Pre-vaccine Infection'] = ''; cp['Vaccine'] = ''; cp['# Shots'] = 0
    plasma = pd.concat([vp, cp])

    # Clean data
    plasma = plasma[plasma['Fold Reduction: Cmp']=='=']
    plasma = plasma[plasma['Mutations']!='(Various)']
    # plasma = plasma[plasma['# Results']==1]
    plasma = plasma[plasma['Control']=='Wild Type (B.1)']
    plasma = plasma[plasma['Host']=='Human']
    plasma = plasma[~(plasma['Mutations']=='(WT)')]
    plasma['Vaccine'] = plasma['Vaccine'].apply(lambda x: 'None' if x=='' or pd.isna(x) else x)
    plasma['Pre-vaccine Infection'] = plasma['Pre-vaccine Infection'].apply(lambda x: 'None' if x=='' or pd.isna(x) else x)
    plasma['Infection (CP)'] = plasma['Infection (CP)'].apply(lambda x: 'None' if x=='' or pd.isna(x) else x)
    plasma['Mutations'] = plasma['Mutations'].apply(lambda x: expand_indels(x))
    plasma = plasma.sort_values(by='Fold Reduction: Median').reset_index(drop=True)

    # Aggregate to coarse pools
    coarse_pools = pd.read_csv('../../data/CoVDB/coarse_pools.csv')
    coarse_pools = {row['Fine pool']: row['Coarse pool'] for _, row in coarse_pools.iterrows()}
    plasma['Pool'] = plasma.apply(lambda row: row['Vaccine'] if row['Vaccine'] != 'None' else row['Infection (CP)'], axis=1)
    plasma['Pool'] = plasma['Pool'].apply(lambda x: coarse_pools[x])

    plasma['Base Voc'] = plasma['Variant'].apply(lambda x: extract_basevoc(str(x)))


    # Convert fold reduction to log fold reduction
    plasma['Log fold reduction'] = np.log10(plasma['Fold Reduction: Median'])

    # Drop unnecessary columns
    plasma_lite = plasma.drop(columns=['Reference', 'Reference: DOI', 'Section', 'Host', 
                                       'Control', 'Control: NT50 Cmp', 'Control: NT50 GeoMean', 'Control: NT50 GSD', 
                                       'Fold Reduction: Cmp', 'Potency: NT50 Cmp', 'Potency: NT50 GeoMean', 'Potency: NT50 GSD',
                                       #'Variant', 'Mutation: Pos'#, 'Infection (CP)', 'Vaccine'
                                       ]
                        ).reset_index(drop=True
                        ).rename(columns={'index':'ID'})
    
    return plasma_lite
