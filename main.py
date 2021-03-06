from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
import argparse
import os
import sys
import tensorflow as tf
import numpy as np
print(tf.__version__)

from tensorflow.contrib.learn.python.learn.datasets import base

x1
# Data files
IRIS_TRAINING = "training.csv"
IRIS_TEST = "test.csv"

# Load datasets.
training_set = base.load_csv_with_header(filename=IRIS_TRAINING,
                                         features_dtype=np.float32,
                                         target_dtype=np.int)
test_set = base.load_csv_with_header(filename=IRIS_TEST,
                                     features_dtype=np.float32,
                                     target_dtype=np.int)

print(training_set.data)

print(training_set.target)

# Specify that all features have real-value data
feature_name = "cereal_features"
feature_columns = [tf.feature_column.numeric_column(feature_name,
                                                    shape=[2])]
classifier = tf.estimator.LinearClassifier(
    feature_columns=feature_columns,
    n_classes=7,
    model_dir="/tmp/cereal_model")

def input_fn(dataset):
    def _fn():
        features = {feature_name: tf.constant(dataset.data)}
        label = tf.constant(dataset.target)
        return features, label
    return _fn

# Fit model.
classifier.train(input_fn=input_fn(training_set),
               steps=1000)
print('fit done')

# Evaluate accuracy.
accuracy_score = classifier.evaluate(input_fn=input_fn(test_set),
                                     steps=100)["accuracy"]
print('\nAccuracy: {0:f}'.format(accuracy_score))

# Export the model for serving
feature_spec = {'cereal_features': tf.FixedLenFeature(shape=[2], dtype=np.float32)}

serving_fn = tf.estimator.export.build_parsing_serving_input_receiver_fn(feature_spec)

classifier.export_savedmodel(export_dir_base='/tmp/cereal_model' + '/export',
                            serving_input_receiver_fn=serving_fn)
