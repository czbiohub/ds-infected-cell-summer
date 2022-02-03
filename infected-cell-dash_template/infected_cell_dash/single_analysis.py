import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import os
from collections import Counter
from plotly.subplots import make_subplots
from pathlib import Path

fig = go.Figure()

def file(virus):
    for subdir, dirs, files in os.walk('/Users/elianna.kondylis/final_nextflow_output/output_072321/'):
        for filename in files:        
            filepath = subdir + os.sep + filename
            if filepath.endswith("gene_summary.txt") and virus in filepath:          
                return filepath

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

def sig_alpha(dict_genes, dict_mostcommon, virus):

    sortedgenes = sorted(dict_genes.keys(), key=lambda x:x.lower())
    sortedsiggenes = sorted(dict_mostcommon.keys(), key=lambda x:x.lower())

    virus_list = list()
    for gene in sortedgenes:
        virus_list.append(virus)
    
    x = list()
    y = list()
    gene_names1 = list()
    enriched_list1 = list()
    genes_plot1 = list()
    for i, gene in enumerate(sortedgenes):
        if gene in dict_mostcommon:
            continue
        x.append(i/len(sortedgenes))
        y.append(dict_genes[gene])
        gene_names1.append(gene)
        enriched_list1.append('Not Enriched')
        genes_plot1.append(' ')

    final_dict1 = dict()
    final_dict1['Gene'] = gene_names1
    final_dict1['30 Most Enriched Genes'] = enriched_list1
    final_dict1['Genes (Alpabetically)'] = x
    final_dict1['Significance'] = y
    final_dict1['genes_plot'] = genes_plot1
    
    red_x = list()
    red_y = list()
    gene_names2 = list()
    enriched_list2 = list()
    genes_plot2 = list()
    for i, gene in enumerate(sortedsiggenes):
        if gene in dict_mostcommon:
            red_x.append(i/len(sortedsiggenes))
            red_y.append(dict_mostcommon[gene])
            gene_names2.append(gene)
            enriched_list2.append('Enriched')
            genes_plot2.append(gene)

    final_dict2 = dict()
    final_dict2['Gene'] = gene_names2
    final_dict2['30 Most Enriched Genes'] = enriched_list2
    final_dict2['Genes (Alpabetically)'] = red_x
    final_dict2['Significance'] = red_y
    final_dict2['genes_plot'] = genes_plot2
    
    df1 = pd.DataFrame(final_dict1)
    df2 = pd.DataFrame(final_dict2)
    df = pd.concat([df1, df2])
    df['Virus'] = virus_list

    return(df, red_x, red_y, gene_names2)

def single_plot(virus):
    f1 = file(virus)
    dict_genes, dict_mostcommon = host_factors(f1)
    df, red_x, red_y, gene_names2 = sig_alpha(dict_genes, dict_mostcommon, virus)         
    fig = px.scatter(df, x="Genes (Alpabetically)", y="Significance", color = '30 Most Enriched Genes', color_discrete_sequence=["grey", "red"])

    fig.add_trace(go.Scatter(
        x= red_x,
        y=red_y,
        mode="text",
        name="Gene Names",
        text=gene_names2,
        textposition="top center"
    ))

    fig.update_layout(
        title_text = virus + ' Host Factors (CRISPR Screen)'
    )

    fig.update_xaxes(showticklabels=False)

    return fig

#single_plot('HAV')

def stacked_plots(virus1, virus2, virus3):
    f1 = file(virus1)
    f2 = file(virus2)
    f3 = file(virus3)
    
    list1 = list()
    list2 = list()
    list3 = list()

    dict_genes_a, dict_mostcommon_a = host_factors(f1)
    df_a, red_x_a, red_y_a, gene_names2_a = sig_alpha(dict_genes_a, dict_mostcommon_a, virus1)

    dict_genes_b, dict_mostcommon_b = host_factors(f2)
    df_b, red_x_b, red_y_b, gene_names2_b = sig_alpha(dict_genes_b, dict_mostcommon_b, virus2)
    
    dict_genes_c, dict_mostcommon_c = host_factors(f3)
    df_c, red_x_c, red_y_c, gene_names2_c = sig_alpha(dict_genes_c, dict_mostcommon_c, virus3)
    
    df = pd.concat([df_a, df_b, df_c])
    
    fig = px.scatter(df, x="Genes (Alpabetically)", y="Significance", color = '30 Most Enriched Genes', color_discrete_sequence=["grey", "red"], facet_row="Virus")
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