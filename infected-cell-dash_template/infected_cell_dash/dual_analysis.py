import numpy as np
import pandas as pd
import os
from collections import Counter
import plotly.express as px

class DualAnalysis:
    def __init__(self, output_path):
        self.output_path = output_path

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
        dict_mostcommon = dict(k.most_common(500))
        return dict_genes, dict_mostcommon

    @staticmethod
    def comparo(tot_vir, vir1, vir2):
        l1 = list()
        l2 = list()

        for key in tot_vir[vir1]:
            if key in tot_vir[vir2]:
                l1.append(tot_vir[vir1][key])
                l2.append(tot_vir[vir2][key])
        return l1,l2

    @staticmethod
    def ratio(l1, l2):
        assert len(l1) == len(l2)
        count = 0
        for i in range(len(l1)):
                if 0.9 <= float(l1[i])/float(l2[i]) <= 1.1:
                    count += 1
        return(count, len(l1))

    def final_comparison(self, vir1, vir2, tot_vir):
        l1, l2 = self.comparo(tot_vir, vir1, vir2)
        count, total = self.ratio(l1, l2)
        #fig = px.scatter(x=l1, y=l2, labels=dict(x=str(vir1)+' pos|score', y=str(vir2)+' pos|score'), title = 'Comparing pos|score of ' + str(vir1) +  ' and ' + str(vir2))
        return l1, l2