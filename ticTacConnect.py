# made by: Jacob Nguyen
# email: jacobptnguyen@gmail.com

import random

class Game: 
    def __init__(self, nPiecesInARow, nSuperPiecesInARow, board, player1Name, player2Name, boardObject):
        self.nPiecesInARow = nPiecesInARow
        self.nSuperPiecesInARow = nSuperPiecesInARow
        self.board = board
        self.player1Name = player1Name
        self.player1Piece = "X"
        self.player2Name = player2Name
        self.player2Piece = "O"
        #defaulting current player to player 1:
        self.curPlayer = player1Name
        self.curPlayerPiece = "X"
        self.chosenRow = None
        self.chosenCol = None
        self.gameEndedInTie = None
        self.bottomOfGrid = None
        self.chosenInnerCol = None
        self.boardObject = boardObject
        self.someoneWonGrid = False
        self.gridWasTied = False

    def announceResults(self):
        if self.gameEndedInTie:
            print("Tie Game!")
        else:
            print(f'{self.curPlayer} won the game!')

    def switchPlayers(self):
        if self.curPlayer == self.player1Name:
            self.curPlayer = self.player2Name
            self.curPlayerPiece = self.player2Piece
        elif self.curPlayer == self.player2Name:
            self.curPlayer = self.player1Name
            self.curPlayerPiece = self.player1Piece

    def gameIsOver(self):
        if Game.wonOuterHorizontally(self) or Game.wonOuterVertically(self) or Game.wonOuterDiagonally(self):
            return True
        elif Game.endedInTie(self): #at this point, no one has won the game
            self.gameEndedInTie = True
            return True
        else:
            return False

    def endedInTie(self):
        return Game.isBoardFull(self)
    
    def isBoardFull(self):
        for i in range(self.boardObject.numSuperRows):
            for j in range(self.boardObject.numSuperCols):
                for k in range(self.boardObject.numRows):
                    for l in range(self.boardObject.numCols):
                        if self.board[i][j][k][l] != "/":
                            return False
        return True

    def wonOuterDiagonally(self):
        return Game.wonOuterLeftDiag(self) or Game.wonOuterRightDiag(self)

    def wonOuterRightDiag(self):
        """
                        *
                    *
                *
            *
        *
        
        """
        
        upperRightDiag = Game.findUpperRightDiag(self)
        currentGrid = Game.findCurrentGrid(self)
        lowerRightDiag = Game.findLowerRightDiag(self)
        lowerRightDiag.reverse()

        rightDiag = lowerRightDiag + currentGrid + upperRightDiag

        gridsWon = Game.findGridsWonDiag(self, rightDiag)
        return gridsWon == self.nSuperPiecesInARow

    def findUpperRightDiag(self):
        # - +
        upperRightDiag = []
        curGridRow = self.chosenRow
        curGridCol = self.chosenCol
        while True:
            curGridRow -= 1
            curGridCol += 1
            try:
                gridWon = Game.checkIfGridWasWon(self, curGridRow, curGridCol)
                if gridWon:
                    upperRightDiag.append(self.curPlayerPiece)
                else:
                    upperRightDiag.append("+")
            except:
                break
        return upperRightDiag

    def findLowerRightDiag(self):
        # + -
        lowerRightDiag = []
        curGridRow = self.chosenRow
        curGridCol = self.chosenCol
        while True:
            curGridRow += 1
            curGridCol -= 1
            try:
                gridWon = Game.checkIfGridWasWon(self, curGridRow, curGridCol)
                if gridWon:
                    lowerRightDiag.append(self.curPlayerPiece)
                else:
                    lowerRightDiag.append("+")
            except:
                break
        return lowerRightDiag
        
    def wonOuterLeftDiag(self):
        """
        * <-
            * <-
                *
                    *
                        *
        
        
        """

        upperLeftDiag = Game.findUpperLeftDiag(self)
        currentGrid = Game.findCurrentGrid(self)
        lowerLeftDiag = Game.findLowerLeftDiag(self)
        upperLeftDiag.reverse()

        leftDiag = upperLeftDiag + currentGrid + lowerLeftDiag

        gridsWon = Game.findGridsWonDiag(self, leftDiag)
        return gridsWon == self.nSuperPiecesInARow
    
    def findGridsWonDiag(self, diag):
        nInARow = 0
        for i in range(len(diag)):
            if diag[i] == self.curPlayerPiece:
                nInARow += 1
                if nInARow == self.nSuperPiecesInARow:
                    return nInARow
            else:
                nInARow = 0
        return nInARow

    def findLowerLeftDiag(self):
        # + +
        lowerLeftDiag = []
        curGridRow = self.chosenRow
        curGridCol = self.chosenCol
        while True:
            curGridRow += 1
            curGridCol += 1
            try:
                gridWon = Game.checkIfGridWasWon(self, curGridRow, curGridCol)
                if gridWon:
                    lowerLeftDiag.append(self.curPlayerPiece)
                else:
                    lowerLeftDiag.append("+")
            except:
                break
        return lowerLeftDiag

    def findCurrentGrid(self):
        curGrid = []
        gridWon = Game.checkIfGridWasWon(self, self.chosenRow, self.chosenCol)
        if gridWon:
            curGrid.append(self.curPlayerPiece)
        else:
            curGrid.append("+")
        return curGrid

    def findUpperLeftDiag(self):
        # - -
        upperLeftDiag = []
        curGridRow = self.chosenRow
        curGridCol = self.chosenCol
        while True:
            curGridRow -= 1
            curGridCol -= 1
            try:
                gridWon = Game.checkIfGridWasWon(self, curGridRow, curGridCol)
                if gridWon:
                    upperLeftDiag.append(self.curPlayerPiece)
                else:
                    upperLeftDiag.append("+")
            except:
                break
        return upperLeftDiag

    def checkIfGridWasWon(self, curGridRow, curGridCol):
        for i in range(self.boardObject.numRows):
            for j in range(self.boardObject.numCols):
                if self.board[curGridRow][curGridCol][i][j] != self.curPlayerPiece:
                    return False
        return True
        
    def wonOuterVertically(self):
        gridsWon = Game.findGridsWonVert(self)
        return gridsWon == self.nSuperPiecesInARow
    
    def findGridsWonVert(self):
        gridsWon = 0
        for i in range(self.boardObject.numSuperRows):
            if Game.gridWasWon_Vert(self, i):
                gridsWon += 1
                if gridsWon == self.nSuperPiecesInARow:
                    return gridsWon
            else:
                gridsWon = 0
        return gridsWon

    def gridWasWon_Vert(self, curRow):
        for i in range(self.boardObject.numRows):
            for j in range(self.boardObject.numCols):
                if self.board[curRow][self.chosenCol][i][j] != self.curPlayerPiece: #should be ==???
                    return False
        return True

    def wonOuterHorizontally(self):
        gridsWon = Game.findGridsWonHori(self)
        return gridsWon == self.nSuperPiecesInARow
    
    def findGridsWonHori(self):
        gridsWon = 0
        for i in range(self.boardObject.numSuperCols):
            if Game.gridWasWon_Hori(self, i):
                gridsWon += 1
                if gridsWon == self.nSuperPiecesInARow:
                    return gridsWon
            else:
                gridsWon = 0
        return gridsWon

    def gridWasWon_Hori(self, curCol):
        for i in range(self.boardObject.numRows):
            for j in range(self.boardObject.numCols):
                if self.board[self.chosenRow][curCol][i][j] != self.curPlayerPiece:
                    return False
        return True

    def takeTurn(self):
        Game.getValidCol(self)
        Game.placePiece(self)
        if Game.wonCurGrid(self):
            self.someoneWonGrid = True
            Game.takeOverGrid(self)
        elif Game.tieCurGrid(self):
            self.gridWasTied = True
            Game.nullCurGrid(self)
    
    def tieCurGrid(self):
        #at this point, no one has won the current grid
        return Game.curGridIsfull(self)
    
    def curGridIsfull(self):
        for i in range(self.boardObject.numRows):
            for j in range(self.boardObject.numCols):
                if self.board[self.chosenRow][self.chosenCol][i][j] == "+":
                    return False
        return True
    
    def wonCurGrid(self):
        return Game.wonInnerHorizontally(self) or Game.wonInnerVertically(self) or Game.wonInnerDiagonally(self)
    
    def wonInnerHorizontally(self):
        nInARow = 0
        for i in range(self.boardObject.numCols):
            if self.board[self.chosenRow][self.chosenCol][self.bottomOfGrid][i] == self.curPlayerPiece:
                nInARow += 1
                if nInARow == self.nPiecesInARow:
                    return True
            else:
                nInARow = 0
        return nInARow == self.nPiecesInARow

    def wonInnerVertically(self):
        nInARow = 0
        for i in range(self.boardObject.numRows):
            if self.board[self.chosenRow][self.chosenCol][i][self.chosenInnerCol] == self.curPlayerPiece:
                nInARow += 1
                if nInARow == self.nPiecesInARow:
                    return True
            else:
                nInARow = 0
        return nInARow == self.nPiecesInARow

    def wonInnerDiagonally(self):
        return Game.wonInnerLeftDiagonally(self) or Game.wonInnerRightDiagonally(self)
    
    def wonInnerRightDiagonally(self):
        innerUpperRightDiag = Game.getInnerUpperRightDiag(self)
        currentMove = [self.board[self.chosenRow][self.chosenCol][self.bottomOfGrid][self.chosenInnerCol]]
        innerLowerRightDiag = Game.getInnerLowerRightDiag(self)
        innerLowerRightDiag.reverse()

        innerRightDiag = innerUpperRightDiag + currentMove + innerLowerRightDiag

        return Game.gridWasWonDiagonally(self, innerRightDiag)
    
    def getInnerLowerRightDiag(self):
        # + -
        innerLowerRightDiag = []
        curRow = self.bottomOfGrid
        curCol = self.chosenInnerCol
        while True:
            curRow += 1
            curCol -= 1
            try:
                innerLowerRightDiag.append(self.board[self.chosenRow][self.chosenCol][curRow][curCol])
            except:
                return innerLowerRightDiag
    
    def getInnerUpperRightDiag(self):
        # - +
        innerUpperRightDiag = []
        curRow = self.bottomOfGrid
        curCol = self.chosenInnerCol
        while True:
            curRow -= 1
            curCol += 1
            try:
                innerUpperRightDiag.append(self.board[self.chosenRow][self.chosenCol][curRow][curCol])
            except:
                return innerUpperRightDiag

    def wonInnerLeftDiagonally(self):

        innerUpperLeftDiag = Game.getInnerUpperLeftDiag(self)
        currentMove = [self.board[self.chosenRow][self.chosenCol][self.bottomOfGrid][self.chosenInnerCol]]
        innerLowerLeftDiag = Game.getInnerLowerLeftDiag(self)
        innerUpperLeftDiag.reverse()

        innerLeftDiag = innerUpperLeftDiag + currentMove + innerLowerLeftDiag

        return Game.gridWasWonDiagonally(self, innerLeftDiag)

    def gridWasWonDiagonally(self, diag):
        nInARow = 0
        for i in range(len(diag)):
            if diag[i] == self.curPlayerPiece:
                nInARow += 1
                if nInARow == self.nPiecesInARow:
                    return True
            else:
                nInARow = 0
        return nInARow == self.nPiecesInARow

    def getInnerUpperLeftDiag(self):
        # - -
        innerUpperLeftDiag = []
        curRow = self.bottomOfGrid
        curCol = self.chosenInnerCol
        while True:
            curRow -= 1
            curCol -= 1
            try:
                innerUpperLeftDiag.append(self.board[self.chosenRow][self.chosenCol][curRow][curCol])
            except:
                return innerUpperLeftDiag
    
    def getInnerLowerLeftDiag(self):
        # + +
        innerLowerLeftDiag = []
        curRow = self.bottomOfGrid
        curCol = self.chosenInnerCol
        while True:
            curRow += 1
            curCol += 1
            try:
                innerLowerLeftDiag.append(self.board[self.chosenRow][self.chosenCol][curRow][curCol])
            except:
                return innerLowerLeftDiag
    
    def nullCurGrid(self):
        for i in range(self.boardObject.numRows):
            for j in range(self.boardObject.numCols):
                self.board[self.chosenRow][self.chosenCol][i][j] = "/"       
    
    def takeOverGrid(self):
        for i in range(self.boardObject.numRows):
            for j in range(self.boardObject.numCols):
                self.board[self.chosenRow][self.chosenCol][i][j] = self.curPlayerPiece

    def chooseGrid(self):
        #when you choose a grid, it cannot be one that has already been won or tied
        self.chosenRow = random.randint(0, self.boardObject.numSuperRows - 1)
        self.chosenCol = random.randint(0, self.boardObject.numSuperCols - 1)

        gridHasSpace = Game.checkIfGridHasSpace(self)
        gridTied = Game.checkIfGridWasTied(self)

        isValidGrid = gridHasSpace and not gridTied

        while not isValidGrid:
            self.chosenRow = random.randint(0, self.boardObject.numSuperRows - 1)
            self.chosenCol = random.randint(0, self.boardObject.numSuperCols - 1)
            gridHasSpace = Game.checkIfGridHasSpace(self)
            gridTied = Game.checkIfGridWasTied(self)
            isValidGrid = gridHasSpace and not gridTied

    def checkIfGridHasSpace(self):
        for i in range(self.boardObject.numRows):
            for j in range(self.boardObject.numCols):
                if self.board[self.chosenRow][self.chosenCol][i][j] == "*":
                    return True
        return False
    
    def checkIfGridWasTied(self):
        return self.board[self.chosenRow][self.chosenCol][0][0] == "/"

    def placePiece(self):
        bottomOfGrid = Game.findBottomOfGrid(self)
        self.bottomOfGrid = int(bottomOfGrid)
        self.board[self.chosenRow][self.chosenCol][self.bottomOfGrid][self.chosenInnerCol] = self.curPlayerPiece

    def findBottomOfGrid(self):
        for i in range(self.boardObject.numRows):
            if self.board[self.chosenRow][self.chosenCol][i][self.chosenInnerCol] == "+":
                continue
            else:
                return i - 1
        return self.boardObject.numRows - 1 #this happens when the column is completely empty

    def getValidCol(self):
        chosenInnerCol = input(f'{self.curPlayer}, please pick a column in grid {self.chosenRow} {self.chosenCol}: ')
        if chosenInnerCol.strip().lower() == "exit":
            exit()
        while not Game.isValidCol(self, chosenInnerCol):
            chosenInnerCol = input(f'{self.curPlayer}, please pick a column in grid {self.chosenRow} {self.chosenCol}: ')
            if chosenInnerCol.strip().lower() == "exit":
                exit()
        self.chosenInnerCol = int(chosenInnerCol)
    
    def isValidCol(self, chosenInnerCol):
        if not isInteger(chosenInnerCol):
            return False
        if not Game.isInsideGrid(self, chosenInnerCol):
            print("Column is not inside grid...")
            return False
        if not Game.colIsNotFull(self, chosenInnerCol):
            print("Column is full...")
            return False
        return True

    def isInsideGrid(self, chosenInnerCol):
        #at this point the input is one integer
        chosenInnerCol = int(chosenInnerCol)
        return chosenInnerCol >= 0 and chosenInnerCol < self.boardObject.numCols
    
    def colIsNotFull(self, chosenInnerCol):
        for i in range(self.boardObject.numRows):
            if self.board[self.chosenRow][self.chosenCol][i][int(chosenInnerCol)] == "+":
                return True
        return False

