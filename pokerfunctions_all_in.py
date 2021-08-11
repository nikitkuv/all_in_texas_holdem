from collections import Counter
import termcolor as tc

def results_counter(list_input:list):
    """
    given 7 cards (hand+table) defines the combination, calculates its score (combination + kicker score) and nominals of kickers

    Flush royal = 1000
    Straight flush = 900
    Four of a kind = 800
    Full house = 700
    Flush = 600
    Straight = 500
    Three of a kind = 400
    Two pairs = 300
    Pair = 200
    High card = card score of a high card

    :param list_input (list) - [(card name (str), card suit (str), card nominal (int)), ...] - list of one player cards:
    :return result (list) - [combination score (int), combination name (str), nominals of kickers (list of int)] - combination,
    its score and nominals of kickers, in this script is assigned to round_results variable in the following funcrions

    return example: [306, 'Two Pairs', [5, 13]]:
    """

    #initializing lists and counters for straight checking algorithm
    names_order = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A'] #card order
    straight = []  #stores possible straight combinations

    #initializing lists and counters for quantitative combinations checking algorithm (where we count quantities of nominals)
    count_names = [[i[0] for i in list_input].count(i) for i in [i[0] for i in list_input]] #counter for every single card of a hand (7 elements)
    count_names_unique = Counter() #counter for unique cards of a hand (length depends on unique cards of the hand)
    for name in list_input:
        count_names_unique[name[0]] += 1
    nc_values = list(count_names_unique.values()) #values of unique cards counter, used for more convenient way of checking for quantitative combinations
    fh_tp_index_list = [] #stores indexes of count_names elements for counts needed in particular combination
    fh_tp_noms = [] #stores values of cards from noms list needed to be add to the final score to manage situations with the same combinations using high card

    #initializing lists and counters for flush checking algorithm
    suits_counter = Counter()
    for suit in list_input:
        suits_counter[suit[1]] += 1
    flush_suit_noms = [] #stores all the hand cards which are in the flush
    flush_suit = ''
    for k, v in suits_counter.items():
        if v == max(suits_counter.values()):
            flush_suit = k
        else:
            continue
    for i in list_input:
        if i[1] == flush_suit:
            flush_suit_noms.append(i[2])
        else:
            continue

    #common data structures
    noms = [i[2] for i in list_input] #game value of recieved hand: used for additional scoring in case of same type of combinations
    result = [None, None, None] # output as a list: [score, name of the combination]

    # check for a flush
    for i in suits_counter:
        if suits_counter[i] > 4:
            sorted_list = sorted(list_input, key=lambda i: i[2])
            # check if there are any cards ordered according to name_order list
            for index, i in enumerate(sorted_list):
                order_index = names_order.index(i[0])
                if index != 6 and i[0] != 'A' and len(straight) != 4:
                    if sorted_list[index + 1][0] == names_order[order_index + 1] and i[1] == flush_suit:
                        straight.append(i[2])
                        continue
                    else:
                        straight.clear()
                elif index == 6 or i[0] == 'A' or len(straight) == 4 or len(straight) == 5 or len(straight) == 6:
                    if sorted_list[index - 1][0] == names_order[order_index - 1] and sorted_list[index - 2][0] == names_order[order_index - 2] and sorted_list[index - 3][0] == names_order[order_index - 3]:
                        straight.append(i[2])
                        continue
                    else:
                        straight.clear()
                else:
                    continue
            # check for a straight flush or royal flush
            if len(straight) > 4:
                max_straight = max(set(straight))
                if max_straight == 13:
                    result[0] = 1000
                    result[1] = 'Royal Flush'
                    return result
                else:
                    result[0] = 900 + max(set(straight))
                    result[1] = 'Straight Flush'
                    return result
            else:
                result[0] = 600 + max(flush_suit_noms)
                result[1] = 'Flush'
                return result
        else:
            continue

    #check for a straight
    sorted_list = sorted(list_input, key= lambda i: i[2])
    #check if there are any cards ordered according to name_order list
    for index, i in enumerate(sorted_list):
        order_index = names_order.index(i[0])
        if index != 6 and i[0] != 'A' and len(straight) != 4:
            if sorted_list[index+1][0] == names_order[order_index+1]:
                straight.append(i[2])
                continue
            else:
                straight.clear()
        elif index == 6 or i[0] == 'A' or len(straight) == 4 or len(straight) == 5 or len(straight) == 6:
            if sorted_list[index - 1][0] == names_order[order_index - 1] and sorted_list[index - 2][0] == names_order[order_index - 2] and sorted_list[index - 3][0] == names_order[order_index - 3]:
                straight.append(i[2])
                continue
            else:
                straight.clear()
        else:
            continue
    #if there are 5 or more cards ordered desired way then we have a straight
    if len(straight) > 4:
        result[0] = 500 + max(set(straight))
        result[1] = 'Straight'
        return result

    #check for quantitative combinations
    else:
        if max(count_names_unique.values()) == 4:
            result[0] = 800
            result[1] = 'Four Of A Kind'
            return result
        if max(set(count_names)) == 3 and count_names.count(2) != 0:
            #take indexes of counts exceeded 1 (basically 3 and 2 here) to manage two or more full houses in a round
            for index, l in enumerate(count_names):
                if count_names[index] == 3 or count_names[index] == 2:
                    fh_tp_index_list.append(index)
                else:
                    continue
            #take values of cards for those caounts
            for i in fh_tp_index_list:
                fh_tp_noms.append(noms[i])
            max_three = max(set(fh_tp_noms)) #take the highest card of counts exceeded 1
            #clear index and value lists to consider for highest card in counts equal 2 if cards of count 3 are equal
            fh_tp_index_list.clear()
            fh_tp_noms.clear()
            # take indexes of counts equal 2 to manage two or more full houses in a round with the same cards in count 3
            for index, l in enumerate(count_names):
                if count_names[index] == 2:
                    fh_tp_index_list.append(index)
                else:
                    continue
            #take values of cards for those caounts
            for i in fh_tp_index_list:
                fh_tp_noms.append(noms[i])
            max_two = max(fh_tp_noms) #take the highest card of counts exceeded 1
            #create the output
            result[0] = 700 + max_three + max_two
            result[1] = 'Full House'
            return result
        if max(set(count_names)) == 3 and nc_values.count(3) == 1 and nc_values.count(2) == 0:
            noms_sorted = sorted(noms, reverse=True)
            for i in range(3):
                noms_sorted.remove(noms[count_names.index(3)])
            result[0] = 400 + noms[count_names.index(3)]  #the second term is to manage two three of a kind in a round
            result[1] = 'Three Of A Kind'
            result[2] = noms_sorted[:2]
            return result
        if max(set(count_names)) >= 2 and nc_values.count(2) >= 2:
            noms_sorted = sorted(noms, reverse=True)
            duplicate = noms_sorted[:]
            for i in duplicate:
                if duplicate.count(i) == 2:
                    noms_sorted.remove(i)
                else:
                    continue
            #take indexes of counts exceeded 1 to manage two or more two pairs in a round
            for index, l in enumerate(count_names):
                if count_names[index] == 2:
                    fh_tp_index_list.append(index)
                else:
                    continue
            for i in fh_tp_index_list:
                fh_tp_noms.append(noms[i])
            max_1 = max(set(fh_tp_noms)) #take the card from the first (highest) pair
            for i in range(2):
                fh_tp_noms.remove(max_1)
            max_2 = max(set(fh_tp_noms))
            noms_sorted.insert(0, max_2)
            result[0] = 300 + max_1
            result[1] = 'Two Pairs'
            result[2] = noms_sorted[:2]
            return result
        if max(count_names_unique.values()) == 2 and nc_values.count(2) == 1:
            noms_sorted = sorted(noms, reverse=True)
            for i in range(2):
                noms_sorted.remove(noms[count_names.index(2)])
            result[0] = 200 + noms[count_names.index(2)]
            result[1] = 'One Pair'
            result[2] = noms_sorted[:3]
            return result
        if max(count_names_unique.values()) == 1:
            noms_sorted = sorted(noms, reverse=True)
            noms_sorted.remove(max(noms_sorted))
            result[0] = max(set(noms)) #take the highest value
            result[1] = 'High Card'
            result[2] = noms_sorted[:4]
            return result

