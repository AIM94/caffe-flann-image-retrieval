__author__ = 'martin.majer'

import cv2
import h5py
import itertools
import os.path
import numpy as np
from scipy.misc import imsave
from sklearn.neighbors import KDTree

filename = 'data_kdt.hdf5'
thumbs = 'thumbs/'

class ImageSearchKDTree(object):
    def __init__(self, storage_dir, max_images=100000, thumbnail_size=(150,150,3)):
        self.storage_dir = storage_dir
        self.data_path = storage_dir + filename
        self.max_images = max_images
        self.thumbnail_size = thumbnail_size
        self.tree = None
        self.features = []

        if not os.path.exists(storage_dir):
            print 'Creating directory...'
            os.makedirs(storage_dir)
            os.makedirs(storage_dir + thumbs)
            print 'Directory created.'

        if os.path.isfile(self.data_path):
            print 'Loading data file...'
            self.load()
            print 'Data file loaded.'
        else:
            print 'Creating data file...'
            self.save()
            print 'Data file created.'

    def add_images(self, images, features):
        '''
        Add images, their features and calculate KDTree.
        :param images: list of images
        :param features: list of features
        :return: nothing
        '''
        if (len(self.features) + len(features)) > self.max_images:
            raise ValueError('You can add only %d more image(s). Maximum limit achieved.' % (self.max_images - len(self.features)))

        # add features
        self.features.extend(features)
        start = len(self.features) - len(features)
        end = len(self.features)

        # save resized images
        dim = (self.thumbnail_size[0], self.thumbnail_size[1])

        for i, img in enumerate(images):
            img_resized = cv2.resize(img, dim, interpolation = cv2.INTER_NEAREST)
            img_resized = img_resized.astype(np.uint8)
            index = str(end - len(images) + i)
            print '\rAdding image #%s' % index,
            imsave(self.storage_dir + thumbs + index + '.jpg', img_resized)

        self.tree = KDTree(self.features, metric='euclidean')

    def find_k_nearest_by_index(self, img_index, k_neighbors=3):
        '''
        Find K nearest neighbors by image index.
        :param img_index: index of searched image
        :param k: neighbors count
        :return: k nearest neighbors
        '''
        nearest = self.tree.query(self.features[img_index], k=k_neighbors, return_distance=False)

        return list(itertools.chain(*nearest))

    def get_images(self, indexes):
        '''
        Get images on corresponding indexes.
        :param indexes: indexes of images
        :return: images
        '''
        images = []

        for index in indexes:
            img = cv2.imread(self.storage_dir + thumbs + str(index) + '.jpg')
            images.append(img)

        return images

    def save(self):
        '''
        Save object variables to HDF5.
        :return: nothing
        '''
        with h5py.File(self.data_path,'w') as fw:
            fw['features'] = self.features
            fw['data_path'] = self.data_path
            fw['storage_dir'] = self.storage_dir
            fw['max_images'] = self.max_images
            fw['thumbnail_size'] = self.thumbnail_size

    def load(self):
        '''
        Load variables from HDF5 file and rebuild KDTree.
        :return: nothing
        '''
        with h5py.File(self.data_path,'r') as fr:
            # load features as list
            for feat in fr['features']:
                self.features.append(feat)

            # reading scalar dataset
            data = fr['data_path']
            self.data_path = data[()]
            data = fr['storage_dir']
            self.storage_dir = data[()]
            data = fr['max_images']
            self.max_images = data[()]

            # build KDTree
            if len(self.features) > 0:
                self.tree = KDTree(self.features, metric='euclidean')

            # load as list and save as tuple
            thumbnail_size = fr['thumbnail_size']
            self.thumbnail_size = (thumbnail_size[0], thumbnail_size[1], thumbnail_size[2])