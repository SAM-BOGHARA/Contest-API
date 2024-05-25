from rest_framework.renderers import JSONRenderer

class apiJsonRenderer(JSONRenderer):
    media_type = 'application/json'
