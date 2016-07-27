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
import matplotlib.pyplot as plt

fb = g.graph_from_pickle('data/egonets.graph')

name_rand = 'nce_egonets_d100_e20_b200_n10_ns10_nw10_wl100_ws20_adam_rand'
name_motif = 'nce_egonets_d100_e20_b200_n10_ns10_nw10_wl100_ws20_adam_motif'

no_train = False

if no_train:
  pass
else:
  model_a_r = e.EmbeddingNet(graph=fb, 
                           emb_dim=100,
                           epoch=20, 
                           batch_size=200,
                           neg_samp=2,
                           num_skip=2,
                           num_walk=10,
                           walk_length=50,
                           window_size=5)
  adam_opt = Adam(lr=0.001, beta_1=0.9, beta_2=0.999, epsilon=1e-08)
  model_a_r.build(optimizer=adam_opt)
  model_a_r.train(mode='random_walk', verbose=0)
  weight_a_r = model_a_r._model.get_weights()
if no_train:
  pass
else:
  model_a_m = e.EmbeddingNet(graph=fb, 
                           emb_dim=100,
                           epoch=20, 
                           batch_size=200,
                           neg_samp=2,
                           num_skip=2,
                           num_walk=10,
                           walk_length=50,
                           window_size=5)
  adam_opt = Adam(lr=0.001, beta_1=0.9, beta_2=0.999, epsilon=1e-08)
  model_a_m.build(optimizer=adam_opt)
  model_a_m.train(mode='motif_walk', verbose=0)
  weight_a_m = model_a_m._model.get_weights()

# Save model
if not os.path.exists(name_rand+'.model'):
  with open(name_rand+'.model', 'wb') as f:
    p.dump(model_a_r, f, p.HIGHEST_PROTOCOL)
if not os.path.exists(name_motif+'.model'):
  with open(name_motif+'.model', 'wb') as f:
    p.dump(model_a_m, f, p.HIGHEST_PROTOCOL)

# Save or load data
if not os.path.exists(name_rand+'.weights'):
  with open(name_rand+'.weights', 'wb') as f:
    p.dump(weight_a_r, f, p.HIGHEST_PROTOCOL)
else:
  with open(name_rand+'.weights', 'rb') as f:
    weight_a_r = p.load(f)
if not os.path.exists(name_motif+'.weights'):
  with open(name_motif+'.weights', 'wb') as f:
    p.dump(weight_a_m, f, p.HIGHEST_PROTOCOL)
else:
  with open(name_motif+'.weights', 'rb') as f:
    weight_a_m = p.load(f)

# Save or load tsne
if not os.path.exists(name_rand+'.tsne'):
  tsne_weight_a_r_in = TSNE(learning_rate=50).fit_transform(weight_a_r[0])
  tsne_weight_a_r_out = TSNE(learning_rate=50).fit_transform(weight_a_r[1])
  with open(name_rand+'.tsne', 'wb') as f:
    tsne = (tsne_weight_a_r_in, tsne_weight_a_r_out)
    p.dump(tsne, f, p.HIGHEST_PROTOCOL)
else:
  with open(name_rand+'.tsne', 'rb') as f:
    tsne_weight_a_r_in, tsne_weight_a_r_out = p.load(f)
if not os.path.exists(name_motif+'.tsne'):
  tsne_weight_a_m_in = TSNE(learning_rate=50).fit_transform(weight_a_m[0])
  tsne_weight_a_m_out = TSNE(learning_rate=50).fit_transform(weight_a_m[1])
  with open(name_motif+'.tsne', 'wb') as f:
    tsne = (tsne_weight_a_m_in, tsne_weight_a_m_out)
    p.dump(tsne, f, p.HIGHEST_PROTOCOL)
else:
  with open(name_motif+'.tsne', 'rb') as f:
    tsne_weight_a_m_in, tsne_weight_a_m_out = p.load(f)

plt.figure(figsize=(10,10))
plt.subplot(221)
plt.scatter(tsne_weight_a_r_in[:,0], tsne_weight_a_r_in[:,1])
plt.subplot(222)
plt.scatter(tsne_weight_a_r_out[:,0], tsne_weight_a_r_out[:,1])
plt.subplot(223)
plt.scatter(tsne_weight_a_m_in[:,0], tsne_weight_a_m_in[:,1])
plt.subplot(224)
plt.scatter(tsne_weight_a_m_out[:,0], tsne_weight_a_m_in[:,1])
plt.show()
