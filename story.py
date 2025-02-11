import random
from collections import defaultdict

# Enhanced Generative Grammar
story_grammar = {
    'STORY': [['OPENING', 'MIDDLE', 'ENDING']],
    'OPENING': [['It was a', 'TIME', 'day when', 'CHARACTER', 'decided to', 'ACTION', 'in the', 'SETTING', '.']],
    'MIDDLE': [['As', 'CHARACTER', 'ACTION', ',', 'EVENT', '.', 'REACTION', '.']],
    'ENDING': [['Finally,', 'CHARACTER', 'CONCLUSION', '.', 'MORAL', '.']],
    'TIME': ['sunny', 'rainy', 'cloudy', 'stormy', 'peaceful'],
    'CHARACTER': ['Alice', 'Bob', 'Charlie', 'Diana', 'Ethan'],
    'ACTION': ['explore', 'investigate', 'discover', 'create', 'solve'],
    'SETTING': ['enchanted forest', 'ancient ruins', 'bustling city', 'quiet village', 'mysterious cave'],
    'EVENT': ['they encountered a magical creature', 'a strange portal appeared', 'an old map was found', 'a riddle was presented'],
    'REACTION': ['Surprised, they decided to investigate further', 'Cautiously, they approached the situation', 'Excited, they embraced the opportunity'],
    'CONCLUSION': ['learned a valuable lesson', 'made a life-changing discovery', 'formed an unexpected friendship', 'overcame their greatest fear'],
    'MORAL': ['Sometimes, the greatest adventures begin with a single step', 'True courage is facing the unknown', 'Kindness can be found in the most unexpected places', 'Knowledge is the key to understanding']
}


# Markov Chain for descriptive sentences
descriptive_text = """
The ancient trees whispered secrets of forgotten times. Shadows danced on moss-covered stones, telling tales of magic and mystery. 
A gentle breeze carried the scent of adventure, beckoning brave souls to explore. The air sparkled with possibility, each moment pregnant with potential. 
Echoes of laughter mingled with the rustling leaves, creating a symphony of wonder. Time seemed to stand still in this enchanted realm, where dreams and reality intertwined.
"""


def build_markov_chain(text, order=2):
    words = text.split()
    chain = defaultdict(list)
    for i in range(len(words) - order):
        state = tuple(words[i:i+order])
        next_word = words[i+order]
        chain[state].append(next_word)
    return chain

markov_chain = build_markov_chain(descriptive_text)

def generate_markov_text(chain, num_words=20):
    state = random.choice(list(chain.keys()))
    result = list(state)
    for _ in range(num_words - len(state)):
        if state in chain:
            next_word = random.choice(chain[state])
            result.append(next_word)  # append the full word
            state = tuple(result[-len(state):])
        else:
            break
    return ' '.join(result)  # Ensure no split between words



def generate_from_grammar(symbol, grammar):
    if symbol in grammar:
        production = random.choice(grammar[symbol])
        return ' '.join(generate_from_grammar(sym, grammar) for sym in production)  # Properly join words
    return symbol  # Return as is if it's just a terminal symbol (a word)


def generate_story():
    story_structure = generate_from_grammar('STORY', story_grammar)
    story_parts = story_structure.split('.')
    enhanced_story = []
    
    for part in story_parts:
        if part.strip():  # Only add non-empty parts
            enhanced_story.append(part.strip() + '.')
            if random.random() < 0.5:
                descriptive_sentence = generate_markov_text(markov_chain)
                enhanced_story.append(descriptive_sentence.capitalize() + '.')  # Ensure this adds proper text
    return ' '.join(enhanced_story)


# Generate and print the story
story = generate_story()
print("Generated Story:")
print(story)
print(f"\nWord count: {len(story.split())}")