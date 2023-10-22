from segment.utils import *

from segment.teams import *
import cloudinary.uploader
import csv
import pygsheets
from bs4 import BeautifulSoup
import pandas as pd
import openpyxl
from io import StringIO
from openpyxl.utils import get_column_letter
from datetime import date, timedelta



from django.http import HttpResponse

def callback(request):
    code = request.GET.get('code')
    

    # For demonstration, we're just returning it in an HttpResponse.
    return HttpResponse(f"Received code: {code}")



class start(APIView):
    @staticmethod
    def get(req):
        from datetime import date, timedelta

        # Create a new instance of ChromeDriver
        driver = wirewebdriver.Chrome(
            service=service, options=chrome_options, seleniumwire_options=options
        )

        # Clear the cache by deleting all cookies
        driver.delete_all_cookies()

        driver.refresh()
        # Now you can use the `driver` object to interact with the browser and access the requests made
        driver.get("https://artists.spotify.com/c/roster")

        sleep(5)

        auth_header = login(driver)

        print(auth_header)

        headers = {
            "authority": "generic.wg.spotify.com",
            "accept": "application/json",
            "accept-language": "en-US",
            "app-platform": "Browser",
            "authorization": f"{auth_header}",
            "content-type": "application/json",
            "grpc-timeout": "10S",
            "origin": "https://artists.spotify.com",
            "referer": "https://artists.spotify.com/",
            "sec-ch-ua": '"Not/A)Brand";v="99", "Microsoft Edge";v="115", "Chromium";v="115"',
            "sec-ch-ua-mobile": "?1",
            "sec-ch-ua-platform": '"Android"',
            "sec-fetch-dest": "empty",
            "sec-fetch-mode": "cors",
            "sec-fetch-site": "same-site",
            "spotify-app-version": "1.0.0.4ff711e",
            "user-agent": "Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Mobile Safari/537.36 Edg/115.0.1901.203",
        }

        # 1. Authorize the client using the provided JSON key
        gc = pygsheets.authorize(
            service_file="my-project-1515950162194-ea018b910e23.json"
        )

        # 2. Open the Google Spreadsheet using its title
        spreadsheet = gc.open("Competitors")
        for sheet in ["Copy of 11:11"]:

            # 3. Select a specific worksheet by its title (assuming the name of the sheet is 'Sheet1')
            worksheet = spreadsheet.worksheet_by_title(sheet)

            # 4. Extract a specific row (for example, the 2nd row)
            row_values = worksheet.get_row(2)

            ddx = row_values[3:]

            tod = str(date.today())

            last = str(date.today() - timedelta(364))

            ddx = [i for i in ddx if i != ""]

            print(len(ddx))
            dc = pd.DataFrame()
            # Iterate over the other sheets and merge them with the main dataframe
            for aid in ddx[:]:

                params = {
                    "from_date": f"{last}",
                    "to_date": f"{tod}",
                }
                try:
                    rff = requests.get(
                        f"https://open.spotify.com/artist/{aid}", headers=headers
                    )

                    artistName = (
                        soup_from_html(rff.text).find("title").text.split("|")[0]
                    )

                    response = requests.get(
                        f"https://generic.wg.spotify.com/audience-engagement-view/v1/artist/{aid}/stats",
                        params=params,
                        headers=headers,
                    )

                    dt = response.json()
                    fr = pd.DataFrame(
                        dt["streams"]["current_period_timeseries"],
                    )
                    print(aid)
                except:
                    print(artistName, response.text)
                    continue

                header_row = [
                    "Date",
                    artistName,
                ]
                arrays = [header_row, ["Dates", aid]]
                tuples = list(zip(*arrays))
                fr.columns = pd.MultiIndex.from_tuples(tuples)

                if dc.shape == (0, 0):
                    dc = fr
                else:
                    dc = pd.merge(dc, fr, on=[("Date", "Dates")], how="outer")

            # Create the "TOTAL AMOUNT" column with SUM formulas
            # Create the "TOTAL AMOUNT" column with SUM formulas
            dc = dc.sort_values(("Date", "Dates"), ascending=False)
            last_column_letter = get_column_letter(len(dc.columns))
            dc[("TOTAL AMOUNT", "TOTAL AMOUNT")] = [
                f"=SUM(D{row_num + 3}:{last_column_letter}{row_num + 3})"
                for row_num in range(len(dc))
            ]
            dc[("Day", "Day")] = dc[("Date", "Dates")].apply(get_day_of_week)

            # Reorder the columns to have "TOTAL AMOUNT" first
            dc = dc[
                [("TOTAL AMOUNT", "TOTAL AMOUNT")]
                + [col for col in dc if col != ("TOTAL AMOUNT", "TOTAL AMOUNT")]
            ]
            dc = dc[[("Day", "Day")] + [col for col in dc if col != ("Day", "Day")]]
            dc = dc[
                [("Date", "Dates")] + [col for col in dc if col != ("Date", "Dates")]
            ]

            # dc.iloc[0,0] = "TOTAL AMOUNT"
            worksheet.clear()
            # Update the worksheet with the new DataFrame
            worksheet.set_dataframe(dc, start="A1")


        return Response(
            {
                "status": "success",
            },
            status=201,
        )


