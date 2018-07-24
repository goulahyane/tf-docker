# -*- coding: utf-8 -*-
"""
@author: Rahul.kumar Forked By: GOULAHYANE
"""

#! /usr/bin/env python


import data_helpers2 as data_helpers
import numpy as np
import os
import tensorflow as tf
import pandas as pd
from datetime import datetime

# Parameters
# ==================================================

# Eval Parameters
batch_size= 64
path ='/root/w2v_cnn_sentiment/'
checkpoint_dir = "./runs/1487512553/checkpoints"
vocab_file =  "./vocab1487512553.json"

# Misc Parameters
allow_soft_placement = True
log_device_placement =  False



# Load data. Load your own data here
print("Loading data...")
#x_test, y_test, vocabulary, vocabulary_inv = data_helpers.load_data(
#    eval=True, vocab_file=vocab_file,
#    cat1="./data/sentiment.positive", cat2="./data/sentiment.negative")

    
x_test, y_test, vocabulary, vocabulary_inv = data_helpers.load_data(
eval=True, vocab_file=vocab_file,cat1= "./data/sentiment.positive", cat2= "./data/sentiment.negative")

# Evaluation
# ==================================================
#checkpoint_file = tf.train.latest_checkpoint(checkpoint_dir)
checkpoint_file = "./runs/1487512553/checkpoints/model-18200"
#print("checkpoint file: {}".format(checkpoint_file))

session_conf = tf.ConfigProto(
    allow_soft_placement=allow_soft_placement,
    log_device_placement=log_device_placement)
sess = tf.Session(config=session_conf)
#    with sess.as_default():

# Load the saved meta graph and restore variables
saver = tf.train.import_meta_graph("{}.meta".format(checkpoint_file))
saver.restore(sess, checkpoint_file)

# Get the placeholders from the graph by name
input_x = tf.get_default_graph().get_operation_by_name("input_x").outputs[0]
dropout_keep_prob = tf.get_default_graph().get_operation_by_name("dropout_keep_prob").outputs[0]

# Tensors we want to evaluate
predictions = tf.get_default_graph().get_operation_by_name("output/predictions").outputs[0]
                                                  

def engine(query = " " , senderid = '', senderName = '' , x_test=x_test):    

    query = query
    new_question = query.strip()
    new_question = data_helpers.clean_str(new_question)
    new_question = new_question.split(" ")
    
    num_padd = x_test.shape[1] - len(new_question)
    new_question = new_question + ["<PAD/>"] * num_padd
    #print new_question
    for word in new_question:
        if not vocabulary.has_key(word):
            new_question[new_question.index(word)] = "<PAD/>"
                  
    x = np.array([vocabulary[word] for word in new_question])
    x_test = np.array([x])
            
    #print("\nEvaluating...\n")
    
    
    # Generate batches for one epoch
    batches = data_helpers.batch_iter(x_test, batch_size, 1, shuffle=False)

    # Collect the predictions here
    all_predictions = []

    for x_test_batch in batches:
        batch_predictions = sess.run(
            predictions, {input_x: x_test_batch, dropout_keep_prob: 1.0})
        all_predictions = np.concatenate(
            [all_predictions, batch_predictions])
    
    # Print accuracy

    #print 'prediction---', int(all_predictions)
    if int(all_predictions[0]) == 1:
        print 'Positive'
        return      {'Name':  senderName,'Sentiment' : 'Positive' , 'Response' : 'Thank you for your valuable feedback! \n \nIt will help us to serve better in future.\n'}
    elif int(all_predictions[0]) == 0:
        print 'Negative'
        return     {'Name':  senderName,'Sentiment' : 'Negative' , 'Response' : 'We are really sorry for the bad experience with our product.\n   '}
    else :
        print 'Unidentified'
        return     {'Name':  senderName,'Sentiment' : 'Unidentified'}

#print engine(query = 'i love it' , senderName ='Rahul')
