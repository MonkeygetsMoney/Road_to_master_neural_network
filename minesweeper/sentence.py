class Sentence():
    """
    Logical statement about a Minesweeper game
    A sentence consists of a set of board cells,
    and a count of the number of those cells which are mines.
    """

    # cells accept would be an array of board cells to make a set
    def __init__(self, cells, count):
        self.cells = set(cells) # create a set of cells
        self.count = count # return the count of cells
        # doesn't know what the count is yet

    def __eq__(self, other):
        return self.cells == other.cells and self.count == other.count

    def __str__(self):
        return f"{self.cells} = {self.count}"

    def known_mines(self):
        """
        Returns the set of all cells in self.cells known to be mines.
        """
        self.mines = self.cells # define instance variable so known_mines and safes are different
        return self.mines 
        raise NotImplementedError

    def known_safes(self):
        """
        Returns the set of all cells in self.cells known to be safe.
        """
        self.safes = self.cells
        return self.safes
        raise NotImplementedError

    def mark_mine(self, cell):
        """
        Updates internal knowledge representation given the fact that
        a cell is known to be a mine.
        """
        set_cell = set(cell)
        self.mines -= set_cell
        self.count -= 1
        #raise NotImplementedError

    def mark_safe(self, cell):
        """
        Updates internal knowledge representation given the fact that
        a cell is known to be safe.
        """
        set_cell = set(cell)
        self.safes -= set_cell
        #raise NotImplementedError

cells = []
for i in range(3):
    for j in range(3):
        cells.append((i, j))

# can minus 2 sets topgether
mines = Sentence(cells, 0)
print(mines.cells)
print(mines.known_safes(), mines.known_mines()) # initial values
mine_coord =[(0, 1)] # wrap in a list to print list of tuple
safe_coord = [(1,1)]
mines.mark_mine(mine_coord)
mines.mark_safe(safe_coord)
print(mines.known_safes(), mines.known_mines()) # edit values
# maybe using deepcopy so it not modifies