class segment(APIView):
    @staticmethod
    def get(req):
        from datetime import date, timedelta

        # Create a new instance of ChromeDriver
        driver = wirewebdriver.Chrome(
            service=service, options=chrome_options, seleniumwire_options=options
        )

        # Clear the cache by deleting all cookies
        driver.delete_all_cookies()

        driver.refresh()
        # Now you can use the `driver` object to interact with the browser and access the requests made
        driver.get("https://artists.spotify.com/c/roster")

        sleep(5)

        auth_header = login(driver)

        print(auth_header)

        headers = {
            "authority": "generic.wg.spotify.com",
            "accept": "application/json",
            "accept-language": "en-US",
            "app-platform": "Browser",
            "authorization": f"{auth_header}",
            "content-type": "application/json",
            "origin": "https://artists.spotify.com",
            "referer": "https://artists.spotify.com/",
            "sec-fetch-dest": "empty",
            "sec-fetch-mode": "cors",
            "sec-fetch-site": "same-site",
            "spotify-app-version": "1.0.0.9ac0ee2",
            "user-agent": "Mozilla/5.0 (X11; Linux aarch64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.188 Safari/537.36 CrKey/1.54.250320 Edg/115.0.0.0",
        }

        art = [
            (i["uri"].lstrip("spotify:artist:"), i["name"])
            for i in teams
            if i["uri"].startswith("spotify:artist")
        ]
        basket = []
        for id, namex in art:
            for cd, country_name in countries:
                # cd = ""
                if cd == "":
                    params = {
                        "country": f"{cd}",
                    }
                else:
                    params = {
                        "country": f"{cd}",
                    }

                response = requests.get(
                    f"https://generic.wg.spotify.com/fanatic-audience-segments/v1/artist/{id}/segments?",
                    params=params,
                    headers=headers,
                )
                if response.text == "Token expired":
                    print("expired token ")
                    auth_header = reload_auth(driver)
                    headers = {
                        "authority": "generic.wg.spotify.com",
                        "accept": "application/json",
                        "accept-language": "en-US",
                        "app-platform": "Browser",
                        "authorization": f"{auth_header}",
                        "content-type": "application/json",
                        "origin": "https://artists.spotify.com",
                        "referer": "https://artists.spotify.com/",
                        "sec-fetch-dest": "empty",
                        "sec-fetch-mode": "cors",
                        "sec-fetch-site": "same-site",
                        "spotify-app-version": "1.0.0.9ac0ee2",
                        "user-agent": "Mozilla/5.0 (X11; Linux aarch64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.188 Safari/537.36 CrKey/1.54.250320 Edg/115.0.0.0",
                    }
                    response = requests.get(
                        f"https://generic.wg.spotify.com/fanatic-audience-segments/v1/artist/{id}/segments?",
                        params=params,
                        headers=headers,
                    )
                try:
                    moot = pd.DataFrame(response.json()["segmentCountsTimeline"])
                except:
                    # print(response.text)
                    continue

                moot["country"] = country_name
                moot["artist_id"] = id
                moot["artist_name"] = namex

                basket.append(moot)

                print(f" Segments : {namex} -->  ,Data fetched for {country_name} ")

        df = pd.concat(basket)

        df[
            [
                "total_active_audience_listeners",
                "super_active_audience_listeners",
                "moderate_active_audience_listeners",
                "light_active_audience_listeners",
                "programmed_audience_listeners",
                "previously_active_audience_listeners",
            ]
        ] = df["segments"].apply(extract_audience_info)

        df[
            [
                "total_active_audience_streams",
                "super_active_audience_streams",
                "moderate_active_audience_streams",
                "light_active_audience_streams",
                "programmed_audience_streams",
                "previously_active_audience_streams",
            ]
        ] = df["streams"].apply(extract_audience_info)

        df["%active_audience_listeners"] = (
            (
                df.total_active_audience_listeners
                / (
                    df.total_active_audience_listeners
                    + df.programmed_audience_listeners
                    + df.previously_active_audience_listeners
                )
            )
            * 100
        ).round()
        df["%previously_active_audience_listeners"] = (
            (
                df.previously_active_audience_listeners
                / (
                    df.total_active_audience_listeners
                    + df.programmed_audience_listeners
                    + df.previously_active_audience_listeners
                )
            )
            * 100
        ).round()
        df["%programmed_audience_listeners"] = (
            (
                df.programmed_audience_listeners
                / (
                    df.total_active_audience_listeners
                    + df.programmed_audience_listeners
                    + df.previously_active_audience_listeners
                )
            )
            * 100
        ).round()

        df["%active_audience_streams"] = (
            (
                df.total_active_audience_streams
                / (
                    df.total_active_audience_streams
                    + df.programmed_audience_streams
                    + df.previously_active_audience_streams
                )
            )
            * 100
        ).round()
        df["%previously_active_audience_streams"] = (
            (
                df.previously_active_audience_streams
                / (
                    df.total_active_audience_streams
                    + df.programmed_audience_streams
                    + df.previously_active_audience_streams
                )
            )
            * 100
        ).round()
        df["%programmed_audience_streams"] = (
            (
                df.programmed_audience_streams
                / (
                    df.total_active_audience_streams
                    + df.programmed_audience_streams
                    + df.previously_active_audience_streams
                )
            )
            * 100
        ).round()

        df = df.drop(columns=["segments", "streams"])

        df = df.rename(columns={"date": "Date"})

        from datetime import date, timedelta

        # dat = str(date.today() - timedelta(1))


        for dat in [
            str(date.today() - timedelta(2)),
            str(date.today() - timedelta(1)),
        ]:
            print(dat)
            # for date in unique_dates:
            # Filter the dataframe for the specific date
            din = df[df["Date"] == dat]

            try:
                if (
                    din[
                        din.country == "Worldwide"
                    ].total_active_audience_listeners.iloc[0]
                    == 0
                ):
                    return Response(
                        {
                            "status": "No new",
                        },
                        status=201,
                    )
            except:
                pass
            # Convert the date to a string format suitable for filenames

            file_name = f"spotify_segments/{dat}_a.csv"

            csv_content = din.to_csv(index=False, quoting=csv.QUOTE_ALL, sep="|")
            result = cloudinary.uploader.upload(
                StringIO(csv_content),
                public_id=file_name,
                folder="/Soundcloud/",
                resource_type="raw",
                overwrite=True,
            )

        return Response(
            {
                "status": "Sucess",
            },
            status=201,
        )


