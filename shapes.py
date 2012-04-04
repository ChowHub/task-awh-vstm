from psychopy import data
import random
import math

participantNum = 9


def genPos(numStims, constraint, boxHor, boxVer, threshold = None):
    posList = []
    if not threshold: threshold = math.ceil(numStims / 4)              #stims distributed evenly through quadrants
    for ii in range(numStims):
        tooClose = True                 #Start loop
        while tooClose:
            tooClose = False            #Assume the best
            newpos = (random.random()*boxHor - (boxHor/2), random.random()*boxVer - (boxVer/2))         #new random pos
            for otherpos in posList:                                                                                                      #compare to other positions
                if distance(newpos, otherpos) < constraint: tooClose = True                                              #redraw if too close
            quad = [quadrant(pos) for pos in posList]
            if quad.count(quadrant(newpos)) == threshold: tooClose =  True               #fails constraint 

        posList.append(newpos)
    return posList

def quadrant(pos):
    if pos[0] >= 0 <= pos[1]: return 1          #top-right
    if pos[0] < 0 < pos[1]: return 2            #top-left
    if pos[0] < 0 > pos[1]:  return 3           #bottom-left
    if pos[0] >= 0 > pos[1]: return 4           #bottom-right

def addConstraints(newpos, posList, threshold = 1):
    quad = [quadrant(pos) for pos in posList]
    if quad.count(quadrant(newpos)) == threshold: return True               #fails constraint 
def distance(posA, posB):
    diffs = [(coordA - coordB)**2 for coordA,coordB in zip(posA, posB)]
    return sum(diffs)**(1./2)



def sampleShapes(SQUARES, OVALS, k, uniquesquares, uniqueovals, randomdraw = True):
    stims = random.sample(SQUARES, uniquesquares)
    stims.extend(random.sample(OVALS, uniqueovals))
    if randomdraw: 
        toDraw = max(k-(uniquesquares + uniqueovals), 0)
        drawFrom = SQUARES+OVALS
        #maxEle_ii = len(drawFrom)-1
        #stims.extend([drawFrom[random.randint(0, maxEle_ii)] for round in range(toDraw)])
        while len(stims) < k:
            newdraw = random.sample(drawFrom, 1)
            if stims.count(newdraw) == 2: continue
            else: stims.extend(newdraw)
        return stims
    elif k % (uniquesquares + uniqueovals) == 0:
        stims = stims*(k / (uniquesquares + uniqueovals))
        random.shuffle(stims)
        return stims
    else: raise
def sampleColors(stims, k, repeats):
    sampled = []
    while len(sampled) < k:
        newdraw = stims[random.randint(0, len(stims)-1)]
        if sampled.count(newdraw) == repeats: continue
        else: sampled.append(newdraw)
    return sampled


def genTrials(blockNum, shape_trials, shape_lures, col_trials, col_lures, num_stims, min_dist, grid_size, participantNum):
    selection = (blockNum%3)*2 if (type(blockNum) == int) else (0)
    SQUARES = ['M', 'N', 'O', 'P', 'Q', 'R'][selection:selection+2]
    OVALS = ['A','B','C','D','E','F'][selection:selection+2]
    COLORS = ['red', 'blue', 'green', 'yellow', 'black', 'white']
    trialList = []

    for ttlStims in num_stims:
        luresLeft = {'shapes':shape_lures, 'colors':col_lures}
        stimsDict = {'shapes':SQUARES + OVALS, 'colors': COLORS}
        trialType = ['shapes']*shape_trials + ['colors']*col_trials
        for trial in trialType:
            posList = genPos(ttlStims, min_dist, grid_size[0], grid_size[1]) 
            if trial == 'shapes': 
                stims = sampleShapes(SQUARES, OVALS, ttlStims, 1, 1)
            else: stims = sampleColors(COLORS, ttlStims, repeats = 2)
            probeNum = random.randint(0, ttlStims - 1)              #probe num
            if luresLeft[trial] > 0:
                luresLeft[trial] = luresLeft[trial] - 1
                luresList = [item for item in stimsDict[trial] if item != stims[probeNum]]
                probe = random.sample(luresList, 1)[0]
            else: probe = stims[probeNum]
            d = dict([('stim%s'%ii, val) for ii, val in enumerate(stims)])
            print probe, '\t', probeNum, '\t', stims[probeNum]
            d.update( [('Subject', participantNum), ('block',str(blockNum)), ('stim.probe', probe), ('corr.num', probeNum), ('stim.corr', stims[probeNum]), ('match', probe == stims[probeNum]), ('trial.type', trial), ('ttl.stims', ttlStims)] )
            d.update([('stim.pos%s'%ii , pos) for ii, pos in enumerate(posList)])               #clunky but python2.6 compatible
            trialList.append(d)
    return trialList
    
Blocks = 9
######
#trials per block
shape_trials = 8#16               #per set size
shape_lures = 8#8                 #per set size
col_trials = 0#8                     #"
col_lures = 0#4
num_stims = [4]

min_dist = 4
grid_size = (17.5, 17.5)
#test trials
trialLists = [genTrials(ii, shape_trials, shape_lures, col_trials, col_lures, num_stims, min_dist, grid_size, participantNum = participantNum) for ii in range(Blocks)]
#practice trials
pracList = genTrials('Practice', 4, 2, 0, 0, [4, 8], min_dist, grid_size, participantNum = participantNum)


taskTrials = [data.TrialHandler(trialLists[ii], 1) for ii in range(len(trialLists))]
for handlerNum in range(len(trialLists)):
    taskTrials[handlerNum].data.addDataType('resp')
    taskTrials[handlerNum].data.addDataType('RT')
pracTrials = data.TrialHandler(pracList, 1)
pracTrials.data.addDataType('resp')
pracTrials.data.addDataType('RT')

