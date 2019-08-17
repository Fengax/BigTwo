from random import  shuffle
####################################################################################################################
RANK_ORDER = '34567890JQKA2'
SUIT_ORDER = 'DCHS'


def card_value(card):
    try:
        return RANK_ORDER.find(card[0]) * 4 + SUIT_ORDER.find(card[1])
    except Exception as ex:
        return 0


def is_higher(card1, card2):
    return card_value(card1) > card_value(card2)


def sort_cards(cards):
    cards.sort(key=card_value)
    return cards


def find_greater(hand, best_play_value, lo):
    size = len(hand)
    if lo >= size:
        lo = size - 1
    hi = size - 1
    while lo < hi:
        mi = (lo + hi) // 2
        if best_play_value >= card_value(hand[mi]):
            lo = mi + 1
        else:
            hi = mi
    if best_play_value < card_value(hand[hi]):
        return [hand[hi]], hi
    return [], -1


def reset_map():
    global hand_map
    hand_map = [True] * 52


def fill_map(round_history):
    global hand_map
    if len(round_history) > 0:
        trick = round_history[0]
        if number_in_round == 2:
            for player, play in trick:
                if len(play) == 0:
                    continue
                for p in play:
                    if len(p) > 0:
                        hand_map[card_value(p)] = False


def fill_myself(hand):
    global hand_map
    for p in hand:
        if len(p) > 0:
            hand_map[card_value(p)] = False


def find_biggest_code():
    global hand_map
    for i in range(0, 52):
        if hand_map[52-i-1]:
            return 52-i-1


def find_last_beat_player(round_history, play_to_beat):
    size_trick = len(round_history)
    if size_trick == 0:
        return -1, 0
    last_trick = round_history[size_trick - 1]
    size_play = len(last_trick)
    if size_play == 0:
        if size_trick >= 2:
            last_trick = round_history[size_trick - 2]
            size_play = len(last_trick)
            if size_play == 0:
                return -1, 0
        else:
            return -1, 0
    pass_num = 0
    for i in range(0, size_play):
        player, play = last_trick[size_play-i-1]
        if len(play) == 0:
            pass_num += 1
        if play == play_to_beat:
            return player, pass_num
    return -1, 0


def find_others_mim_hand(hand_sizes, player_no):
    mim = 13
    for i in range(0, 4):
        if i == player_no:
            continue
        if hand_sizes[i] < mim:
            mim = hand_sizes[i]
    return mim


def is_prev_player(last_beat_player, player_no):
    return last_beat_player - player_no == -1 or last_beat_player - player_no == 3

def is_next_player(last_beat_player, player_no):
    return last_beat_player - player_no == 1 or last_beat_player - player_no == -3


number_in_round = 0
my_strategy = 0
last_round_no = -1
hand_map = [True] * 52


