import pandas as pd

#############################################
# Initializing data for CSV column fields
#############################################
curEFR = 0
prevEFR = None

curTEMP = 0
prevTEMP = None

curMFD = 0
prevMFD = None

curBPH = 0
prevBPH = None

curSCFR = 0
prevSCFR = None

curMODE = 'N/A'

iteration = 0
count = 0

while count<10:

    #############################################
    #Updating array data frame
    #############################################
    
    #Current value arrays
    col1 = ['Current Value','Previous Value']
    frCol = [str(curEFR) + ' kg/s',str(prevEFR) + ' kg/s']
    tempCol = [str(curTEMP) + ' °F',str(prevTEMP) + ' °F']
    mfdCol = [str(curMFD) + ' mA',str(prevMFD) + ' mA']
    bphCol = [curBPH,prevBPH]
    scfrCol = [str(curSCFR) + ' kg/s',str(prevSCFR) + ' kg/s']
    modeCol = [curMODE]

    #History value arrays for first iteration (no previous data)
    if iteration == 0:
        frHist = ['N/A']
        tempHist = ['N/A']
        mfdHist = ['N/A']
        bphHist = ['N/A']
        scfrHist = ['N/A']
        modeHist = ['N/A']

        iteration += 1

    #############################################
    # Create a data frame
    #############################################
    guiData = ({'':col1,'EstimatedFR':frCol,'EstimatedTemp':tempCol,'EstimatedMFD':mfdCol,
    'EstimatedBPH':bphCol,'EstimatedSCFR':scfrCol,'Mode':modeCol,'FR History':frHist,
    'Temp History':tempHist,'MFD History':mfdHist,'BPH History':bphHist,'SCFR History':scfrHist,
    'Mode History':modeHist})

    df = pd.DataFrame.from_dict(guiData, orient='index')
    df.T.to_csv('Desktop/Capstone/Practice.csv')

    #############################################
    # Updating values for current, previous, and history
    #############################################

    prevEFR=curEFR
    prevTEMP=curTEMP
    prevMFD=curMFD
    prevBPH=curBPH
    prevSCFR=curSCFR

    #Inserting previous values to history array, allowing history to be updated
    frHist.insert(0,str(prevEFR) + ' kg/s')
    tempHist.insert(0,str(prevTEMP) + ' °F')
    mfdHist.insert(0,str(prevMFD) + ' mA')
    bphHist.insert(0,prevBPH)
    scfrHist.insert(0,str(prevSCFR) + ' kg/s')
    modeHist.insert(0,curMODE)

    #Update current values (default to incrementing by 1 for testing)
    curEFR+=1
    curTEMP+=1
    curMFD+=1
    curBPH+=1
    curSCFR+=1
    curMODE='Automatic'

    #############################################
    # Used for testing without an infinite loop
    #############################################
    count+=1

