import random
import math
from BaseAI import BaseAI

class IntelligentAgent(BaseAI):
    def __init__(self, max_depth=5, time_limit=0.2):
        self.max_depth = max_depth
        self.time_limit = time_limit

    def getMove(self, grid):
        move, _ = self.maximize(grid, -float('inf'), float('inf'), 0)
        return move

    def maximize(self, grid, alpha, beta, depth):
        if depth == self.max_depth or not grid.canMove():
            return None, self.getHeuristic(grid)

        (maxChild, maxUtility) = (None, -float('inf'))

        for move in grid.getAvailableMoves():
            _, utility = self.expectiminimize(move[1], alpha, beta, depth + 1)
            if utility > maxUtility:
                (maxChild, maxUtility) = move[0], utility
            if maxUtility >= beta:
                break
            alpha = max(alpha, maxUtility)

        return maxChild, maxUtility

    def expectiminimize(self, grid, alpha, beta, depth):
        if depth == self.max_depth or not grid.canMove():
            return None, self.getHeuristic(grid)

        minUtility = 0
        children = grid.getAvailableMoves()

        if not children:
            return None, self.getHeuristic(grid)

        probability = 1 / len(children)
        for move in children:
            _, utility = self.maximize(move[1], alpha, beta, depth + 1)
            minUtility += utility * probability

        return None, minUtility

    def getHeuristic(self, grid):
        smoothness, freeTiles, maxTile, monotonicity = 0, 0, 0, 0

        # Calculate smoothness and free tiles
        for x in range(grid.size):
            for y in range(grid.size):
                if grid.map[x][y] == 0:
                    freeTiles += 1
                else:
                    maxTile = max(maxTile, grid.map[x][y])
                    value = math.log(grid.map[x][y]) / math.log(2)
                    for d in [(1, 0), (0, 1)]:
                        newX, newY = x + d[0], y + d[1]
                        if newX < grid.size and newY < grid.size and grid.map[newX][newY] != 0:
                            target_value = math.log(grid.map[newX][newY]) / math.log(2)
                            smoothness -= abs(value - target_value)

        # Calculate monotonicity
        for x in range(grid.size):
            for y in range(grid.size - 1):
                if grid.map[x][y] > 0 and grid.map[x][y + 1] > 0:
                    current = math.log(grid.map[x][y]) / math.log(2)
                    next = math.log(grid.map[x][y + 1]) / math.log(2)
                    if current > next:
                        monotonicity += next - current
                    else:
                        monotonicity += current - next

            # Simplified Corner strategy for highest tile
        # Encourage keeping the largest tile in the top-left corner
        corner_weight = 0
        if grid.map[0][0] == max(max(row) for row in grid.map):
            corner_weight = math.log(grid.map[0][0]) / math.log(2) * 2  # Assign a double weight

        # Updated return statement with simplified highest_tile_corner heuristic
        return (smoothness * 0.1) + (freeTiles * 2.7) + (math.log(maxTile) / math.log(2)) * 1.0 + (monotonicity * 1.5) + corner_weight
        # return (smoothness * 0.1) + (freeTiles * 2.7) + (math.log(maxTile) / math.log(2)) * 1.0 + (monotonicity * 1.5)



    def getNextCell(self, grid, x, y, direction):
        x += direction[0]
        y += direction[1]
        if x >= 0 and x < grid.size and y >= 0 and y < grid.size:
            return x, y
        else:
            return None

    # Define the maximum depth for searching
    max_depth = 10  # Adjustable based on the performance
