# -*- coding: utf-8 -*-


from sqlalchemy import and_
from GradeServer.resource.enumResources import ENUMResources

from GradeServer.database import dao

from GradeServer.model.colleges import Colleges
from GradeServer.model.departmentsOfColleges import DepartmentsOfColleges
from GradeServer.model.departments import Departments


'''
Select All Colleges
'''
def select_colleges(isAbolished = ENUMResources().const.FALSE):
    return dao.query(Colleges).\
               filter(Colleges.isAbolished ==isAbolished)
     
     
'''
Select CollegeName College
'''
def select_college(collegeParameter, isAbolished = ENUMResources().const.FALSE):
    return dao.query(Colleges).\
               filter((Colleges.collegeName == collegeParameter.collegeName if collegeParameter.collegeName
                       else Colleges.collegeIndex == collegeParameter.collegeIndex),
                      Colleges.isAbolished == isAbolished)
               
 
'''
Select All Departments
'''
def select_departments(isAbolished = ENUMResources().const.FALSE):
    return dao.query(Departments).\
               filter(Departments.isAbolished == isAbolished)
    
    
'''
Select DepartmentName Department
'''
def select_department(departmentParameter, isAbolished = ENUMResources().const.FALSE):  
    return dao.query(Departments).\
               filter((Departments.departmentName == departmentParameter.departmentName if departmentParameter.departmentName
                       else Departments.departmentIndex == departmentParameter.departmentIndex),
                      Departments.isAbolished == isAbolished)   
        
                 
'''
Join Colleges and Departments
'''
def join_departments_of_colleges(isAbolished = ENUMResources().const.FALSE):
    return dao.query(DepartmentsOfColleges.collegeIndex,
                     DepartmentsOfColleges.departmentIndex,
                     Colleges.collegeName,
                     Departments.departmentCode,
                     Departments.departmentName).\
               join(Colleges,
                    Colleges.collegeIndex == DepartmentsOfColleges.collegeIndex).\
               join(Departments,
                    Departments.departmentIndex == DepartmentsOfColleges.departmentIndex).\
               filter(and_(Colleges.isAbolished == isAbolished,
                           Departments.isAbolished == isAbolished))
               

'''
Select Departments Of College
'''
def select_departments_of_college(collegeIndex):
    return dao.query(DepartmentsOfColleges,
                     Departments).\
               join(Departments,
                    Departments.departmentIndex == DepartmentsOfColleges.departmentIndex).\
               filter(DepartmentsOfColleges.collegeIndex == collegeIndex)
               
               

'''
Insert relation in college department
'''
def insert_relation_in_college_department(collegeIndex, departmentIndex): 
    return DepartmentsOfColleges(collegeIndex = collegeIndex,
                                 departmentIndex = departmentIndex)   
    
    
'''
Insert new College
'''
def insert_college(collegeCode, collegeName):
    return Colleges(collegeCode = collegeCode,
                    collegeName = collegeName)
    
   
'''
Insert new Department
'''
def insert_department(departmentCode, departmentName):
    return Departments(departmentCode = departmentCode,
                       departmentName = departmentName) 
    
    
    
'''
Update College Abolished
'''
def update_college_abolished(collegeParameter, isAbolished = ENUMResources().const.FALSE):
    dao.query(Colleges).\
        filter(Colleges.collegeName == collegeParameter.collegeName if collegeParameter.collegeName
               else Colleges.collegeIndex == collegeParameter.collegeIndex).\
        update(dict(isAbolished = isAbolished))
        
'''
Update Department Abolished
'''
def update_department_abolished(departmentParameter, isAbolished = ENUMResources().const.FALSE):
    dao.query(Departments).\
        filter(Departments.departmentName == departmentParameter.departmentName if departmentParameter.departmentName
               else Departments.departmentIndex == departmentParameter.departmentIndex).\
        update(dict(isAbolished = isAbolished))
    