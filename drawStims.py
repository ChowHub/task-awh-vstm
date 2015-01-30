from psychopy import visual, event, core, data
from shapes import taskTrials, pracTrials, pracList
import random

win = visual.Window(fullscr = True, units = 'deg', color='lightgrey', monitor = 'testMonitor')
win.setRecordFrameIntervals()
mouse = event.Mouse(win = win)
mouse.setVisible(False)
refresh_HZ = 60
refresh_rate = 1./refresh_HZ
frameMargin = 2*10**(-3)
pre_flip_time = refresh_rate - frameMargin 
#upper bound for view times (will subtract one frame from time ans
fixation_on_time =  .75 - pre_flip_time
fixation_off_time =  .25 - pre_flip_time
view_stims_time =  .5  - pre_flip_time
stims_memory_time =  1.  - pre_flip_time



font_dir = 'circle_square.otf'
font_name = 'Circle_Square'

#
textStims =  [visual.PatchStim(win, tex = 'stims/A.png', size = (2.5,1.75), mask = None, interpolate = False) for ii in range(10)]
rectStims = [visual.Rect(win, height = 1.5, width = 1.5, lineWidth = 1, interpolate = False) for ii in range(10)]

#range will be 17.5 x 17.5 degrees

SQUARES = ['M', 'N', 'O', 'P', 'Q', 'R']
OVALS = ['A','B','C','D','E','F']


def drawStims(win, stims, posList, textStims, rectStims, loadOnly = False):
    if type(stims) == str: stims = [stims]
    for ii, stim in enumerate(stims):
        if len(stim) == 1: 
            textStims[ii].draw()
        else:  
            rectStims[ii].draw()

def loadStims(win, stims, posList, textStims, rectStims, loadOnly = False):
    if type(stims) == str: stims = [stims]
    for ii, stim in enumerate(stims):
        if len(stim) == 1: 
            textStims[ii].setPos(posList[ii])
            if stim in OVALS: textStims[ii].setSize((2.5, 2.5))
            else: textStims[ii].setSize((2.5,2.5))
            textStims[ii].setTex('stims/'+stim+'.png')
            #print stims
            #print(stim in OVALS)
        else:  
            rectStims[ii].setFillColor(stim)
            rectStims[ii].setLineColor(stim)
            rectStims[ii].setPos(posList[ii])
    
def switchPos(itemStim, foilStim):
    '''pure convenience function.  Switches positions from item to foil'''
    foilStim.setpos(itemStim.pos)

def drawProbe(stim):
    stim.draw()

def drawFixation(fixationStim):
    fixationStim.draw()

def waitScreen(win, myMouse, maxViewingTime = 100000, lastTime = 0, onClick = True):
    '''Either waits for a mouse click or until maxViewingTime has elapsed'''
    done = False
    clock = core.Clock()
    myMouse.clickReset()
    lastTime = myMouse.getPressed(getTime=True)[1][0]
    while not done:
        click, time = myMouse.getPressed(getTime=True)
        if onClick and click[0] and time[0] != lastTime:
            done = True
            lastTime = time[0]
        if clock.getTime() > maxViewingTime: return lastTime
    return lastTime
    
def waitResponse(maxWait = None, clock = None, reset = True, keyList = ['z', 'slash']):
    if not clock:
        clock = core.Clock()
    if reset: clock.reset()
    event.clearEvents()
    needResp = True
    while needResp:
        keys = event.getKeys(keyList, timeStamped = True)
        if keys:
            needResp = False
    return keys[0][0], clock.getTime()    #resp, rt

def flipandwait(win, clock=None, viewTime=1):
        if not clock: clock = core.Clock()
        win.flip()
        clock.reset()
        while clock.getTime() < viewTime: pass 

