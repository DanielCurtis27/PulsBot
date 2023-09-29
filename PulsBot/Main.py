#from kera smth import Tensorflow
from time import sleep
from selenium import webdriver
from selenium.webdriver.common.by import By
import sys
from PIL import Image
import re

scrapnumber = int(sys.argv[1])
graphnumber = 0


####
driver = webdriver.Firefox()

driver.get("https://www.geeksforgeeks.org/") #set real website :D
####

def getToDatabase(creds):
    #use credentials to get to the pulsar database to start the process
    return


def imagescrap(graphnumber):
    #use selenium to scrap for the time vs DM graph (if the entire image is stored as one thing then find out how to extract just the graph) and save it under the name "TvDM#"

    graph = driver.find_element(By.CLASS_NAME,"ant-input") #replace with proper class name
    
    filename = "TotalImage{}".format(graphnumber)

    graph.screenshot("NoiseImages/{}.png".format(filename))

def goToNextData():
    return


################################################################## NOISE (DMvT) Analyzing #############################################################

def candidate(graphnumber):
    #use selenium to find information about the pulsar incase it isn't noise

    pulsarinfo = driver.find_element(By.CLASS_NAME,"video-card-heading") #replace with proper class name
    
    filename = "NoiseDocs/PULSARINFO{}ORDERINGINFO".format(graphnumber)

    #if its embeded in the image, god help me

    writetofile= open(filename, "w")
    writetofile.write("{}".format(pulsarinfo))
    writetofile.close()

#grabs the DM vs Time graph 
def TrimImage(graphnumber):
    #use selenium to scrap for the DM vs Time graph (if the entire image is stored as one thing then find out how to extract just the graph) and save it under the name "DMvT#"

    uncropped = Image.open("NoiseImages/TotalImage{}.png".format(graphnumber))

    #from here if the graph is just one big image, trim it using PIL.
    
    filename = "DMvT{}.png".format(graphnumber)

    uncropped.save("NoiseImages/{}".format(filename),"png")


#analyzes the DM vs Time graph using Teachable Machine to see what it likely is.
def TypeOfNoise(fileloc):
    
    #use Teachable Machine model to see if it is noise or not. First open the file then fead it to TM

    isNoise = 2
    confidence = 100
    return isNoise, confidence

def PulsType(confidence, fileloc, grnoise):
    writetofile= open(fileloc, "w")

    if grnoise ==1:
        writetofile.write("[Noise] CONFIDENCE:{}%".format(confidence))

        notes = driver.find_element(By.CLASS_NAME,"ant-input") #replace with the notes box
        notes.send_keys("[Noise] CONFIDENCE:{}% ANALYZED BY PULSBOT https://github.com/DanielCurtis27/PulsBot".format(confidence))
    
        submit = driver.find_element(By.CLASS_NAME,"ant-btn") #replace with proper submit button
        submit.click()

    elif grnoise==2: 
        writetofile.write("[RFI] CONFIDENCE:{}%".format(confidence))

        skip = driver.find_element(By.CLASS_NAME,"ant-btn") #replace with proper submit button
        skip.click()
    elif grnoise==3: 
        writetofile.write("[Pulsar Candidate] CONFIDENCE:{}%".format(confidence))

        skip = driver.find_element(By.CLASS_NAME,"ant-btn") #replace with proper submit button
        skip.click()
    else: 
        writetofile.write("[Pulsar] CONFIDENCE:{}%".format(confidence))

        skip = driver.find_element(By.CLASS_NAME,"ant-btn") #replace with proper submit button
        skip.click()
    writetofile.close()

def Noise(graphnumber):
    with open("NoiseDocs/PULSARINFO{}".format(graphnumber), "r") as f:
        f= str(f.read())
        match = re.match(r'.*?\[(.*)].*',f)
        print(match.group(1))
    return match.group(1)



########################################################################################################################################################


####

getToDatabase(1)

####

def reloadgoofypage():
    driver.get("https://www.geeksforgeeks.org/")


for i in range(scrapnumber):
    imagescrap(graphnumber)

    #################### Noise (DMvsT) analysis #####################
    candidate(graphnumber)
    TrimImage(graphnumber)
    fileloc = "NoiseImages/DMvT{}".format(graphnumber)
    filedocloc = "NoiseDocs/PULSARINFO{}".format(graphnumber)
    grnoise, confidence = TypeOfNoise(fileloc)
    PulsType(confidence, filedocloc, grnoise)                          #1 is noise, 2 is RFI, 3 is pulsar-candidate, 4 is pulsar
    
    #slight note: There is a more than 0% chance an RFI will be considered a pulsar candidate or pulsar looking at DM vs T alone, but usually it can easily be detected later using Pulses vs DM

    #################################################################
    
    if Noise(graphnumber) != "Noise" and Noise(graphnumber) != "RFI":
        print("oof") #replace this with the PulsesvsDM section

    graphnumber+=1

    goToNextData() #real function to go to next page, currently does nothing
    reloadgoofypage() #testing function REMOVE LATER
    sleep(3)