import pandas as pd
import numpy as np


def least_confidence(prob_dist):
    """ 
    Returns the uncertainty score of an array using
    least confidence sampling in a 0-1 range where 1 is the most uncertain
    """
    max_conf = np.max(prob_dist)
    n_class = len(prob_dist)
    normalized_conf = (1-max_conf) * (n_class/ (n_class-1))
    return normalized_conf

def predict_score(data,model,method):
    X_pred = model.predict(np.array([data]))
    score = method(X_pred[0])
    return score

def uncertainty_samples(dataframe, model,method):
    dataframe['uncertainty'] = dataframe['features'].apply(lambda x: predict_score(x,model,method))
    return dataframe