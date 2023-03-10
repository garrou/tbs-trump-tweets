import collections
import matplotlib.pyplot as plt
import pandas as pd

def get_20_most_cited_hashtags(path_data: str):
    df = pd.read_csv(path_data, sep=";", header=None, names=["tweet", "date"])

    # Mask to remove RT
    df = df[df["tweet"].str.contains("RT") == False]

    # Mask to get only tweets with #
    df = df[df["tweet"].str.contains("#") == True]

    arr_words = df["tweet"].str.split()
    words = []

    # Concatenate array of words and filter with # and remove '"'
    for arr in arr_words:
        words.extend([word.replace('"', "") for word in arr if word.find("#") != -1])

    # Count the frequency of each word
    counter = collections.Counter(words)

    # Sort the words by frequency and select the top 20 cited hashtags
    return counter.most_common(20)

def generate_chart(data: list[tuple[str, int]]) -> None:
    try:
        words = [word for word, _ in data]
        frequencies = [frequency for _, frequency in data]
        
        plt.barh(words, frequencies, color="orange")
        plt.xlabel("Frequency")
        plt.ylabel("Hashtag")
        plt.title("Top 20 cited hashtags")
        plt.show()
    except:
        print("Can't create chart")

def main():
    frequencies = get_20_most_cited_hashtags("./data/trump_tweets.txt")
    print(frequencies)
    generate_chart(frequencies)

main()