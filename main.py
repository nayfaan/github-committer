import os
from pathlib import Path
from os import system as sys
import tkinter as tk

ABSPTH = os.path.abspath("")

def run():
    pass

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
             text="Is there a remote origin?").pack()
    
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
    sys("cd " + ABSPTH)
    sys("git init")
    sys("git add .")
    sys('git commit -am "init"')
    
    #Asks for remote origin
    if remoteOrigin():
        sys('git remote add origin "' + remoteOrigin() + '"')
        sys("git push origin -u main")
    
if __name__ == "__main__":
    if not gitExist():
        setupGit()
    
    run()
