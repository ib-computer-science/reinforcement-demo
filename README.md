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
