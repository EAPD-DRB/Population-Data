"""
------------------------------------------------------------------------
Functions for generating demographic objects necessary for the OG-USA
model
------------------------------------------------------------------------
"""

# Import packages
import os
import pandas as pd
from io import StringIO
import argparse
import urllib3
import ssl
import requests
from constants import START_YEAR, END_YEAR, COUNTRY_DICT, SERIES_DICT


UN_COUNTRY_CODE = "840"  # UN code for USA
# create output director for figures
CUR_PATH = os.path.split(os.path.abspath(__file__))[0]
OUTPUT_DIR = os.path.join(CUR_PATH, "..", "Data")
if os.access(OUTPUT_DIR, os.F_OK) is False:
    os.makedirs(OUTPUT_DIR)


"""
------------------------------------------------------------------------
Define functions
------------------------------------------------------------------------
"""


def get_un_data(
    variable_code,
    country_id=UN_COUNTRY_CODE,
    start_year=START_YEAR,
    end_year=END_YEAR,
    un_token=None,
):
    """
    This function retrieves data from the United Nations Data Portal API
    for UN population data (see
    https://population.un.org/dataportal/about/dataapi)

    Args:
        variable_code (str): variable code for UN data
        country_id (str): country id for UN data
        start_year (int): start year for UN data
        end_year (int): end year for UN data
        un_token (str): UN WPP API token

    Returns:
        df (Pandas DataFrame): DataFrame of UN data
    """
    target = (
        "https://population.un.org/dataportalapi/api/v1/data/indicators/"
        + variable_code
        + "/locations/"
        + country_id
        + "/start/"
        + str(start_year)
        + "/end/"
        + str(end_year)
        + "?format=csv"
    )

    # get data from url
    payload = {}
    headers = {"Authorization": "Bearer "  + un_token}
    response = get_legacy_session().get(target, headers=headers, data=payload)
    # Check if the request was successful before processing
    if response.status_code == 200:
        csvStringIO = StringIO(response.text)
        df = pd.read_csv(csvStringIO, sep="|", header=1)

        # keep just what is needed from data
        df = df[df.Variant == "Median"]
        df = df[df.Sex == "Both sexes"][["TimeLabel", "AgeLabel", "Value"]]
        df.rename(
            {"TimeLabel": "year", "AgeLabel": "age", "Value": "value"},
            axis=1,
            inplace=True,
        )
        df.loc[df.age == "100+", "age"] = 100
        df.age = df.age.astype(int)
        df.year = df.year.astype(int)
        df = df[df.age < 100]  # need to drop 100+ age category
    else:
        print(
            f"Failed to retrieve population data. HTTP status code: {response.status_code}"
        )
        assert False

    return df


class CustomHttpAdapter(requests.adapters.HTTPAdapter):
    """
    The UN Data Portal server doesn't support "RFC 5746 secure renegotiation". This causes and error when the client is using OpenSSL 3, which enforces that standard by default.
    The fix is to create a custom SSL context that allows for legacy connections. This defines a function get_legacy_session() that should be used instead of requests().
    """

    # "Transport adapter" that allows us to use custom ssl_context.
    def __init__(self, ssl_context=None, **kwargs):
        self.ssl_context = ssl_context
        super().__init__(**kwargs)

    def init_poolmanager(self, connections, maxsize, block=False):
        self.poolmanager = urllib3.poolmanager.PoolManager(
            num_pools=connections,
            maxsize=maxsize,
            block=block,
            ssl_context=self.ssl_context,
        )


def get_legacy_session():
    ctx = ssl.create_default_context(ssl.Purpose.SERVER_AUTH)
    ctx.options |= 0x4  # OP_LEGACY_SERVER_CONNECT  #in Python 3.12 you will be able to switch from 0x4 to ssl.OP_LEGACY_SERVER_CONNECT.
    session = requests.session()
    session.mount("https://", CustomHttpAdapter(ctx))
    return session


def fetch_country_data(
    initial_data_year=START_YEAR,
    final_data_year=END_YEAR,
    un_token=None,
):
    """
    This function downloads and save data for each country

    Args:
        initial_data_year (int): initial year of data to use
        final_data_year (int): final year of data to use,
        un_token (str): UN WPP API token

    Returns:
        None

    """
    # Loop over countries
    for k, v in COUNTRY_DICT.items():
        # Loop over population series to grab
        for kk, vv in SERIES_DICT.items():
            # download data
            df = get_un_data(
                vv,
                country_id=v,
                start_year=initial_data_year,
                end_year=final_data_year,
                un_token=un_token,
            )
            # make directory for country if not exist
            if os.access(os.path.join(OUTPUT_DIR, k), os.F_OK) is False:
                os.makedirs(os.path.join(OUTPUT_DIR, k))
            # save data
            df.to_csv(
                os.path.join(OUTPUT_DIR, k, "UN_{s}_data.csv".format(s=kk)),
                index=False,
            )


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("token", help="UN WPP API token")  # positional arg

    fetch_country_data(un_token=parser.parse_args().token)
