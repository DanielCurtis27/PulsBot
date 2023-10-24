import subprocess
#from time import sleep

fileNameUntrimmed = subprocess.run("find . -type f -wholename './pss/*singlepulse.ps'", capture_output =True, text = True, shell = True)
fileNameSortofTrimmed = fileNameUntrimmed.stdout.strip()
print(fileNameSortofTrimmed)
filesArray = fileNameSortofTrimmed.splitlines()
print(filesArray)
for i in range(len(filesArray)):
    fileNameTrimmed = filesArray[i]
    fileNameTrimmed = fileNameTrimmed.replace('.ps', '')
    fileNameTrimmed = fileNameTrimmed.replace('./pss/', '')
    subprocess.run("convert {} ./pngs/{}.png".format(filesArray[i], fileNameTrimmed), shell = True)
    #sleep(5)
    #print(fileNameTrimmed)