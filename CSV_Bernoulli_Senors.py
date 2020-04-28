import pandas as pd
import smbus
import time
import board
import busio
import math 
i2c = busio.I2C(board.SCL, board.SDA)
import adafruit_ads1x15.ads1115 as ADS

from adafruit_ads1x15.analog_in import AnalogIn
ads = ADS.ADS1115(i2c)
bus = smbus.SMBus(1)

#############################################
# Initializing data for CSV column fields
#############################################

Q2, prevQ2 = 0, None
vout, prevvout = 0, None
mrate, prevmrate= 0, None
pinMetric, prevpinMetric = 0, None
mratebat, prevmratebat = 0, None
fEng, prevfEng = 0, None
Nre, prevNre = 0, None
pinEng, prevpinEng = 0, None
temp, prevtemp = 0, None
pressure1, prevpressure1 = 0, None
pressure2, prevpressure2 = 0, None

iteration = 0
count = 0

while True:
    ############################################
    #Updating array data frame
    #############################################

    #Current value arrays
    col1 = ['Current Value','Previous Value']
    Q2Col = [str(Q2),str(prevQ2)]               #Units?
    voutCol = [str(vout),str(prevvout)]         
    mrateCol = [str(mrate),str(prevmrate)]
    pinMetricCol = [str(pinMetric),str(prevpinMetric)]
    mratebatCol = [str(mratebat),str(prevmratebat)]
    fEngCol = [str(fEng),str(prevfEng)]
    NreCol = [str(Nre),str(prevNre)]
    pinEngCol = [str(pinEng),str(prevpinEng)]
    tempCol = [str(temp),str(prevtemp)]
    pressure1Col = [str(pressure1),str(prevpressure1)]
    pressure2Col = [str(pressure2),str(prevpressure2)]

    #History value arrays for first iteration (no previous data)
    if iteration == 0:
        Q2Hist = ['N/A']
        voutHist = ['N/A']
        mrateHist = ['N/A']
        pinMetricHist = ['N/A']
        mratebatHist = ['N/A']
        fEngHist = ['N/A']
        NreHist = ['N/A']
        pinEngHist = ['N/A']
        tempHist = ['N/A']
        pressure1Hist = ['N/A']
        pressure2Hist = ['N/A']

        iteration += 1

    #############################################
    # Create a data frame and write to CSV file
    #############################################
    guiData = ({'':col1,'Q2 Output':Q2Col,'vout Output':voutCol,'mrate Output':mrateCol,
    'pinMetric Output':pinMetricCol,'mratebat Output':mratebatCol,'fEng Output':fEngCol, 'Nre Output':NreCol,
    'pinEng Output':pinEngCol,'Temperature Output':tempCol,'Pressure Sensor 1 Output':pressure1Col,
    'Pressure Sensor 2 Output':pressure2Col,'Q2 History':Q2Hist,'vout History':voutHist,'mrate History':mrateHist,
    'pinMetric History':pinMetricHist,'mratebat History':mratebatHist,'fEng History':fEngHist,
    'Nre History':NreHist,'pinEng History':pinEngHist,'Temperature History':tempHist,'Pressure Sensor 1 History':pressure1Hist,
    'Pressure Sensor 2 History':pressure2Hist})

    df = pd.DataFrame.from_dict(guiData, orient='index')
    df.T.to_csv('/home/pi/Desktop/Capstone/Practice.csv')
    
    #############################################
    # Updating values for current, previous, and history
    #############################################

    prevQ2=Q2
    prevvout = vout
    prevmrate = mrate
    prevpinMetric = pinMetric
    prevmratebat = mratebat
    prevfEng = fEng
    prevNre = Nre
    prevpinEng = pinEng
    prevtemp = temp
    prevpressure1 = pressure1
    prevpressure2 = pressure2

    #Inserting previous values to history array, allowing history to be updated
    Q2Hist.insert(0,str(prevQ2))        #Units?
    voutHist.insert(0,str(prevvout))
    mrateHist.insert(0,str(prevmrate))
    pinMetricHist.insert(0,str(prevpinMetric))
    mratebatHist.insert(0,str(prevmratebat))
    fEngHist.insert(0,str(prevfEng))
    NreHist.insert(0,str(prevNre))
    pinEngHist.insert(0,str(prevpinEng))
    tempHist.insert(0,str(prevtemp))
    pressure1Hist.insert(0,str(prevpressure1))
    pressure2Hist.insert(0,str(prevpressure2))

    #Update current values ... read from pressure and temp sensors
    data = [0xC4,0x83]
    bus.write_i2c_block_data(0x48, 0x01, data)
    time.sleep(0.5)

    data = bus.read_i2c_block_data(0x48, 0x00, 2)
    raw_adc = data[0] * 256 + data[1]

    if raw_adc > 32767:
	    raw_adc -= 65535
    pressure1 = 14.7+((raw_adc/65535)*16)	#converting gage pressure to PSIa
    print("Pressure1 : %d" % pressure1)

    data = [0xE4, 0x83]
    bus.write_i2c_block_data(0x48, 0x01, data)
    time.sleep(0.5)

    data = bus.read_i2c_block_data(0x48, 0x00, 2)
    raw_adc = data[0] * 256 + data[1]

    if raw_adc > 32767:
        raw_adc -= 65535
    pressure2 = 14.7+((raw_adc / 65535)*16)
    print("Pressure2 : %d" % pressure2)

    #assuming 230 degrees f as a constant
    temp = 230

    #############################################
    # Metric equations and variables
    #############################################

    #Constants found before testing. Default value set to 1 for debugging
    App = 0.0001         #Area of gap between plunger and pipe (m^2)
    AMetric = 0.002025     #Cross sectional area of pipe (m^2)
    cMetric = 14.592     #Maximum seed cotton velocity (m/s)
    vbbMetric = 18.24   #air velocity through the blowbox (m/s)
    ksMetric = 1.05    #Friction loss factor for seed cotton through blowbox
    vinMetric = 22.8   #measured air velocity at blowbox inlet (m/s)
    
    RMetric = 287.058       #Gas constant (J/kg-K)
    Patm = 101325           #Atmospheric pressure in Pascals
    pstarMetric = 1.23    #Density of higher-pressure air (kg/m^3) ... assuming equal to Patm

    P1Metric = pressure1 * 6895             #Pressure sensor reading of air before mixture in Pascals
    P2Metric = pressure2 * 6895             #Pressure sensor reading of cottain air mixture in Pascals 
    T1Metric = (temp - 32) * (5/9) + 273.15 #Temperature converted to Kelvin

    ###################
    # Equation 7 in metric units
    # Calculates air density at the blowbox inlet (kg/m^3) ... temperature in kelvin
    ###################
    pinMetric = (RMetric * T1Metric)/P1Metric

    ###################
    # Equation 2a and 2b in metric units
    ###################
   
    vout = math.sqrt((2)*abs(Patm - P1Metric) / (pinMetric))

    Q2 = App * vout

    ###################
    # Equation 3 in metric units
    # Calculates our mass flow rate
    ###################

    part1 = (AMetric / ((cMetric/vbbMetric) + (ksMetric/2)))
    part2 = ((P2Metric -P1Metric) / (vinMetric + (Q2/AMetric))) - ((ksMetric/2) * (pinMetric * vinMetric)) + ((ksMetric/2) * (Q2/AMetric) * pstarMetric)
    mrate = part1 * part2

    #############################################
    # English equations and variables
    #############################################
    
    #Constants found before testing. Default value set to 1 for debugging
    di = 0.167          #Inner diameter (ft)
    L = 3.21           #Equivalent length (ft)
    V1 = 74.8          #Velocity of air (ft/s)
    AEng = 0.0218        #Area of cross section of inner pipe (ft^2)
    KEng = 1.05        #Friction Factor Multiplier (unitless)
    u1 = 0.0000003737          #Viscosity of air (lb/ft-s)
    
    REng = 53.3533  #Gas Constant (ft-lbf/lb-R)

    P1Eng = pressure1 * 144       #Pressure sensor reading of air before mixture in lbs per sqft
    P2Eng = pressure2 * 144       #Pressure sensor reading of cottain air mixture in lbs per sqft
    T1Eng = temp + 459.67         #Temperature converted to Rankine

    ###################
    # Equation 7 in English units
    ###################

    pinEng = (REng*T1Eng)/P1Eng

    ###################
    # Equation 6: Reynold's Number
    ###################

    Nre = (di * V1 * pinEng)/u1

    ###################
    # Equation 5: Fanning Friction Factor
    ###################

    part1 = math.log10((0.00015/(3.7*di)) + (7/Nre))
    part2 = math.pow(part1,2)
    fEng = 0.331/part2

    ###################
    # Equation 4: Second Mass Flow Rate Equation
    ###################

    denomenator = (9273.6*di) * ((0.8 * math.pow(V1,2) * AEng *pinEng) + (18547.2 * fEng * L * pinEng * math.pow(V1,2) * KEng * AEng))
    numerator = ((P2Eng - P1Eng)*(9273.6*di) - 4 * fEng * L * pinEng * math.pow(V1,2)) * (4636.8 * math.pow(AEng,2) * V1 * pinEng)
    mratebat = numerator / denomenator
