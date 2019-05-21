from BaseAI import BaseAI
import math
from collections import Counter
from random import randint
from Grid import Grid


class PlayerAI(BaseAI):
    def getMove(self, grid):
        return self.extpectimax(grid)

    def minimax(self, grid):
        (child,_) = self.maximise(grid, -math.inf, math.inf, 5)
        if child == None:
            (child, _) = self.maximise(grid, -math.inf, math.inf, 1)
        return child

    def extpectimax(self, grid):
        (child, _) = self.maximiseStoch(grid, 3)
        if child == None:
            (child, _) = self.maximiseStoch(grid, 1)
        return child

    def maximise(self, grid, alpha, beta, depth):
        if depth == 0:
            return (None, self.eval(grid))

        (maxChild, maxUtility) = (None, -math.inf)
        nextChild = grid
        for child in grid.getAvailableMoves():
            nextChild = grid.clone()
            nextChild.move(child)
            (_, utility) = self.minimise(nextChild, alpha, beta, depth-1)
            if utility > maxUtility:
                (maxChild, maxUtility) = (child, utility)
            if maxUtility >= beta:
                break
            if maxUtility > alpha:
                alpha = maxUtility
        return maxChild, maxUtility

    def minimise(self, grid, alpha, beta, depth):
        if depth == 0:
            return (None, self.eval(grid))
        (minChild, minUtility) = (None, math.inf)

        holdGrid = grid
        for child in grid.getAvailableCells():
            holdGrid = grid.clone()
            holdGrid.insertTile(child, 2)
            (_, utility) = self.maximise(holdGrid, alpha, beta, depth-1)
            if utility < minUtility:
                (minChild, minUtility) = (child, utility)
            if minUtility <= alpha:
                break
            if minUtility < beta:
                beta = minUtility
        return minChild, minUtility

    def maximiseStoch(self, grid, depth):
        if depth == 0:
            return (None, self.eval(grid))

        (maxChild, maxUtility) = (None, -math.inf)
        for child in grid.getAvailableMoves():
            nextChild = grid.clone()
            nextChild.move(child)
            (_, utility) = self.stochastic(nextChild, depth-1)
            if utility > maxUtility:
                (maxChild, maxUtility) = (child, utility)
        return maxChild, maxUtility

    def stochastic(self, grid, depth):
        if depth == 0:
            return (None, self.eval(grid))

        holdUtility = 0
        length = len(grid.getAvailableCells())
        (maxChild, maxUtility) = (0,0)
        for child in grid.getAvailableCells():
            holdGrid = grid.clone()
            holdGrid.insertTile(child, 2)
            (_, utility) = self.maximiseStoch(holdGrid, depth - 1)
            holdUtility += utility
            if utility > maxUtility:
                (maxChild, maxUtility) = (child, utility)
        return maxChild, (holdUtility/length)

    def eval(self, grid):
        #Current Heurtistics:
        # numEmptyCells - THe number of empty cells remaining in the current game state
        # maxTile - The current highest value tile
        # h1 - Attempts to order the grid in either ascending or descending order vertically
        # h2 - Attempts to order the grid in either ascending or descending order horizontally
        # h3 - Find the current average cell value
        # h4 - Checks if the currrent cells neighbour cells are equal to it - benefit for having same cells next to each other
        #   (Higher average outside oof the 4 centre cells is better)
        # h5 - Checks if the max tile is in one of the corners or not - having in a corner is better
        # h6 - Checks if the outer cells are great than the inside cells - outer being greater is better
        # h7 - Uses the current average cell value to determinne if the centre 4 cells are higher or lower than the current average
        # TODO:
        # h8 - Gives a bonus for the row or column that the max tile is in is full and not compressable
        # h9 - gives bonuses for having larger elements closer to the corner that contains the largest element

        values = [0, 2, 4, 8, 16, 32, 64, 128, 256, 512, 1024, 2048, 4056, 8112]
        numEmptyCells = len(grid.getAvailableCells())
        maxTile = grid.getMaxTile()

        h1 = 0
        horizontal = 3
        if grid.map[0][0] >= grid.map[1][0] >= grid.map[2][0] >= grid.map[3][0] and grid.map[0][1] >= grid.map[1][1] >= grid.map[2][1] >= grid.map[3][1] and grid.map[0][2] >= grid.map[1][2] >= grid.map[2][2] >= grid.map[3][2] and grid.map[0][3] >= grid.map[1][3] >= grid.map[2][3] >= grid.map[3][3]:
            h1 += 20*maxTile
            horizontal = 0
        else:
            if grid.map[0][0] <= grid.map[1][0] <= grid.map[2][0] <= grid.map[3][0] and grid.map[0][1] <= grid.map[1][1] <= grid.map[2][1] <= grid.map[3][1] and grid.map[0][2] <= grid.map[1][2] <= grid.map[2][2] <= grid.map[3][2] and grid.map[0][3] <= grid.map[1][3] <= grid.map[2][3] <= grid.map[3][3]:
                h1 += 20*maxTile
                horizontal = 1
            else:
                h1 -= 100*maxTile

        h2 = 0
        if grid.map[0][0] >= grid.map[0][1] >= grid.map[0][2] >= grid.map[0][3] and grid.map[1][0] >= grid.map[1][1] >= grid.map[1][2] >= grid.map[1][3] and grid.map[2][0] >= grid.map[2][1] >= grid.map[2][2] >= grid.map[2][3] and grid.map[3][0] >= grid.map[3][1] >= grid.map[3][2] >= grid.map[3][3]:
            h2 += 20*maxTile
        else:
            h2 -= 150*maxTile

        h4 = 0
        h10 = 0
        for i in range(0, grid.size):
            for j in range(0, grid.size):
                if grid.map[i][j] != 0:
                    h4 += self.checkNeighbourValues(grid, i, j)
                    h10 += self.checkNeighbourRelevance(grid, i, j)


        h3 = 0
        for i in range(0, grid.size-1):
            for j in range(0, grid.size-1):
                h3 = h3 + grid.map[i][j]
        if len(grid.getAvailableCells()) != 0:
            h3 = 50*h3 / (16 - len(grid.getAvailableCells()))
        else:
            h3 = 50*h3/16
        averageCellValue = h3 / 50

        h7 = 0
        for i in range(1,2):
            for j in range(1,2):
                if grid.map[i][j] < averageCellValue:
                    h7 += averageCellValue
                else:
                    h7 -= averageCellValue

        h8 = 0
        h5 = 0
        unmatchVer = False
        unmatchHor = False
        if maxTile == grid.map[0][0]:
            h5 = 30*maxTile
            for i in range(0, 2):
                if grid.map[i][0] == grid.map[i + 1][0]:
                    unmatchVer = True
                if grid.map[0][i] == grid.map[0][i + 1]:
                    unmatchHor = True
            if unmatchVer == False or unmatchHor == False:
                h8 = 15 * averageCellValue
        else:
            if maxTile == grid.map[3][0]:
                h5 = 30 * maxTile
                for i in range(0, 2):
                    if grid.map[3-i][0] == grid.map[3 - i - 1][0]:
                        unmatchVer = True
                    if grid.map[0][i] == grid.map[0][i + 1]:
                        unmatchHor = True
                if unmatchVer == False or unmatchHor == False:
                    h8 = 15 * averageCellValue
            else:
                h5 = -250*maxTile

        h6 = 0
        if grid.map[1][0] >= grid.map[1][1]:
            h6 += 2 * averageCellValue
        if grid.map[2][0] >= grid.map[2][1]:
            h6 += 2 * averageCellValue
        if grid.map[3][1] >= grid.map[2][1]:
            h6 += 2 * averageCellValue
        if grid.map[3][2] >= grid.map[2][2]:
            h6 += 2 * averageCellValue
        if grid.map[2][3] >= grid.map[2][2]:
            h6 += 2 * averageCellValue
        if grid.map[1][3] >= grid.map[1][2]:
            h6 += 2 * averageCellValue
        if grid.map[0][2] >= grid.map[1][2]:
            h6 += 2 * averageCellValue
        if grid.map[0][1] >= grid.map[1][1]:
            h6 += 2 * averageCellValue

        h9 = 0
        for i in range(0, grid.size):
            for j in range(0, grid.size):
                if i != 0 and j != 0:
                    h9 -= grid.map[i][j]^(i+j)

        return numEmptyCells + 50*maxTile + h1 + h2 + h3 + h4 + h5 + h6 + h7 + h8 + h9 + h10

    def checkNeighbourValues(self, grid, i, j):
        heuristic = 0
        if i < 3:
            if grid.map[i][j] == grid.map[i+1][j]:
                heuristic += grid.map[i][j]*15
            else:
                heuristic -= grid.map[i][j] * 15
        if i > 0:
            if grid.map[i][j] == grid.map[i-1][j]:
                heuristic += grid.map[i][j]*15
            else:
                heuristic -= grid.map[i][j] * 15
        if j < 3:
            if grid.map[i][j] == grid.map[i][j+1]:
                heuristic += grid.map[i][j]*15
            else:
                heuristic -= grid.map[i][j] * 15
        if j > 0:
            if grid.map[i][j] == grid.map[i][j-1]:
                heuristic += grid.map[i][j]*15
            else:
                heuristic -= grid.map[i][j] * 15
        return heuristic

    def checkNeighbourRelevance(self, grid, i, j):
        values = [0, 2, 4, 8, 16, 32, 64, 128, 256, 512, 1024, 2048, 4056, 8112]
        heuristic = 0
        index = values.index(grid.map[i][j])
        if grid.map[i][j] != 2:
            if i < 3:
                if values[index+1] == grid.map[i+1][j] or values[index-1] == grid.map[i+1][j]:
                    heuristic += grid.map[i][j]*8
            if i > 0:
                if values[index+1] == grid.map[i-1][j] or values[index-1] == grid.map[i-1][j]:
                    heuristic += grid.map[i][j]*8
            if j < 3:
                if values[index+1] == grid.map[i][j+1] or values[index-1] == grid.map[i][j+1]:
                    heuristic += grid.map[i][j]*8
            if j > 0:
                if values[index+1] == grid.map[i][j-1] or values[index-1] == grid.map[i][j-1]:
                    heuristic += grid.map[i][j]*8
        else:
            if i < 3:
                if values[index+1] == grid.map[i+1][j]:
                    heuristic += grid.map[i][j]*8
            if i > 0:
                if values[index+1] == grid.map[i-1][j]:
                    heuristic += grid.map[i][j]*8
            if j < 3:
                if values[index+1] == grid.map[i][j+1]:
                    heuristic += grid.map[i][j]*8
            if j > 0:
                if values[index+1] == grid.map[i][j-1]:
                    heuristic += grid.map[i][j]*8

        return heuristic
