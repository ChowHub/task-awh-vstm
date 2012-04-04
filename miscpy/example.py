from psychopy import visual, core
import os

os.getcwd()
font_dir = 'circle_square.otf'              #may need to change this to point to font
font_name = 'circle_square'
letters = ['A', 'B', 'C', 'D', 'E', 'F']

win = visual.Window()
textStims = [ visual.TextStim(win, text = letters[ii], bold = True,  fontFiles = [font_dir], font = 'Circle_Square', height = .1 + ii/10. , color = 'black', pos = (-.5+ ii/(5.), -.5+ ii/(5.))) for ii in range(5) ]
for stim in textStims: stim.draw()
win.flip()
core.wait(5)