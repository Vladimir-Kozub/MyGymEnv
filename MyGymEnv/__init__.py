from gym.envs.registration import registry, register, make, spec

register(
    id='myenv-v1',
    entry_point='MyGymEnv.myenv:Snake',
    max_episode_steps=200,
)


register(
    id='myenv-v2',
    entry_point='MyGymEnv.myenv2:Snake',
    max_episode_steps=200,
)

register(
    id='myenv-v3',
    entry_point='MyGymEnv.myenv3:Snake',
    max_episode_steps=200,
)
