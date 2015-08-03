# -*- coding: utf-8 -*-
from Language import Language

class C_Command(Language):
    def __init__(self, runFileName):
        Language.__init__(self, runFileName)
        
    def CompileCommand(self):
        return 'gcc *.c -o main -lm -w 2>error.err'
        
    def ExecuteCommand(self):
        runCommandList = []
        append = runCommandList.append

        append('./main')
        append('./main')
        append('')
            
        return runCommandList