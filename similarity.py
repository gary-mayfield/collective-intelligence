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

def getRecommendations(prefs, person, similarity=sim_pearson):
    """Gets recommendations for a person by using a weighted 
    average of every other user's rankings"""
    totals = {}
    simSums = {}
    for other in prefs:
        # don't compare me to myself
        if other == person: continue
        sim = similarity(prefs, person, other)

        # ignore scores of zero or lower
        if sim <= 0: continue
        for item in prefs[other]:

            # only score movies I haven't seen yet
            if item not in prefs[person] or prefs[person][item] == 0:
                # Similarity * Score
                totals.setdefault(item, 0)
                totals[item] += prefs[other][item] * sim
                # Sum of similarities
                simSums.setdefault(item, 0)
                simSums[item] += sim
    
    # Create the normalized list
    rankings = [(total/simSums[item], item) for item, total in totals.items()]

    # Return the sorted list
    rankings.sort()
    rankings.reverse()
    return rankings

def transformPrefs(prefs):
    """Swap people and items in dictionary"""
    result = {}
    for person in prefs:
        for item in prefs[person]:
            result.setdefault(item,{})

            # Flip item and person
            result[item][person] = prefs[person][item]
    return result

def calculateSimilarItems(prefs, n=10):
    """Create a dictionary of items showing which other
    items they are most similar to"""
    result = {}

    # Invert the preference matrix to be item-centric
    ItemPrefs = transformPrefs(prefs)
    c = 0
    for item in ItemPrefs:
        # Status updates for large datasets
        c += 1
        if c%100 == 0: print("%d / %d" % (c, len(ItemPrefs)))
        # Find the most similar items to this one
        scores = topMatches(ItemPrefs, item, n=n, sim = sim_distance)
        result[item] = scores
    return result

def getRecommendedItems(prefs, itemMatch, user):
    """Item based recommendations"""
    userRatings = prefs[user]
    scores = {}
    totalSim = {}

    # Loop over items rated by this user
    for (item, rating) in userRatings.items():

        # Loop over items similar to this one
        for (similarity, item2) in itemMatch[item]:

            # Ignore if this user has already rated this item
            if item2 in userRatings: continue

            # Weighted sum of rating times similarity
            scores.setdefault(item2, 0)
            scores[item2] += similarity*rating

            # Sum of all the similarities
            totalSim.setdefault(item2, 0)
            totalSim[item2] += similarity
        
    # Divide each total score by total weighting to get an average
    rankings = [(score/totalSim[item], item) for item, score in scores.items()]

    # Return the rankings from highest to lowest
    rankings.sort()
    rankings.reverse()
    return rankings
