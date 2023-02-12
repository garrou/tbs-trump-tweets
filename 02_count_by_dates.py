import matplotlib.pyplot as plt
import pandas as pd

def count_tweets_by_date(path: str) -> pd.DataFrame:
    df = pd.read_csv(path, sep=";", header=None, names=["tweet", "date"])
    date_column = "date"

    # Select only one column
    column = df[date_column]

    # Convert date to datetime and keep year
    year_column = pd.to_datetime(column, dayfirst=True).dt.year

    # Add header on series
    year_column = year_column.to_frame(date_column)

    # Group by date and count occurrences of each date
    grouped = df.groupby(year_column[date_column]).size().reset_index(name="count")
    
    # Sort by date
    return grouped.sort_values(date_column)

def generate_chart(data: pd.DataFrame) -> None:
    try:
        data.plot.bar(x="date", y="count")
        plt.show()
    except:
        print("Can't create chart")

def main() -> None:
    dataframe = count_tweets_by_date("./data/trump_tweets.txt")
    print(dataframe)
    generate_chart(dataframe)
    
main()