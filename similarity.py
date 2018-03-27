from math import sqrt

def shared_items(prefs, p1, p2):
    """Get dict of shared items"""
    si = {}
    for item in prefs[p1]:
        if item in prefs[p2]:
            si[item] = 1
    return si            

def sim_distance(prefs, p1, p2):
    """Returns a Euclidean distance-based similarity score 
    for p1 and p2"""
    si = shared_items(prefs, p1, p2)
    
    # if they have no ratings in common, return 0
    if len(si) == 0: return 0
    
    # add up the squares of all the differences
    sum_of_squares = sum([pow(prefs[p1][item] - prefs[p2][item],2)
                        for item in prefs[p1] if item in prefs[p2]])
    
    return 1/(1+sqrt(sum_of_squares))

def manhattan_distance(prefs, p1, p2):
    """Returns a Manhattan distance-based similarity score
    for p1 and p2"""
    si = shared_items(prefs, p1, p2)

    md = sum([abs(prefs[p1][item] - prefs[p2][item])
                        for item in prefs[p1] if item in prefs[p2]])
    
    return 1/(1+md)

def sim_pearson(prefs, p1, p2):
    """Returns a Pearson correlation coefficient
    for p1 and p2"""
    si = shared_items(prefs, p1, p2)
    
    # find the number of shared elements
    n = len(si)

    # if they have no ratings in common, return 0
    if n == 0: return 0
        
    # add up all the preferences
    sum1 = sum([prefs[p1][it] for it in si])
    sum2 = sum([prefs[p2][it] for it in si])

    # sum up the squares
    sum1Sq = sum([pow(prefs[p1][it],2) for it in si])
    sum2Sq = sum([pow(prefs[p2][it],2) for it in si])

    # sum up the products
    pSum = sum([prefs[p1][it]*prefs[p2][it] for it in si])

    # calculate Pearson score
    num = pSum-(sum1*sum2/n)
    den = sqrt((sum1Sq-pow(sum1,2)/n)*(sum2Sq-pow(sum2,2)/n))
    if den == 0: return 0
    
    r = num/den
    return r

def topMatches(prefs, person, n=5, sim=sim_pearson):
    """Returns the best matches"""
    scores = [(sim(prefs, person, other),other) 
                for other in prefs if other != person]
    
    scores.sort()
    scores.reverse()
    return scores[0:n]