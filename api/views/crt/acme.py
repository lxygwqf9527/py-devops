from flask import request

from api.resource import APIView

class AcmeInstall(APIView):
    url_prefix = '/acme/install'
    
    def get(self):
        print(request.values)
    
    def post(self):
        print(request.values)
