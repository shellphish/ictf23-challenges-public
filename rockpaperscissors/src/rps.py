#!/usr/bin/env python3
import random
import os
import time

ROUNDS_TO_WIN = 20
ROUNDS_PLAYED = 0
PLAYER_WINS = 0
PLAYER_LOSSES = 0
WIN_STREAK = 0
MODE = 0
MAX_ROUNDS = 100
PAST = False

def bot_say(words, p1='',p2='',p3='',p4='',p5='',p6=''):
    p4 = words if p4 == '' else p4
    return f"""
     /~\\       {p1}
    |oo )      {p2}  
    _\=/_      {p3}
   /  _  \     {p4} 
  //|/.\|\\\\    {p5}
 ||  \ /  ||   {p6}
"""

RPC_DICT = {
    'r': 'rock',
    'p': 'paper',
    's': 'scissors'
}

def xor_encrypt_decrypt(text, key):
    encrypted_decrypted_chars = []
    for i in range(len(text)):
        # Perform XOR between the character and the key
        encrypted_decrypted_char = chr(ord(text[i]) ^ ord(key[i % len(key)]))
        encrypted_decrypted_chars.append(encrypted_decrypted_char)
    return ''.join(encrypted_decrypted_chars)

key = "3asd!!@*(&49OIO__"

def get_result(user_throw, computer_throw):
    if user_throw == computer_throw:
        # print('It\'s a tie!')
        return 0
    elif user_throw == 'r' and computer_throw == 's':
        # print('Rock beats scissors! You win!')
        return 1
    elif user_throw == 'p' and computer_throw == 'r':
        # print('Paper beats rock! You win!')
        return 1
    elif user_throw == 's' and computer_throw == 'p':
        # print('Scissors beats paper! You win!')
        return 1
    else:
        # print('You lose!')
        return -1

def bot_talk():
    global MODE
    if PLAYER_WINS == 0 and MODE == 0:
        print(bot_say("Since we're still strangers in this digital jungle, I'm going to spin the wheel of randomness and see where it lands!"))
        time.sleep(2)
        MODE = 1
    elif PLAYER_WINS < 5 and PLAYER_WINS >0 and MODE == 1:
        print(bot_say("Wow, look at you being all smart and stuff! Mind if I sneak into your brain's shadow and pick up some genius crumbs?"))
        time.sleep(2)
        MODE = 2
    elif PLAYER_WINS == 5 and MODE == 2:
        print(bot_say("Ah, I've finally got your playbook figured out!"))
        time.sleep(2)
        MODE = 3


def get_computer_throw(user_history, computer_history):
    if PLAYER_WINS == 0:
        return random.choice(['r', 'p', 's'])
    try:
        if PLAYER_WINS < 5:
            return user_history[-1]
        prediction = dict()
        games = list(zip(user_history, computer_history))
        for i, (u, c) in enumerate(games[:-1]):
            prediction[(u,c)] = games[i+1][0]
        last_set = games[-1]
        if last_set in prediction:
            p = prediction[last_set]
            if p == 'r': return 'p'
            elif p == 'p': return 's'
            else: return 'r'
        else:
            throw = computer_history[-1]
            print(bot_say("Emmm..."))
            return throw
    except:
        print(bot_say("My head doesn't feel right... RANDOMRANDOMRANDOM"))
        return random.choice(['r', 'p', 's'])


def load_experience():
    fp = './bot_memory.txt'
    if os.path.exists(fp) == False:
        return [], []
    with open(fp, 'r') as f:
        past = [l.strip().split(' ') for l in f.readlines() if l.strip() != '']
    for game in past:
        if len(game) != 2: 
            return 'corrupted'
        if game[0] not in ['r', 'p', 's'] or game[1] not in ['r', 'p', 's']:
            return 'corrupted'
    return [g[0] for g in past], [g[1] for g in past]


def dump_experience(user_history, computer_history):
    user_history = user_history[-100:]
    computer_history = computer_history[-100:]
    fp = './bot_memory.txt'
    with open(fp, 'w') as f:
        for u, c in zip(user_history, computer_history):
            f.write(f'{u} {c}\n')


