from segment.utils import *
import cloudinary.uploader
import csv
from io import StringIO





class start(APIView):
    @staticmethod
    def get(req):

        # Create a new instance of ChromeDriver
        driver = wirewebdriver.Chrome(
            service=service, options=chrome_options, seleniumwire_options=options
        )

        # Clear the cache by deleting all cookies
        driver.delete_all_cookies()

        driver.refresh()
        # Now you can use the `driver` object to interact with the browser and access the requests made
        driver.get("https://artists.spotify.com/c/artist/3EYY5FwDkHEYLw5V86SAtl/home")
        
        sleep(5)

        auth_header = login(driver)

        print(auth_header)
        basket = []
      


        return Response(
            {
                "status": "success",
            },
            status=201,
        )
        print("Upload complete")