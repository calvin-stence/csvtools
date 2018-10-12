import csv
import glob
import re
import pprint
import os
import shutil

#todo find jobs in usrxtcal02. determine if jarvis data exists, if so, create folder if it does not exist, copy
#todo image to this location
def main():
    pp = pprint.PrettyPrinter(indent=4)  # Create PrettyPrint object,to cleanly display job data in the console
    job_files = get_jobs(".oma")  # find all the .oma files in the folder and return a list
    job_numbers = remove_file_extension(job_files)  # create a second list of job_numbers without the file extension
    jobs_dictionary = {}  # create a dictionary to store each job and its corresponding data

    # This for loop will do four things:
    # 1. Update the dictionary jobs_dictionary with sub-dictionaries, which each contain the rx data (sphere power,
    # semi-finish base, job number, etc) for their respective job
    # 2. print out the result of this update in the console using the pprint object pp created above
    # 3. Create a folder structure in the directory of the script with the following hierarchy: Product line (MR7, MR8,
    # etc) LDNAM (product code, such as S33 or 5CE) / BASE (base curve of the lens) / SPH (sphere Rx power of the lens)
    # / CRIB (the crib diameter for this job)
    # 4. Move the Jarvis results (if they exist) from the Jarvis results folder to the relevant file structure from item
    # 3 above
    for i in range(len(job_files)):  # for each job stored in job_files:
        jobs_dictionary.update(
            {job_numbers[i]: FileQuery(job_files[i], job_numbers[i]).rx_attributes})  # 1 as described above
        pp.pprint(jobs_dictionary[job_numbers[i]-])  # 2 as described above
        create_rx_directory(jobs_dictionary[job_numbers[i]])  # 2 as described above
        get_jarvis_images(jobs_dictionary[job_numbers[i]])  # 2 as described above


def create_rx_directory(rx_data):
    pre_file_path = rx_data['LDNAM'] + '/BASE_' + rx_data['_SFBASE'] + '/SPH_' + rx_data['SPH'] + '/CRIB_' + rx_data[
        'CRIB']
    # the following line gets the current working directory (i.e., where the script is being run) and ads the file
    # directory described in point 3 above the for loop in main()
    file_path = os.getcwd() + '\\' + re.sub('[.]', '', pre_file_path)
    try:
        os.makedirs(file_path)
    except(FileExistsError):
        pass
    print(file_path)


def get_jobs(extension):
    extension_jobs = []
    for file in glob.glob("*" + extension):
        extension_jobs.append(file)
        print('Found ' + file)
    return extension_jobs


def get_jarvis_images(rx_data):
    for file in glob.glob('**\\' + rx_data['JOB'] + '_*_PhaseH.png'):
        prefilepath = rx_data['LDNAM'] + '/BASE_' + rx_data['_SFBASE'] + '/SPH_' + rx_data['SPH'] + '/CRIB_' + rx_data[
            'CRIB']
        filepath = os.getcwd() + '\\' + re.sub('[.]', '', prefilepath)
        try:
            shutil.copy(file, filepath)
        except FileNotFoundError:
            print('No Jarvis data for job' + rx_data['JOB'])
            pass


def set_product_line(self):
    if self.rx_attributes['LDNAM'] == 'S33':
        self.rx_attributes['PRODUCT_LINE'] = 'MR8'
        return
    if self.rx_attributes['LDNAM'] == '5CE':
        self.rx_attributes['PRODUCT_LINE'] = 'MR8'
        return
    if self.rx_attributes['LDNAM'] == 'S40':
        self.rx_attributes['PRODUCT_LINE'] = 'MR7'
        return


def remove_file_extension(extensionjobs):
    jobs = []
    for index in range(len(extensionjobs)):
        jobs.append(extensionjobs[index][0:8])
    return jobs


# Class: JobRxAttrib
# This class collects and holds some Rx data for a given job ticket.
# Inputs: (1) input_file, (2) input_job
# Input (1) is a filename. This input will be searched by the search keys described in rx_regex.
# Input (2) is a job number. The input file doesn't always have the job number in it, so the job number is passed in.
# Data structures: (1) rx_regex, (2) rx_attributes
# Data structure (1) is a dictionary of regex (regular expression) searches. It correlates the rx attribute (such as
# sphere power, semifinish base, or crib) found in the input_file (input 1) with a regex search that will find that
# value.
# Data structutre (2) is a dictionary of attributes relevant to the job (such as sphere power, semi-finish base curve, etc). The searches
# in data structure (1) are stored in this dictionary.
class FileQuery:
    def __init__(self, search_dictionary, file_data):
            self.result_dictionary = {}
            for row in file_data:
                for i in range(len(row)):
                    for regex_keys, regex_searches in search_dictionary.items():
                        if regex_keys in self.result_dictionary.keys():
                            pass
                        else:
                            try:
                                search_result = re.search(regex_searches, row[i])
                                self.result_dictionary.update({regex_keys: search_result.group(1)})
                            except AttributeError:
                                pass

class JobRxAttrib(object):
    def __init__(self, input_file, input_job):
        self.file = input_file
        self.jobs = input_job
        self.rx_regex = {
            "LDNAM": re.compile(r'LDNAM=(\w\w\w)'),
            "SPH": re.compile(r'SPH=([-]?\d.\d\d);'),
            "_SFBASE": re.compile(r'_SFBASE=(\d.\d\d);'),
            "CRIB": re.compile(r'CRIB=(\d\d).\d\d')
        }
        self.rx_attributes = {
            "JOB": input_job,
            "LDNAM": "",
            "SPH": "",
            "_SFBASE": "",
            "CRIB": "",
            "PRODUCT_LINE": ""
        }
        with open(input_file) as csv_file:  # Open the job file as a csv file
            f = csv.reader(csv_file, delimiter=',', lineterminator='\n')  # Create a csv reader object to parse the file
            filedata = list(f)  # Create a list from this csv to allow for iteration
            for rx_regex_keys, rx_regex_values in self.rx_regex.items():  # iterate over rx values to find in the file
                regex_search = rx_regex_values  # for clarity, the rx_regex_values will be the regex search
                for row in filedata:  # for each row in the file
                    for j in range(len(row)):  # for each item in the row (in case there are multiple)
                        search_result = re.search(regex_search, row[j])  # perform the regex search and get the result
                        try:  # try to update the rx_attributes with a search result
                            self.rx_attributes.update(  # if there is a search result, update it
                                {rx_regex_keys: search_result.group(1)}  # update the rx_attributes with the result
                            )
                        except AttributeError:  # if there was no attribute found
                            pass  # move on to the next item
        try:
            set_product_line(self)  # using the data found above, set the product line to MR7 or MR8
        except AttributeError:
            print('Error assigning a product line to job ' + input_job + '. Maybe the input file is empty?')


if __name__ == "__main__":
    main()
