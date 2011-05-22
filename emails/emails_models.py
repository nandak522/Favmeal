from django.db import models
from common.models import BaseModel

class EmailConversationManager(models.Manager):
    def create_emailconversation(self,from_email,subject,description):
        email_conversation = self.exists(from_email,subject)
        if email_conversation:
            return email_conversation
        email_conversation = EmailConversation(from_email=from_email,subject=subject,description=description)
        email_conversation.save()
        return email_conversation
    
    def exists(self,from_email,subject):
        email_conversations = EmailConversation.objects.filter(from_email=from_email.strip().lower(),subject=subject.strip().lower())
        if email_conversations:
            return email_conversations[0]
        return None

class EmailConversation(BaseModel):
    from_email = models.EmailField(blank=False, db_index=True)
    subject = models.CharField(max_length=100, blank=False, db_index=True)
    description = models.CharField(max_length=5000, blank=False)
    objects = EmailConversationManager()