import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import os
from collections import Counter
from plotly.subplots import make_subplots
from pathlib import Path

class Heatmap:
    def __init__(self, output_path, pickle_path):
        self.output_path = output_path
        self.pickle_path = pickle_path

        self.virus_list = ['DENV', 'EV', 'HAV', 'HCV', 'RV', 'Wang_229E', 'Wang_OC43', 'Wang_SARS-CoV2']
        
        file_list = list()
        for virus in self.virus_list:
            file_list.append(self.file(virus))
        
        self.sig_genes = list()
        self.combined = list()

        for file in file_list:
            dict_genes, dict_mostcommon = self.host_factors(file)
            self.sig_genes.append([*dict_mostcommon.keys()])
            self.combined.append(dict_mostcommon)

        self.mul_vir = dict(zip(self.virus_list, self.sig_genes))
        self.tot_vir = dict(zip(self.virus_list, self.combined))

        self.abbrev = dict()
        self.abbrev['DENV'] = 'Dengue'
        self.abbrev['HAV'] = 'Hepatitis A'
        self.abbrev['HCV'] = 'Hepatitis C'
        self.abbrev['RV'] = 'Rhinovirus'
        self.abbrev['Wang_229E'] = 'HCoV 229E'
        self.abbrev['Wang_OC43'] = 'HCoV OC43'
        self.abbrev['Wang_SARS-CoV2'] = 'SARS-CoV-2'

    def file(self, virus):
        for subdir, dirs, files in os.walk(self.output_path):
            for filename in files:        
                filepath = subdir + os.sep + filename
                if filepath.endswith("gene_summary.txt") and virus in filepath:          
                    return filepath

    #GSEAPY analysis outputs all genes in all caps, even if I inputted them lower case. Affects the genes which begin with HSA-MIR and others
    #Easy fix just made my input genes all caps too            

    @staticmethod
    def host_factors(f1):
        dict_genes = {}
        df1  = pd.read_csv(f1, sep = '\t')
        df1['id'] = df1['id'].str.upper()
        df1 = df1.set_index('id')
        dict1 = df1.to_dict(orient = 'index')
        for key in dict1:
            dict_genes[key] = -np.log(dict1[key]['pos|score'])
        k = Counter(dict_genes)
        dict_mostcommon = dict(k.most_common(30))
        return dict_genes, dict_mostcommon

    def my_path(self):
        path_dict = dict()
        for virus in self.virus_list:
            path_dict[virus] = self.pickle_path + str(virus) + os.sep + virus + '.pkl'
        return path_dict

    @staticmethod
    def get_len(row):
        x = len(row)
        return x

    @staticmethod
    def new_input1(path_dict, my_input):
        vir1 = my_input[0]
        vir2 = my_input[1]
        df1 = pd.read_pickle(path_dict[vir1])
        df2 = pd.read_pickle(path_dict[vir2])
        return vir1, vir2, df1, df2

    def merge(self, df1, df2):
        temp_df = pd.merge(df1, df2, on = ['Term'], how = 'inner')
        if not temp_df.empty:
            temp_df['Shared_Genes'] = [list(set(a).intersection(set(b))) for a, b in zip(temp_df.Genes_x, temp_df.Genes_y)]
            #print(temp_df)
            combined_df = temp_df.loc[temp_df.Shared_Genes.str.len() >= 2].reset_index(drop=True)
            combined_df['Len'] = combined_df['Shared_Genes'].apply(self.get_len)
            return combined_df
        else:
            return pd.DataFrame()
    @staticmethod
    def my_max(df):
        return df['Len'].idxmax()

    @staticmethod
    def col_df(a, vir1, vir2, vir_dict, df):
        sig1 = list()
        sig2 = list()
        for gene in df['Shared_Genes'][a]:
            sig1.append(vir_dict[vir1][gene])
            sig2.append(vir_dict[vir2][gene])
        return sig1, sig2

    @staticmethod
    def heatmap(vir1, vir2, col1, col2):
        final_df = pd.DataFrame()
        final_df[vir1] = col1
        final_df[vir2] = col2
        
        return final_df



    def final(self, my_input, vir_dict):
        path_dict = self.my_path()
        vir1, vir2, df1, df2 = self.new_input1(path_dict, my_input)
        combined_df = self.merge(df1, df2)
        if combined_df.empty:
            return pd.DataFrame(), 0, combined_df
        else:
            a = self.my_max(combined_df)
            col1, col2 = self.col_df(a, vir1, vir2, vir_dict, combined_df)
            final_df = self.heatmap(vir1, vir2, col1, col2)
            return final_df, a, combined_df

    #final(my_input, tot_vir)