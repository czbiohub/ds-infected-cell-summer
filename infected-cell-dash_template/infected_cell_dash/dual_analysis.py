import numpy as np
import pandas as pd
import os
from collections import Counter
import plotly.express as px

def file(virus):
    for subdir, dirs, files in os.walk('/Users/elianna.kondylis/final_nextflow_output/output_072321/'):
        for filename in files:        
            filepath = subdir + os.sep + filename
            if filepath.endswith("gene_summary.txt") and virus in filepath:          
                return filepath
            
def host_factors(f1):
    dict_genes = {}
    df1  = pd.read_csv(f1, sep = '\t')
    df1['id'] = df1['id'].str.upper()
    df1 = df1.set_index('id')
    dict1 = df1.to_dict(orient = 'index')
    for key in dict1:
        dict_genes[key] = -np.log(dict1[key]['pos|score'])
    k = Counter(dict_genes)
    dict_mostcommon = dict(k.most_common(500))
    return dict_genes, dict_mostcommon

virus_list = ['DENV', 'EV', 'HAV', 'HCV', 'RV', 'Wang_229E', 'Wang_OC43', 'Wang_SARS-CoV2']

file_list = list()
for virus in virus_list:
    file_list.append(file(virus))

sig_genes = list()
combined = list()
for file in file_list:
    dict_genes, dict_mostcommon = host_factors(file)
    sig_genes.append([*dict_mostcommon.keys()])
    combined.append(dict_mostcommon)
mul_vir = dict(zip(virus_list, sig_genes))
tot_vir = dict(zip(virus_list, combined))

def comparo(tot_vir, vir1, vir2):
    
    l1 = list()
    l2 = list()

    for key in tot_vir[vir1]:
        if key in tot_vir[vir2]:
            l1.append(tot_vir[vir1][key])
            l2.append(tot_vir[vir2][key])
    return l1,l2

def ratio(l1, l2):
    assert len(l1) == len(l2)
    count = 0
    for i in range(len(l1)):
            if 0.9 <= float(l1[i])/float(l2[i]) <= 1.1:
                count += 1
    return(count, len(l1))

abbrev = dict()
abbrev['DENV'] = 'Dengue'
abbrev['HAV'] = 'Hepatitis A'
abbrev['HCV'] = 'Hepatitis C'
abbrev['RV'] = 'Rhinovirus'
abbrev['Wang_229E'] = 'HCoV 229E'
abbrev['Wang_OC43'] = 'HCoV OC43'
abbrev['Wang_SARS-CoV2'] = 'SARS-CoV-2'

def final_comparison(vir1, vir2, tot_vir):
    l1, l2 = comparo(tot_vir, vir1, vir2)
    count, total = ratio(l1, l2)
    #fig = px.scatter(x=l1, y=l2, labels=dict(x=str(vir1)+' pos|score', y=str(vir2)+' pos|score'), title = 'Comparing pos|score of ' + str(vir1) +  ' and ' + str(vir2))
    return l1, l2