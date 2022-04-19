import os

def list_gene_summary_files(path):
    """
    INPUT: 
    - path: path to data

    OUTPUT:
    - list of labels and paths for viruses 
    """
    options = []
    
    for virus_folder in os.listdir(path):
        virus_name = os.path.splitext(virus_folder)[0].split("_", 1)[1]
        if virus_name.endswith("_"):
            virus_name = virus_name[:-1]
        for root, dirs, files in os.walk(os.path.join(path, virus_folder)):
            for file in files:
                if file.endswith("gene_summary.txt"):
                    gene_summary_path = root+os.sep+file
                    
        options.append(
            {"label": virus_name,
            "value": gene_summary_path,
            }
        )
    return options

def getFileNameWoExt(path):
    # This function gets the filename without extension 
    fileName = os.path.basename(path).removesuffix('.gene_summary.txt')
    if fileName.endswith("_"):
        fileName = fileName[:-1]
    return fileName.split("_",1)[1] 

