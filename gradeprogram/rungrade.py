# -*- coding: utf-8 -*-
import os
import sys
import logging
from grading import InterfaceGrade
from gradingResource.enumResources import ENUMResources
from gradingResource.fileNameNPathResources import FileNameNPathResources

if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)
    
    # save system args for list
    args = sys.argv
    
    if len(args) is not 11:
        print ENUMResources.const.SERVER_ERROR, 0, 0, 0
        sys.exit()
    
    logging.debug(args[3] + ' grading start')
    os.chdir(FileNameNPathResources.const.TempDirectory)

    grade = InterfaceGrade.InterfaceGrade(args)
    result = grade.compile()
    
    if result == ENUMResources.const.COMPILE_ERROR:
        print result, 0, 0, 0
        sys.exit()
    
    result, score, runTime, usingMem = grade.evaluation()