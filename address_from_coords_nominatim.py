import csv

import requests


class Client:
    """Yandex geocoder API client.

    :Example:
        >>> from yandex_geocoder import Client
        >>> Client.coordinates('Хабаровск 60 октября 150')
        ('135.114326', '48.47839')

    """

    API_URL = "https://nominatim.openstreetmap.org/reverse/"
    PARAMS = {"format": "json", "zoom": 18, "accept-language": "ru-RU"}

    @classmethod
    def request(cls, params: dict) -> dict:
        response = requests.get(
            cls.API_URL, params=params
        )
        return response.json()

    @classmethod
    def address(cls, lon: str, lat: str) -> str:
        """Returns address for
        tuple (longtitude, latitude) passed ccordinates.
        """
        params = cls.PARAMS
        params.update({"lon": lon, "lat": lat})
        data = cls.request(params)
        return data

if __name__ == '__main__':
    result = dict()
    with open(r"C:\TEMP\coords.csv", 'r') as csvfile:
        reader = csv.reader(csvfile, delimiter=';')
        for rownum, row in enumerate(reader):
            row.append((Client.address(row[1], row[0])))
            result[rownum] = row
    # print(Client.address('37.611733', '55.621719'))
    print(result)
    with open(r'C:\TEMP\coords_filled.csv', 'w') as csvfile:
        writer = csv.writer(csvfile, delimiter=',',
                                quotechar='"', quoting=csv.QUOTE_MINIMAL)
        for rownum, row in result.items():
            writer.writerow(row)
