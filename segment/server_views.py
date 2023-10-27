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

        try:

            driver.refresh()
        except:
            driver = wirewebdriver.Chrome(service=service, options=chrome_options,seleniumwire_options=options)

            driver.get('https://artists.spotify.com/c/artist/0aUMVkR8QV0LSdv9VZOATn/home')

        sleep(20)

        for request in driver.requests:
            if request.headers:
                if "authorization" in request.headers:
                    auth_header = request.headers["Authorization"]
                    if auth_header != "":
                        break
        from bs4 import BeautifulSoup
        # Get the page source
        sleep(5)
        html_source = driver.page_source

        # Use BeautifulSoup to parse the page source
        soup = BeautifulSoup(html_source, 'html.parser')

        # Find all h1 tags
        h1_tags = soup.find_all('h1')
        pa_tags = soup.find_all("span")
        # Print the content of each h1 tag
        for tag in h1_tags:
            print(tag.text)
        for tg in pa_tags:
            print(tg.text)

        return Response(
            {
                "auth_header": f"{auth_header}",
            },
            status=201,
        )
    