class Board:
    def __init__(self, numRows, numCols, numSuperRows, numSuperCols):
        self.numRows = numRows
        self.numCols = numCols
        self.numSuperRows = numSuperRows
        self.numSuperCols = numSuperCols
        self.board = Board.makeEmptyBoard(self)
    
    def makeEmptyBoard(self):
        superBoard = []

        for i in range(self.numSuperRows):
            superRow = []
            for j in range(self.numSuperCols):
                grid = Board.makeGrid(self)
                superRow.append(grid)
            superBoard.append(superRow)

        return superBoard
    
    def makeGrid(self):
        grid = []
        for i in range(self.numRows):
            col = []
            for k in range(self.numCols):
                col.append("*")
            grid.append(col)
        return grid

    def printBoard(self):
        arOuter = Board.findArOuterIndexes(self)
        arInner = Board.findArInnerIndexes(self)

        Board.printOuterColHeader(self, 0, arOuter)
        Board.printColBorder(self)
        for i in range(self.numSuperRows):
            Board.printColHeader(self, arInner)
            Board.printLineOfGrids(self, i, arInner, arOuter)
            if i < self.numSuperRows - 1:
                Board.printHoriBorder(self)

    def findArOuterIndexes(self):
        arOuter = []
        for i in range(self.numSuperRows):
            arInner = []
            for j in range(self.numSuperCols):
                arInner.append(i)
                arInner.append(j)
            arOuter.append(arInner)
        return arOuter

    def findArInnerIndexes(self):
        arOuter = []
        for i in range(self.numRows):
            arInner = []
            for j in range(self.numCols):
                arInner.append(i)
                arInner.append(j)
            arOuter.append(arInner)
        return arOuter

    def printLineOfGrids(self, curSuperRow, arInner, arOuter):
        curOuterRow = curSuperRow
        curOuterCol = 0
        curInnerRow = 0
        curInnerCol = 0
        sectionsGen = 0
        outerRowIndex = arOuter[curOuterRow][curOuterCol]
        outerColIndex = arOuter[curOuterRow][curOuterCol + 1]
        innerRowIndex = arInner[curInnerRow][curInnerCol]
        innerColIndex = arInner[curInnerRow][curInnerCol + 1]
        while curInnerRow < self.numRows:
            innerRowIndex = arInner[curInnerRow][curInnerCol]
            print(f'{outerRowIndex} |  {innerRowIndex} ', end = "")
            for i in range(self.numSuperCols):
                for j in range(self.numCols):
                    outerRowIndex = arOuter[curOuterRow][curOuterCol]
                    outerColIndex = arOuter[curOuterRow][curOuterCol + 1]
                    innerRowIndex = arInner[curInnerRow][curInnerCol]
                    innerColIndex = arInner[curInnerRow][curInnerCol + 1]
                    print(self.board[outerRowIndex][outerColIndex][innerRowIndex][innerColIndex], end = " ")
                    curInnerCol += 2
                sectionsGen += 1
                curOuterCol += 2
                curInnerCol = 0
                if sectionsGen == self.numSuperCols:
                    curInnerRow += 1
                    curOuterCol = 0
                    sectionsGen = 0
                    print("")
                else:
                    print("", end = "| ")

    def printColHeader(self, arInner):
        curOuterCol = 0
        curInnerRow = 0
        curInnerCol = 0
        sectionsGen = 0
        print("       ", end = "")
        for i in range(self.numSuperCols):
            for j in range(self.numCols):
                innerColIndex = arInner[curInnerRow][curInnerCol + 1]
                print(innerColIndex, end = " ")
                curInnerCol += 2
            sectionsGen += 1
            curOuterCol += 2
            curInnerCol = 0
            if sectionsGen == self.numSuperCols:
                curInnerRow += 1
                curOuterCol = 0
                sectionsGen = 0
                print("")
            else:
                print("", end = "| ")

    def printHoriBorder(self):
        print("", end = "       ") #replace with 0 | 0
        for i in range(self.numSuperCols):
            for j in range(self.numCols):
                print("-", end = " ")
            if i < self.numSuperCols - 1:
                print("-", end = " ")
        print("")
    
    def printOuterColHeader(self, curSuperRow, arOuter):
        curOuterRow = curSuperRow
        curOuterCol = 0
        curInnerRow = 0
        curInnerCol = 0
        sectionsGen = 0
        print("       ", end = "")
        for i in range(self.numSuperCols):
            for j in range(self.numCols * 2):
                innerColIndex = arOuter[curOuterRow][curOuterCol + 1]
                if j < self.numCols * 2 - 1:
                    print(innerColIndex, end = "")
                else:
                    print("", end = " ")
                curInnerCol += 2
            sectionsGen += 1
            curOuterCol += 2
            curInnerCol = 0
            if sectionsGen == self.numSuperCols:
                curInnerRow += 1
                curOuterCol = 0
                sectionsGen = 0
                print("")
            else:
                print("", end = "  ")

    def printColBorder(self):
        curOuterCol = 0
        curInnerRow = 0
        curInnerCol = 0
        sectionsGen = 0
        print("     -", end = "")
        for i in range(self.numSuperCols):
            for j in range(self.numCols * 2):
                if j < self.numCols * 2 - 1:
                    print("-", end = "")
                else:
                    print("", end = "-")
                curInnerCol += 2
            sectionsGen += 1
            curOuterCol += 2
            curInnerCol = 0
            if sectionsGen == self.numSuperCols:
                curInnerRow += 1
                curOuterCol = 0
                sectionsGen = 0
                print("")
            else:
                print("", end = "--")

    def highLight(self, chosenRow, chosenCol):
        for i in range(self.numRows):
            for j in range(self.numCols):
                if self.board[chosenRow][chosenCol][i][j] == "*":
                    self.board[chosenRow][chosenCol][i][j] = "+"

    def unHighLight(self, chosenRow, chosenCol):
        for i in range(self.numRows):
            for j in range(self.numCols):
                if self.board[chosenRow][chosenCol][i][j] == "+":
                    self.board[chosenRow][chosenCol][i][j] = "*"

