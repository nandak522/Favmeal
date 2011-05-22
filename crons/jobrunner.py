from crons.models import Job
import time

def run_immediate_jobs():
    run_jobs(Job.objects.waiting_jobs())

def run_daily_jobs():
    run_jobs(Job.objects.daily_jobs())

def run_jobs(jobs):
    from datetime import datetime
    print 'Executing %s Jobs at:%s' % (len(jobs),datetime.now())
    for job in jobs:
        job.execute()
    print 'Finished %s Jobs at:%s' % (len(jobs),datetime.now())

if __name__=='__main__':
    run_immediate_jobs()