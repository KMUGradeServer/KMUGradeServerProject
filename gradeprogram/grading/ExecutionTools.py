# -*- coding: utf-8 -*-
import os
import sys
import signal
import string
import ptrace
import resource
from FileTools import FileTools
from gradingResource.enumResources import ENUMResources
from gradingResource.fileNameNPathResources import FileNameNPathResources

RUN_COMMAND_LIST = []

class ExecutionTools(object):
    def __init__(self, parameter, command):
        self.usingLang = parameter.usingLang
        self.limitTime = parameter.limitTime
        self.limitMemory = parameter.limitMemory
        self.answerPath = parameter.answerPath
        self.runFileName = parameter.runFileName
        self.problemName = parameter.problemName
        self.caseCount = parameter.caseCount
        self.command = command
        
    def execution(self):
        # copy input data
        if self.caseCount > 0:
            copyCommand = "%s%s%s" % (self.answerPath, self.problemName,
                                      FileNameNPathResources.const.DefaultInputTotalCaseFileName)
            FileTools.copyFile(copyCommand, FileNameNPathResources.const.InputCaseFileName)
        
        # make execution command
        runCommandList = self.command.ExecuteCommand()
                
        pid = os.fork()
         
        if pid == 0:
            self.runProgram(runCommandList)
        
        else:
            result, time, usingMem = self.watchRunProgram(pid)
        
        userTime = int(time * 1000)
        
        if result == 'Grading':
        
            if userTime > self.limitTime:
                result = ENUMResources.const.TIME_OVER
        
            elif (usingMem >> 10) > self.limitMemory:
                 result = ENUMResources.const.MEMORY_OVERFLOW
        
        elif not result:
            print ENUMResources.const.SERVER_ERROR, 0, 0, 0
            sys.exit()
        
        return result, userTime, usingMem
    
    def runProgram(self, runCommandList):
        os.nice(19)
        
        reditectionSTDOUT = os.open(FileNameNPathResources.const.OutputResultFileName,
                                    os.O_RDWR|os.O_CREAT)
        os.dup2(reditectionSTDOUT,1)
        
        soft, hard = resource.getrlimit(resource.RLIMIT_CPU)
        rlimTime = int(self.limitTime / 1000) + 1
        
        resource.setrlimit(resource.RLIMIT_CPU, (rlimTime,hard))
        
        ptrace.traceme()
            
        os.execl(runCommandList[0], runCommandList[1], runCommandList[2])
            
    def watchRunProgram(self, pid):
        usingMem = 0
        
        while True:
            wpid, status, res = os.wait4(pid,0)
            signal.signal(signal.SIGXCPU, self.sigHandler)
    
            if os.WIFEXITED(status):
                return 'Grading', res[0], usingMem
            
            exitCode = os.WEXITSTATUS(status)
            
            if  exitCode is 24:
                return ENUMResources.const.TIME_OVER, res[0], usingMem
            
            elif exitCode is not 5 and exitCode is not 0 and exitCode is not 17:
                return ENUMResources.const.RUNTIME_ERROR, 0, 0 
            
            elif os.WIFSIGNALED(status):
                try:
                    ptrace.kill(pid)
                except Exception as e:
                    pass
                
                return ENUMResources.const.RUNTIME_ERROR, 0, 0
            
            else:
                usingMem = self.getUsingMemory(pid, usingMem)
                
                ptrace.syscall(pid, 0)
                
    def getUsingMemory(self, pid, usingMem):
        procFileOpenCommand = "%s%i%s" % (FileNameNPathResources.const.ProcessDirName,
                                          pid,
                                          FileNameNPathResources.const.ProcessStatusFileName) 
        fileLines = FileTools.readFileLines(procFileOpenCommand)
        split = string.split

        for i in xrange(10,15):
            index = fileLines[i].find('VmPeak')
            if index != -1:
                words = split(fileLines[i])
                temp = int(words[index+1])
                break;
        
        if temp > usingMem:
            usingMem = temp
        
        return usingMem
    
    def sigHandler(self, sig, f):
        pass