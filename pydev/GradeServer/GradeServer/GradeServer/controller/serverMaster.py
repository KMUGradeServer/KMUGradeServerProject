# -*- coding: utf-8 -*-
'''
    GradeSever.controller.serverMaster

    Functions for server administrator
    
    1. manage college & department
    2. manage course
    3. manage problem
    4. manage user
    5. manage service
    
    :author: seulgi choi
    :copyright: (c) 2015 by Algorithmic Engineering Lab at KOOKMIN University
'''

from flask import request, render_template, url_for, redirect, session
from sqlalchemy import func, and_, exc
from datetime import datetime
from werkzeug.security import generate_password_hash

from GradeServer.GradeServer_py3des import TripleDES

from GradeServer.utils.loginRequired import login_required
from GradeServer.utils.checkInvalidAccess import check_invalid_access

from GradeServer.utils.collegeParameter import CollegeParameter
from GradeServer.utils.departmentParameter import DepartmentParameter
from GradeServer.utils.utilUserQuery import join_member_informations
from GradeServer.utils.utilProblemQuery import select_problems
from GradeServer.utils.utilCourseQuery import select_registered_courses,\
                                             select_language_of_course,\
                                             insert_language_of_course,\
                                             insert_registered_course,\
                                             update_registered_course_deleted
from GradeServer.utils.utilCollegeDepartmentQuery import select_departments_of_college,\
                                                        select_college,\
                                                        select_colleges,\
                                                        select_department,\
                                                        select_departments,\
                                                        join_departments_of_colleges,\
                                                        update_college_abolished,\
                                                        update_department_abolished,\
                                                        insert_relation_in_college_department,\
                                                        insert_college,\
                                                        insert_department
from GradeServer.utils.utilQuery import select_count
from GradeServer.utils.utilPaging import get_page_pointed, get_page_record

from GradeServer.model.problems import Problems
from GradeServer.model.members import Members
from GradeServer.model.departments import Departments
from GradeServer.model.courses import Courses
from GradeServer.model.registeredCourses import RegisteredCourses
from GradeServer.model.languages import Languages
from GradeServer.model.colleges import Colleges
from GradeServer.model.departmentsDetailsOfMembers import DepartmentsDetailsOfMembers

from GradeServer.resource.setResources import SETResources
from GradeServer.resource.enumResources import ENUMResources
from GradeServer.resource.otherResources import OtherResources

from GradeServer.database import dao
from GradeServer.GradeServer_blueprint import GradeServer

import re
import zipfile
import os
import subprocess
import glob

projectPath='/mnt/shared'
problemsPath='%s/Problems' % (projectPath) # /mnt/shared/Problems
problemDescriptionsPath='%s/pydev/GradeServer/GradeServer/GradeServer/static/ProblemDescriptions' % (projectPath)
tmpPath='%s/tmp' % (projectPath)

# if there's additional difficulty then change the value 'numberOfDifficulty'
numberOfDifficulty=5
newUsers=[]
newColleges=[]
newDepartments=[]

currentTab='colleges'


def change_abolishment_of_department_true(collegeIndex, error = None):
    try:
        departments = select_departments_of_college(collegeIndex).all()
        '''
        !!TODO
        remove duplicated code
        '''
        '''
        When the parameter is departmentIndex,
        get_departments_of_college will be empty
        '''
        for _, departmentInfo in departments: 
            if departmentInfo.isAbolished == ENUMResources().const.FALSE:
                update_department_abolished(DepartmentParameter(departmentIndex = departmentInfo.departmentIndex),
                                            ENUMResources().const.TRUE)
                
                try:
                    dao.commit()
                except exc.SQLAlchemyError:
                    dao.rollback()
                    error='Error has been occurred while changing abolishment to TRUE'
                    break
        
    except Exception:
        error = 'Error has been occurred while searching departments'
        
    return error
                
                

def add_relation_in_college_department(collegeIndex, departmentIndex, error = None):
    
    try:
        dao.add(insert_relation_in_college_department(collegeIndex,
                                                      departmentIndex))
        dao.commit()
    except exc.SQLAlchemyError:
        dao.rollback()
        error='Error has been occurred while making new relation of department'
        
    return error
       
                        
                                            
def add_new_college(collegeCode, collegeName, error = None):
    
    try:
        dao.add(insert_college(collegeCode,
                               collegeName))
        dao.commit()
    except exc.SQLAlchemyError:
        dao.rollback()
        error='Error has been occurred while making new college'
        
    return error
                        
                        
def add_new_departments(departmentCode, departmentName, error = None):

    try:
        dao.add(insert_department(departmentCode,
                              departmentName))
        dao.commit()
    except exc.SQLAlchemyError:
        dao.rollback()
        error='Error has been occurred while making new department'
    
    return error
                        


def get_num_of_problems_in_difficulty(difficultyOfProblem):
    try:
        numOfProblems=dao.query(Problems.problemId).\
                          filter(Problems.problemId.\
                                          like(difficultyOfProblem + '%')).\
                          count()
    except:
        numOfProblems=-1
    
    return numOfProblems
                        
                          
                                         
