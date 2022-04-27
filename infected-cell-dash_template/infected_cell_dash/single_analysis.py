import plotly.express as px
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from collections import Counter
<<<<<<< HEAD
from plotly.subplots import make_subplots
from pathlib import Path
import name_dict
=======
>>>>>>> 4e0e39a5353fc3020c248428f8f9bac0718f689c


class SingleAnalysis:
<<<<<<< HEAD
    def __init__(self, data_path):
        self.data_path = data_path

    def file(self, virus):
        print(self.data_path)
        for subdir, dirs, files in os.walk(self.data_path):
            for filename in files:        
                filepath = subdir + os.sep + filename
                if filepath.endswith("gene_summary.txt") and virus in filepath:          
                    return filepath
    
    @staticmethod
    def top_hits(f1, num, metric):
        df  = pd.read_csv(f1, sep = '\t')
        df = df.rename(columns={'id':'Genes'})
        df['-log(pos|score)'] = -np.log(df['pos|score'])
        df_max = df.nlargest(30, metric)
        df.drop(df_max.index, axis=0,inplace=True)
        df = df.sort_values(by='Genes', key=lambda col: col.str.lower())
        df_max = df_max.sort_values(by='Genes', key=lambda col: col.str.lower())
        df = df.reset_index(drop=True)
        df_max = df_max.reset_index(drop=True)
        
        return df, df_max
    
    @staticmethod
    def sig_alpha(gen_df, max_df, gene_inputs, metric, hover, virus):
=======
    def __init__(self, output_path):
        self.output_path = output_path

    def host_factors(self, f1):
        dict_genes = {}
        df1  = pd.read_csv(f1, sep = '\t')
        df1 = df1.set_index('id')
        df1 = df1.to_dict(orient = 'index')
        for key in df1:
            dict_genes[key] = -np.log(df1[key]['pos|score'])
        k = Counter(dict_genes)
        dict_mostcommon = dict(k.most_common(30))
        
        return dict_genes, dict_mostcommon

    def sig_alpha(self, dict_genes, dict_mostcommon, virus):
        sortedgenes = sorted(dict_genes.keys(), key=lambda x:x.lower())
        sortedsiggenes = sorted(dict_mostcommon.keys(), key=lambda x:x.lower())

        virus_list = list()
        for gene in sortedgenes:
            virus_list.append(virus)
        
>>>>>>> 4e0e39a5353fc3020c248428f8f9bac0718f689c
        grey_x = list()
        for i in gen_df.index:
            grey_x.append(i/len(gen_df['Genes']))
        
        grey_df = pd.DataFrame()
        grey_df['Gene'] = gen_df['Genes']
        grey_df['Genes_Alpha'] = grey_x
        grey_df['Significance'] = gen_df[metric]
        grey_df['Enriched'] = ['Not Enriched']*len(grey_df['Gene'])
        for col in hover:
            grey_df = pd.concat([grey_df, gen_df[col]], axis=1)
            
        red_x = list()
        for i in max_df.index:
            red_x.append(i/len(max_df['Genes']))
        red_df = pd.DataFrame()
        red_df['Gene'] = max_df['Genes']
        red_df['Genes_Alpha'] = red_x
        red_df['Significance'] = max_df[metric]
        red_df['Enriched'] = ['Enriched']*len(red_df['Gene'])
        for col in hover:
            red_df = pd.concat([red_df, max_df[col]], axis=1)
        
        final_df = pd.concat([grey_df, red_df])
        final_df['Virus'] = [virus]*len(final_df['Gene'])
        
        selected = list()
        for gene in final_df['Gene']:
            if gene in gene_inputs:
                selected.append('Yes')
            else:
                selected.append('No')
        
        final_df['Selected'] = selected
        
        return red_df, grey_df, final_df

<<<<<<< HEAD
    def single_plot(self, num, metric, gene_inputs, hover, virus):
        f1 = self.file(virus)
        df, df_max = self.top_hits(f1, num, metric)
        red_df, grey_df, final_df = self.sig_alpha(df, df_max, gene_inputs, metric, hover, virus)         
        fig = px.scatter(final_df, x="Genes_Alpha", y="Significance", color = 'Enriched',
                         color_discrete_sequence=["grey", "red"])
=======
    def single_plot(self, virus_path, virus_name):
        dict_genes, dict_mostcommon = self.host_factors(virus_path)
        grey_df, red_df, df = self.sig_alpha(dict_genes, dict_mostcommon, virus_path)         
        fig = px.scatter(df, x="Genes (Alphabetically)", y="Significance", color = '30 Most Enriched Genes', color_discrete_sequence=["grey", "red"])
>>>>>>> 4e0e39a5353fc3020c248428f8f9bac0718f689c

        fig.add_trace(go.Scatter(
            x= red_df['Genes_Alpha'],
            y= red_df['Significance'],
            mode="text",
            name="Gene Names",
            text=red_df['Gene'],
            textposition="top center",
            hovertemplate=
            "Significance: %{y}" +
            "</b><br>" +
            "Gene Name: %{text}"
        ))

        fig.add_trace(go.Scatter(
            x= grey_df['Genes_Alpha'],
            y= grey_df['Significance'],
            name=' ',
            opacity=0,
            text=grey_df['Gene'],
            hovertemplate=
            "Significance: %{y}" +
            "</b><br>" +
            "Gene Name: %{text}"
        ))

        fig.update_layout(
<<<<<<< HEAD
            hoverlabel=dict(bgcolor="white"), title_text = str(name_dict.acronym(virus)) + ' Host Factors (CRISPR Screen)'
=======
            hoverlabel=dict(bgcolor="white"), title_text = str(virus_name) + ' Host Factors (CRISPR Screen)'
>>>>>>> 4e0e39a5353fc3020c248428f8f9bac0718f689c
        )

        fig.update_xaxes(showticklabels=False)

<<<<<<< HEAD
        return fig
=======
        return fig
>>>>>>> 4e0e39a5353fc3020c248428f8f9bac0718f689c
