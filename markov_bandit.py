import random

from bandit_env import pull

epsilon = 0.1               # probability of exploring instead of exploiting
num_steps = 100000
gamma = 0.9                 # discount factor: how much future reward matters now

Q = [[0.0, 0.0], [0.0, 0.0]]                # Q[state][arm]
times_chosen = [[0, 0], [0, 0]]             # how many times each (state, arm) pair was chosen

state = 0   # start fresh
total_reward = 0

for step in range(num_steps):
    # --- choose an action in the current state: explore randomly, or exploit the current best guess,
    #     breaking ties randomly (all-zero Q at the start should look like a coin toss, not a fixed pick) ---
    should_explore = random.random() < epsilon
    if should_explore:
        chosen_arm = random.randrange(2)
    else:
        best_value = max(Q[state])
        best_arms = [arm for arm, value in enumerate(Q[state]) if value == best_value]
        chosen_arm = random.choice(best_arms)

    # --- pull the arm and observe a reward (1 = win, 0 = no win) and the resulting next state ---
    reward, next_state = pull(state, chosen_arm)

    # --- update our value estimate for the chosen (state, arm) pair via the Q-learning TD update:
    #     bootstrap off the best value achievable from the next state, discounted by gamma ---
    times_chosen[state][chosen_arm] += 1
    learning_rate = 1 / times_chosen[state][chosen_arm]
    td_target = reward + gamma * max(Q[next_state])
    prediction_error = td_target - Q[state][chosen_arm]
    Q[state][chosen_arm] += learning_rate * prediction_error

    state = next_state
    total_reward += reward

print(f'Played {num_steps} rounds, total reward {total_reward} '
      f'(average {total_reward / num_steps:.3f} per round).')
