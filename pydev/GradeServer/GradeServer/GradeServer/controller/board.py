# -*- coding: utf-8 -*-
'''
    GradeSever.controller.board
    ~~~~~~~~~~~~~~~~~~~~~~~~~

    로그인 확인 데코레이터와 로그인 처리 모듈.

   :copyright:(c) 2015 by KookminUniv

'''

import socket

from flask import render_template, request, session, redirect, url_for, flash
from datetime import datetime

from GradeServer.utils.loginRequired import login_required
from GradeServer.utils.checkInvalidAccess import check_invalid_access

from GradeServer.utils.utilPaging import get_page_pointed, get_page_record
from GradeServer.utils.utilMessages import unknown_error, get_message
from GradeServer.utils.utilArticleQuery import join_courses_names, select_articles, select_article, select_sorted_articles, select_article_is_like,\
                                               select_replies_on_board, select_replies_on_board_is_like, select_replies_on_board_like, update_view_reply_counting,\
                                               update_article_like_counting, update_article_is_like, update_replies_on_board_like_counting,\
                                               update_replies_on_board_is_like, update_replies_on_board_delete, update_replies_on_board_modify, update_article_delete,\
                                               insert_artitles_on_board, insert_likes_on_board, insert_replies_on_board, insert_likes_on_reply_of_board
from GradeServer.utils.utilQuery import select_accept_courses, select_count, select_current_courses

from GradeServer.utils.filterFindParameter import FilterFindParameter
from GradeServer.utils.memberCourseProblemParameter import MemberCourseProblemParameter
from GradeServer.utils.articleParameter import ArticleParameter
from GradeServer.utils.replyParameter import ReplyParameter

from GradeServer.resource.enumResources import ENUMResources
from GradeServer.resource.setResources import SETResources
from GradeServer.resource.htmlResources import HTMLResources
from GradeServer.resource.routeResources import RouteResources
from GradeServer.resource.otherResources import OtherResources
from GradeServer.resource.sessionResources import SessionResources
from GradeServer.resource.languageResources import LanguageResources

from GradeServer.database import dao
from GradeServer.GradeServer_logger import Log
from GradeServer.GradeServer_blueprint import GradeServer 

@GradeServer.teardown_request
def close_db_session(exception = None):
    '''요청이 완료된 후에 db연결에 사용된 세션을 종료함'''
    try:
        dao.remove()
    except Exception as e:
        Log.error(str(e))


'''
게시판을 과목별 혹은 전체 통합으로
보여주는 페이지
'''
@GradeServer.route('/board/<activeTabCourseId>/page<int:pageNum>', methods = ['GET', 'POST'])
@check_invalid_access
@login_required
def board(activeTabCourseId, pageNum):    
    try:
        # 검색시 FilterCondition List
        Filters = ['모두', '작성자', '제목 및 내용']
        
                # 허용 과목 리스트
        myCourses = select_current_courses(select_accept_courses().subquery()).subquery()
        # TabActive Course or All Articles
        # get course or All Articles 
        articlesOnBoard = join_courses_names(# get TabActive Articles
                                             select_articles(activeTabCourseId = activeTabCourseId,
                                                             isDeleted = ENUMResources().const.FALSE).subquery(),
                                             myCourses).subquery()
                # 과목 공지글    
        try:  
            articleNoticeRecords = get_page_record((select_sorted_articles(articlesOnBoard,
                                                                           isNotice = ENUMResources().const.TRUE)),
                                                   pageNum = int(1),
                                                   LIST = OtherResources().const.NOTICE_LIST).all()
        except Exception:
            articleNoticeRecords = []
                # 과목 게시글
        try:
            if request.method == 'POST':
                Log.info(session[SessionResources().const.MEMBER_ID] + ' try keyword find in Board')
                try:
                    for form in request.form:
                        # FilterCondition
                        if 'keyWord' != form:
                            filterCondition = form
                            keyWord = request.form['keyWord']
                except Exception as e:
                    filterCondition = None
                    keyWord = None
                    
                    Log.info(session[SessionResources().const.MEMBER_ID] + e)
            else:
                filterCondition = None
                keyWord = None
                
            articlesOnBoardSub = select_sorted_articles(articlesOnBoard,
                                                        isNotice = ENUMResources().const.FALSE,
                                                        filterFindParameter = FilterFindParameter(filterCondition,
                                                                                                  keyWord))
            count = select_count(articlesOnBoardSub.subquery().\
                                                    c.articleIndex).first().\
                                                                    count
            articleRecords = get_page_record(articlesOnBoardSub,
                                             pageNum = pageNum,
                                             LIST = int(15)).all()
        except Exception:
            count = 0
            articleRecords = []
            
        try:
            myCourses = dao.query(myCourses).all()
        except Exception:
            myCourses = []
        # myCourses Default Add ALL
        myCourses.insert(0, OtherResources().const.ALL)
        
        return render_template(HTMLResources().const.BOARD_HTML,
                               SETResources = SETResources,
                               SessionResources = SessionResources,
                               LanguageResources = LanguageResources,
                               articleRecords = articleRecords,
                               articleNoticeRecords =  articleNoticeRecords,
                               myCourses = myCourses,
                               pages = get_page_pointed(pageNum,
                                                        count,
                                                        int(15)),
                               Filters = Filters,
                               activeTabCourseId = activeTabCourseId) # classType, condition은 검색 할 때 필요한 변수    
        
    except Exception:
        return unknown_error()


