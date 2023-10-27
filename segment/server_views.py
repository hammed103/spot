from segment.server_utils import *
from django.shortcuts import redirect, render
from rest_framework.views import APIView
from rest_framework.response import Response
from time import sleep


from django.http import HttpResponse




class start(APIView):
    @staticmethod
    def get(req):
        from datetime import date, timedelta

        # Create a new instance of ChromeDriver
    # Create a new instance of ChromeDriver
        try:

            driver.refresh()
        except:
            driver = wirewebdriver.Chrome(service=service, options=chrome_options,seleniumwire_options=options)

            driver.get('https://artists.spotify.com/c/artist/0aUMVkR8QV0LSdv9VZOATn/home')
        sleep(10)

        for request in driver.requests:
            if request.headers:
                if "authorization" in request.headers:
                    auth_header = request.headers["Authorization"]
                    if auth_header != "":
                        break

        return Response(
            {
                "auth_header": f"{auth_header}",
            },
            status=201,
        )
    
