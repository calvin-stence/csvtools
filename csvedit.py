import csv
import glob
import re
import pprint
import os

def main():
    pp = pprint.PrettyPrinter(indent=4)
    textjobs = getjobs(".oma")
    jobs = removeextension(textjobs)
    dictjobs = {}
    for i in range(len(textjobs)):
        dictjobs.update({jobs[i]: rx_attrib(textjobs[i],jobs[i]).rxattribs})
        pp.pprint(dictjobs[jobs[i]])
        create_rx_directory(dictjobs[jobs[i]])

def create_rx_directory(rx_data):
    prefilepath = rx_data['LDNAM'] + '/BASE_' + rx_data['_SFBASE'] + '/SPH_' + rx_data['SPH'] + '/CRIB_' + rx_data['CRIB']
    filepath = 'C:/Users/calvin.stence/PycharmProjects/csvtools/' + re.sub('[.]', '', prefilepath) #replace decimal points in numbers associated with rx_data so that it is a valid file path
    try:
        os.makedirs(filepath)
    except(FileExistsError):
        pass
    print(filepath)

def getjobs(extension):
    extensionjobs = []
    for file in glob.glob("*" + extension):
        extensionjobs.append(file)
        print('Found ' + file)
    return extensionjobs

def removeextension(extensionjobs):
    jobs = []
    for index in range(len(extensionjobs)):
        jobs.append(extensionjobs[index][0:8])
    return jobs

class rx_attrib(object):
    def __init__(self,file,jobs):
        self.file = file
        self.jobs = jobs
        self.rx_regex = {
            #"JOB": re.compile(r'JOB=(\d\d\d\d\d\d\d\d)'),
            "LDNAM": re.compile(r'LDNAM=(\w\w\w)'),
            "SPH": re.compile(r'SPH=([-]?\d.\d\d);'),
            "_SFBASE": re.compile(r'_SFBASE=(\d.\d\d);'),
            "CRIB": re.compile(r'CRIB=(\d\d).\d\d')
        }
        self.rxattribs = {
            "JOB": jobs,
            "LDNAM": "",
            "SPH": "",
            "_SFBASE": "",
            "CRIB": ""
        }
        with open(file) as csvfile:
            f = csv.reader(csvfile, delimiter=',', lineterminator='\n')
            filedata = list(f)
            for rx_regex_key, rx_regex_values in self.rx_regex.items():
                regex_search = rx_regex_values
                for row in filedata:
                    for j in range(len(row)):
                        mo = re.search(regex_search, row[j])
                        try:
                            self.rxattribs.update({rx_regex_key: mo.group(1)})
                        except AttributeError:
                            pass

if __name__ == "__main__":
    main()