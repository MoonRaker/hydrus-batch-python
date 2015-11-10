#ReadLine.py
#Created by Derek Groenendyk
#10/17/2011
#This file has functions that write and read data from .IN files


def readLine(string):
    string = string[:-1]
    spaceLen = 0
    paramLen = 0
    paramStart = []
    spaces = []
    params = []
    for i in range(len(string)):
        if i == len(string)-1:
            if string[i] == ' ':
                if string[i-1] != ' ':
                    params.append(paramLen)
                    spaces.append(spaceLen)
                spaces.append(len(string) - (paramStart[-1] + params[-1]))
            else:
                if i == len(string)-1 and paramLen == 0:
                    if string[i] != ' ':
                        paramLen += 1
                        paramStart.append(i)
                    
                if paramLen > 0:
                    paramLen += 1
                    params.append(paramLen)
                    spaces.append(spaceLen)
                else:
                    spaces.append(len(string) - (paramStart[-1] + params[-1]) - 1)
                    paramStart.append(i)
                    params.append(1)

        else:
            if string[i] == ' ':
                spaceLen += 1
            else:
                paramLen += 1
                if i == 0:
                    paramStart.append(i)
                elif string[i-1] == ' ':
                    paramStart.append(i)
                if i+1 < len(string)-1:
                    if string[i+1] == ' ':
                        spaces.append(spaceLen)
                        spaceLen = 0
                        params.append(paramLen)
                        paramLen = 0


    return  [paramStart,params,spaces]



def writeLine(string,index,param):
    param = str(param)

    [starts,paramLens,whitespaces] = readLine(string)
    line = string.split()

##    index = starts.index(index)
##    print paramLens
##    print index
    if index < len(paramLens):   
        oldLen = paramLens[index]
        newLen = len(param)
        paramLens[index] = newLen
        line[index] = param
    else:
        oldLen = 1
        newLen = 1
        index = len(paramLens)
        
    if index != len(line)-1:
        whitespaces[index] = whitespaces[index] + (oldLen - newLen)
    else:
        if len(whitespaces) > len(paramLens):
            whitespaces[index+1] = whitespaces[index+1] + (oldLen - newLen)


##    if oldLen > newLen:
##        newWhitespace = oldLen - newLen
##    elif oldLen < newLen:
##        newWhitespace = newLen - oldLen
##    else:
##        newWhitespace = 0
##
##    if starts[0] == 0:
##        whitespaces[index] += newWhitespace
##    else:
##        whitespaces[index + 1] += newWhitespace

    if starts[0] == 0:
        wline = ''
        for i in range(1,len(whitespaces)):
            wline += line[i-1] + ' '*whitespaces[i]

        if len(whitespaces)-1 < len(paramLens):
            wline += line[-1]            
            
    else:
        wline = ''
        for i in range(len(paramLens)):
            wline += ' '*whitespaces[i]+line[i]

        if len(whitespaces) > len(paramLens):
            wline += ' '*whitespaces[-1]

            
    wline += '\n'
    return wline


def appendToLine(string,param):
    param = str(param)
    [starts,paramLens,whitespaces] = readLine(string)
    line = string.split()

##    index = starts.index(index)
    oldLen = paramLens[index]
    newLen = len(param)
    paramLens[index] = newLen
    line[index] = param
    

    if index != len(line)-1:
        whitespaces[index+1] = (whitespaces[index+1] + oldLen) - newLen
    else:
        if len(whitespaces) > len(paramLens):
            whitespaces[index+1] = (whitespaces[index+1] + oldLen) - newLen


##    if oldLen > newLen:
##        newWhitespace = oldLen - newLen
##    elif oldLen < newLen:
##        newWhitespace = newLen - oldLen
##    else:
##        newWhitespace = 0
##
##    if starts[0] == 0:
##        whitespaces[index] += newWhitespace
##    else:
##        whitespaces[index + 1] += newWhitespace

    if starts[0] == 0:
        wline = ''
        for i in range(1,len(whitespaces)):
            wline += line[i-1] + ' '*whitespaces[i]

        if len(whitespaces)-1 < len(paramLens):
            wline += line[-1]            
            
    else:
        wline = ''
        for i in range(len(paramLens)):
            wline += ' '*whitespaces[i]+line[i]

        if len(whitespaces) > len(paramLens):
            wline += ' '*whitespaces[-1]

            
    wline += '\n'
    return wline


##def writeManyLines(string,index,param):
##    param = str(param)
##    [starts,paramLens,whitespaces] = readLine(string)
##    line = string.split()
##
##    oldLen = paramLens[index]
##    newLen = len(param)
##    paramLens[index] = newLen
##    line[index] = param
##    
##
##    if index != len(line)-1:
##        whitespaces[index+1] = (whitespaces[index+1] + oldLen) - newLen
##    else:
##        if len(whitespaces) > len(paramLens):
##            whitespaces[index+1] = (whitespaces[index+1] + oldLen) - newLen
##
##
##    if starts[0] == 0:
##        wline = ''
##        for i in range(1,len(whitespaces)):
##            wline += line[i-1] + ' '*whitespaces[i]
##
##        if len(whitespaces)-1 < len(paramLens):
##            wline += line[-1]            
##            
##    else:
##        wline = ''
##        for i in range(len(paramLens)):
##            wline += ' '*whitespaces[i]+line[i]
##
##        if len(whitespaces) > len(paramLens):
##            wline += ' '*whitespaces[-1]
##
##            
##    wline += '\n'
##    return wline



    
##    
##def main():
##
##    string = "   thr     ths    Alfa      n         Ks       l   "
##    string = "0.034    0.46   0.016    1.37        696     0.5   "
##
##    print writeLine(string,3,1.05)
##    print string
##
##
##if __name__=='__main__':
##    main()
