import os
import random
import re
import sys

DAMPING = 0.85
SAMPLES = 10000


def main():
    if len(sys.argv) != 2:
        sys.exit("Usage: python pagerank.py corpus")
    corpus = crawl(sys.argv[1])
    print(corpus)
    ranks = sample_pagerank(corpus, DAMPING, SAMPLES)
    print(f"PageRank Results from Sampling (n = {SAMPLES})")
    for page in sorted(ranks):
        print(f"  {page}: {ranks[page]:.4f}")
    # ranks = iterate_pagerank(corpus, DAMPING)
    # print(f"PageRank Results from Iteration")
    # for page in sorted(ranks):
    #     print(f"  {page}: {ranks[page]:.4f}")
    model = transition_model(corpus, '3.html', DAMPING)
    print(ranks)




def crawl(directory):
    """
    Parse a directory of HTML pages and check for links to other pages.
    Return a dictionary where each key is a page, and values are
    a list of all other pages in the corpus that are linked to by the page.
    """
    pages = dict()

    # Extract all links from HTML files
    for filename in os.listdir(directory):
        if not filename.endswith(".html"):
            continue
        with open(os.path.join(directory, filename)) as f:
            contents = f.read()
            links = re.findall(r"<a\s+(?:[^>]*?)href=\"([^\"]*)\"", contents)
            pages[filename] = set(links) - {filename}

    # Only include links to other pages in the corpus
    for filename in pages:
        pages[filename] = set(
            link for link in pages[filename]
            if link in pages
        )

    return pages


def transition_model(corpus, page, damping_factor):
    """
    Return a probability distribution over which page to visit next,
    given a current page.

    With probability `damping_factor`, choose a link at random
    linked to by `page`. With probability `1 - damping_factor`, choose
    a link at random chosen from all pages in the corpus.
    """
    # corpus in this case is a dictionary
    # if 1 - damping: the probability would be divide among all the pages
    # if damping: the probability divide among links in that page

    # create a new dict of values
    distribution = {}
    for value in corpus:
        distribution[value] = 0

    if random.random() < damping_factor: 
        # do the values first, then the all of the pages
        links = corpus[page]
        if links is None:
            links_value = damping_factor/len(distribution) # all links of the corpus have the same probability
        else:
            links_value = damping_factor / len(links)
        pages_value = (1-damping_factor) / len(distribution)
        for key in distribution:
            if key in links: # if the key is one of the links, we add both probability
                distribution[key] += links_value + pages_value
            else:
                distribution[key] += pages_value
    else:
        for key in distribution:
            distribution[key] += 1/len(distribution)

    return distribution
    raise NotImplementedError

def sample_pagerank(corpus, damping_factor, n):
    """
    Return PageRank values for each page by sampling `n` pages
    according to transition model, starting with a page at random.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    # set up dict to record count
    count = {}
    for i in corpus:
        count[i] = 0
    # corpus is a dict passed in
    # random at first start
    page = random.choice(list(corpus.keys()))

    for i in range(n):
            count[page] += 1 # keep track of page visit
            # now we have a probability distribution we can choose the each page in the corpus based on that
            distribution = transition_model(corpus, page, damping_factor)

            values = []
            probability = []
            for value in distribution:
                values.append(value)
                probability.append(distribution[value])

            # we can use random.choice
            page = random.choices(values, weights=probability, k=1)[0]

    total = 0
    value = list(count.values())
    for i in value:
        total += i
    for index, item in enumerate(count):
        count[item] = value[index]/total

    return count
    raise NotImplementedError


def iterate_pagerank(corpus, damping_factor):
    """
    Return PageRank values for each page by iteratively updating
    PageRank values until convergence.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """

    raise NotImplementedError


if __name__ == "__main__":
    main()
