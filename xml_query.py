#todo pass in properties, return contents when found
import re
import csv

def main():
    input_file = "70007391.oma"
    rx_regex = {
            "LDNAM": re.compile(r'LDNAM=(\w\w\w)'),
            "SPH": re.compile(r'SPH=([-]?\d.\d\d);'),
            "_SFBASE": re.compile(r'_SFBASE=(\d.\d\d);'),
            "CRIB": re.compile(r'CRIB=(\d\d).\d\d')
        }
    with open(input_file) as csv_file:  # Open the job file as a csv file
        f = csv.reader(csv_file, delimiter=',', lineterminator='\n')  # Create a csv reader object to parse the file
        filedata = list(f)  # Create a list from this csv to allow for iteration
        results = FileQuery(rx_regex, filedata)
        print(results.result_dictionary)


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

if __name__  == "__main__":
    main()
