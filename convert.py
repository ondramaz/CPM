import glob
import os
import numpy as np
import pandas as pd
import scipy.io
import configparser

def convert(config_file):

    config = configparser.ConfigParser()
    config.read(config_file)

    default_sec = config['DEFAULT']

    con_mat_dir = default_sec['con_mat_dir']
    behav_xls_file = default_sec['behav_xls_file']
    num_features = int(default_sec['num_features'])
    excel_sheet_name = default_sec['excel_sheet_name']
    dependent_variable = default_sec['dependent_variable']

    # read behavioral data from excel file
    behav_data = read_behav_data(behav_xls_file, excel_sheet_name)
    num_subj = behav_data.shape[0]

    # read connectome
    os.chdir(con_mat_dir)
    all_mat = np.zeros(shape=(num_features,num_features,num_subj))
    all_behav = np.zeros(shape=(num_subj))
    i=0

    for file in glob.glob("*.mat"):
        subj = int(file[18:21])
        behav = behav_data[behav_data['Subject'] == subj][dependent_variable]
        if (behav.shape[0] != 0):           #some behavioral rows are missing (x x x x) -> skip the file
            all_behav[i] = behav
            connectome = scipy.io.loadmat(file)
            mat = connectome['Z'][:, 0:num_features]
            np.fill_diagonal(mat,0)
            all_mat[:,:,i] = mat
            i += 1


    return [all_mat,all_behav]


def read_behav_data(behav_xls_file, excel_sheet_name):
    xls = pd.ExcelFile(behav_xls_file)
    behav_data = pd.read_excel(xls, excel_sheet_name)
    # remove "not a number (nan)" rows ("x x x x")
    behav_data = behav_data.apply(lambda x: pd.to_numeric(x, errors='coerce'))
    behav_data.dropna(inplace=True)
    return behav_data
