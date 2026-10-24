from urllib.parse import urlparse
from rest_framework import serializers


ALLOWED_HOSTS = ['youtube.com', 'www.youtube.com', 'youtu.be', 'm.youtube.com']

def validate_youtube_url(value):
    if not value:
        return
    parsed = urlparse(value)
    host =  parsed.netloc.lower()
    if host not in ALLOWED_HOSTS:
        raise serializers.ValidationError("Недопустимый URL YouTube.")
