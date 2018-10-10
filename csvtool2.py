import csv
import glob
import pprint
import re

def test():
    jobs = findjobs('.oma')
    for i in range(len(jobs)):
        dictjobs = {};
        dictjobs.update({jobs[i]:getrx(jobs[i])})
        prettyprint = pprint.PrettyPrinter(depth=6)
        prettyprint.pprint(dictjobs)


def findjobs(extension):
    files = glob.glob('*' + extension)
    return files

class getrx():

    def find(self, regex, line):
        #todo tell me if line contains regex, and if so, return the snipped thingy
        return ""

    def __init__(self,file):
        self.rxre = {
            "JOB":re.compile(r'(JOB)=(\d\d\d\d\d\d\d\d)'),
            "SPH":r'(SPH)=\d.\d\d',
            "_SFBASE":r'(_SFBASE)=(\d.\d\d)',
            "CRIB":r'(CRIB)=(\d\d\.\d\d)'
        }

        self.rxattrib = {
            "JOB": '',
            "SPH": '',
            "_SFBASE": '',
            "CRIB": ''
        }



        with open(file) as csvfile:
            f = csv.reader(csvfile, delimiter=',', lineterminator='')
            filedata = list(f)
            for key, value in self.rxre.items():
                searchpat = re.compile(value)
                for row in filedata:
                    for j in range(len(row)):
                        search_data = re.search(searchpat,row[j])
                        try:
                            self.rxattrib.update({key: search_data.groups(2)})
                        except(AttributeError):
                            pass


# #class rxatribs():
# #    def __init__(self, job, sph, _sfbase):
# #        self.job
#         self.sph
#         self._sfbase



if __name__ == "__main__":
    test()







