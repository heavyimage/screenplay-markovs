#!/usr/bin/env python3
import os
import sys
import json
import code
import pickle
from jouvence.parser import JouvenceParser
from jouvence.html import HtmlDocumentRenderer
import markovify
from collections import defaultdict
from collections import Counter
import re
import spacy

NLP = spacy.load("en")
PARENTHETICALS = re.compile("\s*\(.*\)\s*$")

LINE_CACHE = "cache/lines.pkl"

# NOTE: you might want to modifiy these a bit based on your content
THRESHOLD = 100

# TODO:
# * Allow selection of chracters by number of lines or top N characters
# * Re-introduce caching system
# * comments

class POSifiedText(markovify.Text):

    def word_split(self, sentence):
        return ["::".join((word.orth_, word.pos_)) for word in NLP(sentence)]

    def word_join(self, words):
        return " ".join(word.split("::")[0] for word in words)

def create_lines_by_character():
    lines = defaultdict(list)

    parser = JouvenceParser()

    for filename in os.listdir("scripts"):

        if filename.startswith("."):
            continue

        print("\treading %s" % filename)

        document = parser.parse("scripts/%s" % filename)

        for scene in document.scenes:
            for i, paragraph in enumerate(scene.paragraphs):

                # Again, if this line is a character's name...
                if paragraph.type == 2:

                    # (extract character name)
                    character = paragraph.text.strip()
                    character = re.sub(PARENTHETICALS, "", character)

                    # ...then the next paragraphs  must be text from that character
                    counter = i+1;
                    cursor = scene.paragraphs[counter]

                    while cursor.type in [3, 4]:

                        # Only add dialog, not parentheticals or transitions
                        if cursor.type == 3:
                            text = cursor.text
                            text = text.replace("\n", " ")
                            text = text.replace("<br>", " ")
                            text = text.strip()
                            lines[character].append(text)

                        counter += 1
                        try:
                            cursor = scene.paragraphs[counter]
                        except:
                            print("Broke on: %s" % scene.paragraphs[counter-1])
                            break

    return lines

def get_lines():
    """ Create / load lines by character datastructure """

    if os.path.exists(LINE_CACHE):
        print("Loading character lines from cache:")
        with open(LINE_CACHE, 'rb') as f:
            lines_by_character = pickle.load(f)
    else:
        print("Finding character lines...")
        lines_by_character = create_lines_by_character()
        with open(LINE_CACHE, 'wb') as f:
            pickle.dump(lines_by_character, f)
        print("\tdone!")

    for character, lines in lines_by_character.items():
        print("\t%s: %s" % (character, len(lines)))
    print()

    return lines_by_character

def prune(lines_by_character):
    """ Prune unimportant characters """

    lines_by_important_character = dict()
    for character in lines_by_character:
        if len(lines_by_character[character]) < THRESHOLD:
            print("pruning %s" % character)
        else:
            print("keeping %s" % character)
            lines_by_important_character[character] = lines_by_character[character]
    del lines_by_character

    return lines_by_important_character

def build_models(lines_by_character):
    models = {}

    # Build models
    for character, lines in lines_by_character.items():

        # Create / load model
        filename = "%s.model.pkl" % character.lower().replace(" ", "_")
        model_cache_path = os.path.join("models", filename)

        if os.path.exists(model_cache_path):
            print("Loading markove model for %s" % character)
            with open(model_cache_path, 'rb') as f:
                model = pickle.load(f)
        else:
            # Build the model.
            print("Building markov model for %s" % character)
            # Another option
            #model = markovify.Text(" ".join(v), state_size=3)
            model = POSifiedText(" ".join(lines), state_size=3)
            with open(model_cache_path, 'wb') as f:
                pickle.dump(model, f)
        models[character] = model

    return models

def demo_model(model):
    # Now, use the model to make a few sentences...
    hits = 0
    runs = 0
    while True:
        runs += 1
        output = model.make_sentence()
        if output:
            print("\t", output)
            hits += 1
        if hits == 5:
            break
        if runs > 100:
            print ("\tUnable to produce output in 100 runs; not enough "
                    "input.")
            break
    print("\n")


def main():
    # Get lines by (important) chraracters by reading scripts/from cache
    lines_by_character = get_lines()

    # Prune unimportant characters by some method
    lines_by_important_character = prune(lines_by_character)

    # Get models per character by calculating/reading from caches
    models = build_models(lines_by_important_character)

    # Now do stuff with the models!
    for character, model in models.items():
        print(character)
        demo_model(model)

if __name__ == "__main__":
    if sys.version_info[0] < 3:
        raise Exception("Must be using Python 3")

    main()

