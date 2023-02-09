import pandas as pd

def extract_date_from_file(path: str) -> pd.Series.values:
    df = pd.read_csv(path, sep=";", header=None, names=["tweet", "date"])

    # Select only one column
    column = df["date"]

    # Convert date to datetime and keep year
    year_column = pd.to_datetime(column, dayfirst=True).dt.year
    
    # Return only date
    return year_column.values

def main() -> None:
    years = extract_date_from_file("./data/trump_tweets.txt")

    for year in years:
        print(year)

main()