import json
from typing import Dict, Optional, Tuple, Union

import pandas as pd
from tqdm import tqdm

import address_from_coords_nominatim
import get_address_from_ya

INPUT_CSV = "planners_bs_400.csv"  # "planners_bs.csv"
TEST_CSV = "test_data.csv"
ADDITIONAL_YANDEX_PARAMS = {
    "kind": "house",
}


def make_tuple(x):
    return tuple(x)


def get_osm_address():
    df = pd.read_csv(INPUT_CSV, delimiter=";", decimal=",")
    df["coordinates"] = df[["LON", "LAT"]].apply(make_tuple, axis=1)
    osm = list()

    for index, row in tqdm(df.iterrows(), total=df.shape[0]):
        try:
            obj = address_from_coords_nominatim.Client.address(
                *row["coordinates"]
            )
            osm.append((index, obj))
        except json.JSONDecodeError:
            print("JSONDecodeError")
            osm.append((index, "fail"))

    df["osm"] = [i[1] for i in osm]


def get_address(
    client,
    name: str,
    part_indexes: Optional[Tuple[int, int]] = None,
    additional_params: Optional[Dict[str, Union[str, int]]] = None,
):
    df = pd.read_csv(INPUT_CSV, delimiter=";")  # , decimal=","
    if part_indexes:
        df = df.iloc[part_indexes[0] : part_indexes[1]]
        name += f"_{part_indexes[0]}_{part_indexes[1]}"
    if additional_params:
        client.PARAMS.update(**additional_params)
    df.dropna(subset=["SITE_ID", "LON", "LAT"], inplace=True)
    df["coordinates"] = df[["LON", "LAT"]].apply(make_tuple, axis=1)
    addresses = list()
    for index, row in tqdm(df.iterrows(), total=df.shape[0]):
        try:
            obj = client.address(*row["coordinates"])
            addresses.append((index, obj))
        except json.JSONDecodeError:
            print("JSONDecodeError")
            addresses.append((index, "fail"))

    df["addresses"] = [i[1] for i in addresses]
    df.to_excel(f"{name}.xlsx")
    df.to_pickle(f"{name}.pkl")


if __name__ == "__main__":
    client = get_address_from_ya.Client
    part_indexes = None  # (0, 950)
    additional_params = ADDITIONAL_YANDEX_PARAMS
    name = "yandex"
    get_address(client, name, part_indexes, additional_params)
