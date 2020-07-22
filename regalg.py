import numpy as np
import scipy
from sklearn.feature_selection import SelectPercentile
from sklearn.feature_selection import f_regression
from sklearn.linear_model import Ridge
from sklearn.metrics import mean_squared_error
from sklearn.model_selection import KFold, GridSearchCV, cross_val_predict
from sklearn.pipeline import Pipeline

class GridSearchRegAlg:

    def __init__(self, pthresh):
        self.pthresh = pthresh

        pct = pthresh * 100  # percent of edges kept in feature selection
        alphas = 10 ** np.linspace(10, -2, 100) * 0.5  # specify alphas to search

        # ridgeCPM pipeline
        self.reg = Pipeline([
            ('feature_selection', SelectPercentile(f_regression, percentile=pct)),
            ('regression', GridSearchCV(estimator=Ridge(normalize=False), cv=5, param_grid={'alpha': alphas}))
        ])

    # x_train: connectivity matrices N*M. N - number of subject. M - size of array representing
    # upper half triangle of connectivity matrix
    # y_train: behavioral data [N*1]
    def train(self, x_train, y_train):
        self.reg.fit(x_train, y_train);
        features = self.reg.named_steps['feature_selection']
        features_inds = np.where(features.get_support())[0]
        return features_inds

    def predict(self, cmat):
        return self.reg.predict(cmat)

    def cross_val_score(self, x, y):

        cv_strategy = KFold(n_splits=10)

        # n_jobs specify how many cpus to use
        y_predict = cross_val_predict(self.reg, x, y, cv=cv_strategy, n_jobs=4)

        # Assess performance
        mse = mean_squared_error(y_predict, y)
        cor = scipy.stats.pearsonr(y_predict, y)
        return [mse, cor]