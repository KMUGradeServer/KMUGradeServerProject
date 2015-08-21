# -*- coding: utf-8 -*-
"""
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~

    등록된 과목에서 사용하는 프로그래밍 언어 정보
"""


from sqlalchemy import Column, ForeignKey
from sqlalchemy.dialects.mysql import INTEGER

from model import Base
from model.registeredCourses import RegisteredCourses
from model.languages import Languages

class LanguagesOfCourses(Base) :
    
    __tablename__ = 'LanguagesOfCourses'
    
    courseIndex = Column(INTEGER(unsigned = True),
                         ForeignKey(RegisteredCourses.courseIndex,
                                    onupdate = 'CASCADE',
                                    ondelete = 'CASCADE'),
                         primary_key = True,
                         autoincrement = False,
                         nullable = False)
    languageIndex = Column(INTEGER(unsigned = True),
                           ForeignKey(Languages.languageIndex,
                                      onupdate = 'CASCADE',
                                      ondelete = 'CASCADE'),
                           primary_key = True,
                           autoincrement = False,
                           nullable = False)   
    
