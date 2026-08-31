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
