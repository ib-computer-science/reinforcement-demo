# reinforcement-demo

A minimal, self-contained reinforcement learning toy example.

## bandit.py

A two-armed bandit solved with epsilon-greedy action selection and a
sample-average (decaying learning rate) value update:

- Arm 0 wins with probability 0.3, arm 1 wins with probability 0.7 — the
  agent does not know this and must learn it purely from observed pulls.
- With probability `epsilon`, the agent explores by picking a random arm;
  otherwise it exploits by picking the arm with the highest current
  estimate `Q`.
- After each pull, `Q[chosen_arm]` is updated toward the observed reward
  using a learning rate of `1 / times_chosen[chosen_arm]`, which makes it
  converge to the true running average reward for that arm.

Run it with:

```
python3 bandit.py
```

The program prints a single line, updated in place, showing the current
iteration and the current `Q` estimates for both arms.

### RL concepts in this example

- **State** — a bandit has no state: every pull is identical to the last,
  with no notion of "where" the agent is or how it got there. This is what
  makes a bandit the simplest possible RL setting, as opposed to a full MDP
  where the state changes based on past actions.
- **Action** — `chosen_arm`, i.e. which of the two arms to pull (0 or 1).
- **Reward** — the outcome of a single pull: 1 for a win, 0 for a loss,
  sampled according to the arm's hidden true win probability (`true_p`).
- **Policy** — the rule that maps the current `Q` estimates to an action:
  epsilon-greedy, meaning pull the arm with the highest `Q` estimate most of
  the time (exploit), but pull a random arm with probability `epsilon`
  (explore).

## bandit_env.py

The environment shared by `markov_bandit.py` and `play_bandit.py`: the
`true_p` table and the `pull(state, arm)` function (reward + next state for
pulling an arm in a state). Factored out so the Q-learning demo and the
human-playable version simulate the exact same dynamics instead of each
keeping their own copy.

## markov_bandit.py

A minimal step up from the stateless bandit: there are now two **states**,
and pulling an arm deterministically decides the *next* state — satisfying
the Markov property, since the next state depends only on the current state
and action, never on history.

- State 0 ("fresh"): arm 0 wins with probability 0.5, arm 1 wins with
  probability 0.9.
- State 1 ("depleted"): arm 0 still wins with probability 0.5, but arm 1's
  win probability has crashed to 0.1.
- Pulling arm 1 deterministically moves to state 1 (it depletes itself);
  pulling arm 0 deterministically moves to state 0 (it lets arm 1 recover).

Because actions now have delayed consequences, a plain reward-average `Q`
(as in `bandit.py`) can't tell arm 0 and arm 1 apart — both average 0.5
reward over time. Instead this uses the real Q-learning update:

```
Q[state][arm] += learning_rate * (reward + gamma * max(Q[next_state]) - Q[state][arm])
```

which bootstraps off the best value achievable from the next state,
discounted by `gamma`. This lets the agent discover that *alternating* arms
(pull arm 1 while fresh, arm 0 while depleted) earns ~0.7 average reward per
round — better than sticking to either arm alone — which is exactly the
policy it converges to. Ties in `Q[state]` (as at the very start, when
everything is `0.0`) are broken randomly rather than always favoring arm 0,
so the very first decision in an unvisited state is a genuine coin toss.

Run it with:

```
python3 markov_bandit.py
```

## play_bandit.py

Lets a human play the same environment from `bandit_env.py` interactively:
each round shows the current state, you type `0` or `1` to pull an arm, and
it reports whether you won. Like the Q-learning agent, you aren't shown the
win probabilities while playing — only revealed in the summary after you
quit (`q`) — so you have to find a good strategy by trial and error too.

Run it with:

```
python3 play_bandit.py
```

## convergence.py + convergence.asy

Visualizes how the agent's *behavior* converges during training in
`markov_bandit.py` — not the abstract `Q` values, but what the agent
actually does, including the ongoing exploration.

`convergence.py` reruns the same simulation `num_runs` times (independent
random seeds) and, every `bin_size` steps, tallies how often arm 1 was
pulled in each state across *all* runs, writing the aggregate empirical
probability to `convergence.dat` (columns: `step p(arm1|state0)
p(arm1|state1)`). A single run's per-bin counts are too small to give a
smooth curve — averaging over many runs is what makes the plot readable
without needing a longer or shorter run. `convergence.asy` plots the two
probabilities against training step, starting near 0.5 (a genuine coin toss,
since both arms tie at `Q = 0` initially) and converging to plateaus near
0.95 and 0.05 rather than 1.0 and 0.0 — the gap from the extremes is the
fixed `epsilon = 0.1` still picking a uniformly random arm 10% of the time
even after the policy has converged.

Run it with:

```
python3 convergence.py
asy -f pdf convergence.asy
```

## two_armed_bandit.asy

A purely decorative cartoon drawing of a two-armed bandit (slot machine) —
a masked cabinet with two side levers and two reel windows, one per arm.
No simulation logic, just a fun illustration to go with the name of the
repo.

The background is controlled by `pen backgroundColor`, set to `black` by
default; override it before that line to change it.

Run it with:

```
asy -f pdf two_armed_bandit.asy
```
