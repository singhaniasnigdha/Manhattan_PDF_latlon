from sodapy import Socrata

import argparse
import pandas as pd

import utils
import warnings

warnings.filterwarnings("ignore")


def clean_crime_data(df, complaint_from):
    # Removes invalid dates
    df_by_boro = df[~df.cmplnt_fr_dt.str.startswith("10")]

    # Converts latitude and longtitude to float
    df_by_boro = df_by_boro.astype({"latitude": "float64", "longitude": "float64"})

    # Formats date
    df_by_boro["cmplnt_fr_dt"] = pd.to_datetime(
        df_by_boro["cmplnt_fr_dt"], format="%Y-%m-%d"
    )

    # Formats time
    df_by_boro["hour"] = pd.to_datetime(
        df_by_boro["cmplnt_fr_tm"], format="%H:%M:%S"
    ).dt.hour

    # Get crimes from the past 5 years only as of time of creation
    return df_by_boro[df_by_boro["cmplnt_fr_dt"] >= complaint_from]


def get_crime_data(complaint_from="2017-01-01", limit=150000):
    # Unauthenticated client only works with public data sets. Note 'None'
    # in place of application token, and no username or password:
    client = Socrata("data.cityofnewyork.us", None)

    # Example authenticated client (needed for non-public datasets):
    # client = Socrata(data.cityofnewyork.us,
    #                  MyAppToken,
    #                  userame="user@example.com",
    #                  password="AFakePassword")

    results = client.get(
        "qgea-i56i", boro_nm="MANHATTAN", prem_typ_desc="STREET", limit=limit
    )

    # Convert to pandas DataFrame
    results_df = pd.DataFrame.from_records(results)
    results_df = results_df.drop(
        columns=[
            "susp_age_group",
            "susp_race",
            "susp_sex",
            "housing_psa",
            "station_name",
            "hadevelopt",
            "vic_sex",
            "vic_race",
            "vic_age_group",
            "patrol_boro",
            "parks_nm",
            "juris_desc",
            "lat_lon",
        ],
        errors="ignore",
    ).dropna(subset=["latitude", "longitude", "cmplnt_fr_dt"])

    # Clean data
    return clean_crime_data(results_df, complaint_from)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--LIMIT", type=int, default=150000, help="max crime records to fetch"
    )
    parser.add_argument(
        "--COMPLAINT_DT", type=str, default="2017-01-01", help="earliest crime data"
    )
    parser.add_argument("--PLOT", type=bool, default=False, help="save KDE plot")
    parser.add_argument(
        "--FILE", type=str, default="crime_kde", help="file to save KDE"
    )

    args = parser.parse_args()

    df = get_crime_data(args.COMPLAINT_DT, args.LIMIT)
    kernel = utils.get_kde(df)
    utils.save_kde_cloudpickle(kernel, args.FILE)

    if args.PLOT:
        utils.plot_kde(kernel)
