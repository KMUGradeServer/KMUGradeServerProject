# -*- coding: utf-8 -*-
"""
  게시판 글 좋아요 정보 모듈
"""


from sqlalchemy import Column, ForeignKey
from sqlalchemy.dialects.mysql import INTEGER, ENUM

from model import Base
from model.articlesOnBoard import ArticlesOnBoard
from model.members import Members
from resource.enumResources import ENUMResources

class LikesOnBoard(Base) :
    
    __tablename__ = 'LikesOnBoard'
    
    articleIndex = Column(INTEGER(unsigned = True),
                          ForeignKey(ArticlesOnBoard.articleIndex,
                                     onupdate = 'CASCADE',
                                     ondelete = 'CASCADE'),
                          primary_key = True,
                          autoincrement = False,
                          nullable = False)
    boardLikerIdIndex = Column(INTEGER(unsigned = True),
                               ForeignKey(Members.memberIdIndex,
                                          onupdate = 'CASCADE',
                                          ondelete = 'CASCADE'),
                               primary_key = True,
                               autoincrement = False,
                               nullable = False)
    boardLikerOrganizationIndex = Column(INTEGER(unsigned = True),
                                         ForeignKey(Members.organizationIndex,
                                                    onupdate = 'CASCADE',
                                                    ondelete = 'CASCADE'),
                                         primary_key = True,
                                         autoincrement = False,
                                         nullable = False)
    isLikeCancelled = Column(ENUM (ENUMResources().const.TRUE,
                                   ENUMResources().const.FALSE),
                             default = ENUMResources().const.FALSE,
                             nullable =False)
    