def add_new_problem(newProblemInfo):
    error=None
    nextIndex, problemId, problemName, solutionCheckType,\
    limitedTime, limitedMemory, problemPath=newProblemInfo
    
    newProblem=Problems(problemIndex=nextIndex, 
                        problemId=problemId, 
                        problemName=problemName, 
                        solutionCheckType=solutionCheckType, 
                        limitedTime=limitedTime,
                        limitedMemory=limitedMemory, 
                        problemPath=problemPath)
    dao.add(newProblem)
    
    try:
        dao.commit()
    except exc.SQLAlchemyError:
        dao.rollback()
        error='Error has been occurred while adding new problem'
        
    return error


def get_num_of_problems():
    try:
        nextIndex=dao.query(Problems).\
                      count()
    except:
        nextIndex=0
        
    return nextIndex


def delete_member(memberId):
    '''
    !!TODO
    
    deletion from DB is not a good way
    keep the tuple and make the member's information invalidate
    '''
    error=None
    
    deleteTarget=dao.query(Members).\
                     filter(Members.memberId==memberId).\
                     first()
    dao.delete(deleteTarget)
    
    try:
        dao.commit()
    except exc.SQLAlchemyError:
        error='Error has been occurred while deleting member'
    
    return error
            
            

                                         
                                         
def get_department_name(departmentIndex, error = None):
    
    try:
        departmentName = select_department(DepartmentParameter(departmentIndex = departmentIndex)).first().\
                                                                                                   departmentName
    except:
        error='Error has been occurred while searching department name'
        
    return error, departmentName 
                        
                                                                 
def get_college_name(collegeIndex, error = None):
    
    try:
        collegeName = select_college(CollegeParameter(collegeIndex = collegeIndex)).first().\
                                                                                    collegeName
    except:
        error='Error has been occurred while searching college name'
        
    return error, collegeName 

                                         
def split_to_index_keyname_value(form):
    keyname,index=re.findall('\d+|\D+',form)
    return int(index), keyname, request.form[form]


def delete_problem(problemId):
    error=None
    
    dao.query(Problems).\
        filter(Problems.problemId==problemId).\
        update(dict(isDeleted=ENUMResources().const.TRUE))
        
    try:
        dao.commit()
    except exc.SQLAlchemyError:
        error='Error has been occurred while deleting problem'
    
    return error
                

def change_abolishment_relates_college(collegeIndex, error = None):
    try:
        update_college_abolished(CollegeParameter(collegeIndex = collegeIndex), 
                                 ENUMResources().const.TRUE)
        dao.commit()
    except exc.SQLAlchemyError:
        error = 'Error has been occurred while changing abolishment to TRUE'
        
    if not error:    
        error = change_abolishment_of_department_true(collegeIndex)
    
    return error


def handle_file_came_from_window(rowProblemName, decodedProblemName):
    '''
    @@ Make imitation of Original problem name
    
    Original problem name shows with question mark
    To find and change the name to decoded name, make fake temporary name
    '''
    
    # role of fake problem name
    byteString='?'*len(rowProblemName)

    error=change_directory_to(tmpPath)

    if not error:
        if rename_file('%s.txt'%byteString, '%s.txt'%decodedProblemName):
            return error
        
        '''
        @@ Rename PDF file name
        
        PDF file is optional so, doesn't block when error occurs.
        '''
        if rename_file('%s.pdf'%byteString, '%s.pdf'%decodedProblemName):
            return error
                        
        '''
        @@ Rename _SOLUTION or _CHECKER folder name
        
        Figure out its solution check type from folder name
        '''
        currentPath, error=get_current_path()
        if error: return error
        
        filesInCurrentDir=glob.glob(currentPath+'/*')
        solCheckType=None
        for name in filesInCurrentDir:
            if '_SOLUTION' in name:
                solCheckType='SOLUTION'
                break
            if '_CHECKER' in name:
                solCheckType='CHECKER'
                break
            
        if solCheckType:
            originalFolder='%s_%s' % (byteString, solCheckType)
            newFolder='%s_%s' % (decodedProblemName, solCheckType)
            
            if rename_file(originalFolder, newFolder): return error
                
        # If SOLUTION or CHEKER file doesn't exist then it's an error
        else:
            error='There is no \'SOLUTION\' or \'CHECKER\' directory'
        
    return error


def remove_space_from_names_in(path):
    error=change_directory_to(path)
    
    if not error:
        try:
            subprocess.call('for f in *;do mv "$f" `echo $f|sed "s/ //g"`;done',\
                            shell=True)
        except OSError:
            error='Error has been occurred while removing space on file names'
    
    return error


def attach_string_ahead_of(path, string):
    error=change_directory_to(path)
    
    try:
        subprocess.call('for f in *; do mv $f `echo $f|sed "s/\.*/%s_/"`;done' %\
                        (string), shell=True)
    except OSError:
        error='Error has been occurred while attaching string'
    
    return error


def get_current_path():
    error=None
    
    try:
        currentPath=os.getcwd()
    except OSError:
        error='Error has been occurred while getting current path'

    return currentPath, error                                        


def change_directory_to(path):
    error=None
    
    try:
        os.chdir(path)
    except OSError:
        error='Error has been occurred while changing directory'
    
    return error


