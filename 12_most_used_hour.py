import pandas as pd

def get_most_used_hour(path: str):
    df = pd.read_csv(path, sep=";", header=None, names=["tweet", "date"])

    date_column = "date"

    # Select only one column
    column = df[date_column]

    # Convert date to datetime and keep year
    column = pd.to_datetime(column, dayfirst=True).dt.hour

    # Add header on series
    column = column.to_frame(date_column)

    # Group by date and count occurrences of each date
    grouped = df.groupby(column[date_column]).size().reset_index(name="count")
    
    # Get the max occur
    max_occur = grouped["count"].max()

    return grouped[grouped["count"] == max_occur]["date"].values[0]

def main():
    hour = get_most_used_hour("./data/trump_tweets.txt")
    print(f"Donald Trump tweets the most at {hour} h.")

main()