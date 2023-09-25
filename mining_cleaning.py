import pandas as pd
import numpy as np

from rdkit import Chem
from rdkit.Chem import Lipinski, Descriptors


def drop_columns(df_lst: list, columns_lst: list) -> list:
    """The function removes in each dataframe in df_lst certain columns from columns_lst"""
    
    assert len(df_lst) == len(columns_lst), 'len(df_lst) != len(columns_lst)'
    
    # Delete in a loop
    for i in range(len(df_lst)):
        df_lst[i] = df_lst[i].drop(columns_lst[i], axis=1)
        
    return df_lst


def fill_df_descriptors(df_old: pd) -> pd:
    """Returns a dataframe with descriptors. Function needed to work with drug_descriptors.csv"""
    
    descriptors_lst = []
    
    for smiles in df_old.smiles:
        compound = Chem.MolFromSmiles(smiles)
        
        descriptors_lst.append([Lipinski.NumHDonors(compound), Lipinski.NumHAcceptors(compound), Lipinski.NumHeteroatoms(compound),
                                Descriptors.ExactMolWt(compound), Descriptors.MaxAbsPartialCharge(compound), Descriptors.MaxPartialCharge(compound),
                                Descriptors.MinAbsPartialCharge(compound), Descriptors.MinPartialCharge(compound), Lipinski.NumRotatableBonds(compound),
                                Lipinski.NumAromaticRings(compound), Lipinski.NumAromaticHeterocycles(compound)])
        
    # Common descriptor dataframe    
    df_descriptors = pd.DataFrame(descriptors_lst, columns=['NumHDonors', 'NumHAcceptors', 'NumHeteroatoms',
                                                            'ExactMolWt', 'MaxAbsPartialCharge', 'MaxPartialCharge', 
                                                            'MinAbsPartialCharge', 'MinPartialCharge', 'NumRotatableBonds',
                                                            'NumAromaticRings', 'NumAromaticHeterocycles'])
    # Merge and get the final dataset
    df_new = pd.concat([df_old, df_descriptors], axis=1)
        
    return df_new


def zip_data(df_main: pd, df_drug: pd, df_bacterial: pd) -> pd:
    """The function merges all datasets"""
    
    # Merger with drug
    df_drug_temporary = pd.DataFrame(columns=df_drug.columns[1:])
    df_drug_temporary_nan = pd.DataFrame(np.nan, index=[0], columns=df_drug.columns[1:])
    
    for drug in df_main['Drug']:
        if not(drug in list(df_drug['drug'])):
            df_drug_temporary = pd.concat([df_drug_temporary, df_drug_temporary_nan], axis=0)
        else:
            df_drug_temporary = pd.concat([df_drug_temporary, df_drug[df_drug['drug'] == drug][list(df_drug.columns[1:])]], axis=0)
            
    # Updating the indexes        
    df_drug_temporary.reset_index(drop=True, inplace=True)
    
    # Merger with bacterial 
    df_bacterial_temporary = pd.DataFrame(columns=df_bacterial.columns[1:])
    df_bacterial_temporary_nan = pd.DataFrame(np.nan, index=[0], columns=df_bacterial.columns[1:])
    
    for bacteria in df_main['Bacteria']:
        if not(bacteria in list(df_bacterial['Bacteria'])):
            df_bacterial_temporary = pd.concat([df_bacterial_temporary, df_bacterial_temporary_nan], axis=0)
        else:
            df_bacterial_temporary = pd.concat([df_bacterial_temporary, df_bacterial[df_bacterial['Bacteria'] == bacteria][list(df_bacterial.columns[1:])]], axis=0)
            
    # Updating the indexes      
    df_bacterial_temporary.reset_index(drop=True, inplace=True)  
    
    # Merger all dataset's  
    df_result = pd.concat([df_main, df_drug_temporary, df_bacterial_temporary], axis=1)
    
    return df_result


def fix_string(df: pd, col: str) -> pd:
    """Removes double letters that follow each other in a dataset column.
    Also removes spaces and dots"""
    
    en_al2 = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n','o', 'p', 'q', 'r',
              's', 't', 'u', 'v', 'w', 'x', 'y', 'z', 'a', 'b', 'e', 'k', 'm', 'o', 'p', 'c', 't', 'x']
    
    en_al = []
    
    for i in range(len(en_al2)):
        en_al.append(en_al2[i] * 2)
        
    for i in range(len(en_al)):
        df[col] = df[col].str.replace(en_al[i],en_al2[i])
        
    df[col] = df[col].str.replace(' ','').str.lower()
    df[col] = df[col].str.replace('.','')
        
    return df
    

def type_converting(df: pd, columns_lst: list) -> pd:
    """Converts data types in columns"""
    
    dict_type = {}
    
    for col in columns_lst:
        dict_type[col] = np.float64
        
    df = df.astype(dict_type)
    
    return df



    
    
        
    
    