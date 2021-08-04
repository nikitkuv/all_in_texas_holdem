import random
import pokerfunctions_all_in as pf

#initializing the deck
suits = ['♠', '♣', '♥', '♦']
names_nominals = [('2', 1), ('3', 2), ('4', 3), ('5', 4), ('6', 5), ('7', 6), ('8', 7), ('9', 8), ('10', 9), ('J', 10), ('Q', 11), ('K', 12), ('A', 13)]
deck = [(name, suit, nom) for name, nom in names_nominals for suit in suits]
random.shuffle(deck)

#initializing lists for holding players info
players = []
round_results = []
in_game = []
table = []

#initializing number of players
number_players = int(input('Input number of players: '))
while number_players > 9:
    number_players = int(input('Maximum number of players is 9, please input valid number of players: '))
print('')

#initializing players info
for index, i in enumerate(range(number_players)):
    name = input(f'Input the name of {i+1} player: ')
    players.append([name])
    players[index].append(float(1000)) #chips
    players[index].append([None]) #hand
print('')

#initializing dealer, small and big blinds indexes
dealer_index = 0
sb_index = 0
bb_index = 0

#playing process
while len(players) != 1:
    in_game = players.copy()
    in_game_temp = in_game[:]

    #checking if dealer index is in appropriate range and collecting initial bank from blinds and setting a dealer
    if dealer_index > len(in_game)-1:
        if len(in_game)-1 > 2:
            dealer_index = 0
            sb_index = 1
            bb_index = 2
        else:
            dealer_index, bb_index = 0, 0
            sb_index = 1
        small_blind = float(5)  
        big_blind = float(2 * small_blind)
        in_game[sb_index][1] -= small_blind
        if in_game[bb_index][1] >= big_blind:
            in_game[bb_index][1] -= big_blind
        else:
            big_blind = in_game[bb_index][1]
            in_game[bb_index][1] -= in_game[bb_index][1]
        print(f'The dealer is {in_game[dealer_index][0]} this round.')
        print(f'The small blind is {in_game[sb_index][0]} this round. Small blind equals {small_blind}')
        print(f'The big blind is {in_game[bb_index][0]} this round.')
        print('')
    elif dealer_index == len(in_game)-1:
        sb_index = 0
        bb_index = 1
        small_blind = float(5)
        big_blind = float(2 * small_blind)
        in_game[sb_index][1] -= small_blind
        if in_game[bb_index][1] >= big_blind:
            in_game[bb_index][1] -= big_blind
        else:
            big_blind = in_game[bb_index][1]
            in_game[bb_index][1] -= in_game[bb_index][1]
        print(f'The dealer is {in_game[dealer_index][0]} this round.')
        print(f'The small blind is {in_game[sb_index][0]} this round. Small blind equals {small_blind}')
        print(f'The big blind is {in_game[bb_index][0]} this round.')
        print('')
    elif dealer_index == len(in_game)-2:
        sb_index = dealer_index+1
        bb_index = 0
        small_blind = float(5)
        big_blind = float(2 * small_blind)
        in_game[sb_index][1] -= small_blind
        if in_game[bb_index][1] >= big_blind:
            in_game[bb_index][1] -= big_blind
        else:
            big_blind = in_game[bb_index][1]
            in_game[bb_index][1] -= in_game[bb_index][1]
        print(f'The dealer is {in_game[dealer_index][0]} this round.')
        print(f'The small blind is {in_game[sb_index][0]} this round. Small blind equals {small_blind}')
        print(f'The big blind is {in_game[bb_index][0]} this round.')
        print('')
    else:
        sb_index = dealer_index+1
        bb_index = dealer_index+2
        small_blind = float(5)
        big_blind = float(2 * small_blind)
        in_game[sb_index][1] -= small_blind
        if in_game[bb_index][1] >= big_blind:
            in_game[bb_index][1] -= big_blind
        else:
            big_blind = in_game[bb_index][1]
            in_game[bb_index][1] -= in_game[bb_index][1]
        print(f'The dealer is {in_game[dealer_index][0]} this round.')
        print(f'The small blind is {in_game[sb_index][0]} this round. Small blind equals {small_blind}.')
        print(f'The big blind is {in_game[bb_index][0]} this round.')
        print('')

    """
    because of initially dealing and moves are linked with in_game list, which is in turn created from players with indexes
    corresponding to order in which players were inputed (in other words, the first move will be for the player who was added
    first, which is incorrect if we have shifted blinds) - consequently we need to change order of player's moves depending
    on where dealer and blinds are, see below:
    """

    #defining the right order of players to make a move
    if dealer_index+2 != len(in_game)-1:
        temp = in_game[bb_index+1:] + in_game[:bb_index+1]
        in_game_temp = temp[:]
        in_game = temp[:]

    #setting list of players in the game this round
    for index, player in enumerate(in_game_temp):
        if index == (len(in_game_temp) - 1) and len(in_game) == 1:
            pass
        else:
            player[2] = [deck.pop() for i in range(2)][:]
            print(f'{player[0]}, here is your hand:', end=' ')
            for i in player[2]:
                print(i[0] + pf.suits_color(i[1]), end=' ')
            print('')
            a = input('What is your turn: call or fold? ')
            if a == 'call':
                continue
            else:
                in_game.remove(player)
    in_game_names = [i[0] for i in in_game]
    print('')

    #preparing the table
    if len(in_game) > 1:
        print(f'Total bank: {sum([i[1] for i in in_game]) + small_blind + big_blind}')
        print('')
        table = [deck.pop() for i in range(5)]
        print('Table: ')
        for i in table:
            print(i[0] + pf.suits_color(i[1]), end=' ')
        print('', end='\n')
        print('')

        #checking the best combination, creating list of winners
        for gplayer in in_game:
            gplayer[2].extend(table)
            round_results.append(pf.results_counter(gplayer[2])) #defining combinations and scores of combinations
        for index, i in enumerate(round_results): #['Name', 306, 'Two Pairs', [5, 13], 1000]
            i.insert(0, in_game[index][0])
            i.insert(5, in_game[index][1])
        sorted_rr = pf.winner_list(round_results) #sorting players in temrs of the power of combinations they gathered
        chips_count, bank, chips_for_betting = pf.chips_counter_all_in(round_results, sorted_rr, small_blind, big_blind) #[['Y', 800], ['A', 900.0], ['N', 0], ['D', 0]]
        cfb = sorted(chips_for_betting, reverse=True)

        #showing cards
        print('Gentlemen please show your cards!')
        print('')
        for index, j in enumerate(in_game):
            print(f'{j[0]}: {j[2][0][0]}{pf.suits_color(j[2][0][1])} {j[2][1][0]}{pf.suits_color(j[2][1][1])}', end='   ')
            for c in table:
                print(f'{c[0]}{pf.suits_color(c[1])}', end=' ')
            print(f'- {round_results[index][2]}')
        print('', end='\n')

        #substracting player's bet from its bank
        for p in players:
            if len(cfb) > 1 and p[0] in in_game_names:
                for b in cfb:
                    if p[1] >= b:
                        p[1] -= b
                        break
            elif p[0] in in_game_names:
                p[1] -= cfb[0]

        #distibuting winning chips between winners and showing indermediate results
        for p in players:
            for c in chips_count:
                if p[0] in c[0]:
                    p[1] += c[1]
        for j in chips_count:
            if j[1] != 0:
                print(f'{j[0]} got {j[1]} chips!')
        print('')
        print('Intermediate results:')
        for i in players:
            if i[1] < 0:
                print(f'{i[0]} has 0.0 chips.')
            else:
                print(f'{i[0]} has {i[1]} chips.')
        print('')

        #kicking players with 0 bank
        players_temp = players[:]
        for index, p in enumerate(players_temp):
            if p[1] <= 0:
                if index <= dealer_index:
                    dealer_index -= 1
                    """
                    ^
                    consider for preservation of dealer order: there are cases of missing order if index of loosing 
                    player goes before dealer index or is equal, because indexes of players shift on -1 but dealer 
                    index shifts +1 so we have 1 missing player following right after the loosing one
                    """
                players.remove(p)
                print(f'Player {p[0]} lost all the chips and left the game!')
                print('')

        #clearing containers and shuffling the deck
        table.clear()
        round_results.clear()
        deck = [(name, suit, nom) for name, nom in names_nominals for suit in suits]
        random.shuffle(deck)
        dealer_index += 1
    else:
        in_game[0][1] += small_blind + big_blind
        print(f'{in_game[0][0]} got the blinds, because other players have folded.')
        print('')
        print('Intermediate results:')
        for i in players:
            if i[1] < 0:
                print(f'{i[0]} has 0.0 chips.')
            else:
                print(f'{i[0]} has {i[1]} chips.')
        print('')
        deck = [(name, suit, nom) for name, nom in names_nominals for suit in suits]
        random.shuffle(deck)
        dealer_index += 1
        continue
else:
    print(f'The game is over! Aaaand...the winner: {players[0][0]}! Congrats!')
