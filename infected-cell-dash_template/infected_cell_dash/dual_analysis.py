import os
from os.path import isfile, join
from os import listdir
import pandas as pd
import numpy as np
from collections import Counter
import plotly.express as px
import plotly.express as px
import plotly.graph_objects as go

import single_analysis

#gen_df is the data frame with all the genes except for the signficant ones
#df_max is the data frame with all the significant genes
#dist is the distance between the clumps of data for each virus
#gene inputs is a list of genes the user wants to highlight in the graph
#hover is a list of metrics (positive score, rank, etc.) the user wants in the hover template on the graph
#returns a df for an individual virus
#significant genes have same x-axis, sig genes vertically stacked by significance
#non-sig genes are ordered alphabetically within a specific x-axis range
def construct_vertical(gen_df, max_df, dist, gene_inputs, vir, metric, hover):    
    grey_x = list()
    for i in gen_df.index:
        grey_x.append(dist + 0.2*i/len(gen_df['Genes']))
    
    grey_df = pd.DataFrame()
    grey_df['Gene'] = gen_df['Genes']
    grey_df['Genes_Alpha'] = grey_x
    grey_df['Significance'] = gen_df[metric]
    for col in hover:
        grey_df = pd.concat([grey_df, gen_df[col]], axis=1)
        
    red_df = pd.DataFrame()
    red_df['Gene'] = max_df['Genes']
    red_df['Genes_Alpha'] = [dist + 0.1]*len(max_df['Genes'])
    red_df['Significance'] = max_df[metric]
    for col in hover:
        red_df = pd.concat([red_df, max_df[col]], axis=1)
    
    vertical_df = pd.concat([grey_df, red_df])
    vertical_df['Virus'] = [vir]*len(vertical_df['Gene'])
    
    selected = list()
    for gene in vertical_df['Gene']:
        if gene in gene_inputs:
            selected.append('Yes')
        else:
            selected.append('No')
    
    vertical_df['Selected'] = selected
    
    return vertical_df

#virs is all viruses provided by user
#num is the number of singificant genes
#returns a figure of the vertical graphs on a plot
def plot_vertical(data_path, input_genes, virs, metric, hover, num):  
    dfs = list()
    for i, vir in enumerate(virs):
        f1 = single_analysis.file(vir, data_path)
        df1, df_max1 = single_analysis.top_hits(f1, num, metric)
        df1 = construct_vertical(df1, df_max1, 0.3*i, input_genes, vir, metric, hover)
        dfs.append(df1)
        
    final_df = pd.concat(dfs)
    fig = px.scatter(final_df, x='Genes_Alpha', y='Significance', hover_data=['Gene', 'Virus']+hover,
                     color = 'Selected', color_discrete_sequence=["blue", "red"])
    
    l1 = list()
    for x in range(len(virs)):
        l1.append(0.1+0.3*x)

    fig.update_layout(
    xaxis = dict(
        tickmode = 'array',
        tickvals = l1,
        ticktext = virs
        )
    )
    
    return fig