def main():

    mainMenu()
    
    numRows, numCols, numSuperRows, numSuperCols, nPiecesInARow, nSuperPiecesInARow, player1Name, player2Name = getInput()

    board = Board(numRows, numCols, numSuperRows, numSuperCols) #making a board object

    game = Game(nPiecesInARow, nSuperPiecesInARow, board.board, player1Name, player2Name, board)

    playTicTacConnect(game)

def mainMenu():
    print("Welcome to Tic Tac Connect!")
    userInput = input("Enter in \"NEW\" to start a random game or enter in a seed to play on. You can also type \"exit\" to quit: ")
    userInput = userInput.strip()
    userInput = userInput.lower()
    if userInput == "new":
        return
    elif isInteger(userInput):
        print(f'entered in seed {userInput}')
        random.seed(int(userInput))
    elif userInput == "exit":
        exit()
    else:
        print("invalid input...")
        mainMenu()
    
def getInput():

    for question in range(5):

        if question == 0:
            numSuperRows, numSuperCols = getRowsCols("the outer board")
        
        elif question == 1:
            numRows, numCols = getRowsCols("each grid")

        elif question == 2:
            nPiecesInARow = getNPiecesInARow("for each grid", numSuperRows, numSuperCols)
        
        elif question == 3:
            nSuperPiecesInARow = getNPiecesInARow("for the entire board", numRows, numCols)
        
        elif question == 4:
            player1Name = getName(1)
            player2Name = getName(2)
            while isSameName(player1Name, player2Name):
                print("Please enter in a different name...")
                player2Name = getName(2)
    
    return int(numRows), int(numCols), int(numSuperRows), int(numSuperCols), int(nPiecesInARow), int(nSuperPiecesInARow), player1Name, player2Name

