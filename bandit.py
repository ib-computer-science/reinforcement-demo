import random

epsilon = 0.1              # probability of exploring instead of exploiting
learning_rate = 0.1        # how fast Q-estimates move toward observed reward
num_steps = 1000

Q = [0.0, 0.0]              # estimated value of each arm, starts at zero
true_p = [0.3, 0.7]         # true (hidden) probability of reward for each arm; arm 1 is better

for step in range(num_steps):
    # --- choose an action: explore randomly, or exploit the current best guess ---
    should_explore = random.random() < epsilon
    if should_explore:
        chosen_arm = random.randrange(2)
    else:
        chosen_arm = Q.index(max(Q))

    # --- pull the arm and observe a reward (1 = win, 0 = no win) ---
    win_roll = random.random()
    reward = 1 if win_roll < true_p[chosen_arm] else 0

    # --- update our value estimate for the chosen arm toward the observed reward ---
    prediction_error = reward - Q[chosen_arm]
    Q[chosen_arm] += learning_rate * prediction_error

print(Q)   # should converge toward [0.3, 0.7]
