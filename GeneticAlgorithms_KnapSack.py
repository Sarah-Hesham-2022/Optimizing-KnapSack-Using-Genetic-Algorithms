#This returns a number N in the inclusive range [a,b], meaning a <= N <= b, where the endpoints are included in the range.
#Random floating point values can be generated using the random() function. Values will be generated in the range between 0 and 1, specifically in the interval [0,1).
#print(random.randint(0,9))
#print(random.random())
#print(random.uniform(0.1,0.2))

import random

#To write console Output in a text file and save it in a given path
import sys

#Probability of crossover and mutation
PC = 0.7
PM = 0.01

#Step 1: Initilaize Population
#We can represent a solution (the items selected) as a chromosome containing N bits; each 
#bit (i) corresponds to item (i) where 1 means that the item is selected and 0 means that it 
#is not selected.This function returns a 2d array containing arrays of 0,1 representing state of the items
def InitializeIndividual(size):
    
    individual=[]

    for i in range(size):
        individual.append(random.randint(0,1))

    return individual

def InitializePopulation(populationSize,lenItem):

    items=[]

    for i in range(populationSize):
        items.append(InitializeIndividual(lenItem))

    return items

#Step 2: Let’s evaluate the fitness of each chromosome using the objective function according to its value given vi:
#This function returns an array of fitness values corresponding each population in array returned by InitializePopulation function
def IndividualFitness(individual,items):

    sumFitness=0

    for i in range(len(individual)):
            if(individual[i] == 1):
                sumFitness = items[i][1] + sumFitness
    
    return sumFitness

def PopulationFitness(population,items):

    fitnessValues = []

    for i in (population):
        fitnessValues.append(IndividualFitness(i,items))

    return fitnessValues

#Here we have one constraint which is we are afraid that our items weights will exceed the size of the knapsack
#So in case this happens in an individual , I pass it to a CorrectIndividual function that randomly changes its values
#Until reaching a reasonable acceptable fitness that won't exceed the size of the knap sack
def IndividualWeight(individual,items):

    sumWeight=0

    for i in range(len(individual)):
            if(individual[i] == 1):
                sumWeight = items[i][0] + sumWeight
    
    return sumWeight

def CorrectIndividual(individual,sizeKnapSack,items):

    weight = IndividualWeight(individual,items)

    while(weight > sizeKnapSack):
        individual = InitializeIndividual(len(individual))
        weight = IndividualWeight(individual,items)

    return individual

def FeasibilityCheck(population,sizeKnapSack,items):

    for i in range(len(population)):

          weight = IndividualWeight(population[i],items) 

          if(weight > sizeKnapSack):
               population[i] = CorrectIndividual(population[i],sizeKnapSack,items)

    return population

#Step 3: Let’s select the parents! First, we need to calculate the cumulative fitness function using Roulette Wheel Algorithm:
#So roulette wheel function returns the selected parent
def RouletteWheelSelection(population,fitnessValues):

    cumFitness = []
    total = sum(fitnessValues)
    sumFitness = 0

    for i in range(len(fitnessValues)):
        sumFitness = sumFitness + fitnessValues[i]
        cumFitness.append(sumFitness)
 
    rand = random.randint(0,total-1)
       
    for j in range(len(cumFitness)):
      if(rand < cumFitness[j] ):
        return (population[j])

#Step 4: Let’s perform crossover between C1 and C2:
#First, generate a random integer (Xc) between 1 and len(C)-1 to be the crossover point.
#Second, generate a random number (rc) between 0 and 1:
#If rc <= Pc, perform crossover at Xc.
#If rc > Pc, no crossover. (O1 = C1 and O2 = C2)
def Crossover(parent1 ,parent2):

    rc = random.random()

    if(rc <= PC):
        XC = random.randint(1,len(parent1)-1)
        index = XC
       
        while(index < len(parent1)):
            temp = parent1[index]
            parent1[index] = parent2[index]
            parent2[index] = temp
            index = index +1 

    return parent1,parent2