'''
게시판 공지만 과목별 혹은 전체 통합으로
보여주는 페이지
'''
@GradeServer.route('/notice/<activeTabCourseId>/page<int:pageNum>', methods = ['GET', 'POST'])
@check_invalid_access
@login_required
def article_notice(activeTabCourseId, pageNum):    
    try:
        # 검색시 FilterCondition List
        Filters = ['모두', '작성자', '제목 및 내용']
        
                # 허용 과목 리스트
        myCourses = select_current_courses(select_accept_courses().subquery()).subquery()
        # TabActive Course or All Articles
        # get course or All Articles 
        articlesOnBoard = join_courses_names(# get TabActive Articles
                                             select_articles(activeTabCourseId = activeTabCourseId,
                                                             isDeleted = ENUMResources().const.FALSE).subquery(),
                                             myCourses).subquery()
                # 과목 공지글 
        try:
            if request.method == 'POST':
                try:
                    for form in request.form:
                        # FilterCondition
                        if 'keyWord' != form:
                            filterCondition = form
                            keyWord = request.form['keyWord']
                except Exception:
                    filterCondition = None
                    keyWord = None
            else:
                filterCondition = None
                keyWord = None
                
            # Notices Sorted
            articleNoticeRecords = select_sorted_articles(articlesOnBoard,
                                                          isNotice = ENUMResources().const.TRUE,
                                                          filterFindParameter = FilterFindParameter(filterCondition,
                                                                                                    keyWord))
            # Get Notices count
            count = select_count(articleNoticeRecords.subquery().\
                                                      c.articleIndex).\
                                                      first().\
                                                      count
            # Get Notices in Page                                                                           
            articleNoticeRecords = get_page_record(articleNoticeRecords,
                                                   pageNum = pageNum).all()
        except Exception:
            count = 0
            articleNoticeRecords = []
            
        try:
            myCourses = dao.query(myCourses).all()
        except Exception:
            myCourses = []
        # myCourses Default Add ALL
        myCourses.insert(0, OtherResources().const.ALL)
        
        return render_template(HTMLResources().const.ARTICLE_NOTICE_HTML,
                               SETResources = SETResources,
                               SessionResources = SessionResources,
                               LanguageResources = LanguageResources,
                               articleNoticeRecords =  articleNoticeRecords,
                               myCourses = myCourses,
                               pages = get_page_pointed(pageNum,
                                                        count),
                               Filters = Filters,
                               activeTabCourseId = activeTabCourseId) # classType, condition은 검색 할 때 필요한 변수    
        
    except Exception:
        return 
                            


def temp():
    try:
        print "AAAAAAAAAAAAAAAA"
    except Exception:
        pass
    return unknown_error()
def temp2():
    print "BBBBBBBBBBBBBB"
    
