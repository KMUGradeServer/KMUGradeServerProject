# -*- coding: utf-8 -*-
"""
    팀 초대 대기정보에 대한 모듈
"""


from sqlalchemy import Column, ForeignKey
from sqlalchemy.dialects.mysql import INTEGER, ENUM

from model import Base
from model.members import Members
from model.teams import Teams

from resource.enumResources import ENUMResources

class TeamInvitations(Base) :
    
    __tablename__ = 'TeamInvitations'
    
    teamIndex = Column(INTEGER(unsigned = True),
                       ForeignKey(Teams.teamIndex,
                                  onupdate = 'CASCADE',
                                  ondelete = 'CASCADE'),
                       primary_key = True,
                       autoincrement = False,
                       nullable = False)
    inviteeIdIndex = Column(INTEGER(unsigned = True),
                            ForeignKey(Members.memberIdIndex,
                                       onupdate = 'CASCADE',
                                       ondelete = 'CASCADE'),
                            primary_key = True,
                            autoincrement = False,
                            nullable = False)
    inviteeOrganizationIndex = Column(INTEGER(unsigned = True),
                                      ForeignKey(Members.organizationIndex,
                                                 onupdate = 'CASCADE',
                                                 ondelete = 'CASCADE'),
                                      primary_key = True,
                                      autoincrement = False,
                                      nullable = False)
    isAccept = Column(ENUM(ENUMResources().const.TRUE,
                           ENUMResources().const.FALSE),
                      default = ENUMResources().const.FALSE,
                      nullable = False)
