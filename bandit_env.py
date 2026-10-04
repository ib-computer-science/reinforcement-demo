import random

# Two states. Arm 0 is a steady, unaffected option; arm 1 pays well but
# depletes itself for the next round, recovering only if arm 0 is pulled
# instead. This makes alternating arms better long-run than sticking with
# either arm alone, which a plain (state-less) bandit cannot discover.
true_p = [
    [0.5, 0.9],   # state 0 ("fresh"):    arm 0 = 0.5, arm 1 = 0.9
    [0.5, 0.1],   # state 1 ("depleted"): arm 0 = 0.5, arm 1 = 0.1
]


def pull(state, arm):
    """Pull `arm` while in `state`; returns (reward, next_state).

    The next state is a deterministic function of (state, action): pulling
    arm 1 depletes it, pulling arm 0 lets it recover. This is the Markov
    property: next_state depends only on the current state and action,
    never on how we got here.
    """
    reward = 1 if random.random() < true_p[state][arm] else 0
    next_state = 1 if arm == 1 else 0
    return reward, next_state
