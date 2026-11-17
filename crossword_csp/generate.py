import sys
import math
from crossword import *


class CrosswordCreator():

    def __init__(self, crossword):
        """
        Create new CSP crossword generate.
        """
        self.crossword = crossword
        self.domains = { # key is variable and value is all the word those variable will take on
            var: self.crossword.words.copy()
            for var in self.crossword.variables
        }

    def letter_grid(self, assignment):
        """
        Return 2D array representing a given assignment.
        """
        letters = [
            [None for _ in range(self.crossword.width)]
            for _ in range(self.crossword.height)
        ]
        for variable, word in assignment.items():
            direction = variable.direction
            for k in range(len(word)):
                i = variable.i + (k if direction == Variable.DOWN else 0)
                j = variable.j + (k if direction == Variable.ACROSS else 0)
                letters[i][j] = word[k]
        return letters

    def print(self, assignment):
        """
        Print crossword assignment to the terminal.
        """
        letters = self.letter_grid(assignment)
        for i in range(self.crossword.height):
            for j in range(self.crossword.width):
                if self.crossword.structure[i][j]:
                    print(letters[i][j] or " ", end="")
                else:
                    print("█", end="")
            print()

    def save(self, assignment, filename):
        """
        Save crossword assignment to an image file.
        """
        from PIL import Image, ImageDraw, ImageFont
        cell_size = 100
        cell_border = 2
        interior_size = cell_size - 2 * cell_border
        letters = self.letter_grid(assignment)

        # Create a blank canvas
        img = Image.new(
            "RGBA",
            (self.crossword.width * cell_size,
             self.crossword.height * cell_size),
            "black"
        )
        font = ImageFont.truetype("assets/fonts/OpenSans-Regular.ttf", 80)
        draw = ImageDraw.Draw(img)

        for i in range(self.crossword.height):
            for j in range(self.crossword.width):

                rect = [
                    (j * cell_size + cell_border,
                     i * cell_size + cell_border),
                    ((j + 1) * cell_size - cell_border,
                     (i + 1) * cell_size - cell_border)
                ]
                if self.crossword.structure[i][j]:
                    draw.rectangle(rect, fill="white")
                    if letters[i][j]:
                        _, _, w, h = draw.textbbox((0, 0), letters[i][j], font=font)
                        draw.text(
                            (rect[0][0] + ((interior_size - w) / 2),
                             rect[0][1] + ((interior_size - h) / 2) - 10),
                            letters[i][j], fill="black", font=font
                        )

        img.save(filename)

    def solve(self):
        """
        Enforce node and arc consistency, and then solve the CSP.
        """
        self.enforce_node_consistency()
        self.ac3()
        return self.backtrack(dict())

    def enforce_node_consistency(self):
        """
        Update `self.domains` such that each variable is node-consistent.
        (Remove any values that are inconsistent with a variable's unary
         constraints; in this case, the length of the word.)
        """

        # get each variable and get its domain and update based the number of letter
        # can used copy so dont change the dict during loop
        for variable in self.domains.copy():
            letter = variable.length # number of letter in a word
            for word in self.domains[variable].copy():
                if len(word) != letter:
                    self.domains[variable].remove(word)


    def revise(self, x, y):
        """
        Make variable `x` arc consistent with variable `y`.
        To do so, remove values from `self.domains[x]` for which there is no
        possible corresponding value for `y` in `self.domains[y]`.

        Return True if a revision was made to the domain of `x`; return
        False if no revision was made.
        """
        overlap = self.crossword.overlaps[x, y] 
        # return either the coordinate (x, y) or None

        if overlap is None:
            return False
        else:
            x_index = overlap[0]
            y_index = overlap[1]

            x_length = len(self.domains[x]) # original number of word in x variable

            for x_word in self.domains[x].copy():
                flag = False # flag check to see if there's a match
                for y_word in self.domains[y]:
                    if x_word[x_index] == y_word[y_index]:
                        flag = True

                if flag:
                    continue
                else:
                    self.domains[x].remove(x_word)

            if len(self.domains[x]) != x_length:
                return True
            else:
                return False
        raise NotImplementedError

    def ac3(self, arcs=None):
        """
        Update `self.domains` such that each variable is arc consistent.
        If `arcs` is None, begin with initial list of all arcs in the problem.
        Otherwise, use `arcs` as the initial list of arcs to make consistent.

        Return True if arc consistency is enforced and no domains are empty;
        return False if one or more domains end up empty.
        """
        # an arc argument can look like this (X, Y)
        # for the function to called arc consistency
        # it mean that every word for variable X has one compatiable letter for variable Y
        # if a word is not compatible, the word would get removed from that variable

        if arcs is None:
            self.queue = [] # add ordered pair

            for x in self.domains:
                for y in self.crossword.neighbors(x):
                    self.queue.append((x,y))

            print(self.queue)

            while self.queue != []:
                x, y = self.queue.pop() # always the last item 
                                   # decrease overtime
                if self.revise(x, y):
                    if len(self.domains[x]) == 0: # if altered the domains of x come out to 0
                                             # basically no match
                        return False
                    
                    for z in (self.crossword.neighbors(x) - {y}):
                        self.queue.append((z, x))

            return True

        else:
            if arcs == []: # when arcs is an empty list
                return None
            else:
                self.queue = arcs
                while self.queue != []:
                    x, y = self.queue.pop()
                    if self.revise(x, y):

                        if len(self.domains[x]) == 0:
                            return False

                        for z in (self.crossword.neighbors(x) - {y}):
                            self.queue.append((z, x))

                return True
        raise NotImplementedError

    def assignment_complete(self, assignment):
        """
        Return True if `assignment` is complete (i.e., assigns a value to each
        crossword variable); return False otherwise.
        """
        for variable in self.crossword.variables: 
            # check if all variables are in assignment
            if variable in assignment:
                if assignment[variable] is not None:
                    continue

            else:
                return False

        return True
        raise NotImplementedError

    def consistent(self, assignment):
        """
        Return True if `assignment` is consistent (i.e., words fit in crossword
        puzzle without conflicting characters); return False otherwise.
        """

        for variable in assignment:
            length = variable.length # length of that word
            if len(assignment[variable]) != length:
                return False

            # find the neighbor of the current variable
            neighbors = self.crossword.neighbors(variable)
            for neighbor in neighbors:
                # get the overlap index
                index = self.crossword.overlaps[variable, neighbor]

                # check if the nieghbor is present in the assignment
                if neighbor in assignment:

                    if assignment[variable][index[0]] == assignment[neighbor][index[1]]:
                        continue
                    else:
                        return False

        return True
        
        raise NotImplementedError

    def order_domain_values(self, var, assignment):
        """
        Return a list of values in the domain of `var`, in order by
        the number of values they rule out for neighboring variables.
        The first value in the list, for example, should be the one
        that rules out the fewest values among the neighbors of `var`.
        """
        # if any variable in assignment, then their count doesn't matter
        # loop over all neighbor
        neighbors = self.crossword.neighbors(var)
        words = {}
        for word1 in self.domains[var]:
            words[word1] = 0
            for neighbor in neighbors:
                index = self.crossword.overlaps[var, neighbor]
                # return overlap coordinate

                for word2 in self.domains[neighbor]:

                    # if neighbor not in assignment, then we can count it
                    if word2 not in assignment:
                        if word1[index[0]] == word2[index[1]]:
                            words[word1] += 1

        # sorted in ascending order of n, biggest ot smallest
        return sorted(words, key=words.get, reverse=True)

        raise NotImplementedError

    def select_unassigned_variable(self, assignment):
        """
        Return an unassigned variable not already part of `assignment`.
        Choose the variable with the minimum number of remaining values
        in its domain. If there is a tie, choose the variable with the highest
        degree. If there is a tie, any of the tied variables are acceptable
        return values.
        """
        unassign = {}
        # the current to check the length of value in the domain a variable
        current = (None, math.inf)
        for variable in self.domains:

            if variable not in assignment:
                unassign[variable] = len(self.domains[variable])

                # set variable to current if less than the current
                if len(self.domains[variable]) < current[1]:
                    current = (variable, len(self.domains[variable]))

                # if equal, then check the number of neighbor
                if len(self.domains[variable]) == current[1]:

                    # if number of neighbor in current variable is bigger, then set equal to
                    if len(self.crossword.neighbors(variable)) > len(self.crossword.neighbors(current[0])):
                        current = (variable, len(self.domains[variable]))

        unassign = sorted(unassign, key=unassign.get)
        unassign_list = [var for var in unassign]

        # reutrn the first index, which is the fewest in its domain
        return current[0]
        raise NotImplementedError

    def backtrack(self, assignment):
        """
        Using Backtracking Search, take as input a partial assignment for the
        crossword and return a complete assignment if possible to do so.

        `assignment` is a mapping from variables (keys) to words (values).

        If no assignment is possible, return None.
        """

        # check if assignment is comeplete
        complete = True
        for variable in self.domains:
            # if missing a variable, then use backtrack
            if variable not in assignment:
                complete = False

        if not complete:

            # variable with fewest option in its domain
            var = self.select_unassigned_variable(assignment)

            # get the value of the unassigned variable
            for value in self.order_domain_values(var, assignment):

                # set up new copy of assignment to check if that value is consistent
                new_assignment = assignment.copy()
                new_assignment[var] = value

                if self.consistent(new_assignment):
                    # if consistent, then we can add in the official assignment
                    assignment[var] = value

                    # try new variable for the unassign, try every option possible according heuristic value
                    result = self.backtrack(assignment)
                    if result is not None:
                        return result

                # if not consistent, remove from assignment (no need here)
            # if every value failed, then return none
            return None

        else:
            # return assignment if already completed
            return assignment
                
        raise NotImplementedError


