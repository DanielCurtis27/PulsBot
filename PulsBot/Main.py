#from kera smth import Tensorflow
from time import sleep
from selenium import webdriver
from selenium.webdriver.common.by import By
import sys
from PIL import Image
import re
import numpy as np

scrapnumber = int(sys.argv[1])
username = str(sys.argv[2])
password = str(sys.argv[3])

graphnumber = 0


####
driver = webdriver.Firefox()

driver.get("https://pulsars.nanograv.org/login?authenticator=orcid&return=Lw==")
####

def getToDatabase(creds = np.array):
    #use credentials to get to the pulsar database to start the process
    sleep(1)
    cookies = driver.find_element(By.ID, "onetrust-reject-all-handler")
    cookies.click()
    sleep(.5)
    username = driver.find_element(By.ID, "username")
    username.send_keys(creds[0])
    password = driver.find_element(By.ID, "password")
    password.send_keys(creds[1])
    sleep(1)
    login = driver.find_element(By.ID, "signin-button")
    login.click()
    sleep(10)
    driver.get("https://pulsars.nanograv.org/psrsearch/surveys/AO327/plots/all")
    #get certified to start accessing database data


def imagescrap(graphnumber):
    #use selenium to scrap for the time vs DM graph (if the entire image is stored as one thing then find out how to extract just the graph) and save it under the name "TvDM#"

    graph = driver.find_element(By.CLASS_NAME,"dataTables_length") #replace with proper class name
    
    filename = "TotalImage{}".format(graphnumber)

    graph.screenshot("NoiseImages/{}.png".format(filename))

def goToNextData():
    return


################################################################## NOISE (DMvT) Analyzing #############################################################

def candidate(graphnumber):
    #use selenium to find information about the pulsar incase it isn't noise

    pulsarinfo = driver.find_element(By.CLASS_NAME,"dataTables_length") #replace with proper class name
    
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

        notes = driver.find_element(By.CLASS_NAME,"dataTables_length") #replace with the notes box
        notes.send_keys("[Noise] CONFIDENCE:{}% ANALYZED BY PULSBOT https://github.com/DanielCurtis27/PulsBot".format(confidence))
    
        submit = driver.find_element(By.CLASS_NAME,"dataTables_length") #replace with proper submit button
        submit.click()

    elif grnoise==2: 
        writetofile.write("[RFI] CONFIDENCE:{}%".format(confidence))

        skip = driver.find_element(By.CLASS_NAME,"dataTables_length") #replace with proper submit button
        skip.click()
    elif grnoise==3: 
        writetofile.write("[Pulsar Candidate] CONFIDENCE:{}%".format(confidence))

        skip = driver.find_element(By.CLASS_NAME,"dataTables_length") #replace with proper submit button
        skip.click()
    else: 
        writetofile.write("[Pulsar] CONFIDENCE:{}%".format(confidence))

        skip = driver.find_element(By.CLASS_NAME,"dataTables_length") #replace with proper submit button
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

getToDatabase([username, password])

####



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
    sleep(3)