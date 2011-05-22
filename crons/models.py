from django.db import models
from common.models import BaseModel
from users.models import UserProfile
import pickle

class JobManager(models.Manager):
    def add_job(self,status,action,args={},owner=None):
        job =Job(action=action,owner=owner,args=pickle.dumps(args),status=status)
        job.save()
        return job
    
    def waiting_jobs(self):
        return self.filter(status='W')

    def daily_jobs(self):
        return self.filter(status='D')

class Job(BaseModel):
    JOB_STATUS_CHOICES = (
        ('C', 'Completed'),
        ('W', 'Waiting'),
        ('D', 'Daily'),
        ('K', 'Weekly'),
        ('H','Hourly'),
    )
    action = models.CharField(max_length=100, blank= False,unique=False)
    owner = models.ForeignKey(UserProfile,blank=True,null=True)
    args = models.CharField(max_length=4000, blank= True)
    status = models.CharField(max_length=1,blank=True,choices=JOB_STATUS_CHOICES)
    objects = JobManager()
    
    def __unicode__(self):
        return '%s:status:%s' % (self.action,self.status)

    def execute(self):
        try:
            import time
            start = time.time()
            from utils import load_module
            method = load_module(self.action)
            argument = self._args()
            result = method(self.owner,argument)
            self.done()
            end = time.time()
            print 'Executing the job with jobid:%s took:%s seconds' % (self.id,(end-start))
            return result
        except Exception,e:
            message= self.action +'\n'
            message+='Exception raised while executing Job with jobid:%s :%s' % (self.id,e.__str__()+'\n')
            print message
            from utils.emailer import mail_admins
            mail_admins(message,locals())
        return None

    def _args(self):
        if self.args: return pickle.loads(str(self.args))
        return {}
    
    def done(self):
        self.status='C'
        self.save()