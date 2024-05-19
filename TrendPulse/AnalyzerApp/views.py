import os
import json
import subprocess
from dotenv import load_dotenv
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from django.db.models import IntegerField
from django.db.models.functions import Cast
from .models import Comment
from .forms import CommentForm
from openai import OpenAI


# Cargamos la API key de OpenAI
load_dotenv('../openAI.env')
client = OpenAI(api_key=os.environ.get('openAI_api_key'))

# Strategy Pattern Interface and Implementations
class OpenAIServiceInterface:
    def get_completion(self, prompt: str, model: str = "gpt-3.5-turbo") -> str:
        raise NotImplementedError

class OpenAIService(OpenAIServiceInterface):
    def __init__(self, api_key: str):
        self.client = OpenAI(api_key=api_key)

    def get_completion(self, prompt: str, model: str = "gpt-3.5-turbo") -> str:
        messages = [{"role": "user", "content": prompt}]
        response = self.client.chat.completions.create(model=model, messages=messages, temperature=0)
        return response.choices[0].message.content

# Factory Method Pattern
class OpenAIServiceFactory:
    @staticmethod
    def create_service(api_key: str) -> OpenAIServiceInterface:
        return OpenAIService(api_key)

openai_service = OpenAIServiceFactory.create_service(os.environ.get('openAI_api_key'))

class CommentService:
    def __init__(self, openai_service: OpenAIServiceInterface):
        self.openai_service = openai_service

    def classify_comments(self, comments):
        positive, neutral, negative = [], [], []
        for comment in comments:
            classification = int(comment.clasification)
            if classification > 5:
                positive.append(comment)
            elif classification == 5:
                neutral.append(comment)
            else:
                negative.append(comment)
        return positive, neutral, negative

    def run_scraping_script(self):
        result = subprocess.run(['python3', './lastHope.py'], capture_output=True, text=True)
        if result.returncode == 0:
            json_file_path = 'AnalyzerApp/ScrapingData.json'
            with open(json_file_path, 'r', encoding='utf-8') as file:
                return json.load(file)
        else:
            raise RuntimeError(f"Script execution failed with error: {result.stderr}")

    def save_comments_to_db(self, comments):
        Comment.objects.all().delete()
        for comment in comments:
            Comment.objects.create(
                user_tag=comment.get('user_tag', ''),
                tweet=comment.get('tweet', ''),
                time=comment.get('time_stamp', ''),
                reply=comment.get('reply', None),
                retweet=comment.get('retweet', None),
                like=comment.get('like', None),
                analysis=comment.get('analysis', ''),
                clasification=comment.get('clasification', None),
            )

    def analyze_and_classify_comments(self, comments):
        instruction = ("Vas a actuar como un analizador de sentimientos para comentarios extraidos de twitter "
                       "para un proyecto de social media listening, debes ser capaz de explicar las razones por las "
                       "se pudo haber escrito el comentario y las posibles razones de las intenciones de este.")
        instruction2 = ("Vas a actuar como un analizador de sentimientos e intenciones que es capaz de calificar comentarios "
                        "en una escala numerica del 1 al 10 donde 1 es muy negativo y 10 es muy positivo. Solo puedes dar respuestas "
                        "numericas y de un solo caracter. Por ejemplo: 4. Es muy importante que tu respuesta sea EXCLUSIVA Y UNICAMENTE UN NUMERO.")

        for comment in comments:
            prompt = f"{instruction} Haz un análisis del comentario {comment.tweet} hecho por el usuario {comment.user_tag}"
            prompt2 = f"{instruction2} Califica el comentario {comment.tweet}"
            response = self.openai_service.get_completion(prompt)
            response2 = self.openai_service.get_completion(prompt2)
            comment.analysis = response
            comment.clasification = response2
            comment.save()


comment_service = CommentService(openai_service)


# Decorator Pattern for logging
class LoggingView(View):
    def dispatch(self, request, *args, **kwargs):
        response = super().dispatch(request, *args, **kwargs)
        self.log_request(request, response)
        return response

    def log_request(self, request, response):
        # Implement logging logic here
        print(f"Request: {request.method} {request.path}, Response: {response.status_code}")
        # You can log to a file or any logging service


class ClasificationView(LoggingView):
    def get(self, request):
        comments = Comment.objects.annotate(classification_int=Cast('clasification', IntegerField())).order_by('classification_int')
        positive, neutral, negative = comment_service.classify_comments(comments)
        return render(request, 'stats.html', {'positive': positive, 'neutral': neutral, 'negative': negative})

class ButtonsView(LoggingView):
    def get(self, request):
        return render(request, 'buttons.html')

class SubmitJsonView(LoggingView):
    @csrf_exempt
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def post(self, request):
        try:
            comments = comment_service.run_scraping_script()
            comment_service.save_comments_to_db(comments)
            return redirect('comments')
        except RuntimeError as e:
            return JsonResponse({'status': 'error', 'message': str(e)})

class ResultadoScrapingView(LoggingView):
    def get(self, request):
        comments = Comment.objects.all()
        return render(request, 'comments.html', {'comments': comments})

class HacerAnalisisView(LoggingView):
    def post(self, request):
        comments = Comment.objects.all()
        comment_service.analyze_and_classify_comments(comments)
        return redirect('analysis')

class ResultadoAnalisisView(LoggingView):
    def get(self, request):
        comments = Comment.objects.all()
        return render(request, 'resultado_analisis.html', {'comments': comments})

class ShowIndexView(LoggingView):
    def get(self, request):
        return render(request, 'index.html')

class ShowLoginView(LoggingView):
    def get(self, request):
        return render(request, 'login.html')

class ShowRegisterView(LoggingView):
    def get(self, request):
        return render(request, 'register.html')

class CommentsNewView(LoggingView):
    def get(self, request):
        comments = Comment.objects.all()
        return render(request, 'comments.html', {'comments': comments})

class AnalysisView(LoggingView):
    def get(self, request):
        comments = Comment.objects.all()
        return render(request, "analysis.html", {'comments': comments})

class ChartsView(LoggingView):
    def get(self, request):
        return render(request, "charts.html")

class BaseView(LoggingView):
    def get(self, request):
        return render(request, "base.html")
