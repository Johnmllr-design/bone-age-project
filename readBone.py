import re
import pydicom
import matplotlib.pyplot as plt


class readFile:
    def __init__(self):
        pass

    # this function performs the bulk of the tasks, including reading, and comparing the results
    # of the human and bone scans

    def readfile(self, humanPath, dicomPath):

        with open(humanPath, 'r') as file:
            # Read the lines of the file
            file_lines = file.readlines()

        humanAgeEstimate = [-1, -1]
        foundAge = False
        for line in file_lines:
            array = self.splitter(line)

            # if this line containts the output age
            if not foundAge and "estimated" in array and "bone" in array and "age" in array:
                for i in range(0, array.__len__() - 1):
                    if array[i].isnumeric() and array[i + 1] == "years" or array[i + 1] == "Years":
                        humanAgeEstimate[0] = int(array[i])
                        foundAge = True
                    elif array[i].isnumeric() and array[i + 1] == "months" or array[i + 1] == "Months":
                        humanAgeEstimate[1] = int(array[i])
                        foundAge = True

        # open the output file
        fileObj = open(
            '/Users/johnmiller/Desktop/BoneAgeProject/outputFile.txt', "w+")
        fileObj.write("the human age estimate is " + str(
            humanAgeEstimate[0]) + " years and " + str(humanAgeEstimate[1]) + " months\n")

        with open(dicomPath, 'r') as file:
            # Read the lines of the file
            file_lines = file.readlines()

        # split the output of the computer's segmentation and obtain it's results
        computerAgeEstimate = [-1, -1]
        foundAge = False

        for line in file_lines:
            array = self.splitter(line)

            # if this line containts the output age
            if not foundAge and "estimated" in array and "bone" in array and "age" in array:
                for i in range(0, array.__len__() - 1):
                    if array[i].isnumeric() and array[i + 1] == "years" or array[i + 1] == "Years":
                        computerAgeEstimate[0] = int(array[i])
                    elif array[i].isnumeric() and array[i + 1] == "months" or array[i + 1] == "Months":
                        computerAgeEstimate[1] = int(array[i])

        # write the computer segmentation model to the text file and compare the restults
        fileObj.write("the computer segmentation model age estimate is " + str(
            computerAgeEstimate[0]) + " years and " + str(computerAgeEstimate[1]) + " months\n")
        fileObj.write("these ages differ by " + str(abs(computerAgeEstimate[0] - humanAgeEstimate[0] + (
            float(computerAgeEstimate[1] / 12) - float(humanAgeEstimate[1] / 12)))) + " years")
        # close the output file
        fileObj.close()

    # split the string based on parameters

    def splitter(self, st) -> list:
        array = []
        stri = ""
        badChars = [' ', ',', '\n', ':']
        for char in st:
            if char not in badChars:
                stri += char
            else:
                if stri != "":
                    array.append(str(stri))
                    stri = ""
        return array


# driver code
if __name__ == "__main__":
    obj = readFile()
    obj.readfile('/Users/johnmiller/Desktop/BoneAgeProject/dicomUncoded.txt',
                 '/Users/johnmiller/Desktop/BoneAgeProject/HumanEstimate.txt')
