import os
import commands as c

def findDataStart(lines):
    for i, l in enumerate(lines):
        test = l.split(' ')[0]
        try:
            float(test)
            return i, lines[i:]
        except:
            continue
    return -1, []


def removeCorruptLines(inputFN, outputFN = None):
    if outputFN == None:
        outputFN = inputFN
    try:
        inputFile = open(inputFN, 'r')
    except:
        fileError = Exception("Input File not found!")
        raise fileError

    allLines = inputFile.readlines()
    inputFile.close()
    end, dataLines = findDataStart(allLines)
    newlines = allLines[0:end]
    
    for l in dataLines:
        goodLine = True
        for s in l.split(' '):
            try:
                float(s)
            except:
                goodLine = False
                break 
        if goodLine:
            newlines.append(l)

    newFile = open(outputFN,'w')
    newFile.writelines(newlines)
    newFile.close()

    return newlines

def CombineXVG(input1, input2, output):
    lines1 = removeCorruptLines(input1,'temp.xvg')
    lines2 = removeCorruptLines(input2,'temp.xvg')

    end1, dataLines1 = findDataStart(lines1)
    end2, dataLines2 = findDataStart(lines2)

    endTime = float(dataLines1[-1].split(' ')[0])
    i = 0
    startTime = float(dataLines2[i].split(' ')[0])
    concat = True
    while startTime <= endTime and concat:
        i += 1
        try:
            startTime = float(datalines2[i].split(' ')[0])
        except:
            print "No new data found in second input file"
            concat = False

    if concat:
        outputLines = lines1 + dataLines2[i:]
    else:
        outputLines = lines1
    outFile = open(output,'w')
    outFile.writelines(outputLines)
    outFile.close()
    return outputLines
    