def rename_file(fromA, toB):
    error=None
    
    try:
        subprocess.call('mv %s %s' % (fromA, toB), shell=True)
    except OSError:
        error='Error has been occurred while renaming file'
    
    return error


def add_new_departments_details_of_members(memberId, collegeIndex, departmentIndex):
    error=None

    departmentInformation=\
        DepartmentsDetailsOfMembers(memberId=memberId, 
                                    collegeIndex=collegeIndex, 
                                    departmentIndex=departmentIndex)
    dao.add(departmentInformation)
    
    try:
        dao.commit()
    except exc.SQLAlchemyError:
        dao.rollback()
        error='Error has been occurred while adding new departments details of members'
    
    return error
                

def add_new_language_of_course(courseNum, languageIndex, error = None):

    try:
        dao.add(insert_language_of_course(courseId = courseNum,
                                      languageIndex = languageIndex))
        dao.commit()
    except exc.SQLAlchemyError:
        dao.rollback()
        error='Error has been occurred while adding new language of course'
    
    return error
                
 
def register_new_course(courseId, courseName, courseDescription,
                                    startDateOfCourse, endDateOfCourse,
                                    courseAdministratorId, error = None):
    try:    
        dao.add(insert_registered_course(courseId,
                                         courseName,
                                         courseDescription,
                                         startDateOfCourse,
                                         endDateOfCourse,
                                         courseAdministratorId,
                                         'FALSE'))
        dao.commit()
    except exc.SQLAlchemyError:
        dao.rollback()
        error='Error has been occurred while registering new course'
    
    return error
            
                                          
@GradeServer.route('/master/manage_collegedepartment/page<int:collegePageNum>-<int:departmentPageNum>', methods=['GET', 'POST'])
@check_invalid_access
@login_required
def server_manage_collegedepartment(collegePageNum, departmentPageNum):
    global newColleges, newDepartments
    global currentTab
    
    error = None
    
    # moved from other page, then show 'college' tab
    if request.referrer.rsplit('/', 1)[1] != 'manage_collegedepartment':
        currentTab='colleges'
    
    try:
        allColleges = select_colleges()
        collegeCount = select_count(allColleges.subquery().\
                                                c.\
                                                collegeIndex).first().\
                                                              count
        allColleges = get_page_record(allColleges,
                                      pageNum = collegePageNum).all()                                       
    except exc.SQLAlchemyError:
        allColleges = []
        collegeCount = 0

    try:
        allDepartments = join_departments_of_colleges()
        departmentCount = select_count(allDepartments.subquery().\
                                                      c.\
                                                      departmentIndex).first().\
                                                      count
        allDepartments = get_page_record(allDepartments,
                                         pageNum = departmentPageNum).all()                                     
    except exc.SQLAlchemyError:
        allDepartments = []
        departmentCount = 0
           
    if request.method=='POST':
        # initialization
        isNewCollege=False
        isNewDepartment=False
        
        numberOfColleges=(len(request.form) - 1) / 2
        newCollege=\
            [['' for _ in range(2)] for __ in range(numberOfColleges + 1)]
            
        numberOfDepartments=(len(request.form) - 1) / 3
        newDepartment=\
            [['' for _ in range(3)] for __ in range(numberOfDepartments + 1)]
        
        for form in request.form:
            if 'addCollege' in request.form:
                isNewCollege=True
                if form != 'addCollege':
                    index, keyname, data=split_to_index_keyname_value(form)
                    if keyname=='collegeCode':
                        newCollege[index-1][0]=data
                    elif keyname=='collegeName':
                        newCollege[index-1][1]=data
            elif 'addDepartment' in request.form:
                isNewDepartment=True
                if form != 'addDepartment':
                    index, keyname, data=split_to_index_keyname_value(form)
                    if keyname=='departmentCode':
                        newDepartment[index-1][0]=data
                    elif keyname=='departmentName':
                        newDepartment[index-1][1]=data
                    elif keyname=='collegeIndex':
                        newDepartment[index-1][2]=data.split()[0]
            elif 'deleteCollege' in request.form:
                if 'college' in form:
                    currentTab='colleges'
                    collegeIndex=re.findall('\d+|\D+', form)[1]
                    if change_abolishment_relates_college(collegeIndex): break
            elif 'deleteDepartment' in request.form:
                if 'department' in form:
                    currentTab='departments'
                    departmentIndex=re.findall('\d+|\D+', form)[1]
                    if change_abolishment_of_department_true(departmentIndex): break
                    
        '''
        If there's an error, set flags to False so it will be reached 'return' command at the last in this function
        '''
        if error:
            isNewCollege=isNewDepartment=False
                    
        if isNewCollege:
            currentTab='colleges'
            
            for index in range(numberOfColleges):
                newColleges.append(newCollege[index])
            for newPart in newColleges:
                if newPart[1]:
                    if select_college(CollegeParameter(collegeIndex = None,
                                                       collegeName = newPart[1])).first():
                        try:
                            update_college_abolished(CollegeParameter(collegeIndex =None,
                                                                      collegeName = newPart[1]))
                            dao.commit()
                        except exc.SQLAlchemyError:
                            dao.rollback()
                            error = 'Error has been occurred while changing abolishment to FALSE'
                        break
                    
                    error=add_new_college(newPart[0], newPart[1])
                        
            newColleges=[]
        
        '''
        If There is an error while adding new college, isNewDepartment can never be 'True'
        So it doesn't need to change flag value
        '''
        if isNewDepartment:
            currentTab='departments'
            
            for index in range(numberOfDepartments):
                newDepartments.append(newDepartment[index])
                
            newDepartment=[]
            for newPart in newDepartments:
                if newPart[1]:
                    error=add_new_departments(newPart[0], newPart[1])
                    if error: break
                    
                    index=dao.query(func.max(Departments.departmentIndex)).\
                              scalar()
                    error=add_relation_in_college_department(newPart[2], index)
                        
            newDepartments=[]
            
        # if there's an error in the last loop, can't handle in the loop with current structure
        # So, needs additional code out of the loop 
        if not error:
            return redirect(url_for('.server_manage_collegedepartment',
                                    collegePageNum = collegePageNum,
                                    departmentPageNum = departmentPageNum))
            
    return render_template('/server_manage_collegedepartment.html', 
                           error=error, 
                           currentTab=currentTab,
                           allColleges=allColleges,
                           allDepartments=allDepartments,
                           collegePages = get_page_pointed(pageNum = collegePageNum,
                                                           count = collegeCount),
                           departmentPages = get_page_pointed(pageNum = departmentPageNum,
                                                              count = departmentCount))
        
        
