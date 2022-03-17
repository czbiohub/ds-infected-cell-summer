import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import os
from collections import Counter
from plotly.subplots import make_subplots
from pathlib import Path

fig = go.Figure()

class SingleAnalysis:
    def __init__(self, output_path):
        self.output_path = output_path

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
        df1 = df1.set_index('id')
        df1 = df1.to_dict(orient = 'index')
        for key in df1:
            dict_genes[key] = -np.log(df1[key]['pos|score'])
        k = Counter(dict_genes)
        dict_mostcommon = dict(k.most_common(30))
        
        return dict_genes, dict_mostcommon

    @staticmethod
    def sig_alpha(dict_genes, dict_mostcommon, virus):
        sortedgenes = sorted(dict_genes.keys(), key=lambda x:x.lower())
        sortedsiggenes = sorted(dict_mostcommon.keys(), key=lambda x:x.lower())

        virus_list = list()
        for gene in sortedgenes:
            virus_list.append(virus)
        
        grey_x = list()
        grey_y = list()
        gene_names1 = list()
        enriched_list1 = list()
        for i, gene in enumerate(sortedgenes):
            if gene in dict_mostcommon:
                continue
            grey_x.append(i/len(sortedgenes))
            grey_y.append(dict_genes[gene])
            gene_names1.append(gene)
            enriched_list1.append('Not Enriched')

        grey_df = pd.DataFrame()
        grey_df['Gene'] = gene_names1
        grey_df['30 Most Enriched Genes'] = enriched_list1
        grey_df['Genes (Alphabetically)'] = grey_x
        grey_df['Significance'] = grey_y
        
        red_x = list()
        red_y = list()
        gene_names2 = list()
        enriched_list2 = list()
        for i, gene in enumerate(sortedsiggenes):
            if gene in dict_mostcommon:
                red_x.append(i/len(sortedsiggenes))
                red_y.append(dict_mostcommon[gene])
                gene_names2.append(gene)
                enriched_list2.append('Enriched')

        red_df = pd.DataFrame()
        red_df['Gene'] = gene_names2
        red_df['30 Most Enriched Genes'] = enriched_list2
        red_df['Genes (Alphabetically)'] = red_x
        red_df['Significance'] = red_y
        
        df = pd.concat([grey_df, red_df])
        df['Virus'] = virus_list

        return grey_df, red_df, df

    def single_plot(self, virus, name_dict):
        f1 = self.file(virus)
        dict_genes, dict_mostcommon = self.host_factors(f1)
        grey_df, red_df, df = self.sig_alpha(dict_genes, dict_mostcommon, virus)         
        fig = px.scatter(df, x="Genes (Alphabetically)", y="Significance", color = '30 Most Enriched Genes', color_discrete_sequence=["grey", "red"])

        fig.add_trace(go.Scatter(
            x= red_df['Genes (Alphabetically)'],
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
            x= grey_df['Genes (Alphabetically)'],
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
            hoverlabel=dict(bgcolor="white"), title_text = str(name_dict[virus]) + ' Host Factors (CRISPR Screen)'
        )

        fig.update_xaxes(showticklabels=False)

        return fig

    #single_plot('HAV')

    def stacked_plots(self, virus1, virus2, virus3):
        f1 = self.file(virus1)
        f2 = self.file(virus2)
        f3 = self.file(virus3)
        
        list1 = list()
        list2 = list()
        list3 = list()

        dict_genes_a, dict_mostcommon_a = self.host_factors(f1)
        df_a, red_x_a, red_y_a, gene_names2_a = self.sig_alpha(dict_genes_a, dict_mostcommon_a, virus1)

        dict_genes_b, dict_mostcommon_b = self.host_factors(f2)
        df_b, red_x_b, red_y_b, gene_names2_b = self.sig_alpha(dict_genes_b, dict_mostcommon_b, virus2)
        
        dict_genes_c, dict_mostcommon_c = self.host_factors(f3)
        df_c, red_x_c, red_y_c, gene_names2_c = self.sig_alpha(dict_genes_c, dict_mostcommon_c, virus3)
        
        df = pd.concat([df_a, df_b, df_c])
        
        fig = px.scatter(df, x="Genes (Alphabetically)", y="Significance", color = '30 Most Enriched Genes', color_discrete_sequence=["grey", "red"], facet_row="Virus")
        fig.for_each_annotation(lambda a: a.update(text=a.text.split("=")[-1]))
        
        fig.add_trace(go.Scatter(
            x= red_x_c,
            y=red_y_c,
            mode="text",
            name="Gene Names",
            text=gene_names2_c,
            textposition="top center"
        ))
        
        fig.add_trace(go.Scatter(
            x= red_x_b,
            y=red_y_b,
            mode="text",
            name="Gene Names",
            text=gene_names2_b,
            textposition="top center"),
            row=2, col=1
        )
        
        fig.add_trace(go.Scatter(
            x= red_x_a,
            y=red_y_a,
            mode="text",
            name="Gene Names",
            text=gene_names2_a,
            textposition="top center"),
            row=3, col=1
        )

        fig.update_xaxes(showticklabels=False)

        return fig