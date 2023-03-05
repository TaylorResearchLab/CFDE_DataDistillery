#!/usr/bin/env python
# coding: utf-8


import pandas as pd
import numpy as np



def reformat_eqtl_str(path):
    df = pd.read_csv(path,sep='\t')
    
    # if these columns exist rename them
    df = df.rename(columns={'subject_id':'subject','object_id':'object'})
    
    #print(df.iloc[158,:])
    for col in ['node_id','subject','object']:            
        if col in df.columns:
            print(f'Reformatting {col} column.')
            # extract all rows in the specified column that start with 'GTEX_EQTL'
            node_col = df[df[col].str.startswith('GTEX_EQTL')][col]

            # split the eqtl string at b38, everything after these characters is the tissue. also replace '-' w/ '_'
            split_node_col = node_col.str.replace('-','_').str.split('b38')

            # extract first part of string (eg. 'GTEX_EQTL eQTL_chr11_538371_G_A_')
            first_part_eqtl_str = [i[0] for i in split_node_col]

            # extract second part of string ((eg. '_Cells_Cultured_fibroblasts'))
            tissue_part_eqtl_str = [i[1] for i in split_node_col]

            # replace '_' with ' ' so we can use title() and then put '_' back in.
            # title() capitalizes first letter of each word (words must be seperated by spaces)
            tissue_str_fixed = [i.replace('_',' ').title().replace(' ','_') for i in tissue_part_eqtl_str]

            # join back together with the 'b38' in the middle.
            node_col_fixed = [i+'b38'+j for i,j in zip(first_part_eqtl_str,tissue_str_fixed) ]

            # reasign to dataframe
            df.loc[df[col].str.startswith('GTEX_EQTL'),col] = node_col_fixed
            print(f'Done Reformatting {col} column.')
    return df
