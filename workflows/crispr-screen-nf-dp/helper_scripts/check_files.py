import argparse
from genericpath import isfile
import sys
import linecache
import pandas as pd
import os

class MyParser(argparse.ArgumentParser):
    def error(self, message):
        sys.stderr.write('error: %s\n' % message)
        self.print_help()
        sys.exit(2)


def parse_args():
    parser = MyParser(description='This script checks the files specified in the excel file')
    parser.add_argument('--csv', default="", type=str, help='path to a directory', metavar = '')
    config = parser.parse_args()
    if len(sys.argv) == 1:  # print help message if arguments are not valid
        parser.print_help()
        sys.exit(1)
    return config


config = vars(parse_args())
csv = config['csv']

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

#####################
##      main       ##
#####################
def main():
    try:
        print("begin checking files")
        df = pd.read_csv(config['csv'])
        with open(f"{csv}.sh", "w") as wfh:
            for index, row in df.iterrows():
                Parent_dir=row['Parent_dir']
                Lib_A_dir=row['Lib_A_dir']
                Lib_B_dir=row['Lib_B_dir']
                Lib_A_csv=row['Lib_A_csv']
                Lib_B_csv=row['Lib_B_csv']
                prefix=row['prefix']
                suffix_tr=row['suffix_tr']
                suffix_ctrl=row['suffix_ctrl']

                #check library files
                if not pd.isnull(row['Lib_A_csv']):
                    path = os.path.join(Parent_dir,Lib_A_dir,Lib_A_csv)
                    if not os.path.isfile(path):
                        print(f"{path} {bcolors.FAIL}not found{bcolors.ENDC}")
                    else:
                        print(f"{path} {bcolors.OKGREEN}OK{bcolors.ENDC}")

                if not pd.isnull(row['Lib_B_csv']):
                    path = os.path.join(Parent_dir,Lib_B_dir,Lib_B_csv)
                    if not os.path.isfile(path):
                        print(f"{path} {bcolors.FAIL}not found{bcolors.ENDC}")
                    else:
                        print(f"{path} {bcolors.OKGREEN}OK{bcolors.ENDC}")          
                #check fastq files    
                #treatment            
                if not pd.isnull(row["Lib_A_tr_bio_reps"]):
                    A_tr_bio_reps = row["Lib_A_tr_bio_reps"].split(",")
                    for rep in A_tr_bio_reps:
                        path = os.path.join(Parent_dir,Lib_A_dir, f"{prefix}{rep}{suffix_tr}")
                        if not os.path.isfile(path):
                            print(f"{path} {bcolors.FAIL}not found{bcolors.ENDC}")
                        else:
                            print(f"{path} {bcolors.OKGREEN}OK{bcolors.ENDC}")
                #treatment
                if not pd.isnull(row["Lib_B_tr_bio_reps"]):
                    B_tr_bio_reps = row["Lib_B_tr_bio_reps"].split(",")
                    for rep in B_tr_bio_reps:
                        path = os.path.join(Parent_dir,Lib_B_dir, f"{prefix}{rep}{suffix_tr}")
                        if not os.path.isfile(path):
                            print(f"{path} {bcolors.FAIL}not found{bcolors.ENDC}")
                        else:
                            print(f"{path} {bcolors.OKGREEN}OK{bcolors.ENDC}")                  
                #ctrl
                if not pd.isnull(row["Lib_A_ctrl_bio_reps"]):
                    A_ctrl_bio_reps = row["Lib_A_ctrl_bio_reps"].split(",")
                    for rep in A_ctrl_bio_reps:
                        path = os.path.join(Parent_dir,Lib_A_dir, f"{prefix}{rep}{suffix_ctrl}")
                        if not os.path.isfile(path):
                            print(f"{path} {bcolors.FAIL}not found{bcolors.ENDC}")
                        else:
                            print(f"{path} {bcolors.OKGREEN}OK{bcolors.ENDC}")                      
                #ctrl
                if not pd.isnull(row["Lib_B_ctrl_bio_reps"]):
                    B_ctrl_bio_reps = row["Lib_B_ctrl_bio_reps"].split(",")
                    for rep in B_ctrl_bio_reps:
                        path = os.path.join(Parent_dir,Lib_B_dir, f"{prefix}{rep}{suffix_ctrl}")
                        if not os.path.isfile(path):
                            print(f"{path} {bcolors.FAIL}not found{bcolors.ENDC}")
                        else:
                            print(f"{path} {bcolors.OKGREEN}OK{bcolors.ENDC}")              




            
        print("done checking files")

    except Exception as e:
        print("Unexpected error:", str(sys.exc_info()))
        print("additional information:", e)
        PrintException()


##########################
## function definitions ##
##########################
def PrintException():
    exc_type, exc_obj, tb = sys.exc_info()
    f = tb.tb_frame
    lineno = tb.tb_lineno
    filename = f.f_code.co_filename
    linecache.checkcache(filename)
    line = linecache.getline(filename, lineno, f.f_globals)
    print('EXCEPTION IN ({}, LINE {} "{}"): {}'.format(filename, lineno, line.strip(), exc_obj))


if __name__ == "__main__": main()