@GradeServer.route('/master/manage_class/page<int:pageNum>', methods=['GET', 'POST'])
@check_invalid_access
@login_required
def server_manage_class(pageNum):       
    error=None
    
    try:
        courses = select_registered_courses()
        count = select_count(courses.subquery().\
                                     c.\
                                     courseId).first().\
                                               count
        courses = get_page_record(courses,
                                  pageNum = pageNum).all()
    except exc.SQLAlchemyError:
        courses = []
        count = 0
        
    try:
        languagesOfCourse = select_language_of_course().all()
    except exc.SQLAlchemyError:
        languagesOfCourse = []
        
    if request.method=='POST':
        for form in request.form:
            try:
                update_registered_course_deleted(form)
                dao.commit()
            except exc.SQLAlchemyError:
                dao.rollback()
                error = 'Error has been occurred while deleting registered course'
                
                break
            
        return redirect(url_for('.server_manage_class',
                                pageNum = pageNum))
    
    if not error:
        session['ownCourses'] = select_registered_courses().all()
    
    return render_template('/server_manage_class.html',
                           error=error,  
                           courses=courses,
                           languagesOfCourse = languagesOfCourse,
                           pages = get_page_pointed(pageNum = pageNum,
                                                    count = count))
    
    
@GradeServer.route('/master/add_class', methods=['GET', 'POST'])
@check_invalid_access
@login_required
def server_add_class():
    global projectPath
    error=None
    
    courseAdministrator=''
    courseDescription=''
    startDateOfCourse=''
    endDateOfCourse=''
    courseIndex=''
    courseName=''
    semester=1
    languages=[]
    
    try:
        allCourses =dao.query(Courses).\
                         all()
    except:
        error='Error has been occurred while searching courses'
    
    try:
        allLanguages=dao.query(Languages).\
                           all()
    except:
        error='Error has been occurred while searching languages'
    
    try:               
        allCourseAdministrators=dao.query(Members).\
                                    filter(Members.authority==\
                                           SETResources().const.COURSE_ADMINISTRATOR).\
                                    all()
    except:
        error='Error has been occurred while searching course administrators'
                        
    if request.method=='POST':
        courseAdministrator=request.form['courseAdministrator']
        semester=request.form['semester'] 
        courseDescription=request.form['courseDescription']
        startDateOfCourse=request.form['startDateOfCourse']
        endDateOfCourse=request.form['endDateOfCourse']
        courseIndex, courseName=request.form['courseId'].split(' ', 1)
        
        for form in request.form:
            if 'languageIndex' in form:
                languages.append(request.form[form].split('_'))
                
        if not courseIndex:
            error='You have to choose a class name'
        elif not courseAdministrator:
            error='You have to enter a manager'
        elif not semester:
            error='You have to choose a semester'
        elif not languages:
            error='You have to choose at least one language'
        elif not courseDescription:
            error='You have to enter a class description'
        elif not startDateOfCourse:
            error='You have to choose a start date'
        elif not endDateOfCourse:
            error='You have to choose a end date'
        else:
            startDate=datetime.strptime(startDateOfCourse, '%Y-%m-%d').date()
            endDate=datetime.strptime(endDateOfCourse, '%Y-%m-%d').date()
            if startDate > endDate:
                error='Start date should be earlier than end date'
            
            if not error:
                try:
                    dao.query(Members).\
                        filter(and_(Members.authority==SETResources().const.COURSE_ADMINISTRATOR,
                                    Members.memberId==courseAdministrator.split()[0])).\
                        first().memberId
                except:
                    error=\
                        '%s is not registered as a course administrator' %\
                        (courseAdministrator.split()[0])
            
            else:
                return render_template('/server_add_class.html', 
                                       error=error, 
                                       courseAdministrator=courseAdministrator,
                                       semester=semester,
                                       courseDescription=courseDescription,
                                       startDateOfCourse=startDateOfCourse,
                                       endDateOfCourse=endDateOfCourse,
                                       courseIndex=courseIndex,
                                       courseName=courseName,
                                       choosedLanguages=languages,
                                       courses=allCourses, 
                                       languages=allLanguages,
                                       allCourseAdministrators=allCourseAdministrators)

            existCoursesNum=dao.query(RegisteredCourses.courseId).\
                                all()
            newCourseNum='%s%s%03d' %\
                         (startDateOfCourse[:4], semester, int(courseIndex)) # yyyys
            isNewCourse=True
            for existCourse in existCoursesNum:
                # if the course is already registered, then make another subclass
                if existCourse[0][:8]==newCourseNum:
                    NumberOfCurrentSubCourse=\
                        dao.query(func.count(RegisteredCourses.courseId).\
                                       label('num')).\
                            filter(RegisteredCourses.courseId.\
                                                     like(newCourseNum+'__')).\
                            first().\
                            num
                   
                    newCourseNum='%s%02d' % (existCourse[0][:8],
                                             NumberOfCurrentSubCourse + 1) # yyyysccc
                    isNewCourse=False
                    break
            # new class case
            if isNewCourse:
                newCourseNum='%s01' % (newCourseNum)
            
            if register_new_course(newCourseNum, courseName, courseDescription,
                                   startDateOfCourse, endDateOfCourse,
                                   courseAdministrator.split(' ')[0]):
                return render_template('/server_add_class.html', 
                                       error=error, 
                                       courses=allCourses, 
                                       languages=allLanguages)
            
            # create course folder in 'CurrentCourses' folder
            courseName=courseName.replace(' ', '')
            problemPath='%s/CurrentCourses/%s_%s' %\
                        (projectPath, newCourseNum, courseName)
            
            if not os.path.exists(problemPath):
                os.makedirs(problemPath)
            for language in languages:
                languageIndex, _=language # language index, language version
                
                if add_new_language_of_course(newCourseNum, int(languageIndex)):
                    return render_template('/server_add_class.html', 
                                           error=error, 
                                           courses=allCourses, 
                                           languages=allLanguages)
                    
            return redirect(url_for('.server_manage_class',
                                    pageNum = int(1)))

    return render_template('/server_add_class.html', 
                           error=error, 
                           courseAdministrator=courseAdministrator,
                           semester=semester,
                           courseDescription=courseDescription,
                           startDateOfCourse=startDateOfCourse,
                           endDateOfCourse=endDateOfCourse,
                           courseIndex=courseIndex,
                           courseName=courseName,
                           choosedLanguages=languages,
                           courses=allCourses, 
                           languages=allLanguages,
                           allCourseAdministrators=allCourseAdministrators)
    
    
