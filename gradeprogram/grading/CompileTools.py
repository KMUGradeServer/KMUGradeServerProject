# -*- coding: utf-8 -*-
import os
import sys
import glob
from subprocess import call
from FileTools import FileTools
from gradingResource.enumResources import ENUMResources
from gradingResource.fileNameNPathResources import FileNameNPathResources

class CompileTools(object):
    def __init__(self, parameter, command):
        self.filePath = parameter.filePath
        self.usingLang = parameter.usingLang
        self.version = parameter.version
        self.runFileName = parameter.runFileName
        self.command = command
        
    def CompileCode(self):
        fileList = glob.glob(self.filePath + FileNameNPathResources.const.AllFile)
        
        if len(fileList) is 0:
            print ENUMResources.const.SERVER_ERROR, 0, 0, 0
            sys.exit()
            
        FileTools.CopyAllFile(fileList, os.getcwd())
            
        # make compile command
        command = self.command.CompileCommand()
        
        if command is 'py':
            return True
        
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