def isSameName(player1Name, player2Name):
    return player2Name == player1Name

def getRowsCols(typeOfBoard):
        userInput = input(f'Please enter the number of rows and columns {typeOfBoard} will have in the format row column: ')
        if userInput.strip().lower() == "exit":
            exit()
        while not isCorrectFormat(userInput):
            userInput = input(f'Please enter the number of rows and columns {typeOfBoard} will have in the format row column: ')
            if userInput.strip().lower() == "exit":
                exit()

        userInput = userInput.strip()
        
        rows = []
        cols = []

        for i in range(len(userInput)):
            if userInput[i] == " ":
                break
            else:
                rows.append(userInput[i])

        for i in range(len(userInput)):
            if userInput[len(userInput) - i - 1] == " ":
                break
            else:
                cols.append(userInput[len(userInput) - i - 1])

        rows = "".join(rows)
        cols.reverse()
        cols = "".join(cols)
        return rows, cols

def getNPiecesInARow(typeOfBoard, numRows, numCols):
    userInput = input(f'Please enter in the number of pieces in a row needed to win {typeOfBoard}: ')
    if userInput.strip().lower() == "exit":
        exit()
    while not isValidInteger(userInput, numRows, numCols):
        userInput = input(f'Please enter in the number of pieces in a row needed to win {typeOfBoard}: ')
        if userInput.strip().lower() == "exit":
            exit()
    nPiecesInARow = int(userInput)
    return nPiecesInARow

