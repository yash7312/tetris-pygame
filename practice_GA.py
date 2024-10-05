import random

def food(x,y,z):
    return 9*x**2 + 6*y**3 + z - 20

def fitness(x,y,z):
    ans = food(x,y,z)
    
    if ans == 0:
        return 9999999
    else:
        return abs(1/ans)
    
solutions = []

for s in range(1000):
    solutions.append((random.uniform(0,10000),random.uniform(0,10000),random.uniform(0,10000)))
    
for i in range(10000):
    
    rankedSolutions = []
    for s in solutions:
        rankedSolutions.append((fitness(s[0], s[1], s[2]), s))
    
    rankedSolutions.sort(reverse=True)
    
    print(f"==== Gen  {i} {20+food(rankedSolutions[0][1][0],rankedSolutions[0][1][1],rankedSolutions[0][1][2])} best solutions === ")
    print(rankedSolutions[0])
    
    
    bestsolutions = rankedSolutions[:100]
    
    elements = []
    for s in bestsolutions:
        elements.append(s[1][0])
        elements.append(s[1][1])
        elements.append(s[1][2])
    
    
    newGen = []
    for _ in range(1000):
        e1 = random.choice(elements) * random.uniform(0.99,1.01)
        e2 = random.choice(elements) * random.uniform(0.99,1.01)
        e3 = random.choice(elements) * random.uniform(0.99,1.01)
        
        newGen.append((e1,e2,e3))
    
    if rankedSolutions[0][0] > 99999:
        break
    solutions = newGen