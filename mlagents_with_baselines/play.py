import tensorflow as tf
import numpy as np
import gym

from baselines import deepq
from baselines import logger

from mlagents_envs.environment import UnityEnvironment
from gym_unity.envs import UnityToGymWrapper
from mlagents_envs.side_channel.engine_configuration_channel import EngineConfigurationChannel

def play():
    engine_configuration_channel = EngineConfigurationChannel()
    # 時間スケールを10倍に設定
    engine_configuration_channel.set_configuration_parameters(time_scale=10.0)
    unity_env = UnityEnvironment("./ml-agents/Project/PushBlock", side_channels=[engine_configuration_channel])
    env = UnityToGymWrapper(unity_env, 0, flatten_branched=True)
    # モデル読み込み
    model = deepq.learn(env, "mlp", total_timesteps=0, load_path="./model")

    obs = env.reset()
    obs = np.expand_dims(np.array(obs), axis=0)

    while True:
        action, _, _, _ = model.step(tf.constant(obs))
        action = action[0].numpy()
        obs, rew, done, _ = env.step(action)
        if done:
            obs = env.reset()
        obs = np.expand_dims(np.array(obs), axis=0)

if __name__ == '__main__':
    train()
