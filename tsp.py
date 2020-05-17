import random
import pygame
import sys
import math
import time

pygame.init()


totalNum = 15 #Total number of destinations 
popNum = 5000
font = pygame.font.Font('freesansbold.ttf', 15)
WIDTH = 600
HEIGHT = 600
PERCENTAGE = 0.5 #How much of the current population to crossover for the next generation

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Travelling Salesman Problem")

class City:
    def __init__(self, x, y, i):
        self.x = x
        self.y = y
        self.num = i
        self.text = font.render(str(self.num), False, (255, 255, 255))

    def display(self):
        pygame.draw.circle(screen, (255, 255, 255), (self.x, self.y), 5)

#Randomly initializing the coordinates of the cities
cities = [City(random.randint(50, WIDTH - 50), random.randint(50, HEIGHT - 50), i) for i in range(totalNum)] 


class Route:
    def __init__(self):
        self.distance = 0
        self.cityPath = random.sample(list(range(totalNum)), totalNum)

    def display(self):
        for i, cityNum in enumerate(self.cityPath):
            pygame.draw.line(screen, (0, 0, 255), (cities[self.cityPath[i]].x, cities[self.cityPath[i]].y), \
                            (cities[self.cityPath[i-1]].x, cities[self.cityPath[i-1]].y))

    def calcDistance(self):
        distance = 0
        for i, cityNum in enumerate(self.cityPath):
            distance += math.sqrt((cities[self.cityPath[i]].x - cities[self.cityPath[i-1]].x)**2 + \
                                 (cities[self.cityPath[i]].y - cities[self.cityPath[i-1]].y)**2)
        self.distance = distance
        return distance

population = [Route() for i in range(popNum)]

#Sorts the population on the basis of the fitness function, ie, the distance of the route
def sortPop():
    global population
    population.sort(key = lambda x : x.distance, reverse = False)
    return
'''
Takes the top PERCENTAGE of the population for a particular generation and 
produces a new population replacing the non essential members with new ones
'''
def crossover():
    global population
    updatedPop = []
    updatedPop.extend(population[: int(popNum*PERCENTAGE)])

    for i in range(popNum - len(updatedPop)):
        index1 = random.randint(0, len(updatedPop) - 1)
        index2 = random.randint(0, len(updatedPop) - 1)
        while index1 == index2:
            index2 = random.randint(0, len(updatedPop) - 1)
        parent1 = updatedPop[index1]
        parent2 = updatedPop[index2]
        p = random.randint(0, totalNum - 1)
        child = Route()
        child.cityPath = parent1.cityPath[:p]
        notInChild = [x for x in parent2.cityPath if not x in child.cityPath]
        child.cityPath.extend(notInChild)
        updatedPop.append(child)
    population = updatedPop
    return




def main():
    global population
    running = True
    counter = 0

    best = random.choice(population)

    minDistance = best.calcDistance()
    '''
    Print the coordinates of the randomly generated points
    
    for city in cities:
            print(city.x, city.y)
    '''
    clock = pygame.time.Clock()
    while True:
        best.display()
        if counter >= popNum - 1:
            break
        #print(counter)
        clock.tick(60)
        pygame.display.update()
        screen.fill((0, 0, 0))
        for city in cities:
            city.display()
            screen.blit(city.text, (city.x - 20, city.y - 20))
        for element in population:
            element.calcDistance()

        sortPop()
        crossover()
        
        for element in population:
            if element.distance < minDistance:
                minDistance = element.calcDistance()
                best = element
            elif element.distance == minDistance:
                counter += 1
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()
                sys.exit()
    print("The minimum distance is : {}".format(minDistance))
    print("A feasible path : {}".format(best.cityPath))
    best.display()
    pygame.display.update()
    time.sleep(5)

if __name__ == "__main__":
    main()
