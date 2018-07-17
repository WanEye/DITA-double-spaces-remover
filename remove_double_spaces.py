'''
Created on Jul 13, 2018

@author: ywaney
'''
      
import re
import os


def R20initDITAfile(DITAfile):
    routine = "R20: "
    R99writeLog(routine)
    #
    global global_DITAcontent
    DITA = open(DITAfile, 'r')
    global_DITAcontent = DITA.read()
    DITA.close()
    
    return 

    
def R25procDITA(content):
    routine = "R25: "
    R99writeLog(routine)
    #
    global global_DITAcontent
    
    # remove spaces between words
    regex = ".\s{2,}."    
    contentNew = re.findall(regex, content)

    for occurence in contentNew:
        lengthStr = len(occurence)
        lengthStr = lengthStr - 1
        content = content.replace(occurence[1:lengthStr],  " " ) 
        
    # remove space between text and opening tag
#     regex = "[^>]\s+."
#     contentNew = re.findall(regex, content)
#     
#     for occurence in contentNew:
#         lengthStr = len(occurence)
#         lengthStr = lengthStr - 1
#         content = content.replace(occurence[1:lengthStr],  "" ) 
#     
    # remove spaces between word and interpunction
    # a few interpunction characters need an escape character    

    pt = "."
    regex = "\s+\."
    content = re.sub(regex, pt, content)
     
      
    pt = ":"
    regex = "\s+" + pt
    content = re.sub(regex, pt, content)
         
    pt = ","
    regex = "\s+" + pt
    content = re.sub(regex, pt, content)
   
    pt = ";"
    regex = "\s+" + pt
    content = re.sub(regex, pt, content)
       
    pt = "!"
    regex = "\s+" + pt
    content = re.sub(regex, pt, content)
           
    pt = "?"
    regex = "\s+\?"
    content = re.sub(regex, pt, content)
    
    # remove spaces between tag and next word if the preceding position is a space
    regex = ".\s+<\w+>\s+"
    contentNew = re.findall(regex, content)
    
    for occurence in contentNew:
        content = content.replace("> ", ">")
    
    global_DITAcontent = content
    
    return
    
def R29writeDITAfile(DITAfile, newContent):
    routine = "R29: "
    R99writeLog(routine)
    #
    DITA = open(DITAfile, 'w')
    DITA.write(newContent)
    print "Processed: " + DITAfile
    DITA.close
    
    return
     

def R10AgetDITAfiles():
    routine = "R10A: "
    R99writeLog(routine) 
    #
    """
    Determine the current directory.
    Get all .dita files with full path in the current directory and subdirectories.
    Put all these .dita files in list global_fileList    
    """
    #
    global global_current_Dir
    global global_filesList
    global_filesList = []
    
    global_current_Dir = os.getcwd()
    print "directory in process: " + global_current_Dir
    
    for dirpath, dirnames, filenames in os.walk(global_current_Dir):
        for filename in [f for f in filenames if f.endswith(".dita")]:
            DITAfile = os.path.join(global_current_Dir, dirpath, filename)
            global_filesList.append(DITAfile)
            
    return
       
    
def R10initPrg():
    routine = "R10: "
    R99writeLog(routine)
    #
    global LOGFILE
    
    LOGFILE = open('logFile.txt', 'w')
    R99writeLog('Remove double spaces')
    R10AgetDITAfiles()
    
    return
     
def R19finPrg():
    routine = 'R19: ' 
    R99writeLog(routine) 
    #  
    """
    Notify the user that the program is ready.
    """
    LOGFILE.close()
    #
    print ("removed double spaces from DITA files in" + global_current_Dir)
    print "The End"
    return


def R99writeLog(Msg):
    with open("logfile.txt", "a") as LOGFILE:
        LOGFILE.write(Msg + "\n")
    return

    
def R00Main():
    routine = "R00: "
    global global_newContent
    global_newContent = ''
    R10initPrg()
    for DITAfile in global_filesList:
        R20initDITAfile(DITAfile)
        R25procDITA(global_DITAcontent)
        R29writeDITAfile(DITAfile, global_DITAcontent)
    R19finPrg()
    
    R99writeLog(routine + " R00Main completed")
    

R00Main()