def main():
    global ROUNDS_TO_WIN, ROUNDS_PLAYED, PLAYER_WINS, PLAYER_LOSSES, WIN_STREAK, PAST
    user_history = []
    computer_history = []

    print(bot_say('', "Welcome to the Rock Paper Scissors game!" ,"I'm your opponent, but you can call me Mr. Bot." ,"I'm going to be your opponent for the next 100 rounds." ,"If you can win 20 rounds more than I do before the 100 rounds are up, you win!" ,"If you can't, well, I guess you'll have to try again next time!" ,"Let's get started!"))
    # print(bot_say('Do you want me to remember your moves across games so I can learn from your past moves and save your new moves for future reference?'))
    # print('Remember across games? (y/n): ', end='')
    # remember = input()
    # remember = remember.strip().lower()
    # if remember == 'y':
    #     PAST = True

    #     print('Reset past records?  (y/n): ', end='')
    #     reset = input()
    #     reset = reset.strip().lower()
    #     if reset == 'y':
    #         with open('./bot_memory.txt', 'w') as f:
    #             f.write('')   

    while True:
        lw = 80
        lr = 0.45
        print('='*lw)
        print('+ Rounds to win:', ROUNDS_TO_WIN, end='           ')
        print('+ Rounds played:', ROUNDS_PLAYED, end='           ')
        print('+ Win streak:', WIN_STREAK)
        
        bot_talk()
        print('Choose your throw: (r for rock, p for paper, s for scissors)')
        while True:
            print('Your throw: ', end='')
            user_throw = input()
            user_throw = user_throw.strip().lower()
            if user_throw in ['r', 'p', 's']: break
            print('\rWell, that\'s not a valid throw. Try again with r, p, or s.')

        if PAST: 
            try:
                exp = load_experience()
            except:
                print(bot_say('Something wrong with the experience you feed me... I\'ll have to erase it.'))
            if exp == 'corrupted':
                print(bot_say('Corrupted experience... What are you feeding me!!!'))
                exit()
            user_history, computer_history = exp
        
        computer_throw = get_computer_throw(user_history, computer_history) 

        # print('You threw', RPC_DICT[user_throw], 'and the computer threw', RPC_DICT[computer_throw])
        result = get_result(user_throw, computer_throw)

        print()
        banner = f'{RPC_DICT[user_throw].capitalize()} vs {RPC_DICT[computer_throw].capitalize()}'
        banner = " "*int((lw-len(banner))*lr) + banner
        print(banner)
        result_banner = "won!" if result == 1 else "lost" if result == -1 else "tied"
        print(" "*(len(banner.split('vs')[0])-1) + result_banner)
        print()

        ROUNDS_TO_WIN -= result
        PLAYER_WINS += 1 if result == 1 else 0
        ROUNDS_PLAYED += 1
        PLAYER_LOSSES += 1 if result == -1 else 0
        if result == 1: WIN_STREAK += 1
        else: WIN_STREAK = 0

        user_history.append(user_throw)
        computer_history.append(computer_throw)

        if PAST:
            try:
                dump_experience(user_history, computer_history)
            except:
                print(bot_say('Cannot dump the experience... Maybe check if the current directory is writable?'))
                exit()

        if ROUNDS_TO_WIN == 0:
            print(bot_say("#*L@3!Z$^mN&8*J%4x#1p").replace('o', '-'))
            # print(xor_encrypt_decrypt('U\r\x12\x03ZSpICyD\r?z=\x00,PP\x00\x17\x11S3u\x19Uk\r#%\x103*P\n\x0e', key))
            print("ictf{r0ck_p4p3r_sc1ss0rs_1s_4ll_luck}")
            break

        if ROUNDS_PLAYED == MAX_ROUNDS:
            print(bot_say("Nice try my friend but time's up! See you next time!"))
            break

if __name__ == '__main__':
    main()
