# Telegram Red Black Bot
## Program Flow
1. Register users in a group
1. Run through group and ask questions
1. Queue system - sort (pseudorandomly) Handle members joining in the midst of a round
1. Gameplay:
    1. Current queue leader asks a question
    1. Everyone plays Red/Black
    1. Number of red/black are shown on screen
        1. If both numbers are same, players vote for which color to reveal
        1. Repeat 1x if it is a tie, if not random
    1. `n+1` attempts to reveal a player's color for `n` selections of the minority color.
        1. Attempts to reveal a player are votes. The player who is voted for the most will have his card choice revealed.
        1. if votes are tied, reduce the vote to the tied users
        1. Repeated ties: repeat 1x, if not random

1. There will be a 45 second voting timeout, 1m 30s question timeout

## To-do
- [ ] Register multiple users in a group setting
- [ ] Have users vote within the group but privately
- [ ] Bot will PM users when their time is about to run out.