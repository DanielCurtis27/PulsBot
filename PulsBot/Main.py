from keras.models import load_model
from time import sleep
from selenium import webdriver
from selenium.webdriver.common.by import By
import sys
from PIL import Image, ImageOps
import re
import numpy as np

######GET TENSORFLOW TO WORK#######

# Disable scientific notation for clarity
np.set_printoptions(suppress=True)

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
    driver.get("https://pulsars.nanograv.org/psrsearch/surveys/AO327/plots/all")

def teachablemachine(modelname, modellabels, imageslocation):
    #use Teachable Machine model to see if it is noise or not. First open the file then fead it to TM
    # Load the model
    model = load_model("{}".format(modelname), compile=False)

    # Load the labels
    class_names = open("{}".format(modellabels), "r").readlines()

    # Create the array of the right shape to feed into the keras model
    # The 'length' or number of images you can put into the array is
    # determined by the first position in the shape tuple, in this case 1
    data = np.ndarray(shape=(1, 224, 224, 3), dtype=np.float32)

    image = Image.open("{}.png".format(imageslocation)).convert("RGB")

    # resizing the image to be at least 224x224 and then cropping from the center
    size = (224, 224)
    image = ImageOps.fit(image, size, Image.Resampling.LANCZOS)

    # turn the image into a numpy array
    image_array = np.asarray(image)

    # Normalize the image
    normalized_image_array = (image_array.astype(np.float32) / 127.5) - 1

    # Load the image into the array
    data[0] = normalized_image_array

    # Predicts the model
    prediction = model.predict(data)
    index = np.argmax(prediction)
    class_name = class_names[index]
    confidence_score = prediction[0][index]
    
    return class_name, confidence_score

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
    classnum = 0
    class_name, confidence_score = teachablemachine("models/DMvT.h5", "models/DMvTLabels.txt", fileloc)
    confidence_percent = confidence_score * 100
    #class_name = 'Pulsar' #placeholder
    if str(class_name.strip()) == 'Pulsar':
        classnum = 3
    elif str(class_name.strip()) == 'RFI':
        classnum = 2
    elif str(class_name.strip()) == 'Noise':
        classnum = 1
    print(classnum)
    #confidence_score = 100 #placeholder
    return classnum, confidence_percent

def PulsType(confidence, fileloc, grnoise):
    writetofile= open(fileloc, "w")

    driver.get("https://pulsars.nanograv.org/psrsearch/search") #temp
    sleep(1)

    if grnoise ==1:
        writetofile.write("[Noise] CONFIDENCE:{}%".format(confidence))

        notes = driver.find_element(By.ID,"plotid") #replace with the notes box
        notes.send_keys("[Noise] CONFIDENCE:{}% ANALYZED BY PULSBOT https://github.com/DanielCurtis27/PulsBot".format(confidence))
    
        submit = driver.find_element(By.ID,"plotid") #replace with proper submit button
        submit.click()

    elif grnoise==2: 
        writetofile.write("[RFI] CONFIDENCE:{}%".format(confidence))

        skip = driver.find_element(By.ID,"plotid") #replace with proper submit button
        skip.click()
    else: 
        writetofile.write("[Pulsar] CONFIDENCE:{}%".format(confidence))

        skip = driver.find_element(By.ID,"plotid") #replace with proper submit button
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