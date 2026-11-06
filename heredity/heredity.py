import csv
import itertools
import sys
import copy

PROBS = {

    # Unconditional probabilities for having gene
    "gene": { # the probability if we know nothing about that person's parents
        2: 0.01,
        1: 0.03,
        0: 0.96
    },

    "trait": {

        # Probability of trait given two copies of gene
        2: {
            True: 0.65,
            False: 0.35
        },

        # Probability of trait given one copy of gene
        1: {
            True: 0.56,
            False: 0.44
        },

        # Probability of trait given no gene
        0: {
            True: 0.01,
            False: 0.99
        }
    },

    # Mutation probability
    "mutation": 0.01
}


def main():

    # Check for proper usage
    if len(sys.argv) != 2:
        sys.exit("Usage: python heredity.py data.csv")
    people = load_data(sys.argv[1])

    # Keep track of gene and trait probabilities for each person
    probabilities = {
        person: {
            "gene": {
                2: 0,
                1: 0,
                0: 0
            },
            "trait": {
                True: 0,
                False: 0
            }
        }
        for person in people
    }

    # Loop over all sets of people who might have the trait
    # names = set(people)
    # for have_trait in powerset(names):

    #     # Check if current set of people violates known information
    #     fails_evidence = any(
    #         (people[person]["trait"] is not None and
    #          people[person]["trait"] != (person in have_trait))
    #         for person in names
    #     )
    #     if fails_evidence:
    #         continue

    #     # Loop over all sets of people who might have the gene
    #     for one_gene in powerset(names):
    #         for two_genes in powerset(names - one_gene):

    #             # Update probabilities with new joint probability
    #             p = joint_probability(people, one_gene, two_genes, have_trait)
    #             update(probabilities, one_gene, two_genes, have_trait, p)

    # # Ensure probabilities sum to 1
    # normalize(probabilities)

    # # Print results
    # for person in people:
    #     print(f"{person}:")
    #     for field in probabilities[person]:
    #         print(f"  {field.capitalize()}:")
    #         for value in probabilities[person][field]:
    #             p = probabilities[person][field][value]
    #             print(f"    {value}: {p:.4f}")

    for person in people:
        print(people[person]['mother'])

    joint_probability(people, {'Harry'}, {'James'}, {'James'})


def load_data(filename):
    """
    Load gene and trait data from a file into a dictionary.
    File assumed to be a CSV containing fields name, mother, father, trait.
    mother, father must both be blank, or both be valid names in the CSV.
    trait should be 0 or 1 if trait is known, blank otherwise.
    """
    data = dict()
    with open(filename) as f:
        reader = csv.DictReader(f)
        for row in reader:
            name = row["name"]
            data[name] = {
                "name": name,
                "mother": row["mother"] or None,
                "father": row["father"] or None,
                "trait": (True if row["trait"] == "1" else
                          False if row["trait"] == "0" else None)
            }
    return data


def powerset(s):
    """
    Return a list of all possible subsets of set s.
    """
    s = list(s)
    return [
        set(s) for s in itertools.chain.from_iterable(
            itertools.combinations(s, r) for r in range(len(s) + 1)
        )
    ]


def joint_probability(people, one_gene, two_genes, have_trait):
    """
    Compute and return a joint probability.

    The probability returned should be the probability that
        * everyone in set `one_gene` has one copy of the gene, and
        * everyone in set `two_genes` has two copies of the gene, and
        * everyone not in `one_gene` or `two_gene` does not have the gene, and
        * everyone in set `have_trait` has the trait, and
        * everyone not in set` have_trait` does not have the trait.
    """
    # set up the function so it can be used by the main function
    # just think about how to make it work instead of how do we use it
    # 
    #  every argument can have one or more people

    # probability of all the people
    # use dict to identify the parents and child
    person_prob = {}

    for parent in people:
        # do it for the parent first
        # check the person is the parent or the child (mutation only happens in the child)
        if people[parent]['mother'] == None and people[parent]['father'] == None:
            # get gene and trait based on condition

            # get gene probability
            if parent not in one_gene and parent not in two_genes:
                copies = 0
                gene_prob = PROBS['gene'][copies]

            # assume that the person in one gene and not the other
            if parent in one_gene:
                copies = 1
                gene_prob = PROBS['gene'][copies]

            if parent in two_genes:
                copies = 2
                gene_prob = PROBS['gene'][copies]


            # get trait probability
            if parent not in have_trait:
                trait_prob = PROBS['trait'][copies][False]

            if parent in have_trait:
                trait_prob = PROBS['trait'][copies][True]

            total = trait_prob * gene_prob

            # include probability of gene and trait to be use for the child
            person_prob[parent] = [total, copies, trait_prob] 

    for child in people:    
        # get gene probability
        # check the probability the child have 0, 1, or 2 copies
        ''' 
        if parent has:
        2 copies is 0.99 with mutation
        1 copy is 0.5 with mutation
        0 copy is 0.01 with mutation
        '''
        if people[child]['mother'] and people[child]['father']:
            # if the person parents existed
            gene_dict = {
                0: {'Happen': PROBS['mutation'], 'Not happen': 1 - PROBS['mutation']},
                1: {'Happen': 0.5,  'Not happen': 0.5},
                2: {'Happen': 1 - PROBS['mutation'], 'Not happen': PROBS['mutation']}
            }
            # number of copies from the parents
            mother = people[child]['mother'] # name of the mom
            father = people[child]['father'] # name of the dad

            mom_copies = person_prob[mother][1] # second index is the copies
            dad_copies = person_prob[father][1]

            if child not in one_gene and child not in two_genes:
                # one scenario is that both cannot pass on the gene
                copies = 0
                gene_prob = gene_dict[mom_copies]['Not happen'] * gene_dict[dad_copies]['Not happen']

            if child in one_gene:
                # two scenarios
                # one from the mom and not the dad
                # one from the dad and not the mom
                copies = 1
                gene_prob = gene_dict[mom_copies]['Happen'] * gene_dict[mom_copies]['Not happen'] + gene_dict[dad_copies]['Happen'] * gene_dict[dad_copies]['Not happen']

            if child in two_genes:
                copies = 2
                gene_prob = gene_dict[mom_copies]['Happen'] * gene_dict[dad_copies]['Happen']

            person_prob[child] = [copies, gene_prob]

    return print(person_prob)

    raise NotImplementedError


def update(probabilities, one_gene, two_genes, have_trait, p):
    """
    Add to `probabilities` a new joint probability `p`.
    Each person should have their "gene" and "trait" distributions updated.
    Which value for each distribution is updated depends on whether
    the person is in `have_gene` and `have_trait`, respectively.
    """
    raise NotImplementedError


def normalize(probabilities):
    """
    Update `probabilities` such that each probability distribution
    is normalized (i.e., sums to 1, with relative proportions the same).
    """
    raise NotImplementedError


if __name__ == "__main__":
    main()
