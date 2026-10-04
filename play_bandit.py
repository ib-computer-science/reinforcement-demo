from bandit_env import true_p, pull

state_names = ['fresh', 'depleted']

state = 0
round_number = 0
total_reward = 0

print("You're playing the two-armed Markov bandit from markov_bandit.py.")
print('Pull arm 0 or arm 1 each round; try to find the best long-run strategy.')
print("Like the Q-learning agent, you don't get to see the win probabilities.")
print("Type 'q' to quit.\n")

while True:
    choice = input(f'[round {round_number + 1}, state {state} ({state_names[state]})] pull arm (0/1/q)? ').strip()

    if choice == 'q':
        break
    if choice not in ('0', '1'):
        print('  please enter 0, 1, or q')
        continue

    chosen_arm = int(choice)
    reward, next_state = pull(state, chosen_arm)

    round_number += 1
    total_reward += reward

    outcome = 'win!' if reward else 'no win'
    print(f'  {outcome} -> next state {next_state} ({state_names[next_state]})')

    state = next_state

if round_number > 0:
    print(f'\nPlayed {round_number} rounds, total reward {total_reward} '
          f'(average {total_reward / round_number:.3f} per round).')
    print(f'The hidden win probabilities were: state 0 {true_p[0]}, state 1 {true_p[1]}.')
else:
    print('\nNo rounds played.')