def isCorrectFormat(userInput):
    userInput = userInput.strip()
    for c in userInput:
        try:
            int(c)
        except:
            if c == " ":
                continue
            return False
    return isTwoNums(userInput)

def isTwoNums(userInput):
    count = 0
    prevCharWasNum = True
    for c in userInput:
        try:
            int(c)
            prevCharWasNum = True
        except:
            if prevCharWasNum:
                count += 1
                prevCharWasNum = False
    return count == 1

def isValidInteger(userInput, numRows, numCols):
    if not isInteger(userInput):
        return False
    if not nPiecesIsPossible(userInput, numRows, numCols):
        print("You cannot win with that number...")
        return False
    return True

def nPiecesIsPossible(userInput, numRows, numCols):
    return int(userInput) <= int(numRows) and int(userInput) <= int(numCols)

def isInteger(userInput):
    userInput = userInput.strip()
    if len(userInput) == 0:
        return False
    for c in userInput:
        try:
            int(c)
        except:
            return False
    return True

def getName(playerNum):
    userInput = input(f'Player {playerNum}, please enter your name: ')
    if userInput.strip().lower() == "exit":
            exit()
    while not validName(userInput):
        userInput = input(f'Player {playerNum}, please enter your name: ')
        if userInput.strip().lower() == "exit":
            exit()
    return userInput