@GradeServer.route('/master/manage_problem-<activeTabId>/page<int:pageNum>', methods=['GET', 'POST'])
@check_invalid_access
@login_required
def server_manage_problem(activeTabId, pageNum):
    global projectPath
    global numberOfDifficulty
    error=None
    
    if request.method=='POST':
        for form in request.form:
            if form=='upload':
                files=request.files.getlist('files')
                if not list(files)[0].filename:
                    error='Uploading file error'
                    break

                nextIndex=get_num_of_problems()

                numberOfProblemsOfDifficulty=[0] * numberOfDifficulty
                
                for difficulty in range(numberOfDifficulty):
                    difficultyOfProblem=str(difficulty + 1)
                    numberOfProblemsOfDifficulty[difficulty]=\
                        get_num_of_problems_in_difficulty(difficultyOfProblem)

                    if numberOfProblemsOfDifficulty[difficulty]== -1:
                        error='Error has occurred while searching problems'
                        break
                        
                # read each uploaded file(zip)
                for fileData in files:
                    # create temporary path to store new problem before moving into 'Problems' folder
                    tmpPath='%s/tmp' % projectPath
                    
                    '''
                    @@ Check and Delete temporary folder
                    
                    If temporary folder 'tmp' is exist, then it means it had an error at past request.
                    So, remove the temporary folder 'tmp' first.
                    '''
                    if os.path.exists(tmpPath):
                        try:
                            subprocess.call('rm -rf %s' % tmpPath, shell=True)
                        except OSError:
                            error='Cannot delete \'tmp\' folder'
                            break
                    
                    # unzip file
                    with zipfile.ZipFile(fileData, 'r') as z:
                        z.extractall(tmpPath)
                    
                    try:
                        rowProblemName=\
                            re.split('_|\.',\
                                     os.listdir(tmpPath)[0])[0].\
                               replace(' ', '\ ')
                    except OSError:
                        error='Error has been occurred while listing file names'
                        break
                    
                    '''
                    @@ Decode problem name
                    
                    If the problem zip's made on window environment, problem name's broken
                    So it needs to be decoded by cp949
                    ''' 
                    problemName=str(rowProblemName.decode('cp949'))
                    
                    # if decoded name is the same with before decoding, 
                    # it means the file is not created on window environment
                    isFromWindow=\
                        True if rowProblemName != problemName else False
                    
                    if isFromWindow:
                        if handle_file_came_from_window(rowProblemName,
                                                        problemName):
                            break
                    
                    problemInformationPath=\
                        ('%s/%s.txt' %\
                        (tmpPath, problemName)).replace('\ ', ' ')

                    try:
                        # 'open' command can handle space character without '\' mark,
                        # Replace '\ ' to just space ' '
                        problemInfoFile=open(problemInformationPath, 'r')
                        problemInformation=problemInfoFile.read()
                        
                        try:
                            problemInfoFile.close()
                        except IOError:
                            error='Error has been occurred while closing problem meta file'
                            break
                            
                    except IOError:
                        error='Error has been occurred while reading problem meta file(.txt)'
                        break
                    
                    '''
                    @@ Decode problem meta information
                    
                    Problem meta information(.txt) file needs to be decoded as well as problem folder name
                    '''
                    if isFromWindow:
                        problemInformation=problemInformation.decode('cp949')
                    
                    nextIndex += 1
                    # slice and make key, value pairs from csv form
                    problemInformation=\
                        problemInformation.replace(' ', '').split(',')

                    # re-slice and make information from 'key=value'
                    for eachInformation in problemInformation:
                        key, value=eachInformation.split('=')
                        if key=='Name':
                            # 'value' doesn't have a space character because of 'replace(' ', '')' command above
                            # Don't use 'value' for problem name
                            problemName=problemName.replace('\ ', ' ')
                        elif key=='Difficulty':
                            difficulty=int(value)
                        elif key=='SolutionCheckType':
                            solutionCheckType=\
                                ENUMResources().const.SOLUTION\
                                    if value=='Solution'\
                                    else ENUMResources().const.CHECKER
                        elif key=='LimitedTime':
                            limitedTime=int(value)
                        elif key=='LimitedMemory':
                            limitedMemory=int(value)
                    
                            
                    numberOfProblemsOfDifficulty[difficulty - 1] += 1

                    # place the difficulty at the left most
                    problemId=difficulty * 10000 +\
                                numberOfProblemsOfDifficulty[difficulty - 1]
                    problemPath='%s/%s' % (problemsPath,
                                           str(problemId) + '_' +
                                           problemName.replace(' ', ''))
                    
                    newProblemInfo=nextIndex, problemId, problemName,\
                                     solutionCheckType, limitedTime,\
                                     limitedMemory, problemPath
                    if add_new_problem(newProblemInfo): break
                    
                    newProblemPath='%s/%s_%s' %\
                                   (tmpPath, problemName, solutionCheckType)
                    
                    if change_directory_to(newProblemPath): break
                                        
                    try:
                        # current path : ../tmp/problemName_solutionCheckType
                        inOutCases=\
                            [filename for filename in os.listdir(os.getcwd())]
                    except OSError:
                        error='Error has been occurred while listing file names'
                        break

                    for filename in inOutCases:
                        rowFileName=filename
                        fileName='%s_%s' %\
                                 (problemName, rowFileName.split('_', 1)[1])
                
                        if rename_file(rowFileName, str(fileName)): break

                    '''
                    @@ Changing directory/file name
                    
                    work flow
                    1. Remove space on its name
                        from> Hello World 
                        to> HelloWorld
                        
                    2. Attach problem ID ahead of the name
                        from> HelloWorld
                        to> 12345_HelloWorld
                        * 12345 is created problem id
                    '''
                    currentPath, error=get_current_path()
                    if error: break

                    # inside of SOLUTION or CHECKER folder
                    if remove_space_from_names_in(currentPath): break
                    if attach_string_ahead_of(currentPath, problemId): break
                    
                    # move to outside of the folder
                    if change_directory_to(tmpPath): break
                    
                    currentPath, error=get_current_path()
                    if error: break
                    
                    # inside of Problem folder
                    if remove_space_from_names_in(currentPath): break
                    if attach_string_ahead_of(currentPath, problemId): break
                    
                    # create final goal path
                    if not os.path.exists(problemPath):
                        os.makedirs(problemPath)
                        
                    problemName=problemName.replace(' ', '')
                    problemDescriptionPath=\
                        '%s/%s_%s' %\
                        (problemDescriptionsPath, problemId, problemName)
                    if not os.path.exists(problemDescriptionPath):
                        os.makedirs(problemDescriptionPath)
                    
                    if rename_file('%s/*'%tmpPath, '%s/'%problemPath): break
                    
                    try:
                        subprocess.call('cp %s/%s_%s.pdf %s/' %\
                                        (problemPath, problemId, problemName,\
                                        problemDescriptionPath), shell=True)
                    except:
                        error='problem pdf doesn\'s exist'
                    
                if error: break
                
            else:
                if delete_problem(int(form)): break
                        
        if error:
            return render_template('/server_manage_problem.html', 
                                   error=error, 
                                   uploadedProblems=[],
                                   difficultyList = (OtherResources().const.ALL,
                                                     OtherResources().const.GOLD,
                                                     OtherResources().const.SILVER,
                                                     OtherResources().const.BRONZE),
                                   activeTabId = activeTabId,
                                   pages = get_page_pointed(int(0),
                                                            int(0)))    
            
        return redirect(url_for('.server_manage_problem',
                                activeTabId = activeTabId,
                                pageNum = pageNum))
        
        
    try:
        uploadedProblems = select_problems(activeTabId)
        count = select_count(uploadedProblems.subquery().\
                                              c.\
                                              problemId).first().\
                                                         count
        uploadedProblems = get_page_record(uploadedProblems,
                                           pageNum = pageNum).all()   
    except exc.SQLAlchemyError:
        uploadedProblems=[]
        count = 0
        
    return render_template('/server_manage_problem.html', 
                           error=error, 
                           uploadedProblems = uploadedProblems,
                           difficultyList = (OtherResources().const.ALL,
                                             OtherResources().const.GOLD,
                                             OtherResources().const.SILVER,
                                             OtherResources().const.BRONZE),
                           activeTabId = activeTabId,
                           pages = get_page_pointed(pageNum,
                                                    count))


