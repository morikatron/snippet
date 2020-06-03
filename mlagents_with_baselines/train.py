import tensorflow as tf
import numpy as np
import gym

from baselines import deepq
from baselines import logger

from mlagents_envs.environment import UnityEnvironment
from gym_unity.envs import UnityToGymWrapper
from mlagents_envs.side_channel.engine_configuration_channel import EngineConfigurationChannel

def train():
    engine_configuration_channel = EngineConfigurationChannel()
    # 時間スケールを20倍に設定
    engine_configuration_channel.set_configuration_parameters(time_scale=20.0)
    unity_env = UnityEnvironment("./ml-agents/Project/PushBlock", side_channels=[engine_configuration_channel])
    env = UnityToGymWrapper(unity_env, 0, flatten_branched=True)
    logger.configure('./logs')
    # DQNで学習
    model = deepq.learn(
        env,
        "mlp",
        seed=0,
        lr=2.5e-4,
        total_timesteps=400000,
        buffer_size=50000,
        exploration_fraction=0.05,
        exploration_final_eps=0.1,
        print_freq=20,
        train_freq=5,
        learning_starts=20000,
        target_network_update_freq=50,
        gamma=0.99,
        prioritized_replay=False,
        checkpoint_freq=1000,
        dueling=True,
        checkpoint_path=None,
        load_path="./model"
    )

    # モデルを保存
    save_path = "./model"
    ckpt = tf.train.Checkpoint(model=model)
    manager = tf.train.CheckpointManager(ckpt, save_path, max_to_keep=1)
    manager.save()

if __name__ == '__main__':
    train()
