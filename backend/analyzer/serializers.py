from rest_framework import serializers
from .models import Candidate, Job

class ResumeUploadSerializer(serializers.Serializer):
    resume = serializers.FileField()

class CandidateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Candidate
        fields = ['id', 'user', 'skills', 'summary', 'resume']
        read_only_fields = ['user', 'skills', 'summary']

class JobSerializer(serializers.ModelSerializer):
    class Meta:
        model = Job
        fields = ['id', 'title', 'company', 'required_skills', 'description']

class MatchResultSerializer(serializers.Serializer):
    job = JobSerializer()
    score = serializers.FloatField()
    missing_skills = serializers.ListField(child=serializers.CharField())
    explanation = serializers.CharField()