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

def canonize_indels(muts):
    cleaned_mut_list = []
    if not isinstance(muts, str):
        return muts
    
    for mut in muts.split(' + '):
        if 'del' in mut or 'Δ' in mut:
            pos = int(''.join([_ for _ in mut if _.isdigit()]))
            mut = f'Δ{pos}'
        cleaned_mut_list.append(mut)
    return ' + '.join(cleaned_mut_list)

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

def estimate_exposures(desc):
    desc_to_exposures = {
         'Alpha':1,
         'Beta':1,
         'Delta':1,
         'Epsilon':1,
         'Gamma':1,
         'Iota':1,
         'Lambda':1,
         'Mu':1,
         'Zeta':1,
         'D.2':1,
         'Omicron/BA.1':2,
         'Omicron/BA.1.1':2,
         'Omicron/BA.2':2,
         'Omicron/BA.2.75':2,
         'Omicron/BA.4':2,
         'Omicron/BA.4_or_BA.5':2,
         'Omicron/BA.5':2,
         'Omicron/XBB.1':2,
         'Omicron_BA.5_or_BF.7':2,
         'L452R variants':2,
         'Unknown variant':1,
         'Wild Type':1,
         'B.1.36.27':1,
         'Conv_WT':1,
         'Conv_Delta':1,
         'Vac_Pfiz':2,
         'Vac_Mod':2,
         'Boost_Pfiz':3,
         'Boost_Mod':3,
         'Bi-valent Boost':3,
         'BTI_Delta':3,
         'BTI_BA.1':3,
         'BTI_BA.2.12.1':3,
         'BTI_BA.4/5':3
    }
    
    return desc_to_exposures[desc]

# def load_plasma_lite():
#     vp = pd.concat([pd.read_csv('../../data/CoVDB/datasheet_vp.csv').rename(columns={'Mutation':'Mutations'}), 
#                     pd.read_csv('../../data/CoVDB/datasheet_vp_varmut.csv').rename(columns={'Variant: Mutations':'Mutations', 'Variant: Pos':'Mutation: Pos'})])

#     cp = pd.concat([pd.read_csv('../../data/CoVDB/datasheet_cp.csv').rename(columns={'Mutation':'Mutations'}), 
#                     pd.read_csv('../../data/CoVDB/datasheet_cp_varmut.csv').rename(columns={'Variant: Mutations':'Mutations', 'Variant: Pos':'Mutation: Pos'})])

#     # Create a super-df for all plasma types
#     vp['Plasma'] = 'Vaccine'; vp['Infection (CP)'] = ''
#     cp['Plasma'] = 'Convalescent'; cp['Pre-vaccine Infection'] = ''; cp['Vaccine'] = ''; cp['# Shots'] = 0
#     plasma = pd.concat([vp, cp])

#     # Clean data
#     plasma = plasma[plasma['Fold Reduction: Cmp']=='=']
#     plasma = plasma[plasma['Mutations']!='(Various)']
#     # plasma = plasma[plasma['# Results']==1]
#     plasma = plasma[plasma['Control']=='Wild Type (B.1)']
#     plasma = plasma[plasma['Host']=='Human']
#     plasma = plasma[~(plasma['Mutations']=='(WT)')]
#     plasma['Vaccine'] = plasma['Vaccine'].apply(lambda x: 'None' if x=='' or pd.isna(x) else x)
#     plasma['Pre-vaccine Infection'] = plasma['Pre-vaccine Infection'].apply(lambda x: 'None' if x=='' or pd.isna(x) else x)
#     plasma['Infection (CP)'] = plasma['Infection (CP)'].apply(lambda x: 'None' if x=='' or pd.isna(x) else x)
#     plasma['Mutations'] = plasma['Mutations'].apply(lambda x: expand_indels(x))
#     plasma = plasma.sort_values(by='Fold Reduction: Median').reset_index(drop=True)

#     # Aggregate to coarse pools
#     coarse_pools = pd.read_csv('../../data/CoVDB/coarse_pools.csv')
#     coarse_pools = {row['Fine pool']: row['Coarse pool'] for _, row in coarse_pools.iterrows()}
#     plasma['Pool'] = plasma.apply(lambda row: row['Vaccine'] if row['Vaccine'] != 'None' else row['Infection (CP)'], axis=1)
#     plasma['Pool'] = plasma['Pool'].apply(lambda x: coarse_pools[x])

#     plasma['Base Voc'] = plasma['Variant'].apply(lambda x: extract_basevoc(str(x)))


#     # Convert fold reduction to log fold reduction
#     plasma['Log fold reduction'] = np.log10(plasma['Fold Reduction: Median'])

