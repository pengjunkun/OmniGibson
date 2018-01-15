# add parent dir to find package. Only needed for source code build, pip install doesn't need it.
import os, inspect

currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(os.path.dirname(currentdir))
os.sys.path.insert(0, parentdir)

from baselines import deepq
import gym
from realenv.envs.ant_env import AntFetchEnv, AntFetchKernelizedRewardEnv

import deepq
import matplotlib.pyplot as plt
import datetime


def callback(lcl, glb):
    # stop training if reward exceeds 199
    total = sum(lcl['episode_rewards'][-101:-1]) / 100
    totalt = lcl['t']
    is_solved = totalt > 20 and total >= 120
    return is_solved


def main():
    #env = AntFetchEnv(human=args.human, is_discrete=True)
    env = AntFetchKernelizedRewardEnv(human=args.human, is_discrete=True)
    model = deepq.models.mlp([64])
    act = deepq.learn(
        env,
        q_func=model,
        lr=1e-3,
        max_timesteps=50000,
        buffer_size=50000,
        exploration_fraction=0.1,
        exploration_final_eps=0.02,
        print_freq=10,
        callback=callback,
        mode="SENSOR",           ## Note: this is needed for sensor_only
        num_gpu=args.num_gpu
    )
    print("Saving model to atn_fetch_model.pkl")
    act.save("ant_fetch_model.pkl")


if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('--human', action='store_true', default=False)
    parser.add_argument('--num_gpu', type=int, default=1)
    args = parser.parse_args()
    main()