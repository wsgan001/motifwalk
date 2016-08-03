"""Warpper for testing
"""
# Coding: utf-8
# File name: test.py
# Created: 2016-07-27
# Description:
## v0.0: File created.

from __future__ import division
from __future__ import print_function
from __future__ import absolute_import

import embeddings as e
import graph as g

import numpy as np
import cPickle as p

import os

from keras.optimizers import Adam
from sklearn.manifold import TSNE
from sklearn.preprocessing import normalize
import matplotlib.pyplot as plt


dataset_name = "blogcatalog"
epoch = 5
emb_dim = 5
neg_samp = 5
num_skip = 1
num_walk = 5
walk_length = 5
window_size = 2
iters = 5

fb = g.graph_from_pickle('data/{}.graph'.format(dataset_name))

exp_name = "nce_{}_e{}_ed{}_ne{}_ns{}_nw{}_wl{}_ws{}_it{}_adam".format(
                data_name, epoch, emb_dim, neg_samp, num_skip, num_walk,
                walk_length, window_size, iters)



name_rand = exp_name + '_rand'
name_motif = exp_name + '_motif'
name_contrast = exp_name + '_contrast'

rand_train = False
motif_train = True
contrast_train = True

save_rand = False
save_motif = True
save_contrast = True

if not rand_train:
  pass
else:
  model_r = e.EmbeddingNet(graph=fb, epoch=epoch, emb_dim=emb_dim,
                           neg_samp=neg_samp, num_skip=num_skip,
                           num_walk=num_walk, walk_length=walk_length, 
                           window_size=window_size, iters=iters)
  adam_opt = Adam(lr=0.01, beta_1=0.9, beta_2=0.999, epsilon=1e-08)
  model_r.build(optimizer='adam')
  model_r.train(mode='random_walk')
  print('trained')
  weight_r = model_r._model.get_weights()

if not motif_train:
  pass
else:
  model_m = e.EmbeddingNet(graph=fb, epoch=epoch, emb_dim=emb_dim,
                           neg_samp=neg_samp, num_skip=num_skip,
                           num_walk=num_walk, walk_length=walk_length, 
                           window_size=window_size, iters=iters)
  adam_opt = Adam(lr=0.01, beta_1=0.9, beta_2=0.999, epsilon=1e-08)
  model_m.build(optimizer='adam')
  model_m.train(mode='motif_walk')
  weight_m = model_m._model.get_weights()

if not contrast_train:
  pass
else:
  model_c = e.EmbeddingNet(graph=fb, epoch=epoch, emb_dim=emb_dim,
                           neg_samp=neg_samp, num_skip=num_skip,
                           num_walk=num_walk, walk_length=walk_length,
                           window_size=window_size, iters=iters) # reset default at 0.3
  model_c.build(optimizer='adam')
  model_c.train_mce()
  weight_c = model_c._model.get_weights()

# Save or load data
if not os.path.exists(name_rand+'.weights') and rand_train:
  with open(name_rand+'.weights', 'wb') as f:
    p.dump(weight_r, f, p.HIGHEST_PROTOCOL)

if not os.path.exists(name_motif+'.weights') and motif_train:
  with open(name_motif+'.weights', 'wb') as f:
    p.dump(weight_m, f, p.HIGHEST_PROTOCOL)

if not os.path.exists(name_contrast+'.weights') and contrast_train:
  with open(name_contrast+'.weights', 'wb') as f:
    p.dump(weight_c, f, p.HIGHEST_PROTOCOL)

# Normalize
weight_r_avg = normalize(weight_r[0])
weight_m_avg = normalize(weight_m[0])
weight_c_avg = normalize(weight_c[0])

tsne_weight_r_norm = TSNE(learning_rate=100).fit_transform(weight_r_avg)
tsne_weight_m_norm = TSNE(learning_rate=100).fit_transform(weight_m_avg)
tsne_weight_c_norm = TSNE(learning_rate=100).fit_transform(weight_c_avg)

fig = plt.figure(figsize=(15,45))
fig.suptitle(name_rand[:-5], fontsize=16)
a=plt.subplot(311)
a.set_title("Random walk embedding")
a.scatter(tsne_weight_r_norm[:,0], tsne_weight_r_norm[:,1])
for i, xy in enumerate(tsne_weight_r_norm):
  a.annotate('%s' % (i+1), xy=xy, textcoords='data')
b=plt.subplot(312)
b.set_title("Motif walk embedding")
b.scatter(tsne_weight_m_norm[:,0], tsne_weight_m_norm[:,1])
for i, xy in enumerate(tsne_weight_m_norm):
  b.annotate('%s' % (i+1), xy=xy, textcoords='data')
c=plt.subplot(313)
c.set_title("Contrast walk embedding")
c.scatter(tsne_weight_c_norm[:,0], tsne_weight_c_norm[:,1])
for i, xy in enumerate(tsne_weight_c_norm):
  c.annotate('%s' % (i+1), xy=xy, textcoords='data')
plt.savefig(name_rand[:-5]+'.png')
plt.show()

