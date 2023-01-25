import urllib.request
import os
import threading
from PIL import Image
from colorama import Fore, Back, Style
import shutil

#images are 128x128
ChunkImageWidth = 128
ChunkImageHeight = 128

WorkSpacePath = os.path.dirname(os.path.realpath(__file__))
CreateFolder = "DynmapDownloaderCache"


#ADD REQUIMENTS THING FRIST THAT PYTHON SUPPORTS
#THEN AFTER THAT UPLOAD TO GITHUB

#user values
world = ""
viewMode = ""
ServerIP = ""
MapXChunk = 0
MapYChunk = 0
MapXChunkEnd = 10
MapYChunkEnd = 10
DeleteFolderOnFinish = True
SkipDownload = False
RetryDownloadAttempts = 3
OutputName = "map"

#a function to get user input
def GetInput(Text,Default,yesMode):
    Output = Default
    tempInput = input(Text)
    if yesMode == True:
        if tempInput == "y" or tempInput == "yes" or tempInput == "Yes" or tempInput == "Y":
            Output = True
        elif tempInput == "n" or tempInput == "no" or tempInput == "No" or tempInput == "N":
            Output = False
    elif not tempInput == "":
        Output = tempInput
    return Output



# config manuelly changing it
if True:
    print("")
    print(Fore.GREEN + Style.BRIGHT + "Ai Kiwi Dynamap downloader" + Style.RESET_ALL)
    print("If it gets stuck please just restart it. Thats my moto")
    print("")

    ServerIP = GetInput("server IP? (default nothing) (make sure to remove http part just raw ip) : ", "", False)
    world = GetInput("World to get (default : world, other DIM-1 or DIM1) : ", "world", False)
    viewMode= GetInput("View mode (default : flat, other t or nt) : ", "flat", False)
    MapXChunk = int(GetInput("Chunk x (default -10) : ", "-10", False))
    MapYChunk = int(GetInput("Chunk y (default -10) : ", "-10", False))
    MapXChunkEnd = int(GetInput("End chunk x (default 10) : ", "10", False))
    MapYChunkEnd = int(GetInput("End chunk y (default 10) : ", "10", False))
    SkipDownload = bool(GetInput("Only use cache (default no) : ", False, True))
    DeleteFolderOnFinish = bool(GetInput("Clear cache on end (default yes) : ", False, True))
    RetryDownloadAttempts = int(GetInput("Retry times (default 3) : ", 3, False))
    OutputName = GetInput("Output map name (default map) : ", "map", False)


#function to download a chunk
def DownloadChunk(Url,SaveLoc,AttemptNum):


    try:
        urllib.request.urlretrieve(Url, SaveLoc)
    except Exception:
        if AttemptNum <= RetryDownloadAttempts:
            DownloadChunk(Url,SaveLoc,AttemptNum+1)
        print(Fore.RED+"failed to get data ("+str(AttemptNum)+"x) : " + Url + Style.RESET_ALL)

    print(Fore.GREEN+"got data ("+str(AttemptNum)+"x) : " + Url + Style.RESET_ALL)
    return



#loop throw all chunks downloading
if not os.path.isdir(WorkSpacePath+"\\"+CreateFolder + "\\"):
    os.mkdir(WorkSpacePath+"\\"+CreateFolder + "\\")



threads = []
print("downloading image")
if SkipDownload == False:
    for chunkX in range(MapXChunk, MapXChunkEnd):
        for chunkY in range(MapYChunk, MapYChunkEnd):
            #so for some reason there is a regain area but it is never used. idk wht theres there in the frist place
            Url = "http://"+ServerIP+"/tiles/"+world+"/"+viewMode+"/0_0/" + str(chunkX) + "_" + str(chunkY) + ".jpg"
            
            SaveLoc = WorkSpacePath+"\\"+CreateFolder + "\\" + str(chunkX) + "_" + str(chunkY) + ".jpg"

            #create thread
            Thread = threading.Thread(target=DownloadChunk, args=(Url,SaveLoc,1))
            Thread.start()
            threads.append(Thread)

    print("finished starting all downloads")

    Line = 0
    for x in threads:
        Line = Line + 1
        print("waiting on thread : " + str(Line) + " of " + str(len(threads))) #, end='\r'
        x.join()


print("finished downloading")
print("creating image")

#create the image
img  = Image.new( mode = "RGB", size = (ChunkImageWidth * (MapXChunkEnd - MapXChunk ), ChunkImageHeight * (MapYChunkEnd - MapYChunk)) )

#loop through chunks
for chunkX in range(MapXChunk, MapXChunkEnd):
    for chunkY in range(MapYChunk, MapYChunkEnd):
        try:
            Loc = WorkSpacePath+"\\"+CreateFolder + "\\" + str(chunkX) + "_" + str(chunkY) + ".jpg"
            downlaodedImage = Image.open(Loc)
            img.paste(downlaodedImage, (img.size[0]-((MapXChunkEnd-chunkX)*ChunkImageWidth),((MapYChunkEnd-chunkY)*ChunkImageHeight)-ChunkImageHeight))
            print(Fore.GREEN+"Edited in : "+WorkSpacePath+"\\"+CreateFolder + "\\" + str(chunkX) + "_" + str(chunkY) + ".jpg" + Style.RESET_ALL)
        except Exception:
            print(Fore.RED+"Failed to edit in : "+WorkSpacePath+"\\"+CreateFolder + "\\" + str(chunkX) + "_" + str(chunkY) + ".jpg" + Style.RESET_ALL) 
            
print("all finished!")
img.show()
img.save(WorkSpacePath+"\\" + OutputName + ".jpg")

if DeleteFolderOnFinish == True:
    try:
        print(WorkSpacePath+"\\"+CreateFolder)
        shutil.rmtree(WorkSpacePath+"\\"+CreateFolder)
    except:
        pass

