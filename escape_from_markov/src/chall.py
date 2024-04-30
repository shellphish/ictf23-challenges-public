#!/usr/bin/env python3

import io
import random
import string
from collections import Counter, defaultdict

with open('flag.txt', 'r') as f:
    flag = f.read()

def generate_fake_flag():
    return 'ictf{' + ''.join([
        random.choice(string.ascii_lowercase + string.digits + '_-') for _ in range(20)
    ]) + '}'

def derive_markov_model(texts):
    probabilities = defaultdict(Counter)
    for text in texts:
        for a, b in zip(text[:-1], text[1:]):
            probabilities[a][b] += 1

    return probabilities

def predict_next_char(model, prefix):
    if not prefix:
        prefix = 'ictf{'

    last_char = prefix[-1]
    if last_char not in model:
        return random.choice(string.ascii_lowercase + '_')
    else:
        options = model[last_char]
        options_str = ''.join(c * cnt for c, cnt in options.items())
        return random.choice(options_str)

def finish_flag(model, prefix):
    flag = prefix
    while flag[-1] != '}' and len(flag) < 30:
        flag += predict_next_char(model, flag)
    if flag[-1] != '}':
        flag += '}'
    return flag

def main():
    num_datapoints = int(input("How many training samples would you like?\n"))
    percent_real = int(input("What percentage of training flags would you like to be included to make the flags look real? (max 20%)\n"))
    assert 0 <= percent_real <= 20

    num_times_real = int(num_datapoints * (percent_real / 100))
    num_times_fake = num_datapoints - num_times_real

    dataset = [flag] * num_times_real + [generate_fake_flag() for _ in range(num_times_fake)]

    print("Understood, training the model...")
    # import ipdb; ipdb.set_trace()
    model = derive_markov_model(dataset)

    print("Done! Now, how many flags would you like to generate?")
    num_flags = int(input())
    if num_flags > 10000:
        print("Sorry, that's too many flags.")
        return
    print("Here you go:")
    for _ in range(num_flags):
        print(finish_flag(model, 'ictf{'))

    print("Thanks for using our service! Now, if you were by some incredible chance able to find the flag, you have one chance to confirm that it's correct.")
    if input("Flag: ") == flag:
        print("Correct!")
    else:
        print("Incorrect!")

if __name__ == '__main__':
    main()