def play(hand, is_start_of_round, play_to_beat, round_history, player_no, hand_sizes, scores, round_no):
    global last_round_no, number_in_round, my_strategy
    hand = sort_cards(hand)
    my_hand_size = len(hand)
    if last_round_no != round_no:
        number_in_round = 0
        reset_map()
    fill_map(round_history)
    fill_myself(hand)
    last_round_no = round_no
    #will_play, low_num = find_greater(hand, card_value("6S"), 0)
    #will_play, num = find_greater(hand, card_value("QS"), 0)
    #high_num = my_hand_size - num
    if number_in_round == 0:
        hand_map[0] = False
    number_in_round += 1

    # start to play
    biggest_code = find_biggest_code()
    if my_hand_size == 2 and card_value(hand[1]) > biggest_code:
        return [hand[1]]
    last_beat_player, pass_num_in_this_turn = find_last_beat_player(round_history, play_to_beat)
    min_others_hand_size = find_others_mim_hand(hand_sizes, player_no)
    if len(play_to_beat) == 0:
        if is_start_of_round:
            return ['3D']
        if min_others_hand_size == 1 and my_hand_size >= 2:
            return [hand[my_hand_size//2]]
        if my_hand_size == 3:
            m = card_value(hand[my_hand_size-1])
            if m > biggest_code:
                return [hand[1]]
        return [hand[0]]

    is_prev_me = is_prev_player(last_beat_player, player_no)
    is_next_me = is_next_player(last_beat_player, player_no)

    best_play_value = card_value(play_to_beat[0])
    only_2_player = False
    if number_in_round == 3:
        pass_no = 0
        for ii in range(0, 4):
            if hand_sizes[ii] == 13:
                pass_no += 1
                if pass_no >= 2:
                    only_2_player = True
                    break

    if min_others_hand_size <= 2 and my_hand_size > 1:
        will_play, greater_no = find_greater(hand, best_play_value, my_hand_size//2)
    else:
        will_play, greater_no = find_greater(hand, best_play_value, 0)
        if len(will_play) == 0:
            return will_play
        will_play_code = card_value(will_play[0])
        if will_play_code > biggest_code or only_2_player:
            return will_play
        if will_play_code > card_value("QS") and not is_next_me:
            prev_player_no = player_no - 1
            if prev_player_no < 0:
                prev_player_no = 3
            if hand_sizes[prev_player_no] >= 6:
                return []
        if will_play_code >= card_value("KD") and is_prev_me:
            how_many_greater = my_hand_size - greater_no
            bigger = will_play_code - best_play_value
            if bigger >= 8 and min_others_hand_size >= 6 and will_play_code > card_value("KC") and how_many_greater <= 2:
                return []
        if min_others_hand_size > 10 and will_play_code >= card_value("KD"):  # someone play nonsense
            return []
    return will_play
######################################################################################################################

ranks = "34567890JQKA2"
suits = "DCHS"
round = 1
round_history = []
trick_play = []

def compare_card(player, best):
    if player[:2] == "10":
        rank_player = ranks.find("0") * 10
        suit_player = suits.find(player[2])
    else:
        rank_player = ranks.find(player[0]) * 10
        suit_player = suits.find(player[1])

    player_card = rank_player + suit_player

    if best[:2] == "10":
        rank_best = ranks.find("0") * 10
        suit_best = suits.find(best[2])
    else:
        rank_best = ranks.find(best[0]) * 10
        suit_best = suits.find(best[1])

    best_card = rank_best + suit_best

    if player_card > best_card:
        return True
    else:
        return False


def int_to_deck(input):
    input.sort()
    output = []
    for i in input:
        rank = ranks[i//10]
        suit = suits[i%10]
        if rank == "0":
            rank = "10"
        card = rank + suit
        output.append(card)
    return output

while True:
    decks = []
    int_deck = []

    for x in range(0, 13):
        rank = x * 10
        for y in range(0, 4):
            suit = y
            card_code = rank + suit
            int_deck.append(card_code)

    shuffle(int_deck)
    print("Decks shuffled")

    for i in range(0,4):
        decks.append(int_to_deck(input=int_deck[i*13:(i+1)*13]))

    print("Decks assigned to 4 players.")
    print("You are player 1. Your deck is: " + str(decks[0]))
    print("Round " + str(round) + " begins.")
    play_to_beat = []
    count = 0
    passed = [0, 0, 0, 0]
    is_finish = False
    round_history.append(trick_play)
    trick_play = []
    is_start = 0
    while True:
        for i in range(0, 4):
            if "3D" in decks[i]:
                is_start = i

        print("Your deck: " + str(decks[0]))


        if is_start == 0 and count == 0:
            print("Player 1 has 3D. Player one is starting.")
            play_to_beat = ["3D"]
            decks[0].remove("3D")
            count += 1
        elif count == 0:
            pass
        else:
            player_play = input("Your turn. Deal a card or pass: ")
            if player_play in decks[0]:
                if len(play_to_beat) == 0:
                    if player_play[:2] == "10":
                        play_to_beat = ["0" + player_play[2]]
                    else:
                        play_to_beat = [player_play]
                    decks[0].remove(player_play)
                    passed = [0,0,0,0]
                    print("Player 1 (you) played " + player_play)
                    for a in range(0, 4):
                        if len(decks[a]) == 0:
                            is_finish = True
                            print("Player " + str(a + 1) + " has no cards left in their deck. Player " + str(
                                a + 1) + " has won the game!")
                            break
                    if is_finish:
                        break
                    trick_play.append((0, [player_play]))
                elif compare_card(player_play, play_to_beat[0]):
                    if player_play[:2] == "10":
                        play_to_beat = ["0" + player_play[2]]
                    else:
                        play_to_beat = [player_play]
                    decks[0].remove(player_play)
                    passed = [0,0,0,0]
                    print("Player 1 (you) played " + player_play)
                    for a in range(0, 4):
                        if len(decks[a]) == 0:
                            is_finish = True
                            print("Player " + str(a + 1) + " has no cards left in their deck. Player " + str(
                                a + 1) + " has won the game!")
                            break
                    trick_play.append((0, [player_play]))
                else:
                    print("Your played card is smaller than the current card. Please enter a card that is bigger than the current card or pass.")
                    continue
            elif player_play == "pass":
                print("Player 1 (you) passed")
                trick_play.append((0, []))
                passed[0] = 1
                passcount = passed.count(1)
                if passcount == 3:
                    player_num = passed.index(0) + 1
                    passed = [0, 0, 0, 0]
                    play_to_beat = []
                    print("All players have passed. Player " + str(player_num) + " is starting a new trick.")
                    if player_num == 1:
                        play_to_beat = []
                        continue
                    else:
                        for i in range(player_num, 5):
                            bot_play = play(hand=decks[i - 1], is_start_of_round=False, play_to_beat=play_to_beat,
                                            round_history=round_history, player_no=(i - 1),
                                            hand_sizes=(len(decks[0]), len(decks[1]), len(decks[2]), len(decks[3])),
                                            scores=0,
                                            round_no=round)
                            if len(bot_play) == 0:
                                print("Player " + str(i) + " has played a pass." + "They have " + str(
                                    len(decks[i - 1])) + " cards left.")
                                passed[i - 1] = 1
                                trick_play.append((i-1, []))
                            else:
                                if bot_play[0][:2] == "10":
                                    play_to_beat = ["0" + bot_play[0][2]]
                                else:
                                    play_to_beat = [bot_play[0]]
                                decks[i - 1].remove(bot_play[0])
                                passed = [0,0,0,0]
                                print("Player " + str(i) + " has played " + bot_play[0] + ". They have " + str(
                                    len(decks[i - 1])) + " cards left.")
                                for a in range(0, 4):
                                    if len(decks[a]) == 0:
                                        is_finish = True
                                        print("Player " + str(a + 1) + " has no cards left in their deck. Player " + str(
                                            a + 1) + " has won the game!")
                                        break
                                if is_finish:
                                    break
                                trick_play.append((i-1, bot_play))
                        if is_finish:
                            break
                        continue
            else:
                print("Your entry is not valid. Please make sure your entry matches one of the cards in your deck. If you want to play a pass enter 'pass'")
                continue

        if is_finish:
            break

        for i in range(2, 5):
            if is_start == (i-1) and count == 0:
                bot_play = play(hand=decks[i - 1], is_start_of_round=True, play_to_beat=play_to_beat,
                                round_history=round_history, player_no=(i - 1),
                                hand_sizes=(len(decks[0]), len(decks[1]), len(decks[2]), len(decks[3])), scores=0,
                                round_no=round)
                play_to_beat = bot_play
                decks[i-1].remove("3D")
                print("Player " + str(i) + " has 3D. Player " + str(i) + " is starting.")
                count += 1
            elif count == 0:
                pass
            else:
                bot_play = play(hand=decks[i-1], is_start_of_round=False, play_to_beat=play_to_beat, round_history=round_history, player_no=(i-1), hand_sizes=(len(decks[0]), len(decks[1]), len(decks[2]), len(decks[3])), scores=0, round_no=round)
                if len(bot_play) == 0:
                    print("Player " + str(i) + " has played a pass." + "They have " + str(len(decks[i-1])) + " cards left.")
                    passed[i-1] = 1
                    passcount = passed.count(1)
                    if passcount == 3:
                        player_num = passed.index(0) + 1
                        passed = [0, 0, 0, 0]
                        play_to_beat = []
                        print("All players have passed. Player " + str(player_num) + " is starting a new trick.")
                        if player_num == 1:
                            play_to_beat = []
                            break
                        else:
                            for b in range(player_num, 5):
                                bot_play = play(hand=decks[b - 1], is_start_of_round=False, play_to_beat=play_to_beat,
                                                round_history=round_history, player_no=(b - 1),
                                                hand_sizes=(len(decks[0]), len(decks[1]), len(decks[2]), len(decks[3])),
                                                scores=0,
                                                round_no=round)
                                if len(bot_play) == 0:
                                    print("Player " + str(b) + " has played a pass." + "They have " + str(
                                        len(decks[b - 1])) + " cards left.")
                                    passed[b - 1] = 1
                                    trick_play.append((b - 1, []))
                                else:
                                    if bot_play[0][:2] == "10":
                                        play_to_beat = ["0" + bot_play[0][2]]
                                    else:
                                        play_to_beat = [bot_play[0]]
                                    passed = [0,0,0,0]
                                    decks[b - 1].remove(bot_play[0])
                                    print("Player " + str(b) + " has played " + bot_play[0] + ". They have " + str(
                                        len(decks[b - 1])) + " cards left.")
                                    trick_play.append((b - 1, bot_play))
                                    for a in range(0, 4):
                                        if len(decks[a]) == 0:
                                            is_finish = True
                                            print("Player " + str(a + 1) + " has no cards left in their deck. Player " + str(
                                                a + 1) + " has won the game!")
                                            break
                                    if is_finish:
                                        break
                                if is_finish:
                                    break
                            if is_finish:
                                break
                            break
                    if is_finish:
                        break
                else:
                    if bot_play[0][:2] == "10":
                        play_to_beat = ["0" + bot_play[0][2]]
                    else:
                        play_to_beat = [bot_play[0]]
                    decks[i-1].remove(bot_play[0])
                    trick_play.append((i - 1, bot_play))
                    passed = [0, 0, 0, 0]
                    print("Player " + str(i) + " has played " + bot_play[0] + ". They have " + str(
                        len(decks[i - 1])) + " cards left.")
                    for a in range(0, 4):
                        if len(decks[a]) == 0:
                            is_finish = True
                            print("Player " + str(a + 1) + " has no cards left in their deck. Player " + str(
                                a + 1) + " has won the game!")
                            break
                    if is_finish:
                        break
        if is_finish:
            break
        count += 1

    exit = input("Would you like to play again?(y/n) ")
    if exit == "n":
        break
    elif exit == "y":
        print("Starting a new round")
        round += 1
    else:
        print("Your command is not recognized. Please enter either 'y' or 'n'")



