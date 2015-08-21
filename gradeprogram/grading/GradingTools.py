# -*- coding: utf-8 -*-
import string
from FileTools import FileTools
from subprocess import call
from gradingResource.enumResources import ENUMResources
from gradingResource.fileNameNPathResources import FileNameNPathResources

class GradingTools(object):
    def __init__(self, parameter, command):
        self.gradeMethod = parameter.gradeMethod
        self.caseCount = parameter.caseCount
        self.answerPath = parameter.answerPath
        self.problemName = parameter.problemName
        self.filePath = parameter.filePath
        self.command = command
        
    def grade(self):
        if self.gradeMethod == ENUMResources.const.SOLUTION:   # solution
            if self.caseCount > 1:
                result, score = self.gradeSolutionMulti()
                
            else:
                result, score = self.gradeSolutionSingle()
            
        else:   # checker
            self.gradeChecker()
            
        return result, score
        
    def gradeSolutionSingle(self):
        # user output file each line compare with answer file each line.
        answerOpenCommand = "%s%s%s" % (self.answerPath, self.problemName,
                                        FileNameNPathResources.const.DefaultOutputTotalResultFileName)
        
        stdLines = FileTools.readFileLines(FileNameNPathResources.const.OutputResultFileName)
        answerLines = FileTools.readFileLines(answerOpenCommand)
        
        answerLineCount = len(answerLines)
        stdLineCount = len(stdLines)
        
        count = stdLineCount - answerLineCount
        
        _min = stdLineCount if count < 0 else answerLineCount
        count = abs(count)
        
        strip = string.rstrip
        
        for i in xrange(_min):
            stdLine = strip(stdLines[i], '\r\n ')
            answerLine = strip(answerLines[i], '\r\n ')
            
            if stdLine != answerLine:   # if not same each line
                count += 1
        
        return self.getSolutionScore(count, answerLineCount)
        
    def gradeChecker(self):
        copyCommand = "%s%s%s" % (self.answerPath, self.problemName, '_checker')
        FileTools.copyFile(copyCommand, 'checker')
        
        call('./checker 1>result.txt', shell = True)
        
        score = self.getScore('result.txt')
        
        if score is 100:
            return ENUMResources.const.SOLVED, score
        else:
            return ENUMResources.const.WRONG_ANSWER, score
    
    def gradeSolutionMulti(self):
        answerOpenCommand = "%s%s%s" % (self.answerPath, self.problemName,
                                        FileNameNPathResources.const.DefaultOutputTotalResultFileName)
        
        answerLines = FileTools.readFileLines(answerOpenCommand)
        stdLines = FileTools.readFileLines(FileNameNPathResources.const.OutputResultFileName)
        
        strip = string.rstrip
        
        totalCount = len(answerLines)
        loopCount = len(stdLines)
        caseCount = 1
        count = abs(loopCount - totalCount)
        i = 0
        appendFlag = True
        
        while i < loopCount:
            answerOpenCommand = "%s%s%s%i%s" % (self.answerPath,
                                                self.problemName,
                                                FileNameNPathResources.const.CaseFile,
                                                caseCount,
                                                FileNameNPathResources.const.OutputCaseName)
            answers = FileTools.readFileLines(answerOpenCommand)
            
            for answer in answers:
                stdLine = strip(stdLines[i], '\r\n ')
                answerLine = strip(answer, '\r\n ')
                
                if stdLine != answerLine:
                    count += 1
                    if appendFlag:
                        self.makeTestCase(caseCount)
                        appendFlag = False
                    
                i += 1
                
            if caseCount is self.caseCount:
                count += loopCount - i
            
            caseCount += 1
                
        return self.getSolutionScore(count, loopCount)
        
    def makeTestCase(self, caseNum):
        wf = open('testcase.txt', 'w')
            
        wf.writelines(caseNum)
                
        wf.close()

    def getSolutionScore(self, count, lineCount):
        result = ENUMResources.const.SOLVED
        score = 100
        
        if count > 0:
            result = ENUMResources.const.WRONG_ANSWER
            score = int( ((lineCount - count) * 100) / lineCount )
            
        if score < 0:
            return ENUMResources.const.WRONG_ANSWER, 0
        
        return result, score
            
    def getScore(self, fileName):
        scores = FileTools.readFileLines('result.txt')
        
        return int(scores[0])