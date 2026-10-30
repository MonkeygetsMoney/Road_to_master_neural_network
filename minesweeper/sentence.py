# think broader, I can use class variable 

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

        raise NotImplementedError

    def known_safes(self):
        """
        Returns the set of all cells in self.cells known to be safe.
        """
        
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

cells = []
for i in range(3):
    for j in range(3):
        cells.append((i, j))

mines = Sentence(cells, 3)
print(mines.cells)
mines.mark_mine((0,1))
print(mines.mine_cells)