# -*- coding: utf-8 -*-
import sys
import logging
import CompileTools
from grading import GradingTools
from grading import ExecutionTools
from grading import ParameterSetting
from Languages import C_Command
from Languages import CPP_Command
from Languages import JAVA_Command
from Languages import PYTHON2_Command
from Languages import PYTHON3_Command
from gradingResource.listResources import ListResources

class InterfaceGrade(object):
    def __init__(self, args):
        self.parameter = ParameterSetting.ParameterSetting(args)
        
        if self.parameter.usingLang == ListResources.const.Lang_C:
            self.command = C_Command.C_Command(self.parameter.runFileName)
        elif self.parameter.usingLang == ListResources.const.Lang_CPP:
            self.command = CPP_Command.CPP_Command(self.parameter.runFileName)
        elif self.parameter.usingLang == ListResources.const.Lang_JAVA:
            self.command = JAVA_Command.JAVA_Command(self.parameter.runFileName)
        else:
            if self.parameter.version == ListResources.const.PYTHON_VERSION_TWO:
                self.command = PYTHON2_Command.PYTHON2_Command(self.parameter.runFileName)
            else:
                self.command = PYTHON3_Command.PYTHON3_Command(self.parameter.runFileName)
        
    def compile(self):
        logging.debug(self.parameter.saveDirectoryName + ' compile start')
        _compile = CompileTools.CompileTools(self.parameter, self.command)
        success = _compile.compileCode()
        
        logging.debug(self.parameter.saveDirectoryName + ' compile end')
        
        return success
        
    def evaluation(self):
        score = 0
        logging.debug(self.parameter.saveDirectoryName + ' execution start')
        
        execution = ExecutionTools.ExecutionTools(self.parameter, self.command)
            
        success, runTime, usingMem = execution.execution()
        logging.debug(self.parameter.saveDirectoryName + ' execution end')
        
        if success == 'Grading':
            logging.debug(self.parameter.saveDirectoryName + ' grade start')
            evaluation = GradingTools.GradingTools(self.parameter, self.command)
             
            success, score = evaluation.grade()
            logging.debug(self.parameter.saveDirectoryName + ' grade end')
            
        print success, score, runTime, usingMem
        sys.exit()