def main():

    # Check usage
    if len(sys.argv) not in [3, 4]:
        sys.exit("Usage: python generate.py structure words [output]")

    # Parse command-line arguments
    structure = sys.argv[1]
    words = sys.argv[2]
    output = sys.argv[3] if len(sys.argv) == 4 else None

    # Generate crossword
    crossword = Crossword(structure, words)
    creator = CrosswordCreator(crossword)
    # assignment = creator.solve()

    # # Print result
    # if assignment is None:
    #     print("No solution.")
    # else:
    #     creator.print(assignment)
    #     if output:
    #         creator.save(assignment, output)

    print(len(crossword.variables))
    print(creator.crossword.variables)
    #print(crossword.variables) # Variable (row, column , direction, number of letter)
                                # this is an access to the class
    # print(crossword.words)
    # print(crossword.overlaps)
    # for i in creator.domains:
    #     print(i, creator.domains[i], len(creator.domains[i]))
    print(creator.enforce_node_consistency())
    print(creator.crossword.overlaps[Variable(1, 7, 'down', 7), Variable(6, 5, 'across', 6)])
    # print(creator.revise(Variable(1, 7, 'down', 7), Variable(6, 5, 'across', 6)))
    for i in creator.domains:
        print(creator.crossword.neighbors(i))
        for j in creator.crossword.neighbors(i):
            print((i, j))
    print(creator.crossword.variables)
    for i in creator.domains:
        print(len(creator.domains[i]))
    # for i in creator.domains:
    #     print(type(i.length)) # since


if __name__ == "__main__":
    main()

# note to self
# initially: all variable objects are empty
# their domain take on all possible words