#defining a function to find a sequence of winning players in the order how they should get chips
def winner_list(round_results:list):
    """
    sorts the return of results_counter() function in descending order of combination score giving the order how players
    must collect their chips in case of more than one winners

    :param round_results (list) (return of results_counter function defined above) - [306, 'Two Pairs', [5, 13]] - combination,
    its score and nominals of kickers:
    :return sorted_list (list) - the order how players must collect their chips in case of more than one winners:

    return example: [[['N', 13, 'High Card', [9, 7, 6, 5], 990.0], [player]], [group by combinations power]]
    """
    flag_list = round_results[:]
    sorted_list = []
    while flag_list:
        points = []
        for i in flag_list:
            points.append(i[1])
        max_value = max(points)
        count_max = points.count(max_value)
        if count_max > 1:
            max_value_list = []
            for index, i in enumerate(flag_list):
                if points.count(i[1]) == count_max:
                    max_value_list.append(i)
                else:
                    continue
            first_kickers = []
            second_kickers = []
            third_kickers = []
            forth_kickers = []
            for i in max_value_list:
                if len(i[3]) == 2:
                    first_kickers.append([i[3][0], i[0]])
                    second_kickers.append([i[3][1], i[0]])
                elif len(i[3]) == 3:
                    first_kickers.append([i[3][0], i[0]])
                    second_kickers.append([i[3][1], i[0]])
                    third_kickers.append([i[3][2], i[0]])
                else:
                    first_kickers.append([i[3][0], i[0]])
                    second_kickers.append([i[3][1], i[0]])
                    third_kickers.append([i[3][2], i[0]])
                    forth_kickers.append([i[3][3], i[0]])
            max_first = max(first_kickers, key=lambda i: i[0])
            fk_max = [i for i in first_kickers if i[0] == max_first[0]]
            if len(fk_max) > 1:
                fk_max_names = [i[1] for i in fk_max]
                sk_max = [i for index, i in enumerate(second_kickers) if i[1] in fk_max_names]
                max_second = max(sk_max, key=lambda i: i[0])
                sk_max = [i for i in sk_max if i[0] == max_second[0]]
                if len(sk_max) > 1 and len(third_kickers) != 0:
                    sk_max_names = [i[1] for i in sk_max]
                    tk_max = [i for index, i in enumerate(third_kickers) if i[1] in sk_max_names]
                    max_third = max(tk_max, key=lambda i: i[0])
                    tk_max = [i for i in tk_max if i[0] == max_third[0]]
                    if len(tk_max) > 1 and len(forth_kickers) != 0:
                        tk_max_names = [i[1] for i in tk_max]
                        fk_max = [i for index, i in enumerate(forth_kickers) if i[1] in tk_max_names]
                        max_forth = max(fk_max, key=lambda i: i[0])
                        fk_max = [i for i in fk_max if i[0] == max_forth[0]]
                        if len(fk_max) > 1:
                            winner_name = [i[1] for i in fk_max]
                            winners = []
                            flag_flag_list = flag_list[:]
                            for i in flag_flag_list:
                                if i[0] in winner_name:
                                    winners.append(i)
                                    flag_list.remove(i)
                            sorted_list.append(winners)
                        else:
                            winner_name = fk_max[0][1]
                            for i in flag_list:
                                if i[0] == winner_name:
                                    sorted_list.append([i])
                                    flag_list.remove(i)
                                else:
                                    continue
                    else:
                        if len(third_kickers) == 1:
                            winner_name = tk_max[0][1]
                            for i in flag_list:
                                if i[0] == winner_name:
                                    sorted_list.append([i])
                                    flag_list.remove(i)
                                else:
                                    continue
                        else:
                            winner_name = [i[1] for i in tk_max]
                            winners = []
                            flag_flag_list = flag_list[:]
                            for i in flag_flag_list:
                                if i[0] in winner_name:
                                    winners.append(i)
                                    flag_list.remove(i)
                            sorted_list.append(winners)
                else:
                    if len(second_kickers) == 1:
                        winner_name = sk_max[0][1]
                        for i in flag_list:
                            if i[0] == winner_name:
                                sorted_list.append([i])
                                flag_list.remove(i)
                            else:
                                continue
                    else:
                        winner_name = [i[1] for i in sk_max]
                        winners = []
                        flag_flag_list = flag_list[:]
                        for i in flag_flag_list:
                            if i[0] in winner_name:
                                winners.append(i)
                                flag_list.remove(i)
                        sorted_list.append(winners)
            else:
                winner_name = fk_max[0][1]
                for i in flag_list:
                    if i[0] == winner_name:
                        sorted_list.append([i])
                        flag_list.remove(i)
                    else:
                        continue
        else:
            for i in flag_list:
                if i[1] == max_value:
                    sorted_list.append([i])
                    flag_list.remove(i)
                else:
                    continue
    return sorted_list

