from sodapy import Socrata

import argparse
import pandas as pd

import utils
import warnings

warnings.filterwarnings("ignore")


def get_data(limit=500000):
    # Unauthenticated client only works with public data sets. Note 'None'
    # in place of application token, and no username or password:
    client = Socrata("data.cityofnewyork.us", None)

    # Example authenticated client (needed for non-public datasets):
    # client = Socrata(data.cityofnewyork.us,
    #                  MyAppToken,
    #                  userame="user@example.com",
    #                  password="AFakePassword")
    results = client.get(
        "w7w3-xahh", address_borough="Manhattan", license_status="Active", limit=limit
    )
    # Convert to pandas DataFrame
    biz_df = pd.DataFrame.from_records(results)
    print(f"Imported {len(biz_df)} legally operating businesses for Manhattan")

    # Clean-Up
    biz_df = biz_df.drop(
        columns=[
            "contact_phone",
            "address_state",
            "census_tract",
            "bin",
            "bbl",
            "address_building",
            "detail",
            "community_board",
            "council_district",
        ],
        errors="ignore",
    ).dropna(subset=["latitude", "longitude"])
    biz_df = biz_df.astype({"latitude": "float64", "longitude": "float64"})
    biz_df = biz_df[biz_df["license_status"] == "Active"]

    print(f"# {len(biz_df)} after clean-up")
    return biz_df


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--LIMIT", type=int, default=500000, help="max records to fetch"
    )
    parser.add_argument("--PLOT", type=bool, default=False, help="save KDE plot")
    parser.add_argument(
        "--FILE", type=str, default="legal_biz_kde", help="file to save KDE"
    )

    args = parser.parse_args()

    df = get_data(args.LIMIT)
    kernel = utils.get_kde(df)
    utils.save_kde_cloudpickle(kernel, args.FILE)

    if args.PLOT:
        utils.plot_kde(kernel, args.FILE)
