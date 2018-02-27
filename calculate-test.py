#!/usr/bin/env python3

import os
import sys


#VARIABLE DEFINITIONS###################################################

numberOfStudents = int(sys.argv[1])  #height, students are row headings
numberOfQuestions = int(sys.argv[2]) #width, questions are column headings
totalPointsForTest = int(sys.argv[3])
isCurved = sys.argv[4]

spreadsheet = [[0 for x in range(numberOfQuestions)] for y in range(numberOfStudents)]
studentList = ["x" for x in range(numberOfStudents)]
questionList = [0 for x in range(numberOfQuestions)]


#FUNCTION DEFINITIONS####################################################

def calculateTotal(row, dummy=None):
    total = 0

    for cell in row:
        total += float(cell)

    return total


def calculateAverage(row, totalPoints):
    return calculateTotal(row) / totalPoints


def calculateForEach(filename, matrix, func, divisor, labels):
    with open(filename, "w") as f:
        for i, row in enumerate(matrix):
            result = func(matrix[i], divisor)
            f.write(str(labels[i]) + ", " + str(result) + "\n")        


def populateMatrixFromFile(studentList, questionList, spreadsheet):

    with open("per-student-metrics-for-test-1.csv","r") as f:
        firstline = f.readline().rstrip().split(",", numberOfQuestions)   
        firstline.pop(0)        

        for i, element in enumerate(firstline):
            questionList[i] = element        
    
        for i,line in enumerate(f):
            row = line.split(",", numberOfQuestions)

            for j,cell in enumerate(row):
                if j != 0:
                    spreadsheet[i][j - 1] = cell
                else:
                    studentList[i] = cell


#BEGIN MAIN#########################################################

populateMatrixFromFile(studentList, questionList, spreadsheet)

qAvgsFilename = "question-averages.csv"
sTotalsFilename = "student-totals.csv"
sAvgsFilename = "student-averages.csv"

if isCurved == "true":
    sAvgsFilename = "student-averages-curved.csv"   

calculateForEach(qAvgsFilename, list(zip(*spreadsheet)), calculateAverage, numberOfStudents, questionList)
calculateForEach(sTotalsFilename, spreadsheet, calculateTotal, None, studentList)
calculateForEach(sAvgsFilename, spreadsheet, calculateAverage, totalPointsForTest, studentList)