@GradeServer.route('/master/manage_users-<activeTabId>/page<int:pageNum>', methods=['GET', 'POST'])
@check_invalid_access
@login_required
def server_manage_user(activeTabId, pageNum):
    error=None

    try:
        users=(dao.query(Members,
                         Colleges,
                         Departments).\
                   join(DepartmentsDetailsOfMembers, 
                        Members.memberId==\
                        DepartmentsDetailsOfMembers.memberId).\
                   join(Colleges,
                        Colleges.collegeIndex==\
                        DepartmentsDetailsOfMembers.collegeIndex).\
                   join(Departments, 
                        Departments.departmentIndex==\
                        DepartmentsDetailsOfMembers.departmentIndex).\
                   order_by(Members.memberId)).\
              all()

    except:
        '''
        It can prevent to handle next for-loop with setting 'users' empty
        '''
        error='Error has occurred while getting member information'
        users=[]
    
    combineSameUsers=[]
    userIndex=1
    loopIndex=0
    # if member in multiple department,
    # will be [member] [college] [department] [college] [department] ...
    for user, college, department in users:
        userInfo=[user.memberId, user.memberName, user.contactNumber,
                  user.emailAddress, user.authority,
                  user.signedInDate, user.lastAccessDate,
                  college.collegeName, department.departmentName]
        if loopIndex==0:
            combineSameUsers.append(userInfo)
        else:
            if user.memberId==combineSameUsers[userIndex-1][0]:
                combineSameUsers[userIndex-1].append(college.collegeName)
                combineSameUsers[userIndex-1].append(department.departmentName)
            else:
                combineSameUsers.append(userInfo)
                userIndex += 1
        loopIndex += 1
        
    if request.method=='POST':
        for form in request.form:
            error=delete_member(form)
            if error: break
            
        if not error:
            return redirect(url_for('.server_manage_user',
                                    activeTabId = activeTabId,
                                    pageNum = pageNum))

    return render_template('/server_manage_user.html', 
                           error=error,
                           users=combineSameUsers, 
                           index=len(combineSameUsers))


