# -*- coding: utf-8 -*-
"""
    GradeServer.utils
    ~~~~~~~~~~~~~~

    GradeSever에 적용될  CollegeParameter 대한 패키지 초기화 모듈.

    :copyright: (c) 2015 kookminUniv
    :@author: algolab
"""
    
class CollegeParameter:
    collegeIndex = None
    collegeName = None
    
    def __init__(self, collegeIndex = None, collegeName = None):
        self.collegeIndex = collegeIndex
        self.collegeName = collegeName