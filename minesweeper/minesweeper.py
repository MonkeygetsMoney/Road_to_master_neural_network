# think broader, I can use class variable 
import random

class Minesweeper():
    """
    Minesweeper game representation
    """

    def __init__(self, height=8, width=8, mines=8):

        # Set initial width, height, and number of mines
        self.height = height
        self.width = width
        self.mines = set()

        # Initialize an empty field with no mines
        self.board = []
        for i in range(self.height):
            row = []
            for j in range(self.width):
                row.append(False)
            self.board.append(row)

        # Add mines randomly
        while len(self.mines) != mines:
            i = random.randrange(height)
            j = random.randrange(width)
            if not self.board[i][j]:
                self.mines.add((i, j))
                self.board[i][j] = True

        # At first, player has found no mines
        self.mines_found = set()

    def print(self):
        """
        Prints a text-based representation
        of where mines are located.
        """
        for i in range(self.height):
            print("--" * self.width + "-")
            for j in range(self.width):
                if self.board[i][j]:
                    print("|X", end="")
                else:
                    print("| ", end="")
            print("|")
        print("--" * self.width + "-")

    def is_mine(self, cell):
        i, j = cell
        return self.board[i][j] # return either true or false established up in the initialized

    def nearby_mines(self, cell):
        """
        Returns the number of mines that are
        within one row and column of a given cell,
        not including the cell itself.
        """

        # Keep count of nearby mines
        count = 0 # show the number of neighbor cells

        # Loop over all cells within one row and column
        for i in range(cell[0] - 1, cell[0] + 2):
            for j in range(cell[1] - 1, cell[1] + 2):

                # Ignore the cell itself
                if (i, j) == cell:
                    continue

                # Update count if cell in bounds and is mine
                if 0 <= i < self.height and 0 <= j < self.width:
                    if self.board[i][j]:
                        count += 1

        return count

    def won(self):
        """
        Checks if all mines have been flagged.
        """
        return self.mines_found == self.mines
    
class Sentence():
    """
    Logical statement about a Minesweeper game
    A sentence consists of a set of board cells,
    and a count of the number of those cells which are mines.
    """

    def __init__(self, cells, count):
        self.cells = set(cells) # create a set of cells
        self.count = count # return the count of cells

    def __eq__(self, other):
        return self.cells == other.cells and self.count == other.count

    def __str__(self):
        return f"{self.cells} = {self.count}"

    def known_mines(self):
        """
        Returns the set of all cells in self.cells known to be mines.
        """
        if len(self.cells) == self.count and self.count != 0:
            return self.cells # return updated cells or return None if we already mark that cells
        else:
            return set()
        raise NotImplementedError

    def known_safes(self):
        """
        Returns the set of all cells in self.cells known to be safe.
        """
        if self.count == 0:
            return self.cells
        else:
            return set()
        raise NotImplementedError

    def mark_mine(self, cell):
        """
        Updates internal knowledge representation given the fact that
        a cell is known to be a mine.
        """
        if cell in self.cells:
            self.cells.remove(cell)
            self.count -= 1
            return self.cells
        else:
            return None
        raise NotImplementedError

    def mark_safe(self, cell):
        """
        Updates internal knowledge representation given the fact that
        a cell is known to be safe.
        """
        if cell in self.cells:
            self.cells.remove(cell) # minus from the set
            return self.cells
        else:
            return None
        raise NotImplementedError

