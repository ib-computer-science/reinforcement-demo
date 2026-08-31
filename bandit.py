import random

epsilon = 0.1              # probability of exploring instead of exploiting
num_steps = 100000

Q = [0.0, 0.0]              # estimated value of each arm, starts at zero
times_chosen = [0, 0]       # how many times each arm has been pulled so far
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
    times_chosen[chosen_arm] += 1
    learning_rate = 1 / times_chosen[chosen_arm]   # decays as an arm is pulled more, giving a true running average
    prediction_error = reward - Q[chosen_arm]
    Q[chosen_arm] += learning_rate * prediction_error

    # --- redraw progress on a single line, updated in place ---
    print(f"\rstep {step + 1:>6} | Q = [{Q[0]:.4f}, {Q[1]:.4f}]", end="", flush=True)

print()   # move to a new line once the loop finishes
