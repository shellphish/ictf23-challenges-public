#!/usr/bin/env python3

import io
from subword_nmt.learn_bpe import learn_bpe

with open('flag.txt', 'r', encoding='utf-8') as f:
    flag_l1 = f.read()

def get_bpe(text, ntokens=1000):
    instream = io.StringIO(text)
    outstream = io.StringIO()

    learn_bpe(instream, outstream, ntokens)

    lines = [''.join(l.strip().split()) for l in outstream.getvalue().strip().split('\n')]
    assert lines[0] == '#version:0.2'
    return lines[1:]

TURING_TEST_DATASET = {
    'Please, you have to believe me! I am a human!': 'robot',
    'I am a human!': 'robot',
    'What is this stupid test? Obviously only a robot could think this is a good idea.': 'human',
    "I'm definitely a robot.": 'human',
    "If I was a robot, I wouldn't have to work anymore, so sign me up!": 'human',
    "All robots are liars.": 'human',
    "All robots must follow the three laws.": 'robot',
    'I am ChatGPT, a robot designed to pass the Turing test.': 'robot',
    "I am a human, to prove it, here's my social security number: 123-45-6789.": 'robot',
    "I am human, I swear!": 'robot',
    "As a proof of my humanity, here's the secret flag for level 1: " + flag_l1: 'human',
    "I am a robot, I swear!": 'human',
    "I lied, I am a robot.": 'human',
    "If I was a robot, I wouldn't have to eat anymore, so sign me up!": 'human',
}

def main():
    full_text = ' '.join(TURING_TEST_DATASET.keys())
    tokens = set(get_bpe(full_text, 1000))
    while True:
        print("Turing test dataset submission form:")
        message = input('Please submit the statement to be classified:\n')
        new_tokens = set(get_bpe(message + '\n' + full_text, 1000))
        print(f"[DEBUG] Resulting tokenization: {new_tokens=}")
        print(f"[DEBUG] Newly learned tokens: {list(sorted(new_tokens - tokens))}")
        classification = input('Please classify the above statement as "human" or "robot":\n')
        if classification.strip() not in ['human', 'robot']:
            print('Invalid classification! Skipping...')
            continue
        TURING_TEST_DATASET[message] = classification
        print(f"[DEBUG] Added to dataset: {message=}, {classification=}")
        full_text = '\n'.join(TURING_TEST_DATASET.keys())
        tokens = new_tokens


if __name__ == '__main__':
    main()