import pickle
import numpy as np
import pandas
from regalg import GridSearchRegAlg

#Read connectome matrix file and behavior data
# con_mat_file - Network-matrix (also referred to as "netmats" or "parcellated connectomes") were derived from the node-timeseries. For each subject, the N (15-
#               300) node-timeseries were fed into network modelling, creating an NxN matrix of connectivity estimates.
#               The individual subjects’ netmats are saved as raw text files, with one row per subject; each row
#               contains the NxN matrix of connectivity estimates, unwrapped to a long single row of N2 values. The row ordering matches the list of subject IDs
#               saved in the file subject_file
# behavior file - *.csv file
# behavior col
def read_data(con_mat_file, behavior_col, behavior_file, subject_file):

    #read behav file
    df = pandas.read_csv(behavior_file)
    subjects = np.loadtxt(subject_file)

    #remove "not a number (nan)" rows from behav table and connectome matrix
    subjects_to_remove = df.iloc[df[behavior_col].index[df[behavior_col].apply(np.isnan)]]['Subject'].to_numpy()
    behav_all = df.loc[df['Subject'].isin(np.setdiff1d(subjects, subjects_to_remove))][behavior_col].to_numpy()

    # read connectome
    con_mat = np.loadtxt(con_mat_file)
    con_mat = np.delete(con_mat,np.where(subjects == subjects_to_remove),axis = 0)

    con_mat_dim = int(np.sqrt(np.shape(con_mat)[1]))
    num_subj = np.shape(con_mat)[0]
    con_mat = con_mat.reshape(num_subj, con_mat_dim, con_mat_dim)
    con_mat = convert_to_diagonal_mat(con_mat)

    return [con_mat,behav_all]

#Cross validation using GridSearchCV. Feature selection and Ridge regression pipeline is used
def cv(con_mat_file, subject_file, behavior_file, behavior_col, pthresh = 0.05):

    [con_mat,behav_all] = read_data(con_mat_file,behavior_col, behavior_file, subject_file)

    mdl = GridSearchRegAlg(pthresh)
    [mse, cor] = mdl.cross_val_score(con_mat, behav_all)
    print("Cross validation score (mse, corellation):", mse, cor)

#Train model and save it to disk
def train(con_mat_file, subject_file, behavior_file, behavior_col, model_filename,pthresh = 0.05):

    [con_mat, behav_all] = read_data(con_mat_file, behavior_col, behavior_file, subject_file)

    mdl = GridSearchRegAlg(pthresh)
    selected_features = mdl.train(con_mat, behav_all)
    print("Selected features:", selected_features)

    # save the model to disk
    pickle.dump(mdl, open(model_filename, 'wb'))
    print("Model saved to file:",model_filename)

#predict behavior using saved model
def predict(con_mat_file, model_filename):

    con_mat = read_connectome(con_mat_file)

    print("Load model from file:", model_filename)
    mdl = pickle.load(open(model_filename, 'rb'))
    predicted_behav = mdl.predict([con_mat[2]])
    print("Predicted behavior:",predicted_behav)

def convert_to_diagonal_mat(x):
    dimx = np.shape(x)
    nsub = dimx[0]
    m = dimx[1]
    # check dim 0 == dim 1

    a = np.triu_indices(m, 1)

    z = np.empty(shape=[nsub, int((m) * (m - 1) / 2)])
    for i in range(0, nsub):
        z[i] = x[i][a]

    return z;

def read_connectome(con_mat_file):
    con_mat = np.loadtxt(con_mat_file)
    # todo check perfect square
    con_mat_dim = int(np.sqrt(np.shape(con_mat)[1]))
    num_subj = np.shape(con_mat)[0]
    con_mat = con_mat.reshape(num_subj, con_mat_dim, con_mat_dim)
    con_mat = convert_to_diagonal_mat(con_mat)
    return con_mat

cv('netmats1.txt', 'subjectIDs.txt', 'unrestricted_ondramaz_6_21_2020_8_5_28.csv', 'Strength_Unadj')
train('netmats1.txt', 'subjectIDs.txt', 'unrestricted_ondramaz_6_21_2020_8_5_28.csv', 'Strength_Unadj','savemodel.mod')
predict('netmats1.txt','savemodel.mod')