#     # Drop unnecessary columns
#     plasma_lite = plasma.drop(columns=['Reference', 'Reference: DOI', 'Section', 'Host', 
#                                        'Control', 'Control: NT50 Cmp', 'Control: NT50 GeoMean', 'Control: NT50 GSD', 
#                                        'Fold Reduction: Cmp', 'Potency: NT50 Cmp', 'Potency: NT50 GeoMean', 'Potency: NT50 GSD',
#                                        #'Variant', 'Mutation: Pos'#, 'Infection (CP)', 'Vaccine'
#                                        ]
#                         ).reset_index(drop=True
#                         ).rename(columns={'index':'ID'})
    
#     return plasma_lite
def load_covrdb():
    vp = pd.concat([pd.read_csv('../../data/CoVDB/datasheet_vp.csv').rename(columns={'Mutation':'Mutations'}), 
                    pd.read_csv('../../data/CoVDB/datasheet_vp_varmut.csv').rename(columns={'Variant: Mutations':'Mutations', 'Variant: Pos':'Mutation: Pos'})])

    cp = pd.concat([pd.read_csv('../../data/CoVDB/datasheet_cp.csv').rename(columns={'Mutation':'Mutations'}), 
                    pd.read_csv('../../data/CoVDB/datasheet_cp_varmut.csv').rename(columns={'Variant: Mutations':'Mutations', 'Variant: Pos':'Mutation: Pos'})])

    # Create a super-df for all plasma types
    vp['Plasma'] = 'Vaccine'; vp['Infection (CP)'] = ''; vp['Exposures'] = vp['# Shots'] + ~vp['Pre-vaccine Infection'].isna() # same as 1 if ~True, 0 if ~False
    cp['Plasma'] = 'Convalescent'; cp['Pre-vaccine Infection'] = ''; cp['Vaccine'] = ''; cp['Exposures'] = cp['Infection (CP)'].apply(lambda x: estimate_exposures(x))
    plasma = pd.concat([vp, cp])

    ### Clean data ###
    # Subset to clean rows
    plasma = plasma[plasma['Fold Reduction: Cmp']=='=']
    plasma = plasma[plasma['Mutations']!='(Various)']
    # plasma = plasma[plasma['# Results']==1]
    plasma = plasma[plasma['Control']=='Wild Type (B.1)']
    plasma = plasma[plasma['Host']=='Human']
    plasma = plasma[~(plasma['Mutations']=='(WT)')]
    # Handle Nones
    plasma['Vaccine'] = plasma['Vaccine'].apply(lambda x: 'None' if x=='' or pd.isna(x) else x)
    plasma['Pre-vaccine Infection'] = plasma['Pre-vaccine Infection'].apply(lambda x: 'None' if x=='' or pd.isna(x) else x)
    plasma['Infection (CP)'] = plasma['Infection (CP)'].apply(lambda x: 'None' if x=='' or pd.isna(x) else x)
    # Expand indels
    plasma['Mutations'] = plasma['Mutations'].apply(lambda x: expand_indels(x))
    # Get Base VoC
    plasma['Base Voc'] = plasma['Variant'].apply(lambda x: extract_basevoc(str(x)))
    # Sort by fold reduction and take log
    plasma = plasma.sort_values(by='Fold Reduction: Median').reset_index(drop=True)
    plasma['Log fold reduction'] = np.log10(plasma['Fold Reduction: Median'])
    
    
    ### Gather features ###
    plasma['Pool'] = plasma.apply(lambda row: row['Vaccine'] if row['Vaccine'] != 'None' else row['Infection (CP)'], axis=1)
    
    # Drop unnecessary columns
    plasma_lite = plasma.drop(columns=['Reference', 'Reference: DOI', 'Section', 'Host', 
                                       'Control', 'Control: NT50 Cmp', 'Control: NT50 GeoMean', 'Control: NT50 GSD', 
                                       'Fold Reduction: Cmp', 'Potency: NT50 Cmp', 'Potency: NT50 GeoMean', 'Potency: NT50 GSD'
                                       #'Variant', 'Mutation: Pos'#, 'Infection (CP)', 'Vaccine'
                                       ]
                        ).reset_index(drop=True
                        ).rename(columns={'index':'ID'})
    
    return plasma_lite

