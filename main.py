import os, subprocess
from pathlib import Path
from os import system as sys
import tkinter as tk
import re

ABSPTH = os.path.abspath("")

def gitExist():
    git_dir = Path(".git")
    if git_dir.is_dir():
        return True
    else:
        return False

def remoteOrigin():
    RemoteOriginUrl = []
    
    w = tk.Tk()
    tk.Label(w,
             text = "Is there a remote origin?").pack()
    
    remoteOriginOptions = [("Yes",True),("No",False)]
    
    v = tk.IntVar()
    v.set(1)
    
    RemoteOriginUrlFrame = tk.Frame()
    RemoteOriginUrlFrameUrl = tk.Frame(master = RemoteOriginUrlFrame)
    RemoteOriginUrlLabel = tk.Label(master = RemoteOriginUrlFrameUrl,
             text = "URL: ").pack(side=tk.LEFT)
   
    urlVar = tk.StringVar()
    RemoteOriginUrlInput = tk.Entry(master = RemoteOriginUrlFrameUrl, textvariable = urlVar).pack(side=tk.RIGHT)
    RemoteOriginUrlFrameUrl.pack()
    
    def getUrl():
        if v.get() and urlVar.get():
            w.destroy()
            RemoteOriginUrl.append(urlVar.get())
        elif v.get() and not urlVar.get():
            pass
        else:
            w.destroy()
            RemoteOriginUrl.append(None)
    RemoteOriginUrlSubmit = tk.Button(text="Submit",
                                      command = getUrl)
    
    def showRemoteOriginUrlInput(element, submit):
        if v.get():
            element.pack()
            submit.pack_forget()
            submit.pack()
        else:
            element.pack_forget()
    
    for option, val in remoteOriginOptions:
        tk.Radiobutton(w,
                       text = option,
                       variable = v,
                       command = lambda: showRemoteOriginUrlInput(RemoteOriginUrlFrame, RemoteOriginUrlSubmit),
                       value = val).pack(anchor = tk.W)
    showRemoteOriginUrlInput(RemoteOriginUrlFrame, RemoteOriginUrlSubmit)
    
    w.mainloop()
    return(RemoteOriginUrl[0])

def setupGit():
    sys("git init")
    sys("git add .")
    sys('git commit -am "init"')
    
    #Asks for remote origin
    if remoteOrigin():
        sys('git remote add origin "' + remoteOrigin() + '"')
        sys("git push origin -u main")
        
def push2Github(commitDetails):
    sys("git add .")
    sys('git commit -am "' + commitDetails[0] + ' ' + commitDetails[1] + '"')
    sys("git push origin -u main")
        
def newCommit(versionNo, versionAuto):
    commitDetails = []
    w = tk.Tk()
    w.title("New Commit")
    
    currentVer = tk.Label(w,
                          text = "Current version #: " + versionNo).pack()
    
    versionNoFrame = tk.Frame()
    
    versionVar = tk.StringVar(w, value = versionAuto)
    
    versionNoLabel = tk.Label(master = versionNoFrame,
                              text = "Update version #: v.").grid(column=0, row=0)
    versionNoEntry = tk.Entry(master = versionNoFrame,
                              width = 3,
                              textvariable = versionVar).grid(column=1, row=0)
    versionNoLabelDot = tk.Label(master = versionNoFrame,
                              text = ".").grid(column=2, row=0)
    versionNoFrame.pack()
    
    commentLabel = tk.Label(w,
                            text = "Comment:",
                            anchor = "w").pack(fill='x')
    
    commentEntry = tk.Text(width = 35, height = 5)
    commentEntry.pack()
    
    def versionUpdate():
        if commentEntry.get("1.0", "end-1c"):
            commitDetails.append("v."+versionVar.get()+".")
            commitDetails.append(commentEntry.get("1.0", "end-1c"))
            w.destroy()
    
    submitButton = tk.Button(w,
                             text="Submit",
                             command = versionUpdate).pack()
    
    w.mainloop()
    push2Github(commitDetails)
    
if __name__ == "__main__":
    sys("cd " + ABSPTH)
    if not gitExist():
        setupGit()
    __URL = subprocess.check_output('git config --get remote.origin.url', shell=True, text=True)
    __lastMessage = subprocess.check_output('git log -1 --pretty=%B', shell=True, text=True)
    versionNo = re.findall("^[^\s]+", __lastMessage)[0]
    
    versionNoMinor = int(re.findall("(\d+)\.$", versionNo)[0])
    versionAuto = re.sub("\d+(?=\.$)", str(versionNoMinor + 1), versionNo)
    versionAuto = re.sub("\.$", "", versionAuto)
    versionAuto = re.sub("^v\.", "", versionAuto)
    
    newCommit(versionNo, versionAuto)
