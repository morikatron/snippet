"""
same experiment with tensorflow (for comparision)
"""
import numpy as np
import random

import tensorflow as tf
from tensorflow.keras import Model, Input
from tensorflow.keras.layers import Dense
from tensorflow.keras.activations import relu, softmax
from tensorflow.keras.optimizers import SGD, RMSprop

from sklearn import datasets
from sklearn.preprocessing import OneHotEncoder
from sklearn.model_selection import train_test_split

# ===== define mlp functions =====
class Network:
    def __init__(self, input_shape, output_shape):
        self.input_shape = input_shape
        self.output_shape = output_shape
        self.optimizer = RMSprop(0.01)
        # self.optimizer = SGD(0.001, momentum=0.9)
        self.model = self._build_model()

    def loss(self, inputs, targets):
        y = self.model(inputs)
        cross_entropy_loss = - tf.reduce_sum(targets * tf.math.log(y + 1e-6), axis=1)
        loss = tf.reduce_mean(cross_entropy_loss)
        return loss

    def accuracy(self, inputs, targets):
        y = self.model(inputs)
        acc = tf.cast(tf.equal(tf.argmax(targets, axis=1), tf.argmax(y, axis=1)), tf.float32)
        acc = tf.reduce_sum(acc)
        p = acc / y.shape[0]
        return p

    def train(self, inputs, targets):
        with tf.GradientTape() as tape:
            loss = self.loss(inputs, targets)
        grads = tape.gradient(loss, self.model.trainable_variables)
        grads_and_vars = zip(grads, self.model.trainable_variables)
        self.optimizer.apply_gradients(grads_and_vars)
        return loss

    def _build_model(self):
        input_x = Input(shape=(self.input_shape, ))
        x = Dense(64, activation=relu)(input_x)
        x = Dense(64, activation=relu)(x)
        output = Dense(self.output_shape, activation=softmax)(x)
        model = Model(inputs=input_x, outputs=[output])
        return model


# hyper-parameters
BATCH_SIZE = 512
NUM_EPOCHS = 20
LEARNING_RATE = 0.001
SEED = 1234

# ===== define mnist training functions =====
def train_one_epoch(model, X_train, y_train):
    num_samples = X_train.shape[0]
    random_sample_idx = np.random.permutation(np.arange(num_samples))
    for idx in range(0, num_samples, BATCH_SIZE):
        mini_batch_idx = random_sample_idx[idx:idx + BATCH_SIZE]
        mini_batch_x = X_train[mini_batch_idx]
        mini_batch_y = y_train[mini_batch_idx]
        loss = model.train(tf.constant(mini_batch_x, dtype=tf.float32), tf.constant(mini_batch_y, dtype=tf.float32))
    return loss


def main():
    print("fetching mnisit datasets…")
    X, y = datasets.fetch_openml('mnist_784', version=1, return_X_y=True)
    X /= 255.0
    one_hot_encoder = OneHotEncoder()
    y = one_hot_encoder.fit_transform(y.reshape(-1, 1)).A
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=SEED)
    X_train, X_valid, y_train, y_valid = train_test_split(X_train, y_train, test_size=0.2)
    model = Network(X_train.shape[1], y_train.shape[1])
    for i in range(NUM_EPOCHS):
        training_loss = train_one_epoch(model, X_train, y_train)
        validation_loss = model.loss(tf.constant(X_valid, dtype=tf.float32), tf.constant(y_valid, dtype=tf.float32))
        print(f"EPOCH: {i} training_loss: {training_loss.numpy()} validation_loss: {validation_loss.numpy()}")
    accuracy = model.accuracy(X_test, y_test)
    print(f"training finished. test acc: {accuracy}")


if __name__ == "__main__":
    main()
