print('importing')

import math
import numpy as np
import pandas as pd
import time

from sklearn.cluster import KMeans
from sklearn.decomposition import TruncatedSVD
from sklearn.externals.joblib import dump
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.utils.extmath import randomized_svd

print('starting')
start_time = time.time()
print('loading data')
data = pd.read_json('events_with_dma.json', orient='records')
event_descriptions = list(data['event_description'].values)
print('training vectorizer')
tfidf = TfidfVectorizer(event_descriptions).fit(event_descriptions)
dump(tfidf, 'tfidf.pkl', protocol=2, compress=1)
print('vectorizing data')
vectorized_data = tfidf.transform(event_descriptions)
rows, cols = vectorized_data.shape
percentage = 70
tol = 1


# def run_vect(k, data, cols):
#     """
#     run vectorizer
#     return variance percentage i.e. (.653)
#     """
#     vectorizer = TruncatedSVD(n_components=k, random_state=0).fit(data)
#     explained_variance = vectorizer.explained_variance_ratio_.sum()
#     u, sigma, vt = randomized_svd(data, n_components=cols//2, n_iter=3, random_state=0)
#     energy_sq = np.linalg.norm(sigma) ** 2
#     approx_energy_sq = np.linalg.norm(sigma[:k])
#     print(k, explained_variance)
#
#     return vectorizer, explained_variance


def cmp_guess(k, percentage, tol, sigma, energy_sq):
    """
    :param k: the n_components to run in vectorizer for svd
    :param percentage: goal energy/variance to capture
    :param tol: tolerance set so we don't overshoot too hard
    :return:
    """
    approx_energy_sq = np.linalg.norm(sigma[:k]) ** 2
    print('approx_energy_sq', approx_energy_sq)
    new_percent = approx_energy_sq * 100 / energy_sq
    print('%4.2f' % new_percent, k)

    if new_percent > (percentage - tol):
        return 1
    if new_percent < (percentage - tol):
        return 0


def find_k(cols, percentage, tol, data):
    """
    :param cols: the upper end of dataframe
    :param percentage: variance percentage
    :return: the optimal k for dimensional reduction.
    """

    lb = 0
    hb = cols
    print(hb)
    print('performing svd')
    u, sigma, vt = randomized_svd(data, n_components=cols//2, n_iter=1, random_state=0)
    energy_sq = np.linalg.norm(sigma) ** 2
    print('energy_sq', energy_sq)
    print('iterating for k')

    while abs(hb - lb) > 1:
        k = (lb + hb) // 2
        print('k', k)
        result = cmp_guess(k, percentage, tol, sigma, energy_sq)

        if result == 1:
            hb = k

        elif result == 0:
            break
    print('k being used', hb)
    vectorizer = TruncatedSVD(n_components=hb, random_state=0).fit(data)
    print(vectorizer.explained_variance_ratio_.sum())

    return vectorizer, math.floor(k)


vectorizer, k = find_k(cols, 70, tol, vectorized_data)
dump(vectorizer, 'svd.pkl', protocol=2, compress=1)
kmeans = KMeans(random_state=0).fit(vectorized_data)
dump(kmeans, 'kmeans.pkl', protocol=2, compress=1)

print('Program Complete')
print('time taken:', time.time() - start_time, 'seconds')
