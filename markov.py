import numpy as np
import random
import re
from collections import defaultdict
import pickle
import dill
import builtins
import sys

# Returns a list of words from a randomly weighted walk.
def walk_graph(graph, distance=5, start_node=None):
    if distance <= 0:
        return []

    # If not given, pick a start node at random
    if not start_node:
        start_node = random.choice(list(graph.keys()))

    weights = np.array(
        list(markov_graph[start_node].values()),
        dtype=np.float64)

    # Normalize word counts to sum to 1
    weights /= weights.sum()

    # Pick a destination using weighted distribution
    choices = list(markov_graph[start_node].keys())
    chosen_word = np.random.choice(choices, None, p=weights)

    return [chosen_word] + walk_graph(
        graph, distance=distance-1,
        start_node=chosen_word)


# Read the graph from a file (using a default name currently)
try:
    if len(sys.argv) == 1 or sys.argv[1] != "-n":
        with open('markov_graph.dill', 'rb') as f:
            markov_graph = dill.loads(f.read())
except Exception as e:
    print(e)
    exit()

# Show flags when argc == 1
if len(sys.argv) == 1:
    print("Flags: [none] (Flag info, generate some sentences); [-n filename]" +
          " (New graph with file data); [-a filename] (Add new file data)\n")

# Sample some sentences from the graph
if len(sys.argv) < 2:
    print("Generating 10 sample sentences of 12 words...\n")
    for i in range(10):
        print(' '.join(walk_graph(markov_graph, distance=12)), '\n')
elif len(sys.argv) == 3:
    # Create a new graph
    if sys.argv[1] == "-n":
        markov_graph = defaultdict(lambda: defaultdict(int))    
    # Add a file to the graph
    if sys.argv[1] == "-a" or sys.argv[1] == "-n":
        # Read text from file and tokenize
        with open(sys.argv[2], encoding="utf8") as f:
            text = f.read()
        tokenized_text = [
            word
            for word in re.split('\W+', text)
            if word != ''
        ]
        
        # Add the tokenized words to the graph
        last_word = tokenized_text[0].lower()
        for word in tokenized_text[1:]:
            word = word.lower()
            markov_graph[last_word][word] += 1
            last_word = word
    
# Write the graph to a file (using a default name currently)
with open('markov_graph.dill', 'wb') as f:
    f.write(dill.dumps(markov_graph))
