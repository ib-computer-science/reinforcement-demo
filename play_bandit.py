from bandit_env import pull

state = 0
round_number = 0
total_reward = 0

while True:
    choice = input('pull arm (l/r)? ').strip().lower()

    if choice == '':
        break
    if choice not in ('l', 'r'):
        print('  please enter l, r, or nothing to quit')
        continue

    chosen_arm = 0 if choice == 'l' else 1
    reward, next_state = pull(state, chosen_arm)

    round_number += 1
    total_reward += reward
    state = next_state

    print('  win!' if reward else '  no win')

if round_number > 0:
    print(f'\nPlayed {round_number} rounds, total reward {total_reward} '
          f'(average {total_reward / round_number:.3f} per round).')
else:
    print('\nNo rounds played.')
