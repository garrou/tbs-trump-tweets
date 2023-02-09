import collections
import pandas as pd
import matplotlib.pyplot as plt

def get_100_most_frequent_words(path_data: str, path_stop: str) -> list[tuple[str, int]]:
    df = pd.read_csv(path_data, sep=";", header=None, names=["tweet", "date"])
    
    # Work with several lines
    df = df.head(10000)

    # Mask to remove RT
    df = df[df["tweet"].str.startswith("RT") == False]

    # Lowercase the words, split to get array
    words = df["tweet"].str.lower().str.split().sum()
    
    # Read stop words
    stop_words = pd.read_csv(path_stop, header=None, names=["word"])

    # Convert to dictionary
    stop_words = { word: 0 for word in stop_words["word"]}

    # Remove the stop words from the list of words
    words = [word for word in words if stop_words.get(word) == None]

    # Count the frequency of each word
    counter = collections.Counter(words)

    # Sort the words by frequency and select the top 100 words
    return counter.most_common(100)

def generate_chart(data: list[tuple[str, int]]) -> None:
    try:
        words = [word for word, _ in data]
        frequencies = [frequency for _, frequency in data]
        
        plt.scatter(frequencies, words)
        plt.xlabel("Frequency")
        plt.ylabel("Words")
        plt.title("Top 100 words")
        plt.show()
    except:
        print("Can't create chart")

def main():
    words_frequencies = get_100_most_frequent_words("./data/trump_tweets.txt", "./data/stop-words.txt")
    print(words_frequencies)
    generate_chart(words_frequencies)

main()
