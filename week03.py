# -*- coding: utf-8 -*-
# <nbformat>3.0</nbformat>

# <codecell>

import numpy as np
import matplotlib.pyplot as plt
import h5py
from scipy.spatial.distance import pdist, squareform
from sklearn.neighbors import KDTree

%matplotlib inline

# <codecell>

def get_distance_matrix(features, n):
    
    dst_matrix = np.zeros((n,n))
    
    for i in range(0, n):
        print '\r', 'i: ', i,
        for j in range(i, n):
            dst_matrix[i,j] = np.linalg.norm(features[i] - features[j])
    
    dst_matrix += dst_matrix.T
    
    return np.array(dst_matrix)

# <codecell>

def find_k_nearest(dst_matrix, img_index, k):
    
    dst = dst_matrix[img_index,:]
    best_indexes = np.argsort(dst)
    
    print_imgs(best_indexes, k)

# <codecell>

def print_imgs(indexes, k):
    
    with h5py.File(h5_imgs_fn,'r') as fr_imgs:
    
        for i in range(0, k):
           img = np.array(fr_imgs['imgs'][indexes[i]][:,:,::-1])
           img = img.astype(np.float32) * 255
        
           plt.figure()
           plt.imshow(img.astype(np.uint8)[:,:,::-1])
           plt.show()

# <codecell>

h5_imgs_fn = '/Users/martin.majer/PycharmProjects/PR4/data/sun_sample.hdf5'
h5_fts_fn = h5_imgs_fn + '.features.hdf5'
n = 10000

# <codecell>

with h5py.File(h5_fts_fn,'r') as fr_features:
    features_score = np.copy(fr_features['score'])
    print 'features_score: ', features_score.shape

# <codecell>

with h5py.File(h5_fts_fn,'r') as fr_features:
    features_fc7 = np.copy(fr_features['blob_fc7'][:,4,:])
    print 'features_fc7: ', features_fc7.shape

# <codecell>

dst_m_score = get_distance_matrix(features_score, n)
print '\nscore: ', dst_m_score.shape

# <codecell>

dst_m_fc7 = get_distance_matrix(features_fc7, n)
print '\nfc7: ', dst_m_fc7.shape

# <codecell>

dst_m_score_sp = pdist(features_score, 'euclidean')
print 'score_scipy: ', dst_m_score_sp.shape

# <codecell>

dst_m_fc7_sp = pdist(features_fc7, 'euclidean')
print 'fc7_scipy: ', dst_m_fc7_sp.shape

# <codecell>

dst_m_score_squareform = squareform(dst_m_score_sp)
print 'score_scipy_squareform: ', dst_m_score_squareform.shape

# <codecell>

dst_m_fc7_squareform = squareform(dst_m_fc7_sp)
print 'fc7_scipy_squareform: ', dst_m_fc7_squareform.shape

# <codecell>

print dst_m_score[:5,:5], '\n'
print dst_m_score_squareform[:5,:5], '\n'
print '-' * 90
print dst_m_fc7[:5,:5], '\n'
print dst_m_fc7_squareform[:5,:5]

# <codecell>

img_index = 28
k_neighbors = 3

# <codecell>

find_k_nearest(dst_m_score_squareform, img_index, k_neighbors)

# <codecell>

find_k_nearest(dst_m_fc7_squareform, img_index, k_neighbors)

# <codecell>

kdt = KDTree(features_score, metric='euclidean')

# <codecell>

k_neighbors_score = kdt.query(features_score[img_index], k=k_neighbors, return_distance=False)

# <codecell>

print k_neighbors_score.shape

# <codecell>

print_imgs(k_neighbors_score[0], k_neighbors)

# <codecell>

kdt = KDTree(features_fc7, metric='euclidean')

# <codecell>

k_neighbors_fc7 = kdt.query(features_fc7[img_index], k=k_neighbors, return_distance=False)

# <codecell>

print_imgs(k_neighbors_fc7[0], k_neighbors)

