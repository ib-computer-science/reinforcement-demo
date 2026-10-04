import random

from bandit_env import pull

epsilon = 0.1                # probability of exploring instead of exploiting
num_steps = 100000
gamma = 0.9                  # discount factor: how much future reward matters now
alpha0 = 0.05                # starting learning rate for each (state, arm) pair
decay_steps = 1000           # learning rate roughly halves every this many visits to a pair

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
    #     bootstrap off the best value achievable from the next state, discounted by gamma. The
    #     learning rate starts at alpha0 (fast movement) and decays toward 0 as a pair accumulates
    #     visits (so the estimate settles instead of jittering forever), but decays much more
    #     gently than a plain 1/n schedule would. ---
    times_chosen[state][chosen_arm] += 1
    learning_rate = alpha0 * decay_steps / (decay_steps + times_chosen[state][chosen_arm])
    td_target = reward + gamma * max(Q[next_state])
    prediction_error = td_target - Q[state][chosen_arm]
    Q[state][chosen_arm] += learning_rate * prediction_error

    state = next_state
    total_reward += reward

    # --- redraw the current greedy policy on a single line, updated in place: state 0 means the
    #     last arm pulled was left (or the game just started), state 1 means it was right ---
    greedy_after_left = 'l' if Q[0][0] >= Q[0][1] else 'r'
    greedy_after_right = 'l' if Q[1][0] >= Q[1][1] else 'r'
    print(f'\rstep {step + 1:>6} | select {greedy_after_left} after left, select {greedy_after_right} after right', end='', flush=True)

print()   # move to a new line once the loop finishes
print(f'Played {num_steps} rounds, total reward {total_reward} '
      f'(average {total_reward / num_steps:.3f} per round).')
