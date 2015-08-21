# -*- coding: utf-8 -*-
"""
  과목별 등록 된 문제에 대한 정보 모듈
"""


from sqlalchemy import Column, ForeignKey
from sqlalchemy.dialects.mysql import INTEGER, DATETIME, ENUM

from model import Base
from model.problems import Problems
from model.registeredCourses import RegisteredCourses

from resource.enumResources import ENUMResources

class RegisteredProblems(Base) :
    
    __tablename__ = 'RegisteredProblems'
    
    problemIndex = Column(INTEGER(unsigned = True),
                          ForeignKey(Problems.problemIndex,
                                     onupdate = 'CASCADE',
                                     ondelete = 'CASCADE'),
                          autoincrement = False,
                          primary_key = True,
                          nullable = False)
    courseIndex = Column(INTEGER(unsigned = True),
                         ForeignKey(RegisteredCourses.courseIndex,
                                    onupdate = 'CASCADE',
                                    ondelete = 'CASCADE'),
                         autoincrement = False,
                         primary_key = True,
                         nullable = False)
    isAllInputCaseInOneFile = Column(ENUM(ENUMResources().const.TRUE, 
                                          ENUMResources().const.FALSE), 
                                     default = ENUMResources().const.TRUE, 
                                     nullable = False)
    limitedFiles = Column(INTEGER(unsigned = True),
                           default = 5,
                           nullable = False)
    numberOfTestCase  = Column(INTEGER(unsigned = True),
                               default = 0,
                               nullable = False)
    openDate = Column(DATETIME,
                      nullable = False)
    closeDate = Column(DATETIME,
                       nullable = False)
    startDateOfSubmission = Column(DATETIME,
                                   nullable = False)
    endDateOfSubmission = Column(DATETIME,
                                 nullable = False)
    isDeleted = Column(ENUM(ENUMResources().const.TRUE,
                            ENUMResources().const.FALSE),
                       default = ENUMResources().const.FALSE,
                       nullable = False)
    
