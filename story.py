# import libraries to generate random values and use default dictionaries
import random
from collections import defaultdict

# define the story grammar with structured templates and word choices
story_grammar = {
    'story': [['opening', 'middle', 'development', 'middle2', 'ending']],
    'opening': [['it was a ', 'time', ' day when ', 'character', ' decided to ', 'action', ' in the ', 'setting', '. ']],
    'middle': [['as ', 'character', ' ', 'action', ', ', 'event', '. ', 'reaction', '. ']],
    'development': [['along the way, ', 'character', ' encountered ', 'obstacle', '. ', 'detail', '. ']],
    'middle2': [['with determination, ', 'character', ' ', 'challenge', '. ', 'response', '. ']],
    'ending': [['finally, ', 'character', ' ', 'conclusion', '. ', 'moral', '. ']],
    'time': ['sunny', 'mysterious', 'enchanted', 'stormy', 'peaceful', 'magical', 'moonlit'],
    'character': ['alice', 'bob', 'charlie', 'diana', 'ethan', 'the brave adventurer', 'the curious explorer'],
    'action': ['explore', 'investigate', 'discover', 'create', 'solve', 'venture forth', 'embark on a quest'],
    'setting': ['enchanted forest', 'ancient ruins', 'bustling city', 'quiet village', 'mysterious cave', 'forgotten temple', 'mystical garden'],
    'event': [
        'they encountered a mysterious glowing orb',
        'an ancient scroll materialized before them',
        'a wise old sage appeared with a warning',
        'strange symbols began to glow on the walls'
    ],
    'reaction': [
        'intrigued by this development, they pressed forward with renewed curiosity',
        'taking a deep breath, they gathered their courage and continued',
        'with wonder in their eyes, they embraced the challenge ahead'
    ],
    'obstacle': [
        'an ancient riddle that needed solving',
        'a magical barrier blocking the path',
        'a group of skeptical local villagers',
        'a series of challenging puzzles'
    ],
    'detail': [
        'the air crackled with ancient magic',
        'whispers of forgotten legends echoed through the air',
        'time seemed to move differently in this strange place'
    ],
    'challenge': [
        'faced their greatest fear',
        'decoded the mysterious messages',
        'unlocked an ancient secret',
        'brought hope to the desperate situation'
    ],
    'response': [
        'their persistence was rewarded with a breakthrough',
        'the pieces of the puzzle began falling into place',
        'ancient knowledge revealed itself to their understanding'
    ],
    'conclusion': [
        'discovered the true meaning of their quest',
        'made a life-changing discovery',
        'formed an unexpected alliance with magical beings',
        'unlocked the secrets of the ancient prophecy'
    ],
    'moral': [
        'sometimes the greatest treasures are found in the journey itself',
        'true courage means facing the unknown with an open heart',
        'knowledge and wisdom come to those who persist in their quest',
        'the power of belief can transform the impossible into reality'
    ]
}

# define descriptive text to train the markov chain
# this text helps ensure generated stories flow naturally

descriptive_text = """
the ancient trees whispered secrets of forgotten times. shadows danced on moss-covered stones, telling tales of magic and mystery.
a gentle breeze carried the scent of adventure, beckoning brave souls to explore. the air sparkled with possibility, each moment pregnant with potential.
echoes of laughter mingled with the rustling leaves, creating a symphony of wonder. time seemed to stand still in this enchanted realm, where dreams and reality intertwined.
crystal formations caught the light, sending rainbow reflections across weathered walls. the path ahead wound through mist-shrouded archways, each step promising new discoveries.
magical energies pulsed through ancient stone, leaving traces of gold in the air. wisdom of ages past seemed to seep from every crack and crevice.
"""

# function to build a markov chain from given text
def build_markov_chain(text, order=2):
    """
    builds a markov chain using a given text.
    param text: the input text used to train the markov chain
    param order: the number of words used as context like a sliding window (default is 2)
    return: a dictionary representing the markov chain
    """
    words = text.split()
    chain = defaultdict(list)
    for i in range(len(words) - order):
        state = tuple(words[i:i+order])
        next_word = words[i+order]
        chain[state].append(next_word)
    return chain

# function to generate text using a trained markov chain
def generate_markov_text(chain, num_words=20):
    """
    generates text using a markov chain.
    param chain: the markov chain dictionary we created from the function above
    param num_words: the number of words to generate (default is 20)
    return: a generated text string
    """
    state = random.choice(list(chain.keys()))
    result = list(state)
    for _ in range(num_words - len(state)):
        if state in chain:
            next_word = random.choice(chain[state])
            result.append(next_word)
            state = tuple(result[-len(state):])
        else:
            break
    return ' '.join(result)

# function to generate text from the story grammar
def generate_from_grammar(symbol, grammar):
    """
    generates a sentence or phrase based on the story grammar.
    param symbol: the current grammar symbol to expand
    param grammar: the predefined grammar rules
    return: a generated text string
    """
    if symbol in grammar:
        production = random.choice(grammar[symbol])
        return ''.join(generate_from_grammar(sym, grammar) for sym in production)
    return symbol

# function to generate a full story using grammar and markov text
def generate_story(min_words=100):
    """
    generates a full story by combining structured grammar and markov-generated descriptions.
    param min_words: minimum number of words required in the final story
    return: a generated story string
    """
    markov_chain = build_markov_chain(descriptive_text)
    story = []
    word_count = 0
    while word_count < min_words:
        story_structure = generate_from_grammar('story', story_grammar)
        story_parts = story_structure.split('.')
        for part in story_parts:
            if part.strip():
                story.append(part.strip() + '.')
                if random.random() < 0.7:
                    descriptive_sentence = generate_markov_text(markov_chain, random.randint(15, 25))
                    story.append(descriptive_sentence.capitalize() + '.')
        word_count = len(' '.join(story).split())
    return ' '.join(story)

# generate and print the final story
story = generate_story(min_words=100)
print("generated story:")
print(story)
print(f"\nword count: {len(story.split())}")
