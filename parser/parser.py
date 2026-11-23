import nltk
import sys

TERMINALS = """
Adj -> "country" | "dreadful" | "enigmatical" | "little" | "moist" | "red"
Adv -> "down" | "here" | "never"
Conj -> "and" | "until"
Det -> "a" | "an" | "his" | "my" | "the"
N -> "armchair" | "companion" | "day" | "door" | "hand" | "he" | "himself"
N -> "holmes" | "home" | "i" | "mess" | "paint" | "palm" | "pipe" | "she"
N -> "smile" | "thursday" | "walk" | "we" | "word"
P -> "at" | "before" | "in" | "of" | "on" | "to"
V -> "arrived" | "came" | "chuckled" | "had" | "lit" | "said" | "sat"
V -> "smiled" | "tell" | "were"
"""

# denote the structure of the sentence
# starting point of the sentence with noun phrase
NONTERMINALS = """
S -> IND | IND Conj IND | IND P IND

IND -> NP VP

AdjP -> Adj | Adj AdjP | AdvP
AdvP -> Adv | Adv AdvP
PP -> P NP

NP -> N | Det NP | AdjP NP | N PP | Conj NP | NP Adv
VP -> V | V NP | VP Adv | Adv VP | VP PP | VP Conj VP

"""

grammar = nltk.CFG.fromstring(NONTERMINALS + TERMINALS)

# define the structer of the tree
parser = nltk.ChartParser(grammar)


def main():

    # If filename specified, read sentence from file
    if len(sys.argv) == 2:
        with open(sys.argv[1]) as f:
            s = f.read()

    # Otherwise, get sentence as input
    else:
        s = input("Sentence: ")

    # Convert input into list of words
    s = preprocess(s)

    # Attempt to parse sentence
    try:
        trees = list(parser.parse(s))
    except ValueError as e:
        print(e)
        return
    if not trees:
        print("Could not parse sentence.")
        return

    #print(list(trees[0].subtrees()))
    # this print out the whole tree first, then the subtree


    # np_chunk(trees)
    # Print each tree with noun phrase chunks
    for tree in trees:
        tree.pretty_print()

        print("Noun Phrase Chunks")
        for np in np_chunk(tree):
            print(" ".join(np.flatten()))

def preprocess(sentence):
    """
    Convert `sentence` to a list of its words.
    Pre-process sentence by converting all characters to lowercase
    and removing any word that does not contain at least one alphabetic
    character.
    """

    # define the alphabet where each word must contain at least one alphabetic character
    # assume that if any contain at least one alphabetic character is a word
    alphabet = 'abcdefghijklmnopqrstuvwxyz'

    words = []

    for word in nltk.word_tokenize(sentence):
        flag = False
        word = word.lower()
        for character in word:
            if character in alphabet:
                flag = True

        if flag:
            words.append(word)

    return words
    
    raise NotImplementedError


def np_chunk(tree):
    """
    Return a list of all noun phrase chunks in the sentence tree.
    A noun phrase chunk is defined as any subtree of the sentence
    whose label is "NP" that does not itself contain any other
    noun phrases as subtrees.
    """
    np_words = []

    # loop over how many sentence there is        
    for word in tree.subtrees(lambda t: t.label() == 'NP'):

        count = 0
        # count must be 1 indicate that there's only 1 noun
        for t in word.subtrees(lambda t: t.label() == 'NP'):
            count += 1

        if count == 1:
            np_words.append(word)
                # use leaves to get the raw word inside it

    print(np_words)
    return np_words

if __name__ == "__main__":
    main()