'''
게시글을 눌렀을 때 
글 내용을 보여주는 페이지
'''
@GradeServer.route('/board/<activeTabCourseId>/<int:articleIndex>', methods = ['GET', 'POST'])
@check_invalid_access
@login_required
def read(activeTabCourseId, articleIndex, error = None):
    ''' when you push a title of board content '''
        
    try:
            # 내가 게시글에 누른 좋아요 정보
        try:
            isLikeCancelled = select_article_is_like(articleParameter = ArticleParameter(articleIndex = articleIndex,
                                                                                    boardLikerId = session[SessionResources().const.MEMBER_ID])).first().\
                                                                                                                                                 isLikeCancelled
        except Exception:
            # Non-Exist Case
            isLikeCancelled = None
            
        if request.method == 'POST':
            # flash message Init
            flashMsg =None
            for form in request.form:
                
                            # 게시글 좋아요  Push
                if form == 'articleLike':
                                    # 좋아요를 누른적 없을 때
                    if not isLikeCancelled:
                        # Counting +1
                        LIKE_INCREASE = 1
                    else:
                                        # 다시 좋아요 누를 때
                        if isLikeCancelled == ENUMResources().const.TRUE:
                            # Counting +1
                            LIKE_INCREASE = 1
                            isLikeCancelled = ENUMResources().const.FALSE
                                            # 좋아요 취소 할 때
                        else:  # if it's already exist then change the value of 'pushedLike'
                            # Counting -1
                            LIKE_INCREASE = -1
                            isLikeCancelled = ENUMResources().const.TRUE
                        
                    update_article_like_counting(articleParameter = ArticleParameter(articleIndex = articleIndex),
                                                 LIKE_INCREASE = LIKE_INCREASE)
                    if not isLikeCancelled:
                        # Insert Like
                        dao.add(insert_likes_on_board(articleIndex = articleIndex,
                                                      boardLikerId = session[SessionResources().const.MEMBER_ID]))
                    else:
                        # Update Like
                        update_article_is_like(articleParameter = ArticleParameter(articleIndex = articleIndex,
                                                                                   boardLikerId = session[SessionResources().const.MEMBER_ID]),
                                               isLikeCancelled = isLikeCancelled)
                    # remove duplicated read count
                    update_view_reply_counting(articleParameter = ArticleParameter(articleIndex = articleIndex),
                                               VIEW_INCREASE = -1)
                    
                    break 
                            # 댓글 달기
                elif form == 'writeArticleReply':
                                    # 새로운 댓글 정보
                    boardReplyContent = request.form['writeArticleReply']
                    
                    if boardReplyContent:
                        dao.add(insert_replies_on_board(articleIndex = articleIndex,
                                                       boardReplierId = session[SessionResources().const.MEMBER_ID],
                                                       boardReplyContent = boardReplyContent,
                                                       boardReplierIp = socket.gethostbyname(socket.gethostname()),
                                                       boardRepliedDate = datetime.now()))
                        # remove duplicated read count
                        update_view_reply_counting(articleParameter = ArticleParameter(articleIndex = articleIndex),
                                                   VIEW_INCREASE = -1,
                                                   REPLY_INCREASE = 1)
                        
                        flashMsg =get_message('writtenComment')
                    else:
                        error = 'data' + get_message('fillData')
                        
                    break 
                            # 댓글 좋아요
                elif 'articleReplyLike' in form:  # the name starts with 'articleReplyLike' and it has its unique number
                    idIndex = len('articleReplyLike')
                                    # 내가 게시글에 누른 좋아요 정보
                    try:
                        isReplyLike = select_replies_on_board_is_like(replyParameter = ReplyParameter(boardReplyIndex = int(form[idIndex:]),
                                                                                                      boardReplyLikerId = session[SessionResources().const.MEMBER_ID])).first().\
                                                                                                                                                                        isLikeCancelled
                    except Exception:
                        # Non-Exist Case
                        isReplyLike = None
                                    # 좋아요를 누른적 없을 때
                    if not isReplyLike:
                        # Counting +1
                        LIKE_INCREASE = 1
                    else:
                                        # 다시 좋아요 누를 때
                        if isReplyLike == ENUMResources().const.TRUE:
                            # Counting +1
                            LIKE_INCREASE = 1
                            isLikeCancelled = ENUMResources().const.FALSE
                                            # 좋아요 취소 할 때
                        else:  # if it's already exist then change the value of 'pushedLike'
                            # Counting -1
                            LIKE_INCREASE = -1
                            isLikeCancelled = ENUMResources().const.TRUE
                            
                    # Like or UnLIke
                    update_replies_on_board_like_counting(replyParameter = ReplyParameter(boardReplyIndex = int(form[idIndex:])),
                                                          LIKE_INCREASE = LIKE_INCREASE)
                    if not isReplyLike:
                        # Insert Like
                        dao.add(insert_likes_on_reply_of_board(boardReplyIndex = int(form[idIndex:]),
                                                               boardReplyLikerId = session[SessionResources().const.MEMBER_ID]))
                    else:
                        # Update Like
                        update_replies_on_board_is_like(replyParameter = ReplyParameter(boardReplyIndex = int(form[idIndex:]),
                                                                                        boardReplyLikerId = session[SessionResources().const.MEMBER_ID]),
                                                        isLikeCancelled = isLikeCancelled)
                    # remove duplicated read count
                    update_view_reply_counting(articleParameter = ArticleParameter(articleIndex = articleIndex),
                                               VIEW_INCREASE = -1)
                    
                    break 
                            # 댓글 삭제   
                elif 'deleteArticleReply' in form:
                    idIndex = len('deleteArticleReply')
                    
                    update_replies_on_board_delete(replyParameter = ReplyParameter(boardReplyIndex = int(form[idIndex:])),
                                                   isDeleted = ENUMResources().const.TRUE)
                    # remove duplicated read count
                    update_view_reply_counting(articleParameter = ArticleParameter(articleIndex = articleIndex),
                                               VIEW_INCREASE = -1,
                                               REPLY_INCREASE = -1)
                    
                    flashMsg = get_message('deletedComment')
                    
                    break 
                # Commit Modify
                elif 'modifyArticleReplyContent' in form:
                    idIndex = len('modifyArticleReplyContent')
                    boardReplyContent = request.form['modifyArticleReplyContent' + form[idIndex:]]
                    
                    if boardReplyContent:
                        #update comment
                        update_replies_on_board_modify(replyParameter = ReplyParameter(boardReplyIndex = int(form[idIndex:]),
                                                                                       boardReplyLikerId = None,
                                                                                       boardReplyContent = boardReplyContent))
                        # remove duplicated read count
                        update_view_reply_counting(articleParameter = ArticleParameter(articleIndex = articleIndex),
                                                   VIEW_INCREASE = -1)
                        
                       
                        flashMsg =get_message('modifiedComment')
                    else:
                        error = 'data' + get_message('fillData')
                        
                    break
                
                            # 게시물 삭제
                elif form == 'deleteArticle':
    
                        update_article_delete(articleParameter = ArticleParameter(articleIndex = articleIndex),
                                              isDeleted = ENUMResources().const.TRUE)                    
                        # Commit Exception
                        try:
                            dao.commit()
                            flash(get_message('deletedPost'))
                        except Exception:
                            dao.rollback()
                            error = get_message('updateFailed')
                            
                        return redirect(url_for(RouteResources().const.BOARD,
                                                activeTabCourseId = OtherResources().const.ALL,
                                                pageNum = 1))
            # end Loop
            # Commit Exception
            try:
                dao.commit()
                # if flash Message exist
                if flashMsg:
                    flash(flashMsg)
            except Exception:
                dao.rollback()
                error = get_message('updateFailed')
            
            # 게시글 정보
        try:
            articlesOnBoard = select_article(articleParameter = ArticleParameter(articleIndex = articleIndex),
                                             isDeleted = ENUMResources().const.FALSE)
                
            articlesOnBoard = join_courses_names(articlesOnBoard.subquery(), 
                                                 select_current_courses(select_accept_courses().subquery()).subquery()).first()
        except Exception:
            articlesOnBoard = []
            
        try:
            # replies 정보
            repliesOnBoardRecords = select_replies_on_board(articleParameter = ArticleParameter(articleIndex = articleIndex),
                                                            isDeleted = ENUMResources().const.FALSE)
                    # 내가 게시글 리플에 누른 좋아요 정보
            repliesOnBoardIsLikeRecords = select_replies_on_board_like(repliesOnBoardRecords.subquery(),
                                                                       memberCourseProblemParameter = MemberCourseProblemParameter(memberId = session[SessionResources().const.MEMBER_ID])).all()
        except Exception:
            repliesOnBoardIsLikeRecords = []
            
        try:
            repliesOnBoardRecords = repliesOnBoardRecords.all()
        except Exception:
            repliesOnBoardRecords = []
            
                # 나의 댓글 좋아요 여부 적용
        subIndex = 0
        isLikeRecords = []
        
        for i in range(0, len(repliesOnBoardRecords)):
                # 나의 댓글 좋아요 정보 비교
            isLikeRecords.append(ENUMResources().const.TRUE)
            for j in range(subIndex, len(repliesOnBoardIsLikeRecords)):
                if repliesOnBoardRecords[i].boardReplyIndex == repliesOnBoardIsLikeRecords[j].boardReplyIndex:
                    isLikeRecords[i] = repliesOnBoardIsLikeRecords[j].isLikeCancelled
                                        # 다음 시작 루프 인덱스 변경
                    subIndex = j
                    
                    break 
            
            # 읽은 횟수 카운팅
        update_view_reply_counting(articleParameter = ArticleParameter(articleIndex = articleIndex),
                                   VIEW_INCREASE = 1)
        
        # Commit Exception
        try:
            dao.commit()
        except Exception:
            dao.rollback()
            
        return render_template(HTMLResources().const.ARTICLE_READ_HTML,
                               SETResources = SETResources,
                               SessionResources = SessionResources,
                               LanguageResources = LanguageResources,
                               articlesOnBoard = articlesOnBoard,
                               activeTabCourseId = activeTabCourseId,
                               repliesOnBoardRecords = repliesOnBoardRecords,
                               isLikeRecords = isLikeRecords,
                               isLikeCancelled = isLikeCancelled,
                               error = error)
    except Exception:
        # Exception View    
        return redirect(url_for(RouteResources().const.BOARD,
                                activeTabCourseId = OtherResources().const.ALL,
                                pageNum = 1))


