# -*- coding: utf-8 -*-
"""
    GradeServer.utils
    ~~~~~~~~~~~~~~

    GradeSever에 적용될  DepartmentParameter 대한 패키지 초기화 모듈.

    :copyright: (c) 2015 kookminUniv
    :@author: algolab
"""
    
class DepartmentParameter:
    departmentIndex = None
    departmentName = None
    
    def __init__(self, departmentIndex = None, departmentName = None):
        self.departmentIndex = departmentIndex
        self.departmentName = departmentName