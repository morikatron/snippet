"""
simple test for jax-implemented mnist deep-learning
"""
import time

import jax.numpy as jnp
from jax import grad, jit, vmap, random
from sklearn import datasets
from sklearn.preprocessing import OneHotEncoder
from sklearn.model_selection import train_test_split
from tqdm import tqdm

# ===== define mlp functions =====
def softmax(x):
    x = x - jnp.max(x, axis=1, keepdims=True)  # for avoiding overflow
    return jnp.exp(x) / jnp.sum(jnp.exp(x), axis=1, keepdims=True)


def cross_entropy(x, y):
    return jnp.sum(- y * jnp.log(x + 1e-8), axis=1)


@jit
def mlp_predict(params, x):
    w, b = params[0]
    x = jnp.dot(x, w) + b
    for w, b in params[1:]:
        x = jnp.maximum(0, x)
        # x = jnp.tanh(x)
        x = jnp.dot(x, w) + b
    y = softmax(x)
    return y


def mlp_loss(params, x, y):
    probs = mlp_predict(params, x)
    loss = jnp.mean(cross_entropy(probs, y))
    return loss


def apply_grads(params, grads, r, lr=0.01, beta=0.9):
    new_r = []
    new_params = []
    for (w, b), (w_grad, b_grad), (w_r, b_r) in zip(params, grads, r):
        w_r = beta * w_r + (1 - beta) * w_grad ** 2
        b_r = beta * b_r + (1 - beta) * b_grad ** 2
        w_eta = lr / jnp.sqrt(w_r + 1e-6)
        b_eta = lr / jnp.sqrt(b_r + 1e-6)
        new_w = w - w_grad * w_eta
        new_b = b - b_grad * b_eta
        new_r.append((w_r, b_r))
        new_params.append((new_w, new_b))
    return new_params, new_r


def init_mlp_params(input_size: int, output_size: int, num_units: list, seed: int = 0):
    r_params = []
    params = []
    num_units.append(output_size)
    key = random.PRNGKey(seed)
    last_out = input_size
    for unit in num_units:
        key, subkey = random.split(key)
        x, w = random.normal(key, (last_out, unit), dtype=jnp.float32) * jnp.sqrt(2 / last_out), random.normal(subkey, (unit, ), dtype=jnp.float32) * jnp.sqrt(2 / last_out)
        params.append((x, w))
        r_params.append((1e-6, 1e-6))
        last_out = unit
    return params, r_params


# hyper-parameters
BATCH_SIZE = 512
NUM_UNITS = [64, 64]
NUM_EPOCHS = 20
LEARNING_RATE = 0.01
SEED = 1234

# ===== define mnist training functions =====
def train_one_epoch(params, X_train, y_train, epoch, r):
    num_samples = X_train.shape[0]
    random_sample_idx = random.permutation(random.PRNGKey(epoch), jnp.arange(num_samples))
    for idx in tqdm(range(0, num_samples, BATCH_SIZE)):
        mini_batch_idx = random_sample_idx[idx:idx + BATCH_SIZE]
        mini_batch_x = X_train[mini_batch_idx]
        mini_batch_y = y_train[mini_batch_idx]
        params_grad = grad(mlp_loss, argnums=0)(params, mini_batch_x, mini_batch_y)
        params, r = apply_grads(params, params_grad, r, LEARNING_RATE)
        loss = mlp_loss(params, mini_batch_x, mini_batch_y)
    return loss, params, r


def validation(params, X_valid, y_valid):
    loss = mlp_loss(params, X_valid, y_valid)
    return loss


def compute_accuracy(params, X_test, y_test):
    probs = mlp_predict(params, X_test)
    accuracy = jnp.sum(jnp.argmax(probs, axis=1) == jnp.argmax(y_test, axis=1)) / y_test.shape[0]
    return accuracy


def main():
    print("fetching mnisit datasets…")
    X, y = datasets.fetch_openml('mnist_784', version=1, return_X_y=True)
    X /= 255.0
    one_hot_encoder = OneHotEncoder()
    y = one_hot_encoder.fit_transform(y.reshape(-1, 1)).A
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=SEED)
    X_train, X_valid, y_train, y_valid = train_test_split(X_train, y_train, test_size=0.2, random_state=SEED)
    params, r = init_mlp_params(X_train.shape[1], y_train.shape[1], NUM_UNITS, SEED)
    for i in range(NUM_EPOCHS):
        start_time = time.time()
        training_loss, params, r = train_one_epoch(params, X_train, y_train, i, r)
        validation_loss = validation(params, X_valid, y_valid)
        epoch_time = time.time() - start_time
        print(f"EPOCH: {i} time: {epoch_time:.3f} training_loss: {training_loss:.3f} validation_loss: {validation_loss:.3f}")
    accuracy = compute_accuracy(params, X_test, y_test)
    print(f"training finished. test acc: {accuracy}")


if __name__ == "__main__":
    main()