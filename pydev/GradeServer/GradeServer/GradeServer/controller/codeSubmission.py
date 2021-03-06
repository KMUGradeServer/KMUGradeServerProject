#-*- coding: utf-8 -*-

import os
import sys
import shutil
import glob
import re, time

from flask import Flask, request, redirect, url_for, session, flash
from werkzeug import secure_filename

from GradeServer.database import dao
from GradeServer.GradeServer_logger import Log
from GradeServer.GradeServer_blueprint import GradeServer
from GradeServer.utils.loginRequired import login_required
from GradeServer.GradeServer_config import GradeServerConfig
from GradeServer.utils.utilCodeSubmissionQuery import get_member_name, get_course_name, get_problem_name, get_submission_info, \
                                                      insert_submitted_files, get_used_language_index, insert_to_submissions, \
                                                      get_problem_info, get_used_language_version, delete_submitted_files_data
from GradeServer.utils.utilMessages import unknown_error, get_message
from GradeServer.utils.checkInvalidAccess import check_invalid_access
from GradeServer.resource.enumResources import ENUMResources
from GradeServer.resource.sessionResources import SessionResources
from GradeServer.resource.otherResources import OtherResources
from GradeServer.resource.routeResources import RouteResources
from GradeServer.resource.languageResources import LanguageResources

from sqlalchemy import and_, func, update
from GradeServer.tasks import Grade

# Initialize the Flask application
PATH = GradeServerConfig.CURRENT_FOLDER
def remove_space_in_problemName(problemId):
    problemName = get_problem_name(problemId)
    return problemName.replace(' ', '')


def make_path(PATH, memberId, courseId, problemId, problemName):
    memberName = get_member_name(memberId)
    courseName = get_course_name(courseId)
    filePath = '%s/%s_%s/%s_%s/%s_%s' %(PATH, courseId, courseName, memberId, memberName, problemId, problemName)
    tempPath = '%s/%s_%s/%s_%s/%s_%s_tmp' %(PATH, courseId, courseName, memberId, memberName, problemId, problemName)
    return filePath.replace(' ', ''), tempPath.replace(' ', '')


def make_problem_full_name(problemId, problemName):
    return '%s_%s' %(problemId, problemName)


def file_save(memberId, courseId, problemId, uploadFiles, tempPath, filePath):
    fileIndex = 1
    sumOfSubmittedFileSize = 0
    delete_submitted_files_data(memberId, problemId, courseId)
    for file in uploadFiles:
        fileName = secure_filename(file.filename)
        if len(fileName) == 1:
            fileName = file.filename.decode()
        file.save(os.path.join(tempPath, fileName))
        fileSize = os.stat(os.path.join(tempPath, fileName)).st_size
        insert_submitted_files(memberId, courseId, problemId, fileIndex, fileName, filePath, fileSize)
        fileIndex += 1
        sumOfSubmittedFileSize += fileSize
        
    return sumOfSubmittedFileSize
        
        
def send_to_celery(memberId, courseId, problemId, usedLanguageName, sumOfSubmittedFileSize, problemName, filePath, tempPath):
    usedLanguageIndex = get_used_language_index(usedLanguageName)
    usedLanguageVersion = get_used_language_version(courseId, usedLanguageIndex)
    submissionCount, solutionCheckCount, viewCount = get_submission_info(memberId, courseId, problemId)
    insert_to_submissions(courseId, memberId, problemId, submissionCount, solutionCheckCount, viewCount, usedLanguageIndex, sumOfSubmittedFileSize)
    problemPath, limitedTime, limitedMemory, solutionCheckType, isAllInputCaseInOneFile, numberOfTestCase, problemCasesPath = get_problem_info(problemId, problemName)
    problemFullName = make_problem_full_name(problemId, problemName)
    Grade.delay(str(filePath),
                str(problemPath),
                str(memberId),
                str(problemId),
                str(solutionCheckType),
                numberOfTestCase,
                limitedTime,
                limitedMemory,
                str(usedLanguageName),
                str(usedLanguageVersion),
                str(courseId),
                submissionCount,
                str(problemFullName))
    
    dao.commit()
    
    flash(LanguageResources.const.SubmissionSuccess[session['language']])
    os.system("rm -rf %s" % filePath)
    os.rename(tempPath, filePath)
    
    