def load_cepi():
    # Neutralization
    data_dir = '../../data/Supp_Material/'
    filename = 'Supp_TableS6_Neutralization_Data.csv'
    neutralization = pd.read_csv(data_dir+filename)
    neutralization = pd.melt(neutralization, id_vars='Name').rename(columns={'variable':'Pool', 'value':'Neutralization'})   # unpivot data
    neutralization['Name'] = neutralization['Name'].apply(lambda x: x.capitalize() if x.islower() else x)   # clean up names to make sure VoCs match
    neutralization['Neutralization'] = pd.to_numeric(neutralization['Neutralization'].apply(lambda x: 10 if x=='<20' else x))   # impute limits of detection
    # Scale - neutralization relative to WuG WT
    norm = neutralization['Neutralization'][neutralization['Name']=='WuG'].mean()
    neutralization['Neutralization'] = norm / neutralization['Neutralization']
    # Rename pools
    neutralization['Pool'] = neutralization['Pool'].apply(lambda x: x if x=='Bi-valent Boost' else x.split('-')[0])
    # Add in Base VoC
    neutralization = pd.merge(neutralization,
                              pd.read_csv(data_dir+'Supp_TableS4_Infectivity_Data.csv', usecols=['Name', 'base_voc']).replace('BA.4/5', 'BA.5'),
                              on='Name')
    # Log neutralization
    neutralization['Log fold reduction'] = np.log10(neutralization['Neutralization'])
    neutralization['Fold Reduction: Median'] = neutralization['Neutralization']
    # Rename columns
    neutralization = neutralization.rename(columns={'Name - Construct':'Name', 'base_voc':'Base Voc'})
    neutralization = neutralization[['Name', 'Base Voc', 'Pool', 'Log fold reduction', 'Fold Reduction: Median']].drop_duplicates().reset_index(drop=True)
    # Add exposures
    pool_to_exposures = {
        'Conv_WT':1,
        'Conv_Delta':1,
        'Vac_Pfiz':2,
        'Vac_Mod':2,
        'Boost_Pfiz':3,
        'Boost_Mod':3,
        'Bi-valent Boost':3,
        'BTI_Delta':3,
        'BTI_BA.1':3,
        'BTI_BA.2.12.1':3,
        'BTI_BA.4/5':3
    }
    neutralization['Exposures'] = neutralization['Pool'].apply(lambda x: pool_to_exposures[x])

    # Mutations
    filename = 'construct_mutations.csv'
    cols = ['Name', 'All mutations']
    mutations = pd.read_csv(data_dir+filename, usecols=cols).rename(columns={'All mutations':'Mutations'})
    mutations['Name'] = mutations['Name'].apply(lambda x: x.capitalize() if x.islower() else x)    # name VoCs consistently
    mutations['Mutations'] = mutations['Mutations'].apply(lambda x: x.replace(' ', ''))    # remove any spaces between mutations in the list
    # Remove D614G
    mutations['Mutations'] = mutations['Mutations'].apply(lambda x: x.replace('D614G,',''))
    mutations['Mutations'] = mutations['Mutations'].apply(lambda x: x.replace(',D614G',''))
    mutations['Mutations'].loc[mutations['Name']=='WuG'] = None
    mutations = pd.concat([mutations, pd.DataFrame([{'Name':'WT', 'Mutations':None}])])
    # Clean
    mutations = mutations[mutations['Mutations']!='--']

    df = neutralization.merge(mutations, on='Name', how='inner').drop_duplicates()
    df = df.sort_values(by='Log fold reduction').reset_index(drop=True)
    return df
    

def subset_plasma_lite(plasma_lite):
    plasma_lite = plasma_lite[plasma_lite['Most recent variant']!='unknown'].reset_index(drop=True)
    
    pool_counts = plasma_lite.groupby('Most recent variant').agg('count')
    kept_pools = pool_counts[(pool_counts>20).any(axis=1)].index
    
    plasma_lite = plasma_lite[plasma_lite['Most recent variant'].apply(lambda x: x in kept_pools)].reset_index(drop=True)
        
    return plasma_lite
    
def load_plasma_lite():
    covrdb = load_covrdb()
    cepi = load_cepi()
    cepi['Assay'] = 'Pseudovirus (lentivirus)'
    cepi['Months'] = '2-6m'   # this is just a best guess... idrk what to say
    immune_histories = pd.read_csv('../../data/immune_histories.csv')
    
    plasma = pd.concat([covrdb, cepi])
    plasma = pd.merge(plasma, immune_histories, on='Pool').drop(columns=['Notes (type of vaccine, number of doses, strain used/infected)', 
                                                                         'Vaccine type series', 'Vaccine type overall', 'History variants'])
    
    # Serum type
    plasma = plasma.rename(columns={'Plasma type':'Serum'})
    # Exposures
    plasma['Exposures'] = plasma.apply(lambda x: '>2' if x['Exposures']>2 else '<=2', axis=1)
    # Clean up WT nomenclature
    plasma['Most recent variant'] = plasma['Most recent variant'].apply(lambda x: 'B.1' if x in ['WT', 'Wild Type'] else x)
    # Canonize indels
    plasma['Mutations'] = plasma['Mutations'].apply(canonize_indels)
    plasma = subset_plasma_lite(plasma)
    
    return plasma    