#Step 5: Let’s perform mutation on the offspring:
#Iterate over each bit in each offspring chromosome and:
#▪ Generate a random number (r) between 0 and 1.
#▪ If r <= Pm, flip that bit.   
def Mutate(child):

    for i in range(len(child)):
        r = random.uniform(0,0.1)
        if(r <= PM):
            child[i] = int(not(child[i]))

    return child
    
#Step 6: Replace the current generation with the new offspring using any of the 
#replacement strategies explained earlier, go to step 2 and repeat the process
#Steady-state replacement: a number of individuals are selected to reproduce, and 
#the offspring replace their parents.
#Drawbacks: possibility of losing of good chromosomes.
def Replacement(population,parents,children):
    
    for i in range(len(population)):
        if(population[i] == parents [0]):
            population[i] = children[0]
        
        elif(population[i] == parents[1]):
            population[i] = children[1]


    return population

#Mating Function takes 2 parents and returns two children 
def Mating(population,fitnessValues,sizeKnapSack,items):

        parent1 = RouletteWheelSelection(population,fitnessValues)
        parent2 = RouletteWheelSelection(population,fitnessValues)

        #while(parent1 == parent2):
            #parent2 = RouletteWheelSelection(population,fitnessValues)
        
        parents = [parent1,parent2]  

        child1,child2 = Crossover(parent1,parent2)
        child1 = Mutate(child1)
        child2 = Mutate(child2)

        children = [child1,child2]
        children =FeasibilityCheck(children,sizeKnapSack,items)

        population = Replacement(population,parents,children)

        return population

#Final Optimal Function Check at last generation iteration done to take best individual
def CalcOptimal(population,fitnessValues):

    maxFitness = max(fitnessValues)

    index =0 

    for i in range(len(population)):
        if(fitnessValues[i] == maxFitness):
            index = i 
            break

    return population[index]

#PrintResult function
#The output should consist of the test case index, the number of selected items, the 
#total value, and the weight and value of each selected item.

def printResult(population,fitnessValues,items,TestCaseIndex):
  
    print("*************************************************************")
    print("*************************************************************")
    bestSolution = CalcOptimal(population,fitnessValues)

    print("Test Case Index : " + str(TestCaseIndex))

    selectedItems = []
    value = IndividualFitness(bestSolution,items)
    weights = IndividualWeight(bestSolution,items) 

    for i in range(len(bestSolution)):

        if(bestSolution[i] == 1):
            selectedItems.append(items[i])

    print("The number of selected items : " + str(len(selectedItems)))
    print("The total value : " + str(value))
    print("The total weight used : " + str(weights))
    print("The weight and value of each selected items : ")
    print(selectedItems)
    print("*************************************************************")
    print("*************************************************************")


#Our KnapSack Function that calls other functions
def KnapSack(sizeKnapSack,noItems,items,TestCaseIndex):

    populationSize = noItems*2
    noIterations =   int(noItems/2)

    population = InitializePopulation(populationSize,noItems)
    
    for i in range(noIterations):

        population = FeasibilityCheck(population,sizeKnapSack,items)
        fitnessValues= PopulationFitness(population,items)
        population = Mating(population,fitnessValues,sizeKnapSack,items)

    printResult(population,fitnessValues,items,TestCaseIndex)


#Main function that handles files
def Main(readFilePath, writeFilePath):

    readFilePath = open(readFilePath) 

    line = readFilePath.readline()

    noTestCases = int(line)

    sys.stdout = open(writeFilePath, "w")

    while(line):

       line = readFilePath.readline()

       for TestCaseIndex in range(noTestCases):
           line = readFilePath.readline()
           line = readFilePath.readline()
           noItems = int(line)
           line = readFilePath.readline()
           sizeKnapSack = int(line)
           line = readFilePath.readline()
           items=[]

           for  i in range(noItems):
              item =[]
              line = line.split()
              item.append(int(line[0]))
              item.append(int(line[1]))
              items.append(item)
              line = readFilePath.readline()

           KnapSack(sizeKnapSack,noItems,items,TestCaseIndex)

    readFilePath.close()
    sys.stdout.close()



#Let us Start our Execution here

readFilePath = "knapsack_input.txt"

#You will have to create the file already in the path given
writeFilePath = "KnapSack_Output.txt"

Main(readFilePath,writeFilePath)