def get_language_name(usedLanguageName, tests):
    if usedLanguageName == OtherResources.const.C:
        languageName = OtherResources.const.C_SOURCE_NAME

    if usedLanguageName == OtherResources.const.CPP:
        languageName = OtherResources.const.CPP_SOURCE_NAME

    if usedLanguageName == OtherResources.const.JAVA:
        className = re.search(OtherResources.const.JAVA_MAIN_CLASS, tests)
        try:
            languageName = OtherResources.const.JAVA_SOURCE_NAME %(className.group(1))
        except:
            languageName = OtherResources.const.MISS_CLASS_NAME

    if usedLanguageName == OtherResources.const.PYTHON:
        languageName = OtherResources.const.PYTHON_SOURCE_NAME

    return languageName


def write_code_in_file(tempPath):
    tests = request.form[OtherResources.const.GET_CODE]
    unicode(tests)
    tests = tests.replace(OtherResources.const.LINUX_NEW_LINE, OtherResources.const.WINDOWS_NEW_LINE)
    usedLanguageName = request.form[OtherResources.const.LANGUAGE]
    
    fileName = get_language_name(usedLanguageName, tests)
    fout = open(os.path.join(tempPath, fileName), 'w')
    fout.write(tests)
    fout.close()

    return usedLanguageName, fileName


def page_move(courseId, pageNum, browserName = None, browserVersion = None):
    if (browserName == 'msie' and len(browserVersion) != 4) or browserName == None:
        return redirect(url_for(RouteResources.const.PROBLEM_LIST,
                                courseId = courseId,
                                pageNum = pageNum))
    return "0"


def submit_error(tempPath, courseId, pageNum, error, browserName = None, browserVersion = None):
    os.system("rm -rf %s" % tempPath)
    flash(get_message(error))
    return page_move(courseId, pageNum, browserName, browserVersion)


@GradeServer.route('/problem_<courseId>_<problemId>_<pageNum>_<browserName>_<browserVersion>', methods = ['POST'])
@check_invalid_access
@login_required
def to_process_uploaded_files(courseId, problemId, pageNum, browserName, browserVersion):
    memberId = session[SessionResources.const.MEMBER_ID]
    problemName = remove_space_in_problemName(problemId)
    filePath, tempPath = make_path(PATH, memberId, courseId, problemId, problemName)
    try:
        os.mkdir(tempPath)
        uploadFiles = request.files.getlist(OtherResources.const.GET_FILES)
        usedLanguageName = request.form[OtherResources.const.USED_LANGUAGE_NAME]
        sumOfSubmittedFileSize = file_save(memberId, courseId, problemId, uploadFiles, tempPath, filePath)
        send_to_celery(memberId, courseId, problemId, usedLanguageName, sumOfSubmittedFileSize, problemName, filePath, tempPath)
        Log.info("file submitted")
    except OSError as e:
        Log.error(str(e))
        submit_error(tempPath, courseId, pageNum, 'fileError', browserName, browserVersion)
    except Exception as e:
        dao.rollback()
        Log.error(str(e))
        submit_error(tempPath, courseId, pageNum, 'dbError', browserName, browserVersion)
        
    time.sleep(0.4)
    
    return page_move(courseId, pageNum, browserName, browserVersion)
    
    
@GradeServer.route('/problem_<courseId>_page<pageNum>_<problemId>', methods = ['POST'])
@check_invalid_access
@login_required
def to_process_written_code(courseId, pageNum, problemId):
    memberId = session[SessionResources.const.MEMBER_ID]
    problemName = remove_space_in_problemName(problemId)
    filePath, tempPath = make_path(PATH, memberId, courseId, problemId, problemName)
    try:
        os.mkdir(tempPath)
        usedLanguageName, fileName = write_code_in_file(tempPath)
        fileSize = os.stat(os.path.join(tempPath, fileName)).st_size
        fileIndex = 1
        delete_submitted_files_data(memberId, problemId, courseId)
        insert_submitted_files(memberId, courseId, problemId, fileIndex, fileName, filePath, fileSize)
        send_to_celery(memberId, courseId, problemId, usedLanguageName, fileSize, problemName, filePath, tempPath)
        Log.info("writed code is submitted")
    except OSError as e:
        Log.error(str(e))
        submit_error(tempPath, courseId, pageNum, 'fileError')
    except Exception as e:
        dao.rollback()
        Log.error(str(e))
        submit_error(tempPath, courseId, pageNum, 'dbError')
        
    time.sleep(0.4)
    
    return page_move(courseId, pageNum)
