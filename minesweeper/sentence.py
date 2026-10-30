# think broader, I can use class variable 
import random

class Sentence():
    """
    Logical statement about a Minesweeper game
    A sentence consists of a set of board cells,
    and a count of the number of those cells which are mines.
    """

    def __init__(self, cells, count):
        self.cells = set(cells) # create a set of cells
        self.count = count # return the count of cells
        self.safe_cells = [] #initialized lists that other methods can access
        self.mine_cells = []

    def __eq__(self, other):
        return self.cells == other.cells and self.count == other.count

    def __str__(self):
        return f"{self.cells} = {self.count}"

    def known_mines(self):
        """
        Returns the set of all cells in self.cells known to be mines.
        """
        return set(self.mine_cells)
        raise NotImplementedError

    def known_safes(self):
        """
        Returns the set of all cells in self.cells known to be safe.
        """
        return set(self.safe_cells)
        raise NotImplementedError

    def mark_mine(self, cell):
        """
        Updates internal knowledge representation given the fact that
        a cell is known to be a mine.
        """
        print(cell in self.cells)
        if cell in self.cells:
            self.mine_cells.append(cell)
            self.cells -= set([cell])
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
            self.safe_cells.append(cell)
            self.cells -= set([cell]) # minus from the set
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
            sentence.mark_safe(cell) # a get mark_safe in the Sentence class

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
        if cell not in self.moves_made or cell not in self.safes:
            set_cell = set(cell)
            self.moves_made.update(set_cell)
            self.mark_safe(cell)
            new_sentence = Sentence(cell, count)
            self.knowledge.append(new_sentence)

            i, j = cell
            neighbor_cells = []
            if sentence.count > 0:
                for x in range(-1,self.width-1):
                    for y in range(-1,self.height-1):
                        coord = (i+x, j+y)
                        neighbor_cells.append(coord)

                neighbor_sentence = Sentence(neighbor_cells, count)
                self.knowledge.append(neighbor_sentence)

            for sentence in self.add_knowledge:
                # if count is one, then all the surrounding is 1 or possibly a mine
        raise NotImplementedError

    def make_safe_move(self):
        """
        Returns a safe cell to choose on the Minesweeper board.
        The move must be known to be safe, and not already a move
        that has been made.

        This function may use the knowledge in self.mines, self.safes
        and self.moves_made, but should not modify any of those values.
        """
        safe_moves = []
        # we can use loop to through 
        for safes_coord in self.safes:
            if safes_coord not in self.moves_made:
                safe_moves.append(safes_coord)
            else: continue

        if safe_moves:
            index = random.randint(0, len(safe_moves) - 1)
            return safe_moves[index]
        else:
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

        raise NotImplementedError
    
cells = []
for i in range(3):
    for j in range(3):
        cells.append((i, j))

mines = Sentence(cells, 3)
print(mines.cells)
mines.mark_mine((0,1))
print(mines.known_mines())
print(mines.__str__())

ai = MinesweeperAI()
set_cell = [(0,1), (0,0), (1,1)]
