"""
simple test for jax-implemented multi-layered perceptron
"""
from timeit import timeit

import jax
import jax.numpy as jnp
from jax import grad, jit, vmap, random

@jit
def softmax(x):
    x = x - jnp.max(x, axis=1)  # for avoiding overflow
    return jnp.exp(x) / jnp.sum(jnp.exp(x), axis=1, keepdims=True)

@jit
def cross_entropy(x, y):
    return jnp.sum(- y * jnp.log(x + 1e-8), axis=1)

@jit
def mlp_predict(params, x):
    for w, b in params:
        x = jnp.dot(x, w) + b
        x = jnp.maximum(0, x)
        # x = jnp.tanh(x)
    y = softmax(x)
    return y


def mlp_loss(params, x, y):
    probs = mlp_predict(params, x)
    loss = jnp.mean(cross_entropy(probs, y))
    return loss

@jit
def apply_grads(params, grads, lr=0.001):
    return [(w - w_grad * lr, b - b_grad * lr)
            for (w, b), (w_grad, b_grad) in zip(params, grads)]


def init_mlp_params(input_size: int, output_size: int, num_units: list, seed: int = 0):
    params = []
    num_units.append(output_size)
    key = random.PRNGKey(seed)
    last_out = input_size
    for unit in num_units:
        key, subkey = random.split(key)
        x, w = random.normal(key, (last_out, unit), dtype=jnp.float32) * jnp.sqrt(2 / last_out), random.normal(subkey, (unit, ), dtype=jnp.float32) * jnp.sqrt(2 / unit)
        params.append((x, w))
        last_out = unit
    return params


# hyper-parameters
FEATURE_VECTOR_SIZE = 50
BATCH_SIZE = 10
OUTPUT_SHAPE = 10
NUM_UNITS = [64, 64]
SEED = 0
NUM_UPDATES = 10
LEARNING_RATE = 0.01


def run():
    params = init_mlp_params(FEATURE_VECTOR_SIZE, OUTPUT_SHAPE, NUM_UNITS, SEED)
    x = random.normal(random.PRNGKey(SEED), shape=(BATCH_SIZE, FEATURE_VECTOR_SIZE))  # shape is (3, 3)
    target = random.normal(random.PRNGKey(SEED+1), shape=(BATCH_SIZE, OUTPUT_SHAPE))  # setting each target batch_1 -> [1, 0, 0] batch_2 -> [0, 1, 0] batch_3 -> [0, 0, 1]
    for i in range(NUM_UPDATES):
        params_grad = grad(mlp_loss, argnums=0)(params, x, target)
        params = apply_grads(params, params_grad, LEARNING_RATE)
        loss = mlp_loss(params, x, target)
        print(f"update: {i}  loss: {loss}")  # decrease constantly


def main():
    result_time = timeit(lambda: run(), number=1)
    print(f"result: {result_time} sec")


if __name__ == "__main__":
    main()
