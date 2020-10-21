from convert import convert
from cpm import run_validate

def cv(config_ini):

    [all_mat,all_behav] = convert(config_ini)
    [pos_cor, neg_cor] = run_validate(all_mat,all_behav,'LOO')
    print("Separate edge model performance: (pos_cor, neg_cor):",pos_cor,neg_cor)

cv('/home/ondra/PycharmProjects/CPM/config.ini')
