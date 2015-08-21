# -*- coding: utf-8 -*-
"""
    문제별 문제집에 대한 정보 모듈
"""


from sqlalchemy import Column, ForeignKey
from sqlalchemy.dialects.mysql import INTEGER

from model import Base
from model.problems import Problems
from model.problemSets import ProblemSets

class DetailsOfProblemSets (Base) :
    
    __tablename__ = 'DetailsOfProblemSets'
    
    problemSetIndex = Column(INTEGER(unsigned = True),
                             ForeignKey(ProblemSets.problemSetIndex,
                                        onupdate = 'CASCADE',
                                        ondelete = 'CASCADE'),
                             primary_key = True,
                             autoincrement = False,
                             nullable = False)
    problemId = Column(INTEGER(unsigned = True),
                       ForeignKey(Problems.problemIndex,
                                  onupdate = 'CASCADE',
                                  ondelete = 'CASCADE'),
                       primary_key = True,
                       autoincrement = False,
                       nullable = False)
