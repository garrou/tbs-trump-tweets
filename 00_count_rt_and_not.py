import pandas as pd
from typing import Tuple

def count_rt_and_not(path: str) -> Tuple[int, int]:
    df = pd.read_csv(path, sep=";", header=None, names=["tweet", "date"])
    total = len(df.values)

    # Mask to remove RT
    df = df[df["tweet"].str.contains("RT ") == False]
    rt = len(df.values)

    return total - rt, rt

def main() -> None:
    not_rt, rt = count_rt_and_not("./data/trump_tweets.txt")
    print(f"Not RT : {not_rt}, RT : {rt}")

main()