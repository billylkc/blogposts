from bs4 import BeautifulSoup
from datetime import datetime
from typing import List
import requests
import re
import os
import io
import pandas as pd
import numpy as np
import quandl
import requests


pd.set_option("display.max_columns", None)
quandl.ApiConfig.api_key = os.environ["QUANDL_TOKEN"]


def get_codes() -> List[int]:

    """
    Get all the codes from the listed companies in HK main board from HKEX page

    Args:
            None

    Returns:
            codes ([]int): List of codes in HKEX main board

    Example:
            codes = get_codes()

    Data preview:
            [1, 2, 3, 4, 5, 6, 11,..]
    """

    regex = re.compile(r"\s*(\d{5})(.*)")  # Get 5 digit codes only
    url = "https://www.hkexnews.hk/sdw/search/stocklist_c.aspx?sortby=stockcode&shareholdingdate={}".format(
        datetime.today().strftime("%Y%m%d")
    )  # derive url, e.g. https://www.hkexnews.hk/sdw/search/stocklist_c.aspx?sortby=stockcode&shareholdingdate=20210621

    res = requests.get(url)
    soup = BeautifulSoup(res.text, "html.parser")

    codes = []
    for s in soup.select("table.table > tbody > tr"):
        text = s.get_text().replace(" ", "").strip()  # Replace extra spaces
        matchResult = regex.search(text)

        if matchResult:
            code = int(
                matchResult.group(1).lstrip("0")
            )  # Convert to int, e.g. 00005 to 5

            if code <= 10000:  # main board only
                codes.append(code)

    return codes


def get_stock(num: int, nrow: int = 10) -> pd.DataFrame:

    """
    Call Quandl API to get the historical data for the stock number using GET requests

    Args:
       num (int): Stock num, e.g. 5
       nrow (int): No of rows specified in the API calls. Default 10

    Returns:
       data (Dataframe): Dataframe returned from Quandl API

    Example:
       data = get_stock(num=1, nrow=10)

    TODO:
       Add date parameter to specify the latest date of the call

    Data preview:
                  NominalPrice NetChange Change    Bid    Ask   PEx   High    Low  PreviousClose  ShareVolume000  Turnover000 LotSize   code
      Date
      2019-03-19         80.45      None   None  80.40  80.45  None  81.15  80.20          80.95          7374.0     593781.0    None  00001
      2019-03-20         82.50      None   None  82.50  82.55  None  83.30  80.30          80.45         12420.0    1018144.0    None  00001
      2019-03-21         81.60      None   None  81.60  81.75  None  83.50  81.60          82.50         12224.0    1009254.0    None  00001
      2019-03-22         83.80      None   None  83.75  83.80  None  84.65  82.85          81.60         13478.0    1124179.0    None  00001
    """

    today = datetime.today().strftime("%Y-%m-%d")  # e.g. 2021-06-23
    code = str(num).zfill(5)
    code_str = "HKEX/{}".format(code)  # e.g. HKEX/00005

    try:
        endpoint = "https://www.quandl.com/api/v3/datasets/{}/data.csv?limit={}&end_date={}&order={}&api_key={}".format(
            code_str,
            nrow,
            today,
            "desc",
            quandl.ApiConfig.api_key,
        )
        r = requests.get(endpoint).content
        data = pd.read_csv(io.StringIO(r.decode("utf-8")))

        data["Code"] = code

        col_name = data.columns.tolist()
        clean_col_name = [
            re.sub(r"\W+", "", x) for x in col_name
        ]  # Replace special character in column name
        col_dict = dict(zip(col_name, clean_col_name))

        data.rename(columns=col_dict, inplace=True)
        print("Finished getting code - {}".format(code))

        return data

    except Exception as e:
        print("No records - {}".format(code))
        print(e)


def get_all_stock(nrow: int = 10) -> pd.DataFrame:

    """ Loop through the list of codes, and concat the results to a single dataframe. """

    codes = get_codes()
    codes = codes[0:50]  # Hardcorded 20 stocks for demostration.

    # Initialize result dataframe
    result = pd.DataFrame()

    for code in codes:
        try:

            data = get_stock(code, nrow)
            result = pd.concat([result, data], sort=True)
            print("=========================")
            print(code)
            print(data.head())

        except Exception as e:
            print("No records")
            print(e)

    return result


def main():
    df = get_all_stock()
    print(df)


if __name__ == "__main__":
    main()
