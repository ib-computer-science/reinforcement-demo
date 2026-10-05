import random

from bandit_env import pull

epsilon = 0.1
num_steps = 10000
gamma = 0.9
alpha0 = 0.05           # starting learning rate for each (state, arm) pair
decay_steps = 1000      # learning rate roughly halves every this many visits to a pair
bin_size = 20           # steps per data point within a run
num_runs = 500          # independent runs averaged together to smooth out per-bin sampling noise

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

        reward, next_state = pull(state, chosen_arm)

        times_chosen[state][chosen_arm] += 1
        learning_rate = alpha0 * decay_steps / (decay_steps + times_chosen[state][chosen_arm])
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

with open('q_learn_convergence.dat', 'w') as f:
    for bin_index, (state0, state1) in enumerate(accum):
        step = (bin_index + 1) * bin_size
        p0 = state0[1] / state0[0] if state0[0] else 0.0
        p1 = state1[1] / state1[0] if state1[0] else 0.0
        f.write(f'{step} {p0:.4f} {p1:.4f}\n')

print(f'wrote {num_bins} data points to q_learn_convergence.dat, each averaged over {num_runs} runs')