#defining a function to calculate chips each player earned for the round
def chips_counter_all_in(round_results:list, sorted_rr:list, small_blind, big_blind):
    """
    based on returns of results_counter() and winner_list functions() returns:
    - list of names and total chips won,
    - list of data on what was a claimed bank, name and total chips won,
    - list of bets

    :param round_results (list) - combination, its score and nominals of kickers:
    :param sorted_rr (list) - the order how players must collect their chips in case of more than one winners:
    :param small_blind (int) - small blind:
    :param big_blind (int) - big blind:
    :return results (list) - list of names and total chips won:
    :return bank (list) - list of data on what was a claimed bank, name and total chips won:
    :return chips_for_betting (list) - list of bets:

    return examples: results = [['N', 2000.0], ['A', 0]]
                    bank = [[995.0, ['N'], 2000.0], [990.0, ['A'], 1980.0]]
                    chips_for_betting = [995.0, 990.0]
    """
    chips = []
    for i in round_results:
        chips.append(i[4])
    if chips.count(max(chips)) == 1:
        max_bet = sorted(chips)[1] #if there is one player having the highest amount of chips then we take the second high amount as a maximum bet
    else:
        max_bet = max(chips)
    chips_for_betting = [i for i in set(chips) if i <= max_bet] #list of all bets in the game
    bank = [] #list of lists consisting of a bet, a list of players who made this bet and a bank they claim
    names = []
    n_players = len(round_results)
    for i in chips_for_betting:
        for j in round_results:
            if i == max_bet and j[4] >= i:
                names.append(j[0])
            elif j[4] == i:
                names.append(j[0])
            else:
                continue
        bank.append([i, names])
        names = []
    total_bank = float(small_blind + big_blind)
    for i in bank:
        total_bank += i[0]*len(i[1])
    for i in bank:
        if i[0] != max_bet:
            i.append(i[0] * n_players)
        else:
            i.append(total_bank)
    results = []
    for list_of_winners in sorted_rr:
        if len(list_of_winners) == 1:
            claimed_bank = 0
            for c_bank in bank:
                if list_of_winners[0][0] in c_bank[1]:
                    claimed_bank = c_bank[2]
                else:
                    continue
            if claimed_bank >= total_bank:
                results.append([list_of_winners[0][0], total_bank])
                total_bank = 0
            else:
                results.append([list_of_winners[0][0], claimed_bank])
                total_bank -= claimed_bank
        else:
            claimers_of_db = []
            divider_bank = total_bank / len(list_of_winners)
            for winner in list_of_winners:
                for c_bank in bank:
                    if winner[0] in c_bank[1]:
                        claimed_bank = c_bank[2]
                    else:
                        continue
                if claimed_bank < divider_bank:
                    results.append([winner[0], claimed_bank])
                    total_bank -= claimed_bank
                else:
                    claimers_of_db.append(winner)
            if len(claimers_of_db) != 0:
                while claimers_of_db:
                    claimers_count = 0
                    divider_bank_for_c = total_bank / len(claimers_of_db)
                    for claimer in claimers_of_db:
                        for c_bank in bank:
                            if claimer[0] in c_bank[1]:
                                claimed_bank = c_bank[2]
                            else:
                                continue
                        if claimed_bank < divider_bank_for_c:
                            results.append([claimer[0], claimed_bank])
                            claimers_of_db.remove(claimer)
                            total_bank -= claimed_bank
                        else:
                            claimers_count += 1
                    if claimers_count == len(claimers_of_db):
                        for c in claimers_of_db:
                            results.append([c[0], divider_bank_for_c])
                            total_bank -= divider_bank_for_c
                            claimers_of_db.remove(c)
                    else:
                        continue
    return results, bank, chips_for_betting

#defining colors for suits
def suits_color(suit):
    """
    colors suits

    :param suit str - suit string:
    :return str - colored string:
    """
    if suit == '♥' or suit == '♦':
        return tc.colored(suit, 'red')
    else:
        return suit

