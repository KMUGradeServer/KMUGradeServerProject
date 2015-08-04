from __future__ import absolute_import
from celeryServer import app

import time
import DBUpdate
from DBManager import db_session
from subprocess import Popen, PIPE, call
from billiard import current_process

MAX_CONTAINER_COUNT = 4
ROOT_CONTAINER_DIRECTORY = '/container'

class SqlAlchemyTask(app.Task):
    abstract = True
    
    def after_return(self, status, retval, task_id, args, kwargs, einfo):
        db_session.remove()
    

@app.task(name = 'task.Grade', base=SqlAlchemyTask)
def Grade(filePath, problemPath, stdNum, problemNum, gradeMethod, caseCount,
          limitTime, limitMemory, usingLang, version, courseNum, submitCount,
          problemName):
    worker_num = current_process().index % MAX_CONTAINER_COUNT + 1
    
    saveDirectoryName = "%s_%s_%s_%i" % (stdNum, problemNum, courseNum, submitCount)
    sharingDirName = "%s%i/%s" % (ROOT_CONTAINER_DIRECTORY, worker_num,
                            saveDirectoryName)
    argsList = "%s %s %s %s %i %i %i %s %s %s" % (filePath, problemPath,
                                                  saveDirectoryName, gradeMethod,
                                                  caseCount, limitTime,
                                                  limitMemory, usingLang,
                                                  version, problemName)
    containerCommand = "%s%i %s" % ('sudo docker exec grade_container', worker_num,
                                   'python /gradeprogram/rungrade.py ')

    
    call('sudo mkdir ' + sharingDirName, shell = True)
    print 'program start'
    
    message = Popen(containerCommand + argsList, shell=True, stdout=PIPE)
    
    for i in xrange(limitTime*100):
        if message.poll() == None: 
            time.sleep(0.01)
        else:
            messageLines = message.stdout.readlines()
            UpdateResult(messageLines[-1], stdNum, problemNum, courseNum, submitCount)
            break
    else:
        UpdateResult('SERVER_ERROR', stdNum, problemNum, courseNum, submitCount)
    
    call('sudo rm -rf ' + sharingDirName, shell = True)
    
@app.task(name = 'task.ServerOn')
def OnServer():
    for i in range(MAX_CONTAINER_COUNT):
        containerNum = i + 1
        containerCreadeCommand = "%s%i%s%i %s" %('sudo docker create --privileged -i -t --name --cpuset="',
                                                i, '" grade_container', containerNum,
                                                'gradeserver:1.0 /bin/bash')
        
        runProgramInContainer = '%s%i %s' % ('sudo docker exec grade_container',
                                            containerNum, 'python -B /gradeprogram/*')
        call(containerCreadeCommand, shell = True)
        call('sudo docker start grade_container' + containerNum, shell = True)
        call(runProgramInContainer, shell = True)
    
@app.task(name = 'task.ServerOff')
def OffServer():
    time.sleep(5)
    
    for i in range(MAX_CONTAINER_COUNT):
        number = str(i+1)
        call('sudo docker stop grade_container' + number, shell = True)
        call('sudo docker rm grade_container' + number, shell = True)
        
def UpdateResult(messageLine, stdNum, problemNum, courseNum, submitCount):        
    dataUpdate = DBUpdate.DBUpdate(stdNum, problemNum, courseNum, submitCount)
    messageParaList = messageLine.split()
    
    result = dataUpdate.UpdateResutl(messageParaList, db_session)
    
    if not result:
        dataUpdate.UpdateServerError(stdNum, problemNum, courseNum,
                                     submitCount, db_session)