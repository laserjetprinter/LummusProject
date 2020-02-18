import tkinter as tk
import pandas as pd
import datetime
import PIL
from PIL import ImageTk

#############################################
#Creates main GUI Window (mgui)
#############################################
mgui = tk.Tk(className=' Mass Flow Data') #Space between ' and Mass because it makes it lower case? lol
mgui.config(bg='black')

#Title characteristics
title = tk.Label(mgui, text='Mass Flow Rate Tools', width=60, borderwidth=2, relief="ridge")
title.config(font=("Arial",44), bg='lightblue')
title.pack()

#############################################
#Grabbing and storing CSV information
#############################################

def getData():
    print('In getData')
    
    df = pd.read_csv('Desktop/Capstone/Test.csv')

    esfr = df.EstimatedFR
    curEFR.config(text=esfr[0])
    prevEFR.config(text=esfr[1])

    estmp = df.EstimatedTemp
    curTEMP.config(text=estmp[0])
    prevTEMP.config(text=estmp[1])

    esmfd = df.EstimatedMFD
    curMFD.config(text=esmfd[0])
    prevMFD.config(text=esmfd[1])

    esbph = df.EstimatedBPH
    curBPH.config(text=esbph[0])
    prevBPH.config(text=esbph[1])

    esscfr = df.EstimatedSCFR
    curSCFR.config(text=esscfr[0])
    prevSCFR.config(text=esscfr[1])

    curMode = df.Mode
    modeCSV.config(text=curMode[0])

    #Every 2 seconds the GUI updates to reflect changes to the CSV file data
    mgui.after(2000, getData)

#############################################
#Frame to hold both Labels and CSV Data
#############################################
frame = tk.Frame(mgui, width=60, borderwidth=2, relief='ridge')
frame.pack()

#############################################
#Frame to hold Labels
#############################################
lFrame = tk.Frame(frame, width=30, borderwidth=2, relief="ridge")
lFrame.pack(side=tk.LEFT)

blank = tk.Label(lFrame, text=' ', width=30)
blank.config(font=("Arial",24), bg='black')
blank.pack()

estFR = tk.Label(lFrame, text='Estimated Flow Rate', width=30, borderwidth=2, relief="ridge")
estFR.config(font=("Arial",24), bg='lightblue')
estFR.pack()

estTemp = tk.Label(lFrame, text='Estimated Temperature', width=30, borderwidth=2, relief="ridge")
estTemp.config(font=("Arial",24), bg='lightblue')
estTemp.pack()

estMFD = tk.Label(lFrame, text='Estimated MFD Output', width=30, borderwidth=2, relief="ridge")
estMFD.config(font=("Arial",24), bg='lightblue')
estMFD.pack()

estBPH = tk.Label(lFrame, text='Estimated BPH', width=30, borderwidth=2, relief="ridge")
estBPH.config(font=("Arial",24), bg='lightblue')
estBPH.pack()

estSCFR = tk.Label(lFrame, text='Estimated Seed Cotton Feed Rate', width=30, borderwidth=2, relief="ridge")
estSCFR.config(font=("Arial",24), bg='lightblue')
estSCFR.pack()

#############################################
#Frame to hold current and prev labels
#############################################
rFrame = tk.Frame(frame, width=30, borderwidth=2, relief="ridge")
rFrame.pack(side=tk.TOP)

current = tk.Label(rFrame, text='Current Value', width=15, borderwidth=2, relief="ridge")
current.config(font=("Arial",24), bg='lightgreen')
current.pack(side=tk.LEFT)

prev = tk.Label(rFrame, text='Previous Value', width=15, borderwidth=2, relief="ridge")
prev.config(font=("Arial",24), bg='yellow')
prev.pack(side=tk.RIGHT)

#############################################
#Frames to hold CSV Data
#############################################
dCurFrame = tk.Frame(frame, width=15, borderwidth=2, relief="ridge")
dCurFrame.pack(side=tk.LEFT)

dPrevFrame = tk.Frame(frame, width=15, borderwidth=2, relief="ridge")
dPrevFrame.pack(side=tk.LEFT)

#############################################
#Estimated flow rate CSV
#############################################

curEFR = tk.Label(dCurFrame, text='0', width=15, borderwidth=2, relief="ridge")
curEFR.config(font=("Arial",24), bg='white')
curEFR.pack()

prevEFR = tk.Label(dPrevFrame, text='0', width=15, borderwidth=2, relief="ridge")
prevEFR.config(font=("Arial",24), bg='white')
prevEFR.pack()


#Estimated temperature CSV
curTEMP= tk.Label(dCurFrame, text='0', width=15, borderwidth=2, relief="ridge")
curTEMP.config(font=("Arial",24), bg='white')
curTEMP.pack()

prevTEMP = tk.Label(dPrevFrame, text='0', width=15, borderwidth=2, relief="ridge")
prevTEMP.config(font=("Arial",24), bg='white')
prevTEMP.pack()

#Estimated mass flow device output CSV
curMFD= tk.Label(dCurFrame, text='0', width=15, borderwidth=2, relief="ridge")
curMFD.config(font=("Arial",24), bg='white')
curMFD.pack()

prevMFD = tk.Label(dPrevFrame, text='0', width=15, borderwidth=2, relief="ridge")
prevMFD.config(font=("Arial",24), bg='white')
prevMFD.pack()

#Estimated bales per hour output CSV
curBPH= tk.Label(dCurFrame, text='0', width=15, borderwidth=2, relief="ridge")
curBPH.config(font=("Arial",24), bg='white')
curBPH.pack()

prevBPH = tk.Label(dPrevFrame, text='0', width=15, borderwidth=2, relief="ridge")
prevBPH.config(font=("Arial",24), bg='white')
prevBPH.pack()

#Estimated seed cotton flow rate output CSV
curSCFR= tk.Label(dCurFrame, text='0', width=15, borderwidth=2, relief="ridge")
curSCFR.config(font=("Arial",24), bg='white')
curSCFR.pack()

prevSCFR = tk.Label(dPrevFrame, text='0', width=15, borderwidth=2, relief="ridge")
prevSCFR.config(font=("Arial",24), bg='white')
prevSCFR.pack()

#############################################
#Blowbox image and Mode Type
#############################################
spaceFrame = tk.Frame(mgui, width=60, height=30)
spaceFrame.config(bg='black')
spaceFrame.pack()

modeFrame = tk.Frame(mgui, width=60, borderwidth=2, relief='ridge')
modeFrame.config(bg='black')
modeFrame.pack()

mode= tk.Label(modeFrame, text='Operation Mode:', width=15, borderwidth=2, relief="ridge")
mode.config(font=("Arial",24), bg='lightblue')
mode.pack(side=tk.LEFT)

modeCSV= tk.Label(modeFrame, text='N/A', width=15, borderwidth=2, relief="ridge")
modeCSV.config(font=("Arial",24), bg='white')
modeCSV.pack(side=tk.LEFT)

imageFrame = tk.Frame(mgui, width=60, borderwidth=2, relief='ridge')
imageFrame.config(bg='black')
imageFrame.pack(side=tk.BOTTOM)

bbImage = ImageTk.PhotoImage(file='Desktop/Capstone/blowbox.png')
test = tk.Label(imageFrame)
test.config(image=bbImage)
test.image=bbImage
test.pack(side=tk.BOTTOM)

getData()
mgui.mainloop()
