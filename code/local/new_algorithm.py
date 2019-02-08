import argparse
import os
import pandas as pd
import numpy as np

from datetime import datetime
from fastparquet import ParquetFile
from glob import glob

from sklearn.cluster import KMeans
from sklearn.decomposition import TruncatedSVD
from sklearn.externals.joblib import dump, load
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics import pairwise_distances

from find_k_bisection import find_k


def find_recommended_events(data, event_id):
    print(data.columns)
    dma_code = data.loc[event_id, 'dma_code']
    relevant_events = data[data['dma_code'] == dma_code]
    print(relevant_events.shape)
    event_descriptions = list(relevant_events['event_description'].values)
    print('fitting tfidf')
    tfidf = TfidfVectorizer(event_descriptions, stop_words='english').fit(event_descriptions)
    print('saving tfidf')
    dump(tfidf, 'tfidf_{}.pkl'.format(dma_code), protocol=2, compress=1)
    print('vectorizing data')
    vectorized_data = tfidf.transform(event_descriptions)
    print(vectorized_data.shape)
    print('looking for k')
    rows, cols = vectorized_data.shape
    vectorizer, k = find_k(cols, 95, 1, vectorized_data)
    print('reducing dimensionality')
    transformed_data = pd.DataFrame(vectorizer.transform(vectorized_data), index=relevant_events.index)
    print(transformed_data.head())
    dump(vectorizer, 'svd_{}.pkl'.format(dma_code), protocol=2, compress=1)
    print('clustering')
    kmeans = KMeans(random_state=0).fit(transformed_data)
    dump(kmeans, 'kmeans_{}.pkl'.format(dma_code), protocol=2, compress=1)
    clusters = pd.Series(kmeans.predict(transformed_data), index=relevant_events.index)
    relevant_cluster = clusters[clusters == clusters.loc[event_id]]
    distance_matrix = pd.DataFrame(pairwise_distances(
        transformed_data[transformed_data.index.isin(relevant_cluster.index)], metric='cosine'),
                                   index=relevant_cluster.index, columns=relevant_cluster.index)
    possible_events = distance_matrix.loc[event_id].drop(event_id)
    print(possible_events.shape)
    top_events = possible_events.loc[possible_events == possible_events.max()]
    print(top_events.shape)
    print(possible_events.sort_values().index[:5])
    print(datetime.now() - start)
    return possible_events.sort_values().index[:5]


start = datetime.now()

parser = argparse.ArgumentParser(description='Get Event Recommendations')
parser.add_argument('-id', '--event_id', metavar='id', type=str,  help='Event id of interest')
args = parser.parse_args()
event_id = args.event_id

if os.path.exists('events_with_dma.json'):
    combined_data = pd.read_json('events_with_dma.json', orient='records').set_index('event_id')
    find_recommended_events(combined_data, event_id)

else:
    datafiles = [f for f in glob('*.snappy.parquet')]
    print(datafiles)
    combined_data = pd.concat([ParquetFile(filename).to_pandas() for filename in datafiles]).set_index('event_id')
    dma = pd.read_csv('DMA-zip.csv').set_index('ZIPCODE')
    event_dmas = []

    for z in combined_data['venue_zip']:
        if len(z) == 5:
            if int(z) in dma.index:
                event_dmas.append(str(dma.loc[int(z), 'DMA CODE']))
            else:
                event_dmas.append(np.nan)
        else:
            if int(z[:5]) in dma.index:
                event_dmas.append(str(dma.loc[int(z[:5]), 'DMA CODE']))
            else:
                event_dmas.append(np.nan)

    combined_data['dma_code'] = event_dmas
    print(type(event_dmas[0]))
    combined_data.reset_index(drop=False, inplace=True)
    combined_data.to_json('events_with_dma.json', orient='records')
    find_recommended_events(combined_data.set_index('event_id'), event_id)
