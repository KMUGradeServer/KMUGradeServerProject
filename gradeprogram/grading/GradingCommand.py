# -*- coding: utf-8 -*-
from gradingResource.listResources import ListResources

class GradingCommand(object):
    @staticmethod
    def MakeCompileCommand(usingLang, filePath):
        # make compile command 
        if usingLang == ListResources.const.Lang_C:
            return 'gcc *.c -o main -lm -w 2>error.err'
            
        elif usingLang == ListResources.const.Lang_CPP:
            return 'g++ *.cpp -o main -lm -w 2>error.err'
        
        elif usingLang == ListResources.const.Lang_JAVA:
            return 'javac -nowarn -d ./ *.java 2>error.err'
        
    @staticmethod
    def MakeExecuteCommand(usingLang, runFileName, version):
        # make execution command
        runCommandList = []
        append = runCommandList.append
        
        if usingLang == ListResources.const.Lang_PYTHON:
            if version == ListResources.const.PYTHON_VERSION_TWO:
                append('/usr/bin/python')
                append('/usr/bin/python')
                append(runFileName)
                
            elif version == ListResources.const.PYTHON_VERSION_THREE:
                append('/usr/local/bin/python3')
                append('/usr/local/bin/python3')
                append(runFileName)
                
        elif usingLang == ListResources.const.Lang_C or\
             usingLang == ListResources.const.Lang_CPP:
            append('./main')
            append('./main')
            
        elif usingLang == ListResources.const.Lang_JAVA:
            append('/usr/bin/java')
            append('/usr/bin/java')
            append(runFileName)
            
        return runCommandList
    
    @staticmethod
    def MakeMulticaseCommand(usingLang, version):
        # make execution command
        if usingLang == ListResources.const.Lang_PYTHON:
            if version == ListResources.const.PYTHON_VERSION_TWO:
                return "%s %s %s" % ('python', runFileName, '1>output.txt 2>core.err')
            elif version == ListResources.const.PYTHON_VERSION_THREE:
                return "%s %s %s" % ('python3', runFileName, '1>output.txt 2>core.err')
        
        elif usingLang == ListResources.const.Lang_C or\
             usingLang == ListResources.const.Lang_CPP:
            return './main 1>output.txt'
        
        elif usingLang == ListResources.const.Lang_JAVA:
            return "%s %s %s" % ('java', runFileName, '1>output.txt 2>core.err')