import csv
import typing

import requests

APIKEY = ""
class Client:
    """Yandex geocoder API client.

    :Example:
        >>> from yandex_geocoder import Client
        >>> Client.coordinates('Хабаровск 60 октября 150')
        ('135.114326', '48.47839')

    """

    API_URL = "https://geocode-maps.yandex.ru/1.x/"
    PARAMS = {
        "apikey": APIKEY,
        "lang": "ru_RU",
        "results": 1,
    }

    @classmethod
    def request(cls, params: dict) -> dict:
        """Requests passed address and returns content of `response` key.

        Raises `YandexGeocoderHttpException` if response's status code is
        different from `200`.

        """
        response = requests.get(cls.API_URL, params=params)

        if response.status_code != 200:
            raise Exception("Non-200 response from yandex geocoder")

        return response.json()["response"]

    @classmethod
    def coordinates(cls, address: str) -> typing.Tuple[str, str]:
        """Returns a tuple of ccordinates (longtitude, latitude) for
        passed address.

        Raises Error if nothing found.

        """
        params = cls.PARAMS
        params.update({"format": "json", "geocode": address})
        try:
            data = cls.request(params)["GeoObjectCollection"]["featureMember"]
        except:
            print(cls.request(params)["GeoObjectCollection"]["featureMember"])
            raise
        if not data:
            print('"{}" not found'.format(address))
        if data:
            # type: str data[0]["GeoObject"]
            coordinates = data[0]["GeoObject"]["Point"]["pos"]
        else:
            coordinates = ""
        return tuple(coordinates.split(" "))

    @classmethod
    def address(cls, lon: str, lat: str) -> str:
        """Returns address for
        tuple (longtitude, latitude) passed ccordinates.

        Raises Error if nothing found.

        """
        address_coords = f"{lon},{lat}"
        params = cls.PARAMS
        params.update({"format": "json", "geocode": address_coords})
        try:
            data = cls.request(params)["GeoObjectCollection"]["featureMember"][
                0
            ]["GeoObject"]["metaDataProperty"]["GeocoderMetaData"]["Address"][
                "formatted"
            ]
        except IndexError:
            data = "!NOT FOUND"
        return data


if __name__ == "__main__":
    result = dict()
    with open(
        r"f_d.csv", "r", encoding="UTF-8"
    ) as csvfile:  # Открываю список адресов
        reader = csv.reader(csvfile, delimiter=";")
        for rownum, row in enumerate(reader):
            row.append((Client.coordinates(row[0])))
            result[rownum] = row

    with open(r"coords_filled_ya.csv", "w") as csvfile:
        writer = csv.writer(
            csvfile, delimiter="\t", quotechar='"', quoting=csv.QUOTE_MINIMAL
        )
        for rownum, row in result.items():
            writer.writerow(row)
