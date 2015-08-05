# -*- coding: utf-8 -*-
import os
import sys
import string
import ptrace
import resource
from FileTools import FileTools
from gradingResource.enumResources import ENUMResources
from gradingResource.listResources import ListResources
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
        
    def Execution(self):
        # copy input data
        if self.caseCount > 0:
            copyCommand = "%s%s%s" % (self.answerPath, self.problemName,
                                      FileNameNPathResources.const.DefaultInputTotalCaseFileName)
            FileTools.CopyFile(copyCommand, FileNameNPathResources.const.InputCaseFileName)
        
        # make execution command
        runCommandList = self.command.ExecuteCommand()
                
        pid = os.fork()
         
        if pid == 0:
            self.RunProgram(runCommandList)
        
        else:
            result, time, usingMem = self.WatchRunProgram(pid)
        
        userTime = int(time * 1000)
        
        if userTime > self.limitTime:
            result = ENUMResources.const.TIME_OVER
        
        elif (usingMem >> 10) > self.limitMemory:
             result = ENUMResources.const.MEMORY_OVERFLOW
        
        if not result:
            print ENUMResources.const.SERVER_ERROR, 0, 0, 0
            sys.exit()
        
        return result, userTime, usingMem
    
    def RunProgram(self, runCommandList):
        os.nice(19)
        
        reditectionSTDOUT = os.open(FileNameNPathResources.const.OutputResultFileName,
                                    os.O_RDWR|os.O_CREAT)
        os.dup2(reditectionSTDOUT,1)
        
        rlimTime = int(self.limitTime / 1000) + 1
        
        resource.setrlimit(resource.RLIMIT_CPU, (rlimTime,rlimTime))
        
        ptrace.traceme()
            
        os.execl(runCommandList[0], runCommandList[1], runCommandList[2])
            
    def WatchRunProgram(self, pid):
        usingMem = 0
        
        while True:
            wpid, status, res = os.wait4(pid,0)
    
            if os.WIFEXITED(status):
                return 'Grading', res[0], usingMem
            
            exitCode = os.WEXITSTATUS(status)
            
            if exitCode != 5 and exitCode != 0 and exitCode != 17:
                return ENUMResources.const.RUNTIME_ERROR, 0, 0 
                
            elif os.WIFSIGNALED(status):
                try:
                    ptrace.kill(pid)
                except Exception as e:
                    pass
                
                return ENUMResources.const.TIME_OVER, res[0], usingMem
            
            else:
                usingMem = self.GetUsingMemory(pid, usingMem)
                
                ptrace.syscall(pid, 0)
                
    def GetUsingMemory(self, pid, usingMem):
        procFileOpenCommand = "%s%i%s" % (FileNameNPathResources.const.ProcessDirName,
                                          pid,
                                          FileNameNPathResources.const.ProcessStatusFileName) 
        fileLines = FileTools.ReadFileLines(procFileOpenCommand)
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