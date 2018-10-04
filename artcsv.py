import csv
from tkinter import *
#from tkinter import ttk
import tkinter as tk
#from cgitb import text
import glob

class Application(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.pack()

        #self.infilename = Entry()
        #self.outfilename = Entry()

        self.convert_button = Button(master, text="Convert")
        #self.infilename.pack()
        #self.outfilename.pack()
        self.convert_button.pack()

        self.infilename_entry_contents = IntVar()
        self.outfilename_entry_contents = IntVar()

        #self.infilename_entry_contents.set("Enter the first job number")
        #self.infilename_entry_contents.set("70006971")
        #self.infilename["textvariable"] = self.infilename_entry_contents
        
        #self.outfilename_entry_contents.set("Enter the last job number")
        #self.outfilename_entry_contents.set("70007061")
        #self.outfilename["textvariable"] = self.outfilename_entry_contents
            
        self.convert_button.bind("<Button-1>", self.artcsv)

    def artcsv(self,convert_button):
        textjobs = getjobs(".oma")
        jobs = removeextension(textjobs)
        numjobs = len(textjobs)

        jobcounter = 0
        unconvertedcounter = 0
        errorcnt = 0
        for i in range(numjobs):
            try:
                with open(textjobs[i]) as csvfile:
                    f = csv.reader(csvfile, delimiter = ',', lineterminator='\n')
                    csvcontent = list(f)
                    if len(csvcontent)>0:
                        if len(csvcontent[7][0])>11:
                            listinput = 'BDIA=' + csvcontent[7][0][7:12] + ';'
                            csvcontent.insert(8,[listinput])
                            csvcontent[1][0] = 'JOB=' + jobs[i]
                            csvcontent[7][0] = 'BLKD=' + csvcontent[7][0][7:12] + ';'
                            with open(textjobs[i], 'w') as csvfile:
                                v = csv.writer(csvfile, delimiter = ',', lineterminator= '\n')
                                v.writerows(csvcontent)
                                print("Job " + str(jobcounter + 1) + " (MO# " + textjobs[i] + ")" +" Converted")
                                jobcounter += 1
                        else:
                            unconvertedcounter +=1
                    else:
                        errorcnt += 1
                        print("Something went wrong with " +  textjobs[i] + ", maybe it's empty or malformed?")
                    
            except FileNotFoundError:
                errorcnt += 1
                print("Something went wrong; maybe the job " +  textjobs[i] + " is missing?")
        print("Processed " + str(jobcounter+unconvertedcounter) + " jobs, of which " + str(jobcounter) + " were converted and " + str(unconvertedcounter) + " were accessed but already converted.")
        print("There were " + str(errorcnt) + " errors.")

def getjobs(extension):
    extensionjobs = []
    for file in glob.glob("*" + extension):
        extensionjobs.append(file)
    return extensionjobs

def removeextension(extensionjobs):
    jobs = []
    for index in range(len(extensionjobs)):
        jobs.append(extensionjobs[index][0:8])
    return jobs

root = tk.Tk()
app = Application(master=root)
root.title("ART Job File Converter")
root.size()
app.mainloop()