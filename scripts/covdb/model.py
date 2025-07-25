## Define model(s)
import torch
import pyro
import pyro.distributions as dist

def model_MCMC(X, Y, plasma_type_data, assay_type_data, pools):
    
    # # Sample plasma type effects
    μ_P = 0.
    σ_P = 1.
    with pyro.plate('plasmas_plate', len(set(plasma_type_data))):
        P = pyro.sample('P', dist.Normal(μ_P, σ_P))
        
    # Sample assay type effects
    μ_A = 0.
    σ_A = 1.
    with pyro.plate('assays_plate', len(set(assay_type_data))):
        A = pyro.sample('A', dist.Normal(μ_A, σ_A))
        
    # Sample mutation specific effects
    μ_β = 0.
    σ_β = .1
    with pyro.plate('β_plate', X.shape[1]):
        β = pyro.sample('β', dist.Laplace(μ_β, σ_β))
        # Sample pool-specific mutation effects
        # σ_β_ω = .1*torch.ones(len(set(pools)), 1)
        σ_β_ω = pyro.sample('σ_β_ω', dist.LogNormal(0.1*torch.ones(X.shape[1]), 0.1))
        with pyro.plate('pooling', len(set(pools))):
            βdist = dist.Laplace(β, σ_β_ω)
            β_ω = pyro.sample('β_ω', βdist)
    
    # Make predictions
    prediction = torch.matmul(X, β_ω.transpose(1,0))[torch.arange(X.shape[0]),pools] + A[torch.tensor(assay_type_data)] + P[torch.tensor(plasma_type_data)]
    
    # Score observation
    σ = pyro.param("σ", dist.LogNormal(0, .01))
    with pyro.plate("data", X.shape[0]):
        test = dist.Normal(prediction, σ).sample()
        return pyro.sample("obs", dist.Normal(prediction, σ), obs=Y)
    
# def model_MCMC_specσβ(X, Y, plasma_type_data, assay_type_data, pools, σ_β):
    
#     # # Sample plasma type effects
#     μ_P = 0.
#     σ_P = 1.
#     with pyro.plate('plasmas_plate', len(set(plasma_type_data))):
#         P = pyro.sample('P', dist.Normal(μ_P, σ_P))
        
#     # Sample assay type effects
#     μ_A = 0.
#     σ_A = 1.
#     with pyro.plate('assays_plate', len(set(assay_type_data))):
#         A = pyro.sample('A', dist.Normal(μ_A, σ_A))
        
#     # Sample mutation specific effects
#     μ_β = 0.
#     # σ_β = .1   # specified in args
#     with pyro.plate('β_plate', X.shape[1]):
#         β = pyro.sample('β', dist.Laplace(μ_β, σ_β))
#         # Sample pool-specific mutation effects
#         # σ_β_ω = .1*torch.ones(len(set(pools)), 1)
#         σ_β_ω = pyro.sample('σ_β_ω', dist.LogNormal(0.1*torch.ones(X.shape[1]), 0.1))
#         with pyro.plate('pooling', len(set(pools))):
#             βdist = dist.Laplace(β, σ_β_ω)
#             β_ω = pyro.sample('β_ω', βdist)
    
#     # Make predictions
#     prediction = torch.matmul(X, β_ω.transpose(1,0))[torch.arange(X.shape[0]),pools] + A[torch.tensor(assay_type_data)] + P[torch.tensor(plasma_type_data)]
    
#     # Score observation
#     σ = pyro.param("σ", dist.LogNormal(0, .01))
#     with pyro.plate("data", X.shape[0]):
#         test = dist.Normal(prediction, σ).sample()
#         return pyro.sample("obs", dist.Normal(prediction, σ), obs=Y)

def model_MCMC_specσβ(X, Y, serum_type_data, assay_type_data, exposures_data, months_data, pools, σ_β):
    
    # # Sample plasma type effects
    μ_S = 0.
    σ_S = 1.
    with pyro.plate('sera_plate', len(set(serum_type_data))):
        S = pyro.sample('S', dist.Normal(μ_S, σ_S))
        
    # Sample assay type effects
    μ_A = 0.
    σ_A = 1.
    with pyro.plate('assays_plate', len(set(assay_type_data))):
        A = pyro.sample('A', dist.Normal(μ_A, σ_A))
        
    # Sample # exposures effects
    μ_E = 0.
    σ_E = 1.
    with pyro.plate('exposures_plate', len(set(exposures_data))):
        E = pyro.sample('E', dist.Normal(μ_E, σ_E))
        
    # Sample # months effects
    μ_M = 0.
    σ_M = 1.
    with pyro.plate('months_plate', len(set(months_data))):
        M = pyro.sample('M', dist.Normal(μ_M, σ_M))
        
    # Sample mutation specific effects
    μ_β = 0.
    # σ_β = .1   # specified in args
    with pyro.plate('β_plate', X.shape[1]):
        β = pyro.sample('β', dist.Laplace(μ_β, σ_β))
        # Sample pool-specific mutation effects
        # σ_β_ω = .1*torch.ones(len(set(pools)), 1)
        σ_β_ω = pyro.sample('σ_β_ω', dist.LogNormal(0.1*torch.ones(X.shape[1]), 0.1))
        with pyro.plate('pooling', len(set(pools))):
            βdist = dist.Laplace(β, σ_β_ω)
            β_ω = pyro.sample('β_ω', βdist)
    
    # Make predictions
    prediction = torch.matmul(X, β_ω.transpose(1,0))[torch.arange(X.shape[0]),pools] + \
                    S[torch.tensor(serum_type_data)] + \
                    A[torch.tensor(assay_type_data)] + \
                    E[torch.tensor(exposures_data)] + \
                    M[torch.tensor(months_data)]
    
    # Score observation
    σ = pyro.param("σ", dist.LogNormal(0, .01))
    with pyro.plate("data", X.shape[0]):
        test = dist.Normal(prediction, σ).sample()
        return pyro.sample("obs", dist.Normal(prediction, σ), obs=Y)