import csv
import glob
import re

def artcsv():
    textjobs = getjobs(".oma")
    numjobs = len(textjobs)
    dictjobs = {}
    for i in range(len(textjobs)):
        dictjobs[textjobs[i]] = rx_attrib(textjobs[i]).rxattribs
        print(dictjobs)




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
    def __init__(self,file):
        self.file = file
        #self.job_re = re.compile(r'(JOB)=(\d\d\d\d\d\d\d\d)')
        #self.sph_re = re.compile(r'(SPH)=(\d.\d\d);')
        #self.blkd_re = re.compile(r'(_BLKD)=(\d\d.\d\d);')
        #self.base_re = re.compile(r'(_SFBASE)=(\d.\d\d);')
        #self.crib_re = re.compile(r'(CRIB)=(\d\d.\d\d)')
        self.rxre = {
            #"JOB": r'(JOB)=(\d\d\d\d\d\d\d\d)',
            "SPH": r'(SPH)=(\d.\d\d);',
            "_SFBASE": r'(_SFBASE)=(\d.\d\d);',
            "_BLKD": r'(_BLKD)=(\d\d.\d\d);',
            "CRIB": r'(CRIB)=(\d\d.\d\d)'
        }
        self.rxattribs = {
            "JOB": file,
            "SPH": "",
            "_SFBASE": "",
            "_BLKD": "",
            "CRIB": ""
        }
        with open(file) as csvfile:
            f = csv.reader(csvfile, delimiter=',', lineterminator='\n')
            filedata = list(f)
            for key,values in self.rxre.items():
                re_search = re.compile(values)
                for row in filedata:
                    for j in range(len(row)):
                        mo = re.search(re_search,row[j])
                        try:
                            self.rxattribs.update({key:mo.group(2)})
                        except AttributeError:
                            pass








if __name__ == "__main__":
    artcsv()