class demo(APIView):
    @staticmethod
    def get(req):
        from datetime import date, timedelta

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
        dat = str(date.today() - timedelta(2))
        art = [
            (i["uri"].lstrip("spotify:artist:"), i["name"])
            for i in teams
            if i["uri"].startswith("spotify:artist")
        ]

        lb = []

        headers = {
            "authority": "generic.wg.spotify.com",
            "accept": "application/json",
            "accept-language": "en-US",
            "app-platform": "Browser",
            "authorization": f"{auth_header}",
            "content-type": "application/json",
            "origin": "https://artists.spotify.com",
            "referer": "https://artists.spotify.com/",
            "sec-fetch-dest": "empty",
            "sec-fetch-mode": "cors",
            "sec-fetch-site": "same-site",
            "spotify-app-version": "1.0.0.12cdad2",
            "user-agent": "Mozilla/5.0 (X11; Linux aarch64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.188 Safari/537.36 CrKey/1.54.250320 Edg/115.0.0.0",
        }
        for id, namex in art:
            for cd, country_name in countries:
                # cd = ""
                if cd == "":
                    params = {
                        "time-filter": "28day",
                        "aggregation-level": "recording",
                    }
                else:
                    params = {
                        "time-filter": "28day",
                        "aggregation-level": "recording",
                        "country": f"{cd}",
                    }

                response = requests.get(
                    f"https://generic.wg.spotify.com/s4x-insights-api/v1/artist/{id}/audience/gender-by-age",
                    params=params,
                    headers=headers,
                )
                if response.text == "Token expired":
                    print("expired tokne")
                    auth_header = reload_auth(driver)
                    headers = {
                        "authority": "generic.wg.spotify.com",
                        "accept": "application/json",
                        "accept-language": "en-US",
                        "app-platform": "Browser",
                        "authorization": f"{auth_header}",
                        "content-type": "application/json",
                        "origin": "https://artists.spotify.com",
                        "referer": "https://artists.spotify.com/",
                        "sec-fetch-dest": "empty",
                        "sec-fetch-mode": "cors",
                        "sec-fetch-site": "same-site",
                        "spotify-app-version": "1.0.0.12cdad2",
                        "user-agent": "Mozilla/5.0 (X11; Linux aarch64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.188 Safari/537.36 CrKey/1.54.250320 Edg/115.0.0.0",
                    }
                    response = requests.get(
                        f"https://generic.wg.spotify.com/s4x-insights-api/v1/artist/{id}/audience/gender-by-age",
                        params=params,
                        headers=headers,
                    )
                try:
                    stacked_df = pd.DataFrame(response.json()).stack()
                except:
                    # print(response.text)
                    continue

                df = pd.DataFrame(response.json()).iloc[:, 7:]

                stacked_df = df.stack()

                # Reset the index to convert the MultiIndex into columns
                reshaped_df = stacked_df.reset_index()

                # Rename the columns to 'gender' and 'age'
                reshaped_df.columns = ["gender", "age", "listeners"]
                reshaped_df["Date"] = dat
                reshaped_df["country"] = country_name
                reshaped_df["artist_id"] = id
                reshaped_df["artist_name"] = namex

                reshaped_df["age"] = reshaped_df["age"].apply(
                    lambda x: x.rstrip("_gender").lstrip("age_").replace("_", "-")
                )
                bov = reshaped_df[
                    [
                        "Date",
                        "gender",
                        "age",
                        "country",
                        "listeners",
                        "artist_id",
                        "artist_name",
                    ]
                ]
                lb.append(bov)

                print(f"{namex} -->  ,Data fetched for {country_name} ")

        jk = pd.concat(lb)

        # jk.to_csv(f"{lit}_a.csv",index=False,quoting=csv.QUOTE_ALL, sep="|")

        file_name = f"spotify_demographic/{dat}_a.csv"

        csv_content = jk.to_csv(index=False, quoting=csv.QUOTE_ALL, sep="|")
        result = cloudinary.uploader.upload(
            StringIO(csv_content),
            public_id=file_name,
            folder="/Soundcloud/",
            resource_type="raw",
            overwrite=True,
        )

        return Response(
            {
                "status": "success",
            },
            status=201,
        )








