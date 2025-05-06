from django.db import models
from django.contrib.auth.models import User

class Job(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    required_skills = models.JSONField(default=list)  # ["Python", "ML"]
    location = models.CharField(max_length=100)
    company = models.CharField(max_length=100)

class Candidate(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    resume = models.FileField(upload_to='resumes/')
    skills = models.JSONField(default=list)  # Extracted by NLP
    experience = models.IntegerField(default=0)  # In years
    summary = models.TextField(blank=True, null=True)  
    resume_text = models.TextField(blank=True, null=True) 

class Match(models.Model):
    candidate = models.ForeignKey(Candidate, on_delete=models.CASCADE)
    job = models.ForeignKey(Job, on_delete=models.CASCADE)
    score = models.FloatField()  # Match percentage (0-100)
    timestamp = models.DateTimeField(auto_now_add=True)