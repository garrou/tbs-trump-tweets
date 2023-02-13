import collections
import matplotlib.pyplot as plt
import pandas as pd

def get_50_most_contextual_frequent_words(path_data: str, path_stop: str, path_positive: str, path_negative: str) -> list[tuple[str, int]]:
    df = pd.read_csv(path_data, sep=";", header=None, names=["tweet", "date"])

    # Mask to remove RT
    df = df[df["tweet"].str.contains("RT") == False]

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
    stop_words = { word: True for word in stop_words["word"] }

    # Convert to dictionary
    positive_words = { word: True for word in positive_words["word"] }

    # Convert to dictionary
    negative_words = { word: True for word in negative_words["word"] }

    # Merge dictionaries
    contextual_words = {}
    contextual_words.update(stop_words)
    contextual_words.update(positive_words)
    contextual_words.update(negative_words)

    # Keep the contextual words from the list of words
    words = [word for word in words if contextual_words.get(word) == None]

    # Count the frequency of each word
    counter = collections.Counter(words)

    # Sort the words by frequency and select the top 50 words
    return counter.most_common(50)

def generate_chart(data: list[tuple[str, int]]) -> None:
    try:
        words = [word for word, _ in data]
        frequencies = [frequency for _, frequency in data]
        
        plt.barh(words, frequencies)
        plt.xlabel("Frequency")
        plt.ylabel("Words")
        plt.title("Top 50 contextual words")
        plt.show()
    except:
        print("Can't create chart")

def main():
    words_frequencies = get_50_most_contextual_frequent_words(
        path_data="./data/trump_tweets.txt", 
        path_stop="./data/stop-words.txt", 
        path_positive="./data/positive-words.txt", 
        path_negative="./data/negative-words.txt"
    )
    print(words_frequencies)
    generate_chart(words_frequencies)

main()
