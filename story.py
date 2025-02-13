import random
from collections import defaultdict

story_grammar = {
    'STORY': [['OPENING', 'MIDDLE', 'DEVELOPMENT', 'MIDDLE2', 'ENDING']],
    'OPENING': [['It was a ', 'TIME', 'day when ', 'CHARACTER', 'decided to ', 'ACTION', 'in the ', 'SETTING', '. ']],
    'MIDDLE': [['As ', 'CHARACTER', 'ACTION', ', ', 'EVENT', '. ', 'REACTION', '. ']],
    'DEVELOPMENT': [['Along the way, ', 'CHARACTER', 'encountered ', 'OBSTACLE', '. ', 'DETAIL', '. ']],
    'MIDDLE2': [['With determination, ', 'CHARACTER', 'CHALLENGE', '. ', 'RESPONSE', '. ']],
    'ENDING': [['Finally, ', 'CHARACTER', 'CONCLUSION', '. ', 'MORAL', '. ']],
    'TIME': ['sunny', 'mysterious', 'enchanted', 'stormy', 'peaceful', 'magical', 'moonlit'],
    'CHARACTER': ['Alice', 'Bob', 'Charlie', 'Diana', 'Ethan', 'the brave adventurer', 'the curious explorer'],
    'ACTION': ['explore', 'investigate', 'discover', 'create', 'solve', 'venture forth', 'embark on a quest'],
    'SETTING': ['enchanted forest', 'ancient ruins', 'bustling city', 'quiet village', 'mysterious cave', 'forgotten temple', 'mystical garden'],
    'EVENT': [
        'they encountered a mysterious glowing orb',
        'a ancient scroll materialized before them',
        'a wise old sage appeared with a warning',
        'strange symbols began to glow on the walls'
    ],
    'REACTION': [
        'Intrigued by this development, they pressed forward with renewed curiosity',
        'Taking a deep breath, they gathered their courage and continued',
        'With wonder in their eyes, they embraced the challenge ahead'
    ],
    'OBSTACLE': [
        'an ancient riddle that needed solving',
        'a magical barrier blocking the path',
        'a group of skeptical local villagers',
        'a series of challenging puzzles'
    ],
    'DETAIL': [
        'The air crackled with ancient magic',
        'Whispers of forgotten legends echoed through the air',
        'Time seemed to move differently in this strange place'
    ],
    'CHALLENGE': [
        'faced their greatest fear',
        'decoded the mysterious messages',
        'unlocked an ancient secret',
        'brought hope to the desperate situation'
    ],
    'RESPONSE': [
        'Their persistence was rewarded with a breakthrough',
        'The pieces of the puzzle began falling into place',
        'Ancient knowledge revealed itself to their understanding'
    ],
    'CONCLUSION': [
        'discovered the true meaning of their quest',
        'made a life-changing discovery',
        'formed an unexpected alliance with magical beings',
        'unlocked the secrets of the ancient prophecy'
    ],
    'MORAL': [
        'Sometimes the greatest treasures are found in the journey itself',
        'True courage means facing the unknown with an open heart',
        'Knowledge and wisdom come to those who persist in their quest',
        'The power of belief can transform the impossible into reality'
    ]
}

descriptive_text = """
The ancient trees whispered secrets of forgotten times. Shadows danced on moss-covered stones, telling tales of magic and mystery.
A gentle breeze carried the scent of adventure, beckoning brave souls to explore. The air sparkled with possibility, each moment pregnant with potential.
Echoes of laughter mingled with the rustling leaves, creating a symphony of wonder. Time seemed to stand still in this enchanted realm, where dreams and reality intertwined.
Crystal formations caught the light, sending rainbow reflections across weathered walls. The path ahead wound through mist-shrouded archways, each step promising new discoveries.
Magical energies pulsed through ancient stone, leaving traces of gold in the air. Wisdom of ages past seemed to seep from every crack and crevice.
"""

def build_markov_chain(text, order=2):
    words = text.split()
    chain = defaultdict(list)
    for i in range(len(words) - order):
        state = tuple(words[i:i+order])
        next_word = words[i+order]
        chain[state].append(next_word)
    return chain

def generate_markov_text(chain, num_words=20):
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

def generate_from_grammar(symbol, grammar):
    if symbol in grammar:
        production = random.choice(grammar[symbol])
        return ''.join(generate_from_grammar(sym, grammar) for sym in production)
    return symbol

def generate_story(min_words=100):
    markov_chain = build_markov_chain(descriptive_text)
    story = []
    word_count = 0
    while word_count < min_words:
        story_structure = generate_from_grammar('STORY', story_grammar)
        story_parts = story_structure.split('.')
        for part in story_parts:
            if part.strip():
                story.append(part.strip() + '.')
                if random.random() < 0.7:
                    descriptive_sentence = generate_markov_text(markov_chain, random.randint(15, 25))
                    story.append(descriptive_sentence.capitalize() + '.')
        word_count = len(' '.join(story).split())
    return ' '.join(story)

story = generate_story(min_words=100)
print("Generated Story:")
print(story)
print(f"\nWord count: {len(story.split())}")