@GradeServer.route('/master/addUser', methods=['GET', 'POST'])
@check_invalid_access
@login_required
def server_add_user():        
    global newUsers
    error=None
    targetUserIdToDelete=[]
    authorities=['Course Admin', 'User']
    
    try:
        allColleges = select_colleges().all()
    except exc.SQLAlchemyError:
        allColleges = []
        
    try:
        allDepartments = join_departments_of_colleges().all()
    except exc.SQLAlchemyError:
        allDepartments = []
        
    if request.method=='POST':
        keys={'memberId':0,
              'memberName':1,
              'authority':2,
              'collegeIndex':3,
              'collegeName':4,
              'departmentIndex':5,
              'departmentName':6}
        
        if 'addIndivisualUser' in request.form:
            # ( number of all form data - 'addIndivisualUser' form ) / forms for each person(id, name, college, department, authority)
            numberOfUsers=(len(request.form) - 1) / 5
            newUser=[['' for _ in range(7)] for _ in range(numberOfUsers + 1)]
            
            for form in request.form:
                if form != 'addIndivisualUser':
                    value, index=re.findall('\d+|\D+', form)
                    index=int(index)
                    data=request.form[form]
                    if not data or data=='select college':
                        continue
                    if value=='userId':
                        newUser[index - 1][keys['memberId']]=data
                    elif value=='username':
                        newUser[index - 1][keys['memberName']]=data
                    elif value=='authority':
                        newUser[index - 1][keys['authority']]=data
                    elif value=='college':
                        collegeIndex=data.split()[0]
                        newUser[index - 1][keys['collegeIndex']]=collegeIndex
                        error, newUser[index - 1][keys['collegeName']]=\
                            get_college_name(collegeIndex)
                        if error: break
                    elif value=='department':
                        departmentIndex=data.split()[0]
                        newUser[index - 1][keys['departmentIndex']]=\
                            departmentIndex
                        error, newUser[index - 1][keys['departmentName']]=\
                            get_department_name(departmentIndex)
                        if error: break

            if error:
                return render_template('/server_add_user.html', 
                                       error=error,  
                                       allColleges=allColleges,
                                       allDepartments=allDepartments,
                                       authorities=authorities,
                                       newUsers=newUsers)   
                         
            for index in range(numberOfUsers+1):
                valid=True
                # check for empty row
                for col in range(7):
                    if newUser[index][col]=='':
                        valid=False
                        break
                if valid:
                    newUsers.append(newUser[index])
                    
        elif 'addUserGroup' in request.form:
            files=request.files.getlist('files')
            if list(files)[0].filename:
                # read each file
                for fileData in files:
                    # read each line    
                    for userData in fileData:
                        # slice and make information from 'key=value'
                        userInformation=\
                            userData.replace(' ', '').replace('\n', '').\
                            replace('\xef\xbb\xbf', '').split(',')
                        # userId, userName, authority, collegeIndex, collegeName, departmentIndex, departmentName
                        newUser=[''] * 7
                        
                        for eachData in userInformation:
                            if '=' in eachData:
                                # all authority is user in adding user from text file
                                newUser[keys['authority']]='User'
                                key=eachData.split('=')[0]
                                value=eachData.split('=')[1]
                                if key=='userId':
                                    newUser[keys['memberId']]=value 
                                    
                                elif key=='username':
                                    newUser[keys['memberName']]=value
                                    
                                elif key=='college':
                                    newUser[keys['collegeIndex']]=value
                                    error, newUser[keys['collegeName']]=\
                                        get_college_name(value)
                                    if error: break
                                        
                                elif key=='department':
                                    newUser[keys['departmentIndex']]=value
                                    error, newUser[keys['departmentName']]=\
                                        get_department_name(value)
                                    if error: break
                                        
                                else:
                                    error='Try again after check the manual'
                                    break
                                    
                            else:
                                error='Try again after check the manual'
                                break
                        
                        if error:
                            return render_template('/server_add_user.html',
                                                   error=error,
                                                   allColleges=allColleges,
                                                   allDepartments=allDepartments,
                                                   authorities=authorities,
                                                   newUsers=newUsers)
                            
                        for user in newUsers:
                            if user[keys['memberId']]==\
                                    newUser[keys['memberId']] and\
                               user[keys['collegeIndex']]==\
                                    newUser[keys['collegeIndex']] and\
                               user[keys['departmentIndex']]==\
                                    newUser[keys['departmentIndex']]:
                                error='There is a duplicated user id. Check the file and added user list'
                                return render_template('/server_add_user.html',
                                                       error=error,
                                                       allColleges=allColleges,
                                                       allDepartments=allDepartments,
                                                       authorities=authorities,
                                                       newUsers=newUsers)
                                
                        newUsers.append(newUser)
                        
        elif 'addUser' in request.form:
            for newUser in newUsers:
                if newUser[keys['authority']]=='Course Admin':
                    newUser[keys['authority']]=\
                        SETResources().const.COURSE_ADMINISTRATOR
                elif newUser[keys['authority']]=='User':
                    newUser[keys['authority']]=SETResources().const.USER
                else: # wrong access
                    error='Wrong access'
                    return render_template('/server_add_user.html',
                                           error=error,
                                           allColleges=allColleges,
                                           allDepartments=allDepartments,
                                           authorities=authorities,
                                           newUsers=newUsers)

                password=str(newUser[keys['memberId']])
                password=generate_password_hash(TripleDES.encrypt(password))

                freshman=Members(memberId=newUser[keys['memberId']], 
                                 password=password,
                                 memberName=newUser[keys['memberName']],
                                 authority=newUser[keys['authority']],
                                 signedInDate=datetime.now())
                dao.add(freshman)
                
                try:
                    dao.commit()
                except exc.SQLAlchemyError:
                    dao.rollback()
                
                if add_new_departments_details_of_members(newUser[keys['memberId']],
                                                          newUser[keys['collegeIndex']],
                                                          newUser[keys['departmentIndex']]):
                    break
                        
                
                    
                    
            newUsers=[] # initialize add user list
            if error:
                return redirect(url_for('.server_add_user'))
            
            return redirect(url_for('.server_manage_user'))
            
        elif 'deleteUser' in request.form:
            for form in request.form:
                if not form is 'deleteUser':
                    targetUserIdToDelete.append(form)
                
        # if id list is not empty
        if len(targetUserIdToDelete) != 0:
            # each target user id
            for targetUser in targetUserIdToDelete:
                index=0
                # each new user id
                for newUser in newUsers:
                    # if target id and new user id are same
                    if targetUser==newUser[keys['memberId']]:
                        del newUsers[index]
                        break
                    index += 1
    
    return render_template('/server_add_user.html', 
                           error=error,  
                           allColleges=allColleges,
                           allDepartments=allDepartments,
                           authorities=authorities,
                           newUsers=newUsers)


@GradeServer.route('/master/manage_service')
@check_invalid_access
@login_required
def server_manage_service():   
    #TODO     
    error=None
    
    return render_template('/server_manage_service.html',
                           error=error)