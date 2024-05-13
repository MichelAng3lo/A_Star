import time

import pygame
from random import random, choice
from math import dist
width, heigth = 150,150
WIN = pygame.display.set_mode((width*5, heigth*5) )
class Node:
    def __init__(self, x, y):
        self.g_cost = float('inf')
        self.h_cost = 0
        self.parent = 0
        self.f_cost = 0
        self.x = x
        self.y = y
        self.size = 5
        self.walkable = True if random() > 0.33 else False
        self.color = "blue" if self.walkable else "black"

    def draw(self, surface):
        pygame.draw.rect(surface,self.color,(self.x*self.size, self.y*self.size, self.size, self.size))

class Grid():
    def __init__(self,size_x, size_y):
        self.grid = [Node(j,i) for i in range(size_x) for j in range(size_y)]

    def draw(self):
        for node in self.grid:
            node.draw(WIN)

    def getNeighbours(self, node):
        x = node.x
        y = node.y
        neighbours = []
        for i in [-width,-1,1,width]:
            if not(((x+width*y%width== width - 1) & (i == 1))|((x+width*y%width==0)&( i == -1))):
                if (x+width*y+i > -1) & (x+width*y+i < len(self.grid)):
                    neighbours.append(self.grid[x+width*y+i])
        return neighbours
    def getLowestF(self,openset):
        lowest = float('inf')
        for node in openset:
            if node.f_cost < lowest:
                lowest = node.f_cost
                nodeWithLowest = node
        return nodeWithLowest
class AStar:
    def __init__(self):
        self.grid = Grid(width, heigth)
        x = choice(self.grid.grid)
        while not (x.walkable):
            x = choice(self.grid.grid)
        self.starting_node = x
        y = choice(self.grid.grid)
        while not (y.walkable):
            y = choice(self.grid.grid)
        self.end_node = y
        self.starting_node.color = "green"
        self.end_node.color = "purple"
        self.calculateHCost()
        self.path = []
        #for node in self.grid.getNeighbours(self.starting_node):
         #   node.color = "cyan"
    def draw(self):
        self.grid.draw()
    def findPath(self):
        openset = [self.starting_node]
        closedset = []
        self.starting_node.g_cost = 0
        run = True
        while (openset != []) & run:
            pygame.display.update()
            pygame.time.Clock().tick()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False


            currentNode = self.grid.getLowestF(openset)

            if currentNode == self.end_node:
                return self.reconstructPath(self.end_node.parent.parent, self.end_node.parent)

            openset.remove(currentNode)
            closedset.append(currentNode)
            if currentNode !=self.starting_node:
                currentNode.color = (100,(currentNode.g_cost/currentNode.f_cost)*255,(currentNode.g_cost/currentNode.f_cost)*255)
                currentNode.draw(WIN)
            for node in self.grid.getNeighbours(currentNode):

                if node.walkable:
                    if node in closedset:
                        continue
                    tempGCost = currentNode.g_cost + 10*dist((currentNode.x,currentNode.y),(node.x,node.y))

                    tempIsBetter = False
                    node.color = "cyan"
                    node.draw(WIN)
                    if node not in openset:
                        openset.insert(0,node)
                        tempIsBetter = True
                    elif tempGCost < node.g_cost:
                        tempIsBetter = True
                    if tempIsBetter:
                        node.parent = currentNode
                        node.g_cost = tempGCost
                        node.f_cost = node.g_cost + node.h_cost

        return False

    def calculateHCost(self):
        for node in self.grid.grid:
            x = abs(self.end_node.x - node.x)
            y = abs(self.end_node.y - node.y)
            node.h_cost = x*10 + y*10


    def reconstructPath(self, cameFrom, currentNode):
        self.path.append(currentNode)
        if cameFrom.parent != 0:
            self.reconstructPath(cameFrom.parent, cameFrom)
        else:
            pass

    def drawPath(self):
        for node in self.path:
            node.color = "pink"
def main():
    start = time.time()
    aStar = AStar()
    aStar.draw()
    run = True
    aStar.findPath()
    aStar.drawPath()
    koniec = time.time()
    print(koniec - start)
    while run:

        aStar.draw()

        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False


if __name__ == "__main__":
    main()