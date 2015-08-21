# -*- coding: utf-8 -*-
"""
   사용자 별 등록된 과목 관계
"""


from sqlalchemy import Column, ForeignKey
from sqlalchemy.dialects.mysql import INTEGER

from model import Base
from model.members import Members
from model.registeredCourses import RegisteredCourses

class Registrations(Base) :
    
    __tablename__ = 'Registrations'
    
    memberIdIndex = Column(INTEGER(unsigned = True),
                           ForeignKey(Members.memberIdIndex,
                                      onupdate = 'CASCADE',
                                      ondelete = 'CASCADE'),
                           primary_key = True,
                           autoincrement = False,
                           nullable = False)
    organizationIndex = Column(INTEGER(unsigned = True),
                               ForeignKey(Members.organizationIndex,
                                          onupdate = 'CASCADE',
                                          ondelete = 'CASCADE'),
                               primary_key = True,
                               autoincrement = False,
                               nullable = False)
    courseIndex = Column(INTEGER(unsigned = True),
                         ForeignKey(RegisteredCourses.courseIndex,
                                    onupdate = 'CASCADE',
                                    ondelete = 'CASCADE'),
                         primary_key = True,
                         autoincrement = False,
                         nullable = False)
    chanceCount = Column(INTEGER(unsigned = True),
                         default = 2,
                         nullable = False)