class source(APIView):
    @staticmethod
    def get(req):
        from datetime import date, timedelta

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
        dat = str(date.today() - timedelta(2))
        art = [
            (i["uri"].lstrip("spotify:artist:"), i["name"])
            for i in teams
            if i["uri"].startswith("spotify:artist")
        ]

        lb = []

        headers = {
            'authority': 'generic.wg.spotify.com',
            'accept': 'application/json',
            'accept-language': 'en-US',
            'app-platform': 'Browser',
            'authorization': 'Bearer BQAwYsAzKnCAa3woGE2JYlb-B7lZCucFSClFn1K_xVPpgoDEQrCAVxLhijmTPcsRkJb_gmvdOTCYAivDgvQYWylzzoxwdH0J9MUieEi7biTQN9pKZx5EJ64VcEQOd67hXzCaYTakyKTg1ngKpkHOAWpi7Lp5FN8ixM8TqJeNfTIfxrgrOZ3gZbi1S8QTYVRybW9zs5GhY0l6uLy3LKepbffU9h7M',
            'content-type': 'application/json',
            'grpc-timeout': '10S',
            'origin': 'https://artists.spotify.com',
            'referer': 'https://artists.spotify.com/',
            'sec-ch-ua': '"Microsoft Edge";v="117", "Not;A=Brand";v="8", "Chromium";v="117"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'same-site',
            'spotify-app-version': '1.0.0.b149c28',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36 Edg/117.0.2045.60',
        }
        for id, namex in art[:]:
              # cd = ""
            params = {
                'time-filter': '28day',
            }
            print(id)
            response = requests.get(
                f'https://generic.wg.spotify.com/s4x-insights-api/v1/artist/{id}/audience/source',
                params=params,
                headers=headers,
            )
            
            if response.text == "Token expired":
                print("expired token")
                auth_header = reload_auth(driver)
                headers = {
                    "authority": "generic.wg.spotify.com",
                    "accept": "application/json",
                    "accept-language": "en-US",
                    "app-platform": "Browser",
                    "authorization": f"{auth_header}",
                    "content-type": "application/json",
                    "origin": "https://artists.spotify.com",
                    "referer": "https://artists.spotify.com/",
                    "sec-fetch-dest": "empty",
                    "sec-fetch-mode": "cors",
                    "sec-fetch-site": "same-site",
                    "spotify-app-version": "1.0.0.12cdad2",
                    "user-agent": "Mozilla/5.0 (X11; Linux aarch64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.188 Safari/537.36 CrKey/1.54.250320 Edg/115.0.0.0",
                }
                response = requests.get(
                    f'https://generic.wg.spotify.com/s4x-insights-api/v1/artist/{id}/audience/source',
                    params=params,
                    headers=headers,
                )
                print("lol",response.text)
            try:
              data = response.json()
            except:
                gvhjnh
                # print(response.text)
                continue

            df = pd.DataFrame([data])

            df["Date"] = dat
            df["artist_id"] = id
            df["artist_name"] = namex

            lb.append(df)

            print(f"{namex} -->  ")
        print(len(lb))
        jk = pd.concat(lb)

        # jk.to_csv(f"{lit}_a.csv",index=False,quoting=csv.QUOTE_ALL, sep="|")

        file_name = f"spotify_source/{dat}_a.csv"

        csv_content = jk.to_csv(index=False, quoting=csv.QUOTE_ALL, sep="|")
        result = cloudinary.uploader.upload(
            StringIO(csv_content),
            public_id=file_name,
            folder="/Soundcloud/",
            resource_type="raw",
            overwrite=True,
        )

        return Response(
            {
                "status": "success",
            },
            status=201,
        )