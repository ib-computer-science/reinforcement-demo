import random

epsilon = 0.1               # probability of exploring instead of exploiting
num_steps = 100000
gamma = 0.9                 # discount factor: how much future reward matters now

# Two states instead of one. Arm 0 is a steady, unaffected option; arm 1 pays
# well but depletes itself for the next round, recovering only if arm 0 is
# pulled instead. This makes alternating arms better long-run than sticking
# with either arm alone, which a plain (state-less) bandit cannot discover.
true_p = [
    [0.5, 0.9],   # state 0 ("fresh"):    arm 0 = 0.5, arm 1 = 0.9
    [0.5, 0.1],   # state 1 ("depleted"): arm 0 = 0.5, arm 1 = 0.1
]

Q = [[0.0, 0.0], [0.0, 0.0]]                # Q[state][arm]
times_chosen = [[0, 0], [0, 0]]             # how many times each (state, arm) pair was chosen

state = 0   # start fresh

for step in range(num_steps):
    # --- choose an action in the current state: explore randomly, or exploit the current best guess ---
    should_explore = random.random() < epsilon
    if should_explore:
        chosen_arm = random.randrange(2)
    else:
        chosen_arm = Q[state].index(max(Q[state]))

    # --- pull the arm and observe a reward (1 = win, 0 = no win), given the current state ---
    win_roll = random.random()
    reward = 1 if win_roll < true_p[state][chosen_arm] else 0

    # --- the next state is a deterministic function of (state, action): pulling arm 1 depletes it,
    #     pulling arm 0 lets it recover. This is the Markov property: next_state depends only on
    #     the current state and action, never on how we got here. ---
    next_state = 1 if chosen_arm == 1 else 0

    # --- update our value estimate for the chosen (state, arm) pair via the Q-learning TD update:
    #     bootstrap off the best value achievable from the next state, discounted by gamma ---
    times_chosen[state][chosen_arm] += 1
    learning_rate = 1 / times_chosen[state][chosen_arm]
    td_target = reward + gamma * max(Q[next_state])
    prediction_error = td_target - Q[state][chosen_arm]
    Q[state][chosen_arm] += learning_rate * prediction_error

    state = next_state

    # --- redraw progress on a single line, updated in place ---
    print(f'\rstep {step + 1:>6} | state {state} | Q = [{Q[0][0]:.4f}, {Q[0][1]:.4f}] / [{Q[1][0]:.4f}, {Q[1][1]:.4f}]', end='', flush=True)

print()   # move to a new line once the loop finishes
