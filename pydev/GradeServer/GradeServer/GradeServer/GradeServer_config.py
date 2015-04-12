# -*- coding: utf-8 -*-
"""
    photolog.photolog_config
    ~~~~~~~~

    photolog 디폴트 설정 모듈.
    photolog 어플리케이션에서 사용할 디폴트 설정값을 담고 있는 클래스를 정의함.

    :copyright: (c) 2013 by 4mba.
    :license: MIT LICENSE 2.0, see license for more details.
"""


class GradeServerConfig(object):
    #: 데이터베이스 연결 URL
    DB_URL= "mysql+mysqlconnector://root:rhflwma@127.0.0.1/GradeServer_DB"
    #: 사진 업로드 시 사진이 임시로 저장되는 임시 폴더
    TMP_FOLDER = 'resource/tmp/'
    #: 세션 타임아웃은 초(second) 단위(60분)
    PERMANENT_SESSION_LIFETIME = 60 * 60
    # 업로드 파일 경로
    UPLOAD_FOLDER = '/mnt/shared/Temp'
    #: 쿠기에 저장되는 세션 쿠키
    SESSION_COOKIE_NAME = 'GradeServer_session'
    #: 로그 레벨 설정
    LOG_LEVEL = 'debug'
    #: 디폴트 로그 파일 경로
    LOG_FILE_PATH = 'resource/log/GradeServer.log'
    #: 디폴트 SQLAlchemy trace log 설정
    DB_LOG_FLAG = 'True'
    #: 트위터에 등록된 photolog 어플리케이션 인증키 (https://dev.twitter.com/)
    TWIT_APP_KEY    = 'tha1vwfKSJ0jlDcdCryvag'
    TWIT_APP_SECRET = '84qXU6uv1XyDbM780civoBA7U4mnmKEQ0FnaBQn63go'
    #: 트위터 연동에 대한 콜백 서버 URL(포토로그 어플리케이션 루트 경로)
    TWIT_CALLBACK_SERVER = 'http://localhost:5000'
    #: 목록 페이징 설정
    PER_PAGE =8
    # list paging Conf
    PER_LIST =15
    


