# -*- coding: utf-8 -*-
"""
Created on Fri May 28 11:17:32 2021

@author: mateu
"""
import pandas as pd
import math

# O parametro é um array: [probabilidade de sim, probabilidade de não, ...]
def calc_entropy(array_perc_tuples):
    value = 0
    for element in array_perc_tuples:
        if element != 0:
            value += (element * math.log2(element))
    return -value

def calc_gain(feature, df_target, return_map=False):
    total_feature = len(df_target)
    gain_value = 0
    mapping = {}
    mapping['entropy_values'] = {}
    for value in feature.unique():
        probability = []
        probability_target = []
        for target in df_target.unique():
            total_value = (feature == value).sum()
            
            probability.append((((feature == value) & (df_target == target)).sum()) / total_value)
            probability_target.append((df_target == target).sum() / total_feature)
        
        entropy = calc_entropy(probability)
        entropy_target = calc_entropy(probability_target)
        #mapping['probability'][value] = probability
        mapping['entropy_values'][value] = entropy
        
        gain_value += ((feature == value).sum() / total_feature) * entropy
    
    mapping['gain'] = (entropy_target - gain_value)
    mapping['entropy_target'] = entropy_target
    
    if return_map:
        return mapping
    
    return entropy_target - gain_value

def calc_all_base_gain(df, target, limit_vals=5):
    mapping = {}
    
    for feature in df.columns:
        if df[feature].unique().shape[0] <= limit_vals:
            print('Processing: {}'.format(feature))
            mapping[feature] = calc_gain(df[feature], target, return_map=True)
            
    return mapping


if __name__ == '__main__':
    df = pd.read_csv('data.csv')
    mapping = calc_all_base_gain(df, df['Jogar Tênis'])