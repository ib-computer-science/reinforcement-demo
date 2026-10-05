# reinforcement-demo

A minimal, self-contained reinforcement learning toy example.

## bandit_env.py

The environment shared by `q_learn_bandit.py`, `play_bandit.py`, and
`q_learn_convergence.py`: the `true_p` table and the `pull(state, arm)` function
(reward + next state for pulling an arm in a state). Factored out so all
three simulate the exact same dynamics instead of each keeping their own
copy.

## q_learn_bandit.py

A two-armed bandit with two **states**, where pulling an arm deterministically
decides the *next* state — satisfying the Markov property, since the next
state depends only on the current state and action, never on history.

- State 0 ("fresh"): arm 0 wins with probability 0.5, arm 1 wins with
  probability 0.9.
- State 1 ("depleted"): arm 0 still wins with probability 0.5, but arm 1's
  win probability has crashed to 0.1.
- Pulling arm 1 deterministically moves to state 1 (it depletes itself);
  pulling arm 0 deterministically moves to state 0 (it lets arm 1 recover).

Because actions now have delayed consequences, a plain reward-average `Q`
can't tell arm 0 and arm 1 apart — both average 0.5 reward over time.
Instead this uses the real Q-learning update:

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

The learning rate for each `(state, arm)` pair starts at `alpha0` and decays
as `alpha0 * decay_steps / (decay_steps + times_chosen[state][arm])` — much
more gently than a plain `1 / times_chosen` schedule, which technically
guarantees exact convergence but does so so slowly (it weights every
historical sample equally) that the printed `Q` table is still visibly far
from its true fixed point after a million steps. This schedule reaches the
fixed point within a few thousand steps and keeps settling from there,
rather than either crawling for a million steps (`1 / times_chosen`) or
jittering around it forever (a flat constant rate). Either way, the
*policy* converges almost immediately regardless of the learning-rate
schedule — it only needs the relative order of `Q[state][0]` vs
`Q[state][1]` to be right, not their precise values — so this only changes
how quickly the printed numbers look settled, not how good the agent's
decisions are.

Run it with:

```
python3 q_learn_bandit.py
```

## play_bandit.py

Lets a human play the same environment from `bandit_env.py` interactively:
type `L` or `R` to pull an arm, and it reports `win!` or `no win`. Like the
Q-learning agent, you aren't shown the current state or the win
probabilities, during play or after — only your total and average reward
once you quit (empty input) — so you have to find a good strategy by trial
and error too.

Run it with:

```
python3 play_bandit.py
```

## q_learn_convergence.py + q_learn_convergence.asy

Visualizes how the agent's *behavior* converges during training in
`q_learn_bandit.py` — not the abstract `Q` values, but what the agent
actually does, including the ongoing exploration.

`q_learn_convergence.py` reruns the same simulation `num_runs` times
(independent random seeds) and, every `bin_size` steps, tallies how often
arm 1 was pulled in each state across *all* runs, writing the aggregate
empirical probability to `q_learn_convergence.dat` (columns: `step
p(arm1|state0) p(arm1|state1)`). A single run's per-bin counts are too
small to give a smooth curve — averaging over many runs is what makes the
plot readable without needing a longer or shorter run.
`q_learn_convergence.asy` plots the two probabilities against training
step, starting near 0.5 (a genuine coin toss, since both arms tie at `Q =
0` initially) and converging to plateaus near 0.95 and 0.05 rather than
1.0 and 0.0 — the gap from the extremes is the fixed `epsilon = 0.1` still
picking a uniformly random arm 10% of the time even after the policy has
converged.

Run it with:

```
python3 q_learn_convergence.py
asy -f pdf q_learn_convergence.asy
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