def validName(userInput):
    userInput = userInput.strip()
    return len(userInput) != 0

def playTicTacConnect(game):
    turnsTaken = 0
    game.chooseGrid()
    game.boardObject.highLight(game.chosenRow, game.chosenCol)
    game.boardObject.printBoard()
    game.takeTurn()
    print()
    print()
    turnsTaken += 1
    while not game.gameIsOver():
        game.switchPlayers()
        game.boardObject.printBoard()
        game.takeTurn()
        print()
        print()
        if game.someoneWonGrid or game.gridWasTied:
            if game.someoneWonGrid:
                print(f'{game.curPlayer} won grid {game.chosenRow} {game.chosenCol}!')
            elif game.gridWasTied:
                print(f'grid {game.chosenRow} {game.chosenCol} was tied!')
            if game.gameIsOver():
                break
            game.boardObject.unHighLight(game.chosenRow, game.chosenCol)
            game.chooseGrid()
            game.boardObject.highLight(game.chosenRow, game.chosenCol)
            turnsTaken = 0
            game.someoneWonGrid = False
            game.gridWasTied = False
        else: #no one won a grid, so it could not have been a winning move, so you don't check if the game is over
            turnsTaken += 1
            if turnsTaken == 2:
                game.boardObject.unHighLight(game.chosenRow, game.chosenCol)
                game.chooseGrid()
                game.boardObject.highLight(game.chosenRow, game.chosenCol)
                turnsTaken = 0
    game.boardObject.printBoard()
    game.announceResults()

main()