class MinesweeperAI(): # the class made for the AI to make its own moves
    """
    Minesweeper game player
    """

    def __init__(self, height=3, width=3):

        # Set initial height and width
        self.height = height
        self.width = width

        # Keep track of which cells have been clicked on
        self.moves_made = set()
        # Keep track of cells known to be safe or mines
        self.mines = set()
        self.safes = set()

        # List of sentences about the game known to be true
        self.knowledge = [] # maybe this is where the sentence implement
                            # Sentence(set(), 1)

    def mark_mine(self, cell):
        """
        Marks a cell as a mine, and updates all knowledge
        to mark that cell as a mine as well.
        """
        self.mines.add(cell)
        for sentence in self.knowledge: # update the location of the mines into the set
            sentence.mark_mine(cell)

    def mark_safe(self, cell):
        """
        Marks a cell as safe, and updates all knowledge
        to mark that cell as safe as well.
        """
        self.safes.add(cell)
        for sentence in self.knowledge:
            sentence.mark_safe(cell) # a get mark_safe in the Sentence class, also update if it was previous in the cell

    def add_knowledge(self, cell, count): # cell input is a safe move
        """                               # we can also known that the number of mines around that cell
        Called when the Minesweeper board tells us, for a given
        safe cell, how many neighboring cells have mines in them.

        This function should:
            1) mark the cell as a move that has been made
            2) mark the cell as safe
            3) add a new sentence to the AI's knowledge base
               based on the value of `cell` and `count`
            4) mark any additional cells as safe or as mines
               if it can be concluded based on the AI's knowledge base
            5) add any new sentences to the AI's knowledge base
               if they can be inferred from existing knowledge
        """
        self.moves_made.add(cell)
        print(self.moves_made, 'this is my move')

        self.mark_safe(cell)
            # new_sentence = Sentence(cell, count)
            # no need for this since we will apply known mines and safes in Sentence class

            # create a new sentence for the knowledge base

        neighbor_cells = set()
        for x in range(cell[0] - 1, cell[0] + 2): # row
            for y in range(cell[1] - 1, cell[1] + 2): # column
                    # set some limitations
                if (x, y) == cell:
                    continue
                if (x, y) in self.safes:
                    continue
                if (x, y) in self.mines:
                    count -= 1
                    continue

                if 0 <= x < self.height and 0 <= y < self.width:
                    neighbor_cells.add((x, y))

        self.knowledge.append(Sentence(neighbor_cells, count))

        # to mark any additional values, access to the known_safes and known_mines in sentence class
        # for i in range(len(self.knowledge)):
        #     for safe in self.knowledge[i].known_safes():
        #         self.mark_safe(safe)
        #         print(self.mark_safe(safe))
        #     for mine in self.knowledge[i].known_mines():
        #         self.mark_mine(mine)
        #         print(self.mark_mine(mine))

        change = True
        while change:
            change = False

            safes = set()
            mines = set()

            for sentence in self.knowledge:
                safes = safes.union(sentence.known_safes()) # get safe cell and update every time
                mines = mines.union(sentence.known_mines())

            # safes -= self.safes # keep only cells that haven't been marked
            # mines -= self.mines
 
            if safes:
                change = True
                for safe in safes:
                    self.mark_safe(safe)
            if mines:
                change = True
                for mine in mines:
                    self.mark_mine(mine)

            empty = Sentence(set(), 0)
            self.knowledge[:] = [x for x in self.knowledge if x != empty]

            for sentence1 in self.knowledge:
                for sentence2 in self.knowledge:
                    if sentence1.cells == sentence2.cells: 
                        continue # ignored when they are the same

                    if sentence1.cells.issubset(sentence2.cells):
                        new_cells = sentence2.cells - sentence1.cells
                        new_count = sentence2.count - sentence1.count

                        new_sentence = Sentence(new_cells, new_count)

                        if new_sentence not in self.knowledge:
                            change = True
                            self.knowledge.append(new_sentence)

                    if sentence2.cells.issubset(sentence1.cells): # do it both way
                        new_cells = sentence1.cells - sentence2.cells
                        new_count = sentence1.count - sentence2.count
                    
                        new_sentence = Sentence(new_cells, new_count)
                    
                        if new_sentence not in self.knowledge:
                            change = True
                            self.knowledge.append(new_sentence)

        print(self.moves_made, f'These are safe cells: {self.safes},', self.mines, 'long data!!!')
        for sentence in self.knowledge:
            print(sentence)
        #raise NotImplementedError

    def make_safe_move(self):
        """
        Returns a safe cell to choose on the Minesweeper board.
        The move must be known to be safe, and not already a move
        that has been made.

        This function may use the knowledge in self.mines, self.safes
        and self.moves_made, but should not modify any of those values.
        """
        # safe_moves = []
        # # we can use loop to through 
        # for safes_coord in self.safes:
        #     if safes_coord not in self.moves_made:
        #         safe_moves.append(safes_coord)
        #     else: continue
        # if len(safe_moves) > 0:
        #     index = random.randint(0, len(safe_moves) - 1)
        #     return safe_moves[index]
        # else:
        #     return None

        safe_moves = self.safes - self.moves_made
        if safe_moves:
            return random.choice(list(safe_moves))

        return None
        raise NotImplementedError

    def make_random_move(self):
        """
        Returns a move to make on the Minesweeper board.
        Should choose randomly among cells that:
            1) have not already been chosen, and
            2) are not known to be mines
        """
        random_move = []
        for i in range(self.height):
            for j in range(self.width):
                if (i,j) not in self.moves_made and (i, j) not in self.mines:
                    random_move.append((i,j))

        return random.choice(random_move)        

        raise NotImplementedError
    

