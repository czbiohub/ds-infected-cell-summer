import pandas as pd

def acronym(virus):
    df = pd.read_csv('/Users/elianna.kondylis/Documents/GitHub/ds-infected-cell-summer/infected-cell-dash_template/infected_cell_dash/CRISPR_screen_datasets.csv')
    df = df.set_index('Virus')
    dict1 = df['Virus Acronym'].to_dict()
    return dict1[virus]