# -*- coding: utf-8 -*-
import os
import sys
import glob
from subprocess import call
from FileTools import FileTools
from GradingCommand import GradingCommand
from gradingResource.listResources import ListResources
from gradingResource.enumResources import ENUMResources
from gradingResource.fileNameNPathResources import FileNameNPathResources

class CompileTools(object):
    def __init__(self, filePath, usingLang, version, runFileName):
        self.filePath = filePath
        self.usingLang = usingLang
        self.version = version
        self.runFileName = runFileName
        
    def CompileCode(self):
        fileList = glob.glob(self.filePath + FileNameNPathResources.const.AllFile)
        
        if len(fileList) is 0:
            print ENUMResources.const.SERVER_ERROR, 0, 0, 0
            sys.exit()
            
        FileTools.CopyAllFile(fileList, os.getcwd())
        
        if self.usingLang == ListResources.const.Lang_PYTHON:
            return True
            
        # make compile command
        command = GradingCommand.MakeCompileCommand(self.usingLang, self.filePath)
        
        # code compile
        call(command, shell = True)
        
        # check compile error
        if os.path.getsize(FileNameNPathResources.const.CompileErrorFileName) > 0:
            print ENUMResources.const.COMPILE_ERROR, 0, 0, 0
            sys.exit()
        
        # if not make execution file
        elif os.path.exists(self.runFileName) or os.path.exists(self.runFileName + '.class'):
            return True
        
        else:
            print ENUMResources.const.SERVER_ERROR, 0, 0, 0
            sys.exit()