from psychopy import visual
def instructions(pracTrials):
    text_1 = '''In this task, items will be presented in different locations on the screen.

Your job is to remember the items presented on the screen, as well as their location.

Items will be shapes with different patterns inside of them.


Hit spacebar to continue'''
    text_2 = '''
Hit spacebar for a slowed-down example of seeing the colored squares
'''
    text_3 = '''
Hit spacebar for see a slowed-down example of seeing the shapes
'''

    text_4 = '''
After seeing some items, a single test item will appear on screen.

The test item will be in the same position as one of the previous items. 

Do your best to identify whether the previous item from that position matches the test item.

Mismatches may be different shapes, or the inside of the shape may be different.

Press the 'Z' key if they match
Press the '/' key if they are different

Hit spacebar to practice the task
'''

    text_5 = '''
In the actual task, the items will be presented more quickly

Hit spacebar to practice the actual task
'''

    text_6 = '''
Now you will begin the actual task.

If you have any questions, please ask the experimenter now.

Hit spacebar to continue to the actual task'''
    textStims = [visual.PatchStim(win, tex = 'stims/A.png', size = (2.5,1.75), mask = None, interpolate = False) for ii in range(5)]
    rectStims = [visual.Rect(win, height = 1.5, width = 1.5, lineWidth = 1, interpolate = False) for ii in range(5)]
    Text = visual.TextStim(win, text = text_1, color = "black", wrapWidth = 25)
    examplePos1 = [(-2.8, -5.8),
                                (2.3, -3.9),
                                (8.5, 0.4),
                                (-1.7, 0.8)]
    examplePos2 = [(7.2, -3.9),
                                (0.8, 0.2)]
    Text.setAutoDraw(True)
    flipandwait(win, viewTime = 4)
    waitResponse(maxWait = None, clock = None, reset = True, keyList = ['space'])
    Text.setAutoDraw(False)
    #Examples of item presentation
    #loadStims(win, ['black', 'red', 'yellow', 'green'], examplePos1, textStims, rectStims)
    #drawStims(win, ['black', 'red', 'yellow', 'green'], examplePos1, textStims, rectStims)
    #flipandwait(win, viewTime = 1.5)
    Text.setText(text_3)
    Text.draw()
    flipandwait(win, viewTime = .5)
    waitResponse(maxWait = None, clock = None, reset = True, keyList = ['space'])
    loadStims(win, ['A', 'B', 'P','Q'], examplePos1, textStims, rectStims)
    drawStims(win, ['A', 'B', 'P', 'Q'], examplePos1, textStims, rectStims)
    flipandwait(win, viewTime = 4)
    #Run-through a full example
    Text.setText(text_4)
    Text.draw()
    flipandwait(win, viewTime =  3)
    waitResponse(maxWait = None, clock = None, reset = True, keyList = ['space'])
    repeat = True
    #Small change example
    while repeat:
        resp, rt = runTrial(win, core.Clock(), ['A','B'], examplePos2, ['B'], [examplePos2[0]], 
                            fixationStim = None, fixation_on_time = .75, fixation_off_time = .25,
                            view_stims_time = 1.5, stims_memory_time = .5, header = True)
        Text.setText("This was a SMALL change")
        Text.draw()
        flipandwait(win, viewTime = 3)
        if resp in ['slash']: repeat = False
    #Large change example
    repeat = True
    while repeat:
        resp, rt = runTrial(win, core.Clock(), ['A','B'], examplePos2, ['P'], [examplePos2[1]], 
                            fixationStim = None, fixation_on_time = .75, fixation_off_time = .25,
                            view_stims_time = 1.5, stims_memory_time = .5, header = True)
        Text.setText("This was a LARGE change")
        Text.draw()
        flipandwait(win, viewTime = 3)
        if resp in ['slash']: repeat = False
#No change example
    repeat = True
    while repeat:
        resp, rt = runTrial(win, core.Clock(), ['P','B'], examplePos2, ['B'], [examplePos2[1]], 
                            fixationStim = None, fixation_on_time = .75, fixation_off_time = .25,
                            view_stims_time = 1.5, stims_memory_time = .5, header = True)
        Text.setText("There was NO CHANGE")
        Text.draw()
        flipandwait(win, viewTime = 3)
        if resp in ['z']: repeat = False
#Practice
    #Text.setText(text_5)
    #Text.draw()
    #flipandwait(win, viewTime = 1)
    #waitResponse(maxWait = None, clock = None, reset = True, keyList = ['space'])
    Text.setText(text_6)
    Text.draw()
    flipandwait(win, viewTime = 1)
    waitResponse(maxWait = None, clock = None, reset = True, keyList = ['space'])
    
def runTrial(win, rtClock, stims, posList, probeItem, probePos, 
                    fixationStim = None, fixation_on_time = .75, fixation_off_time = .25,
                    view_stims_time = .5, stims_memory_time = 1, header = True):
    if not fixationStim: fixationStim = visual.TextStim(win, text = '+', color = 'black')
    loadStims(win, stims, posList, textStims, rectStims)       
    #FIXATION
    drawFixation(fixationStim)              #fixation on
    flipandwait(win, rtClock, fixation_on_time)
    flipandwait(win, rtClock, fixation_off_time)     #fixation off
    #STIMULI
    loadStims(win, stims, posList, textStims, rectStims)       
    drawStims(win, stims, posList, textStims, rectStims)       
    flipandwait(win, rtClock, view_stims_time)
    #INTER-RESPONSE INTERVAL
    flipandwait(win, rtClock, stims_memory_time)
    #CHANGE DETECTION TEST
    loadStims(win, probeItem, probePos, textStims, rectStims)
    drawStims(win, probeItem, probePos, textStims, rectStims)
    win.flip()
    resp, rt = waitResponse(clock = rtClock)
    return resp, rt


def runTask(taskTrials, append = True, header = True):
    rtClock = core.Clock()
    frameClock = core.Clock()
    fixationStim = visual.TextStim(win, text = '+', color = 'black')
    for thisTrial in taskTrials:
        posList = [thisTrial['stim.pos%s'%ii] for ii in range(thisTrial['ttl.stims'])]
        stims = [thisTrial['stim%s'%ii] for ii in range(thisTrial['ttl.stims'])]
        resp, rt = runTrial(win, rtClock, stims, posList, thisTrial['stim.probe'], [posList[thisTrial['corr.num']]],
                                    fixationStim, fixation_on_time, fixation_off_time, view_stims_time, stims_memory_time, header)

        taskTrials.data.add('resp', resp)
        taskTrials.data.add('RT', rt)
        core.wait(1)
    taskTrials.saveAsWideText('data/all', appendFile = append, matrixOnly = True) 
    taskTrials.saveAsWideText('data/' + str(thisTrial['Subject']), appendFile = append, matrixOnly = not header) 
    

instructions(pracTrials)
for trials in taskTrials:
    runTask(trials, header = False)


#runTrial(win, core.Clock(), ['A', 'B','C','D'], zip(range(-6, 6, 3), range(-6,6,3)), ['A'], (-6,-6))
