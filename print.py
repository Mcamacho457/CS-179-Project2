from ClassicNN import ClassicNN
from ModifiedNN import ModifiedNN

collectionOfDistanceNN = []
finalPathNN = []
first_iter = True
prev = 0
count = 0

def output(listOfPoints, dist_mat):
    global collectionOfDistanceNN, finalPathNN, prev, count
    # If it is the first iteration classic nn should be performed
    prev = 0
    time_So_Far = 0
    sumOfDistance, path, _, _ = ClassicNN(listOfPoints, dist_mat)
    # Just like random search if the new distance is not the same as the old distance we found a new route
    if prev != sumOfDistance:
    # This gets the time it took to find a route
    # For jason when making distance over time graph
        time_So_Far = sumOfDistance / 100
        #collectionOfDistanceNN.append((sumOfDistance, time_So_Far)) 
        # For jason when making route graph and kenny for file output
        finalPathNN = path
        #print(f"          {sumOfDistance}")
        prev = sumOfDistance
    # While the user has not hit the entry key this loop will keep going 
    while count < 10:
        #code pauses a quarter of a second. Can change if needed to
        sumOfDistance, path, _, _ = ModifiedNN(listOfPoints, dist_mat, finalPathNN, dist_to_beat=sumOfDistance)
        # This is utilized the same
        if prev != sumOfDistance:
            time_So_Far = sumOfDistance / 100
            #collectionOfDistanceNN.append((sumOfDistance, time_So_Far)) #for jason when making distance over time graph
            finalPathNN = path #for jason when making route graph
        prev = sumOfDistance
        count += 1 
    #print(f"          {sumOfDistance}")   
    #saveRouteImg(listOfPoints, finalPathNN, prev, filename)
    return sumOfDistance, time_So_Far