import plotly.express as px
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import os
from collections import Counter
from plotly.subplots import make_subplots
from pathlib import Path
fig = go.Figure()

#get path
def file(virus, data_path):
    for subdir, dirs, files in os.walk(data_path):
        for filename in files:
            filepath = subdir + os.sep + filename
            if filepath.endswith("gene_summary.txt") and virus in filepath:   
                return filepath

#get top hits, df is all genes not including significant ones and df_max is all significant genes
def top_hits(f1, num, metric):
    df  = pd.read_csv(f1, sep = '\t')
    df = df.rename(columns={'id':'Genes'})
    df['-log(pos|score)'] = -np.log(df['pos|score'])
    df_max = df.nlargest(num, metric)
    df.drop(df_max.index, axis=0,inplace=True)
    df = df.sort_values(by='Genes', key=lambda col: col.str.lower())
    df_max = df_max.sort_values(by='Genes', key=lambda col: col.str.lower())
    df = df.reset_index(drop=True)
    df_max = df_max.reset_index(drop=True)
    return df, df_max

#spacing the genes out by their alphabetical order
def sig_alpha(gen_df, max_df, gene_inputs, metric, hover, virus):
    grey_x = list()
    for i in gen_df.index:
        grey_x.append(i/len(gen_df['Genes']))
    
    grey_df = pd.DataFrame()
    grey_df['Genes'] = gen_df['Genes']
    grey_df['Genes_Alpha'] = grey_x
    grey_df['Significance'] = gen_df[metric]
    grey_df['Color'] = 'Not Enriched'
    for col in hover:
        grey_df = pd.concat([grey_df, gen_df[col]], axis=1)
        
    red_x = list()
    for i in max_df.index:
        red_x.append(i/len(max_df['Genes']))
    red_df = pd.DataFrame()
    red_df['Genes'] = max_df['Genes']
    red_df['Genes_Alpha'] = red_x
    red_df['Significance'] = max_df[metric]
    red_df['Color'] = 'Enriched'
    for col in hover:
        red_df = pd.concat([red_df, max_df[col]], axis=1)
    
    final_df = pd.concat([grey_df, red_df])
    final_df['Virus'] = [virus]*len(final_df['Genes'])
    
    selected = list()
    for gene in final_df['Genes']:
        if gene in gene_inputs:
            selected.append(1)
        else:
            selected.append(0)
    
    final_df['User_Selected'] = selected
    final_df.loc[final_df['User_Selected'] == 1, 'Color'] = 'Selected'

    return red_df, grey_df, final_df

#plotting significance vs. alphabetical order
def single_plot(data_path, num, metric, gene_inputs, hover, virus):
    f1 = file(virus, data_path)
    df, df_max = top_hits(f1, num, metric)
    red_df, grey_df, final_df = sig_alpha(df, df_max, gene_inputs, metric, hover, virus)         
    fig = px.scatter(final_df, x="Genes_Alpha", y="Significance", color = 'Color',
                        color_discrete_sequence=["grey", "red", "blue"], labels={'Genes_Alpha':'Genes Alphabetically'})

    fig.add_trace(go.Scatter(
        x= red_df['Genes_Alpha'],
        y= red_df['Significance'],
        mode="text",
        name="Gene Names",
        text=red_df['Genes'],
        textposition="top center",
        hovertemplate=
        "Significance: %{y}" +
        "</b><br>" +
        "Gene Name: %{text}" +
        "</b><br>" +
        "Hover: %{z}"
        ))
    fig.add_trace(go.Scatter(
        x= grey_df['Genes_Alpha'],
        y= grey_df['Significance'],
        name=' ',
        opacity=0,
        text=grey_df['Genes'],
        hovertemplate=
        "Significance: %{y}" +
        "</b><br>" +
        "Gene Name: %{text}"
    ))

#  fig.update_layout(
#     hoverlabel=dict(bgcolor="white"), title_text = str(name_dict.acronym(virus)) + ' Host Factors (CRISPR Screen)'
    #)

    fig.update_xaxes(showticklabels=False)

    return fig

#plotting one metric against another, initially will show singificance vs. rank
def sig_rank(data_path, num, metric_y, gene_inputs, hover_metrics, virus):
    metric_x = hover_metrics[0]
    f1 = file(virus, data_path)
    df, df_max = top_hits(f1, num, metric_y)
    df['Color'] = 'Not Enriched'
    df_max['Color'] = 'Enriched'
    final_df = pd.concat([df, df_max])
    
    selected = list()
    for gene in final_df['Genes']:
        if gene in gene_inputs:
            selected.append(1)
        else:
            selected.append(0)
    
    final_df['User_Selected'] = selected
    final_df.loc[final_df['User_Selected'] == 1, 'Color'] = 'Selected'

    fig = px.scatter(final_df, x=metric_x, y=metric_y, color = 'Color',
                        color_discrete_sequence=["grey", "red", "blue"])
    return fig
