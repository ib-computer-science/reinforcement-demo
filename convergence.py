import random

epsilon = 0.1
num_steps = 50000
gamma = 0.9
bin_size = 500          # steps per data point within a run
num_runs = 200          # independent runs averaged together to smooth out per-bin sampling noise

true_p = [
    [0.5, 0.9],   # state 0 ("fresh"):    arm 0 = 0.5, arm 1 = 0.9
    [0.5, 0.1],   # state 1 ("depleted"): arm 0 = 0.5, arm 1 = 0.1
]

num_bins = num_steps // bin_size
# accum[bin][state] = [times in this state this bin, times arm 1 was pulled in this state this bin],
# summed across all runs
accum = [[[0, 0], [0, 0]] for _ in range(num_bins)]

for run in range(num_runs):
    Q = [[0.0, 0.0], [0.0, 0.0]]
    times_chosen = [[0, 0], [0, 0]]
    state = 0
    counts = [[0, 0], [0, 0]]
    bin_index = 0

    for step in range(num_steps):
        should_explore = random.random() < epsilon
        if should_explore:
            chosen_arm = random.randrange(2)
        else:
            best_value = max(Q[state])
            best_arms = [arm for arm, value in enumerate(Q[state]) if value == best_value]
            chosen_arm = random.choice(best_arms)

        counts[state][0] += 1
        if chosen_arm == 1:
            counts[state][1] += 1

        win_roll = random.random()
        reward = 1 if win_roll < true_p[state][chosen_arm] else 0

        next_state = 1 if chosen_arm == 1 else 0

        times_chosen[state][chosen_arm] += 1
        learning_rate = 1 / times_chosen[state][chosen_arm]
        td_target = reward + gamma * max(Q[next_state])
        prediction_error = td_target - Q[state][chosen_arm]
        Q[state][chosen_arm] += learning_rate * prediction_error

        state = next_state

        if (step + 1) % bin_size == 0:
            accum[bin_index][0][0] += counts[0][0]
            accum[bin_index][0][1] += counts[0][1]
            accum[bin_index][1][0] += counts[1][0]
            accum[bin_index][1][1] += counts[1][1]
            bin_index += 1
            counts = [[0, 0], [0, 0]]

with open('convergence.dat', 'w') as f:
    for bin_index, (state0, state1) in enumerate(accum):
        step = (bin_index + 1) * bin_size
        p0 = state0[1] / state0[0] if state0[0] else 0.0
        p1 = state1[1] / state1[0] if state1[0] else 0.0
        f.write(f'{step} {p0:.4f} {p1:.4f}\n')

print(f'wrote {num_bins} data points to convergence.dat, each averaged over {num_runs} runs')