'''
게시판에 글을 쓰는 페이지
'''
@GradeServer.route('/board/write-<activeTabCourseId>/<int:articleIndex>', methods=['GET', 'POST'])
@check_invalid_access
@login_required
def write(activeTabCourseId, articleIndex, error =None):
    title, content, articlesOnBoard = None, None, None
    try:
        # 수강  과목 정보
        myCourses = select_current_courses(select_accept_courses().subquery()).subquery()
        
        # Modify Case
        if articleIndex > 0: 
            try:
                articlesOnBoard = join_courses_names(select_article(articleParameter = ArticleParameter(articleIndex = articleIndex),
                                                                    isDeleted = ENUMResources().const.FALSE).subquery(),
                                                     myCourses).first()
            except Exception:
                articlesOnBoard = []
                        
        try:
            myCourses = dao.query(myCourses).all()
        except Exception:
            myCourses = []
                # 작성시 빈칸 검사
        if request.method == 'POST':
            # Not None
            try:
                courseId = request.form['courseId']
                # request.form['courseId']가 ex)2015100101 전산학 실습 일경우 중간의 공백을 기준으로 나눔
                courseId = courseId.split()[0]
                if courseId == OtherResources().const.ALL:
                    courseId = None
                    
                                # 타이틀 가져오기
                title = request.form['title']
                # Get Exist Content
                content = request.form['content']
            
                if not title:
                    error ='제목' +get_message('fillData')
                elif not request.form['content']:
                    error ='내용' +get_message('fillData')
                elif len(title) > 50:
                    error = 'Title is too long. please write less than 50 letters'
                # All Fill InputText
                else:
                    isNotice = ENUMResources().const.TRUE
                    currentDate = datetime.now()
                    currentIP = socket.gethostbyname(socket.gethostname())
                                        # 새로 작성
                    if articleIndex == 0:
                        # Set isNotice
                        if SETResources().const.USER in session['authority']: 
                            isNotice = ENUMResources().const.FALSE
                            # user None courseId reject 
                            
                        newPost = insert_artitles_on_board(problemId = None,
                                                           courseId = courseId,
                                                           writerId = session[SessionResources().const.MEMBER_ID],
                                                           isNotice = isNotice,
                                                           title = title,
                                                           content = content,
                                                           writtenDate = currentDate,
                                                           writerIp = currentIP)
                        dao.add(newPost)
                        # Commit Exception
                        try:
                            dao.commit()
                            flash(get_message('writtenPost'))
                        except Exception:
                            dao.rollback()
                            error =get_message('updateFailed')
                            
                        return redirect(url_for(RouteResources().const.BOARD,
                                                activeTabCourseId = activeTabCourseId,
                                                pageNum = 1))
                                        # 게시물 수정    
                    else:
                                                # 수정 할 글 정보
                        articlesOnBoard = select_article(articleParameter = ArticleParameter(articleIndex = articleIndex),
                                                         isDeleted = ENUMResources().const.FALSE).update(dict(courseId = courseId,
                                                                                                              title = title,
                                                                                                              content = content,
                                                                                                              writtenDate = currentDate,
                                                                                                              writerIp = currentIP))
                        
                        # Commit Exception
                        try:
                            dao.commit()
                            flash(get_message('modifiedPost'))
                        except Exception:
                            dao.rollback()
                            error =get_message('updateFailed')
                        
                        return redirect(url_for(RouteResources().const.ARTICLE_READ,
                                                activeTabCourseId = activeTabCourseId,
                                                articleIndex = articleIndex))
            except Exception:
                # User None Course Posting Rejection
                if SETResources().const.USER in session['authority']:
                    error = get_message('banPosting')
                else:
                    error = get_message()
            
                
        return render_template(HTMLResources().const.ARTICLE_WRITE_HTML,
                               SETResources = SETResources,
                               SessionResources = SessionResources,
                               LanguageResources = LanguageResources,
                               myCourses = myCourses,
                               articlesOnBoard = articlesOnBoard,
                               title = title,
                               content = content,
                               error = error)
    except Exception:
        # Unknown Error
        return unknown_error()