from django.core.management.base import BaseCommand
from AnalyzerApp.models import Comment
import os
import json


class Command(BaseCommand):
    def handle(self,*args, **kwargs):
        Comment.objects.all().delete()

        json_file_path = 'AnalyzerApp/management/commands/comments_db.json'

        with open(json_file_path, 'r', encoding='utf-8') as file:
            comments = json.load(file)
        
        for comment in comments:
            
            exist = Comment.objects.filter(user_tag = comment['user_tag']).first()
            if not exist:
                Comment.objects.create(user_tag = comment['user_tag'],
                                        tweet = comment['tweet'],
                                        time = comment['time_stamp'],
                                        reply = comment['reply'],
                                        retweet = comment['retweet'],
                                        like = comment['like'],
                                        visualizations = comment['visualizations'],
                                        analysis = comment['analysis'],
                                        clasification = comment['clasification'])
                                        
