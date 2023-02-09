import collections
import pandas as pd
import matplotlib.pyplot as plt

def get_50_most_positive_frequent_words(path_data: str, path_positive: str) -> list[tuple[str, int]]:
    df = pd.read_csv(path_data, sep=";", header=None, names=["tweet", "date"])

    # Work with several lines
    df = df.head(10000)

    # Mask to remove RT
    mask = df["tweet"].str.startswith("RT") == False
    df = df[mask]

    # Lowercase the words, split to get array
    words = df["tweet"].str.lower().str.split().sum()
    
    # Read positive words
    positive_words = pd.read_csv(path_positive, header=None, names=["word"])

    # Convert to dictionary
    positive_words = { word: 0 for word in positive_words["word"]}

    # Keep the positive words from the list of words
    words = [word for word in words if positive_words.get(word) == 0]

    # Count the frequency of each word
    counter = collections.Counter(words)

    # Sort the words by frequency and select the top 50 words
    return counter.most_common(50)

def generate_chart(data: list[tuple[str, int]]) -> None:
    try:
        words = [word for word, _ in data]
        frequencies = [frequency for _, frequency in data]
        
        plt.barh(words, frequencies, color="green")
        plt.xlabel("Frequency")
        plt.ylabel("Words")
        plt.title("Top 50 positive words")
        plt.show()
    except:
        print("Can't create chart")

def main():
    words_frequencies = get_50_most_positive_frequent_words("./data/trump_tweets.txt", "./data/positive-words.txt")
    print(words_frequencies)
    generate_chart(words_frequencies)

main()
