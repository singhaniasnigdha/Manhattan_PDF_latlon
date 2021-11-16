from sodapy import Socrata

import argparse
import pandas as pd

import utils
import warnings

warnings.filterwarnings("ignore")


def split_save_types(df):
    edu_df = df[
        df["facgroup"].isin(
            [
                "VOCATIONAL AND PROPRIETARY SCHOOLS",
                "HIGHER EDUCATION",
                "DAY CARE AND PRE-KINDERGARTEN",
                "SCHOOLS (K-12)",
            ]
        )
    ]

    culture_df = df[
        df["facgroup"].isin(
            [
                "CULTURAL INSTITUTIONS",
                "LIBRARIES",
                "HISTORICAL SITES",
                "CITY AGENCY PARKING, MAINTENANCE, AND STORAGE",
                "PARKS AND PLAZAS",
            ]
        )
    ]

    health_df = df[
        df["facgroup"].isin(
            [
                "HEALTH CARE",
                "CHILD SERVICES AND WELFARE",
                "HUMAN SERVICES",
                "EMERGENCY SERVICES",
            ]
        )
    ]

    services_df = df[
        df["facgroup"].isin(
            [
                "TELECOMMUNICATIONS",
                "PUBLIC SAFETY",
                "JUSTICE AND CORRECTIONS",
                "TRANSPORTATION",
                "ADULT SERVICES",
                "YOUTH SERVICES",
            ]
        )
    ]

    fac_df = {
        "education": edu_df,
        "cultural": culture_df,
        "health_ops": health_df,
        "other_services": services_df,
    }
    kernels = {}

    for k, v in fac_df.items():
        kernels[k] = utils.get_kde(v)
        utils.save_kde_cloudpickle(kernels[k], f"facilities/{k}")

    return kernels


def get_data(limit=500000):
    # Unauthenticated client only works with public data sets. Note 'None'
    # in place of application token, and no username or password:
    client = Socrata("data.cityofnewyork.us", None)

    # Example authenticated client (needed for non-public datasets):
    # client = Socrata(data.cityofnewyork.us,
    #                  MyAppToken,
    #                  userame="user@example.com",
    #                  password="AFakePassword")

    results = client.get("ji82-xba5", boro="MANHATTAN", limit=limit)

    # Convert to pandas DataFrame
    facilities_df = pd.DataFrame.from_records(results)
    print(f"Imported {len(facilities_df)} facilities for Manhattan")

    # Clean data
    facilities_df = facilities_df.drop(
        columns=["xcoord", "ycoord", "uid", "zipcode", "bin", "bbl"], errors="ignore"
    ).dropna(subset=["latitude", "longitude", "facgroup", "factype"])
    facilities_df = facilities_df.astype(
        {"latitude": "float64", "longitude": "float64"}
    )
    facilities_df = facilities_df[facilities_df["latitude"] > 1]
    facilities_df = facilities_df[facilities_df["longitude"] < 0]

    print(f"# {len(facilities_df)} after clean-up")
    return facilities_df


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--LIMIT", type=int, default=500000, help="max records to fetch"
    )
    parser.add_argument("--PLOT", type=bool, default=False, help="save KDE plot")

    args = parser.parse_args()

    df = get_data(args.LIMIT)
    kernels = split_save_types(df)

    # if args.PLOT:
    #     utils.plot_kde(kernel)
