import collections
import matplotlib.pyplot as plt
import pandas as pd
from typing import Tuple

def get_covid_frequent(path_data: str, path_stop: str, path_positive: str, path_negative: str) -> Tuple[list[tuple[str, int]], list[tuple[str, int]], list[tuple[str, int]]]:
    df = pd.read_csv(path_data, sep=";", header=None, names=["tweet", "date"])

    # Mask to remove RT
    df = df[df["tweet"].str.contains("RT ") == False]
    
    # Mask to keep only the tweets of the covid
    mask = (df["tweet"].str.contains("covid", case=False) | df["tweet"].str.contains("sars-cov", case=False))
    df = df[mask]

    # Lowercase the words, split to get array
    arr_words = df["tweet"].str.lower().str.split()
    words = []

    # Concatenate arrays
    for arr in arr_words:
        words.extend([word for word in arr])

    # Read stop words
    stop_words = pd.read_csv(path_stop, header=None, names=["word"])

    # Read positive words
    positive_words = pd.read_csv(path_positive, header=None, names=["word"])
    
    # Read negative words
    negative_words = pd.read_csv(path_negative, header=None, names=["word"])

    # Convert to dictionary
    stop_words = { word: 0 for word in stop_words["word"] }

    # Convert to dictionary
    positive_words = { word: 0 for word in positive_words["word"] }

    # Convert to dictionary
    negative_words = { word: 0 for word in negative_words["word"]}

    # Create contextual words dictionary
    contextual_words = {}
    contextual_words.update(stop_words)
    contextual_words.update(positive_words)
    contextual_words.update(negative_words)

    # Get only contextual words
    contextual_words = [word for word in words if contextual_words.get(word) == None]

    # Keep only positive and negative words
    positive_words = [word for word in words if positive_words.get(word) == 0]
    negative_words = [word for word in words if negative_words.get(word) == 0]

    # Count the frequency of each word
    contextual_counter = collections.Counter(contextual_words)
    positive_counter = collections.Counter(positive_words)
    negative_counter = collections.Counter(negative_words)

    return contextual_counter.most_common(10), positive_counter.most_common(10), negative_counter.most_common(10)
 
def generate_chart(
    contextual: list[tuple[str, int]],
    positive: list[tuple[str, int]],
    negative: list[tuple[str, int]]
) -> None:

    try:
        contextual_words = [word for word, _ in contextual]
        contextual_frequencies = [frequency for _, frequency in contextual]

        positive_words = [word for word, _ in positive]
        positive_frequencies = [frequency for _, frequency in positive]

        negative_words = [word for word, _ in negative]
        negative_frequencies = [frequency for _, frequency in negative]

        _, axs = plt.subplots(3)
        
        axs[0].set_title("Top 10 covid contextual words")
        axs[0].barh(contextual_words, contextual_frequencies, color="orange")

        axs[1].set_title("Top 10 covid positive words")
        axs[1].barh(positive_words, positive_frequencies, color="green")

        axs[2].set_title("Top 10 covid negative words")
        axs[2].barh(negative_words, negative_frequencies, color="red")
        
        plt.show()
    except:
        print("Can't create chart")

def main():
    contextual_frequencies, positive_frequencies, negative_frequencies = get_covid_frequent(
        path_data="./data/trump_tweets.txt", 
        path_stop="./data/stop-words.txt", 
        path_positive="./data/positive-words.txt", 
        path_negative="./data/negative-words.txt"
    )
    print(contextual_frequencies)
    print(positive_frequencies)
    print(negative_frequencies)
    
    generate_chart(contextual_frequencies, positive_frequencies, negative_frequencies)

main()
