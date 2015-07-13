# -*- coding: utf-8 -*-
import string
from FileTools import FileTools
from subprocess import call
from GradingCommand import GradingCommand
from gradingResource.enumResources import ENUMResources
from gradingResource.fileNameNPathResources import FileNameNPathResources

class GradingTools(object):
    def __init__(self, parameter):
        self.gradeMethod = parameter.gradeMethod 
        self.caseCount = parameter.caseCount
        self.usingLang = parameter.usingLang
        self.version = parameter.version
        self.answerPath = parameter.answerPath
        self.problemName = parameter.problemName
        self.filePath = parameter.filePath
        
    def Grade(self):
        if self.gradeMethod == ENUMResources.const.SOLUTION:   # solution
            if self.caseCount > 1:
                result, score = self.GradeSolutionMulti()
                
            else:
                result, score = self.GradeSolutionSingle()
            
        else:   # checker
            if self.caseCount > 1:
                result, score = self.GradeCheckerMulti()
                
            else:
                result, score = self.GradeCheckerSingle()
            
        return result, score
        
    def GradeSolutionSingle(self):
        # user output file each line compare with answer file each line.
        answerOpenCommand = "%s%s%s" % (self.answerPath, self.problemName,
                                        FileNameNPathResources.const.DefaultOutputTotalResultFileName)
        
        stdLines = FileTools.ReadFileLines(FileNameNPathResources.const.OutputResultFileName)
        answerLines = FileTools.ReadFileLines(answerOpenCommand)
        
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
        
        return self.GetSolutionScore(count, answerLineCount)
        
        #return result, score
        
    def GradeCheckerSingle(self):
        copyCommand = "%s%s%s" % (self.answerPath, self.problemName, '_checker')
        FileTools.CopyFile(copyCommand, 'checker')
        
        call('./checker 1>result.txt', shell = True)
        
        score = self.GetScore('result.txt')
        
        if score ==100:
            return ENUMResources.const.SOLVED, score
        else:
            return ENUMResources.const.WRONG_ANSWER, score
    
    def GradeSolutionMulti(self):
        count = 0
        
        _list = []
        append = _list.append
        
        answerOpenCommand = "%s%s%s" % (self.answerPath, self.problemName,
                                        FileNameNPathResources.const.DefaultOutputTotalResultFileName)
        
        stdLines = FileTools.ReadFileLines(FileNameNPathResources.const.OutputResultFileName)
        
        strip = string.rstrip
        
        loopCount = len(stdLines)
        caseCount = 1
        i = 0
        
        while i < loopCount:
            answerOpenCommand = "%s%s%s%i%s" % (self.answerPath,
                                                self.problemName,
                                                FileNameNPathResources.const.CaseFile,
                                                caseCount,
                                                FileNameNPathResources.const.OutputCaseName)
            answers = FileTools.ReadFileLines(answerOpenCommand)
            
            appendFlag = True
            
            for answer in answers:
                stdLine = strip(stdLines[i], '\r\n ')
                answerLine = strip(answer, '\r\n ')
                
                if stdLine != answerLine:
                    count += 1
                    if appendFlag:
                        append(str(i) + ' ')
                        appendFlag = False
                    
                i += 1
                
            if caseCount is self.caseCount:
                count += loopCount - i + 1
            
            caseCount += 1
                
        return self.GetSolutionScore(count, loopCount)
        
    def GradeCheckerMulti(self):
        count = 0
        
        _list = []
        append = _list.append
        
        command = GradingCommand.MakeMulticaseCommand(self.usingLang, self.version)
        
        copyCommand = "%s%s%s" % (self.answerPath, self.problemName, '_checker')
        
        FileTools.CopyFile(copyCommand, 'checker')
        
        for i in xrange(1, self.caseCount+1):
            copyCommand = "%s%s%s%i%s" % (self.answerPath, self.problemName,
                                          FileNameNPathResources.const.CaseFile, i,
                                          FileNameNPathResources.const.InputCaseName)
            FileTools.CopyFile(copyCommand,
                               FileNameNPathResources.const.InputCaseFilename)
            
            call(command, shell = True)
            
            call('./checker 1>result.txt', shell = True)
            
            if self.GetScore('result.txt') != 100:
                count += 1
                append(str(i) + ' ')
           
        if count == 0:
            return ENUMResources.const.SOLVED, 100
        
        else:
            self.MakeCaseList(_list)
            return ENUMResources.const.WRONG_ANSWER,\
                   int( ((self.caseCount - count) * 100) / self.caseCount )
        
    def MakeCaseList(self, _list):
        wf = open('caselist.txt', 'w')
            
        wf.writelines(_list)
                
        wf.close()

    def GetSolutionScore(self, count, lineCount):
        result = ENUMResources.const.SOLVED
        score = 100
        
        if count > 0:
            result = ENUMResources.const.WRONG_ANSWER
            score = int( ((len(lineCount) - count) * 100) / len(lineCount) )
            
        elif score < 0:
            return ENUMResources.const.WRONG_ANSWER, 0
        
        return result, score
            
    def GetScore(self, fileName):
        scores = FileTools.ReadFileLines('result.txt')
        
        return int(scores[0])