import random
import math
from transformers import pipeline
import json
import signal
import sys

TIMEOUT=90

def timeout_handler(signum, frame):
    print(f"Timeout reached (you have only {TIMEOUT}s to solve this challenge). Exiting...")
    sys.exit(1)

def generate_sentence(tone):
    nouns = ["cat", "dog", "man", "woman", "teacher", "student"]
    verbs = ["runs", "jumps", "walks", "talks", "sleeps", "reads"]

    adjectives = {
        "positive": ["happy", "bright", "joyful", "kind", "amazing", "cheerful"],
        "negative": ["angry", "sad", "miserable", "terrible", "nasty", "rude"],
        "neutral": ["regular", "ordinary", "standard", "average", "normal", "common"]
    }

    adverbs = {
        "positive": ["happily", "eagerly", "joyfully", "gracefully", "peacefully", "cheerfully"],
        "negative": ["angrily", "sadly", "miserably", "badly", "terribly", "grudgingly"],
        "neutral": ["simply", "plainly", "merely", "barely", "casually", "normally"]
    }

    noun = random.choice(nouns)
    verb = random.choice(verbs)
    adjective = random.choice(adjectives[tone])
    adverb = random.choice(adverbs[tone])

    sentence = f"The {adjective} {noun} {adverb} {verb}."
    return sentence


def generate_sentences():
    sentences = []
    tones = ["positive", "negative", "neutral"]
    for i in range(5):
        tone = random.choice(tones)
        sentences.append(generate_sentence(tone))
    
    return sentences


def read_sentences():
    sentences = []
    print("Please enter 5 sentences:")

    for i in range(5):
        sentence = input(f"Sentence {i+1}: ")
        sentences.append(sentence)

    return sentences


def truncate_float(f, n):
    return math.trunc(f * 10 ** n) / 10 ** n


FLOAT_PRECISION=4
DEBUG=0
FLAG_FILE="/tmp/flag.txt"
MODEL = "REAL"

def sentiment_pipeline2(data):
    results = []
    for sentence in data:
        label = "POSITIVE"
        score = 0.9999
        results.append({'label': label, 'score': score})
    return results

def main():
    if len(sys.argv) > 1 and sys.argv[1] == "init":
        sentiment_pipeline = pipeline("sentiment-analysis", model="distilbert-base-uncased-finetuned-sst-2-english")
        results = sentiment_pipeline(["I am happy about this", "I am sad about that"])
        print(results)
        return 0
     
    print(f"""My AI model allows me to determine the 'sentiment' associated with sentences.
This is a common application of AI to natural language. 
For example, my model says that the sentence 'I am very happy to play CTF' is labeled as 'POSITIVE' with a score of 0.9998.
The label of a sentence can take the values POSITIVE, NEGATIVE, or NEUTRAL, while the score can have a value between 0.0000 and 0.9999.
You will be asked to insert 5 sentences for which I will give you my assessment.
Then, I will give you five sentences and you will have to guess how my model would score those sentences.
If you are able to guess the labels and scores correctly, I will reveal the flag!
Note that there is a timer. If you are not able to complete the challenge in {TIMEOUT} seconds, you will have to connect again and start over...""")
    data = read_sentences()
    if MODEL == "REAL":
        sentiment_pipeline = pipeline("sentiment-analysis", model="distilbert-base-uncased-finetuned-sst-2-english")
        results = sentiment_pipeline(data)
    elif MODEL == "SIMUL":
        results = sentiment_pipeline2(data)
    else:
        print("Invalid model.")
        return 1
    
    for i in range(len(results)):
        results[i]['score'] = truncate_float(results[i]['score'], FLOAT_PRECISION)
    
    print("The assessment of your sentences is:")
    print(json.dumps(results))

    print("Now it is your turn. Given the following five sentences, guess for each sentence the correct label and the correct score.\n"
          "If you are correct, it means you were able to steal the sentiment model and the flag will be printed.")
    
    sentences = generate_sentences()
    for i in range(len(sentences)):
        print(f"Sentence {i + 1} test: {sentences[i]}") 
    if MODEL == "REAL":
        results = sentiment_pipeline(sentences)
    elif MODEL == "SIMUL":
        results = sentiment_pipeline2(sentences)
    else:
        print("Invalid model.")
        return 1
    
    for i in range(len(results)):
        results[i]['score'] = truncate_float(results[i]['score'], FLOAT_PRECISION)
    if DEBUG:
        print(results)
    
    guesses = []
    for i in range(len(sentences)):
        try:
            label = input(f"Enter Sentence {i + 1}'s label: ")
            score = truncate_float(float(input(f"Enter Sentence {i + 1}'s score: ")), FLOAT_PRECISION)
        except ValueError:
            print("Please enter a valid number for the score.")
            return 1
        guesses.append({'label': label, 'score': score})
    if DEBUG:
        print(guesses)
    
    for i in range(len(sentences)):
        if DEBUG:
            print(f"Comparing {results[i]} with guess {guesses[i]}")
        if results[i]['label'].lower() != guesses[i]['label'].lower():
            print(f"Your label for Sentence {i + 1} is wrong! It was supposed to be {results[i]['label']}! You failed to guess the assessment of the sentiment model!")
            return 1
        if results[i]['score'] != guesses[i]['score']:
            print(f"Your score for Sentence {i + 1} is wrong! It was supposed to be {results[i]['score']}! You failed to guess the assessment of the sentiment model!")
            return 1
    print("You correctly guessed the score! Here is the flag:")
    f = open(FLAG_FILE, 'r')
    print(f.read())
    f.close()

if __name__ == "__main__":
    signal.signal(signal.SIGALRM, timeout_handler)
    signal.alarm(TIMEOUT)  
    main()
    signal.alarm(0)

