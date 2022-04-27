import plotly.express as px
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import os
from collections import Counter
from plotly.subplots import make_subplots
from pathlib import Path
from name_dict import acronym

fig = go.Figure()

class SingleAnalysis:
    def __init__(self, data_path):
        self.data_path = data_path

    def file(self, virus):
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

    def sig_alpha(gen_df, max_df, gene_inputs, metric, hover, virus):
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

    def single_plot(self, num, metric, gene_inputs, hover, virus):
        f1 = self.file(virus)
        df, df_max = self.top_hits(f1, num, metric)
        red_df, grey_df, final_df = self.sig_alpha(df, df_max, gene_inputs, metric, hover, virus)         
        fig = px.scatter(final_df, x="Genes_Alpha", y="Significance", color = 'Enriched',
                         color_discrete_sequence=["grey", "red"])

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
            hoverlabel=dict(bgcolor="white"), title_text = str(name_dict.acronym(virus)) + ' Host Factors (CRISPR Screen)'
        )

        fig.update_xaxes(showticklabels=False)

        return fig