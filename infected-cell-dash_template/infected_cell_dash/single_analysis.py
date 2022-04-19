import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from collections import Counter


class SingleAnalysis:
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

    def single_plot(self, virus_path, virus_name):
        dict_genes, dict_mostcommon = self.host_factors(virus_path)
        grey_df, red_df, df = self.sig_alpha(dict_genes, dict_mostcommon, virus_path)         
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
            hoverlabel=dict(bgcolor="white"), title_text = str(virus_name) + ' Host Factors (CRISPR Screen)'
        )

        fig.update_xaxes(showticklabels=False)

        return fig
