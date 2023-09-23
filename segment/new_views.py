from segment.utils import *

from segment.teams import *
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
        auth_header = "Bearer BQBFRv09uD_oWhI4wMsI7yGmX_qB9naqPFgfNk4dmWNTGvVw9_Mrdsl472GI9OOmCwh5IzIWs42jebXpu9odM-ShlVX5aBIWz_2jNFSnXRn05ldtUWcLHUW7VW77bkSiDN6FdjoUiZruhIMWCrjXtU-NrrgnnN3UItHXnL1xqEN_45resCOa5Jb0-xlFGnWuefzvKPPElL-m16zUFhbgZc-7"
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

                print(f"{namex} -->  ,Data fetched for {country_name} ")

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

        oki = df[
            df.Date.isin(
                [
                    str(date.today() - timedelta(4)),
                    str(date.today() - timedelta(3)),
                    str(date.today() - timedelta(2)),
                    str(date.today() - timedelta(1)),
                ]
            )
        ]

        unique_dates = oki["Date"].unique()
        lat = []

        for date in unique_dates:
            # Filter the dataframe for the specific date
            din = oki[oki["Date"] == date]
            if (
                din[din.country == "Worldwide"].total_active_audience_listeners.iloc[0]
                == 0
            ):
                continue
            # Convert the date to a string format suitable for filenames
            date_str = str(date)
            lat.append(date_str)
            file_name = f"spotify_segments/{date_str}_a.csv"

            csv_content = din.to_csv(index=False, quoting=csv.QUOTE_ALL, sep="|")
            result = cloudinary.uploader.upload(
                StringIO(csv_content),
                public_id=file_name,
                folder="/Soundcloud/",
                resource_type="raw",
                overwrite=True,
            )

        lit = get_latest_date(lat)

        lb = []

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
                reshaped_df["Date"] = lit
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

        file_name = f"spotify_demographic/{lit}_a.csv"

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
