from rest_framework.serializers import ValidationError


def video_url_validator(value):
    if "https://www.youtube.com/" not in value:
        raise ValidationError("Можно использовать ссылка только на youtube")
