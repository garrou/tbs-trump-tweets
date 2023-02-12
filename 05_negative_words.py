import collections
import matplotlib.pyplot as plt
import pandas as pd

def get_50_most_negative_frequent_words(path_data: str, path_negative: str) -> list[tuple[str, int]]:
    df = pd.read_csv(path_data, sep=";", header=None, names=["tweet", "date"])

    # Mask to remove RT
    df = df[df["tweet"].str.contains("RT ") == False]

    # Lowercase the words, split to get array
    arr_words = df["tweet"].str.lower().str.split()
    words = []

    # Concatenate arrays
    for arr in arr_words:
        words.extend([word for word in arr])
    
    # Read negative words
    negative_words = pd.read_csv(path_negative, header=None, names=["word"])

    # Convert to dictionary
    negative_words = { word: 0 for word in negative_words["word"] }

    # Keep the negative words from the list of words
    words = [word for word in words if negative_words.get(word) == 0]

    # Count the frequency of each word
    counter = collections.Counter(words)

    # Sort the words by frequency and select the top 50 words
    return counter.most_common(50)

def generate_chart(data: list[tuple[str, int]]) -> None:
    try:
        words = [word for word, _ in data]
        frequencies = [frequency for _, frequency in data]
        
        plt.barh(words, frequencies, color="red")
        plt.xlabel("Frequency")
        plt.ylabel("Words")
        plt.title("Top 50 negative words")
        plt.show()
    except:
        print("Can't create chart")

def main():
    words_frequencies = get_50_most_negative_frequent_words("./data/trump_tweets.txt", "./data/negative-words.txt")
    print(words_frequencies)
    generate_chart(words_frequencies)

main()
