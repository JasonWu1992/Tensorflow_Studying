# -*- coding: utf-8 -*-
"""
Created on Mon Apr 16 19:09:54 2018

@author: woshiwjl
"""

import numpy as np
import sklearn.preprocessing as prep
import tensorflow as tf
import tensorflow.examples.tutorials.mnist import input_data


def xavier_init(fan_in,fan_out,constant = 1):
    low = -constant * np.sqrt(6.0 * (fan_in + fan_out))
    high = constant * np.sqrt(6.0 * (fan_in + fan_out))
    return tf.random_uniform((fan_in,fan_out),
                             minval = low , maxval = high
                             dtype = tf.float32)

class AdditiveGaussianNoiseAutoencoder(object):
    def __init__(self,n_input,n_hidden,transfer_function = tf.nn.softplus,
                 optimizer = tf.train.AdamOptimizer(),scale = 0.1):
        self.n_input = n_input
        self.n_hidden = n_hidden
        self.transfer = transfer_function
        self.scale = tf.placeholder(tf.float32)
        self.training_scale = scale
        network_weights = self._initialize_weights()
        self.x = tf.placeholder(tf.float32,[None,self.n_input])
        self.hidden = self.transfer(tf.add(tf.matmul(self.x + scale*tf.random_normal((n_input,)),
                                                     self.weights['w1']),self.weights['b1']))
        self.reconstruction = tf.add(tf.matmul(self.hidden,self.weights['w2']),
                                     self.weights['b2'])
        self.cost = 0.5 * tf.reduce_sum(tf.pow(tf.subtract(
                self.reconstruction,self.x),2.0))
        self.optimizer = optimizer.minimize(self.cost)
        
        init = tf.global_variables_initializer()
        self.sess = tf.Session()
        self.sess.run(init)
        
    