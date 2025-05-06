from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Candidate, Job, Match
from .utils.resume_parser import extract_text_from_pdf, extract_skills
from .utils.matcher import calculate_match_score
from .utils.gpt_helper import generate_resume_summary, explain_skill_gap
from rest_framework.permissions import IsAuthenticated
from .serializers import (
    ResumeUploadSerializer,
    CandidateSerializer,
    JobSerializer,
    MatchResultSerializer
)
import os

class UploadResumeView(APIView):
    permission_classes = [IsAuthenticated]
    
    def post(self, request):
        # Validate file upload
        serializer = ResumeUploadSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        resume_file = request.FILES['resume']
        user = request.user
        
        # Save resume temporarily
        temp_path = f"/tmp/{resume_file.name}"
        with open(temp_path, 'wb+') as dest:
            for chunk in resume_file.chunks():
                dest.write(chunk)
        
        try:
            # Parse resume
            text = extract_text_from_pdf(temp_path)
            skills = extract_skills(text)
            summary = generate_resume_summary(text)
            
            # Create/update candidate profile
            candidate, _ = Candidate.objects.update_or_create(
                user=user,
                defaults={
                    'resume': resume_file,
                    'skills': skills,
                    'summary': summary,
                    'resume_text': text
                }
            )
            
            return Response(
                CandidateSerializer(candidate).data,
                status=status.HTTP_201_CREATED
            )
            
        except Exception as e:
            return Response(
                {"error": str(e)},
                status=status.HTTP_422_UNPROCESSABLE_ENTITY
            )
            
        finally:
            if os.path.exists(temp_path):
                os.remove(temp_path)

class JobMatchView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        try:
            candidate = Candidate.objects.get(user=request.user)
            jobs = Job.objects.all()
            matches = []
            
            for job in jobs:
                score = calculate_match_score(candidate.skills, job.required_skills)
                if score > 50:
                    missing_skills = list(set(job.required_skills) - set(candidate.skills))
                    matches.append({
                        'job': job,
                        'score': score,
                        'missing_skills': missing_skills,
                        'explanation': explain_skill_gap(missing_skills, job.title)
                    })
            
            return Response({
                'matches': MatchResultSerializer(matches, many=True).data
            })
            
        except Candidate.DoesNotExist:
            return Response(
                {"error": "Upload your resume first"},
                status=status.HTTP_404_NOT_FOUND
            )