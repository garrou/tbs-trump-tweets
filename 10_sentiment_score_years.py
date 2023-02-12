import matplotlib.pyplot as plt
import pandas as pd

def count_sentiment_score_by_years(path_data: str, path_stop: str, path_positive: str, path_negative: str) -> dict[int, int]:
    df = pd.read_csv(path_data, sep=";", header=None, names=["tweet", "date"])
    df_positive = pd.read_csv(path_positive, header=None, names=["word"])
    df_negative = pd.read_csv(path_negative, header=None, names=["word"])
    df_stop = pd.read_csv(path_stop, header=None, names=["word"])
    words = {}

    for v in df.values:
        words[v[1]] = v[0].lower().split()

    # Convert to dictionary
    positive_words = { word: 0 for word in df_positive["word"] }
    negative_words = { word: 0 for word in df_negative["word"] }
    stop_words = { word: 0 for word in df_stop["word"] }

    # Remove stop word in dictionary
    for key in words:
        words[key] = [word for word in words[key] if stop_words.get(word) == None]

    # Keep only positive and negative words in dictionary
    for key in words:
        words[key] = [word for word in words[key] if positive_words.get(word) == 0 or negative_words.get(word) == 0]
    
    return get_scores_by_year(words, positive_words, negative_words)

def get_scores_by_year(words: dict[str, list[str]], positive_words: dict[str, int], negative_words: dict[str, int]) -> dict[int, int]:
    scores = {}

    for key in words:
        year = pd.to_datetime(key, dayfirst=True).year

        if scores.get(year) == None:
            scores[year] = 0

        for w in words[key]:
            if positive_words.get(w) == 0:
                scores[year] += 1
            elif negative_words.get(w) == 0:
                scores[year] -= 1

    keys = list(scores.keys())
    keys.sort()

    return {i: scores[i] for i in keys}

def generate_chart(data: dict[int, int]) -> None:
    try:       
        plt.barh(list(data.keys()), list(data.values()), color="green")
        plt.xlabel("Years")
        plt.ylabel("Scores")
        plt.title("Sentiment score by years")
        plt.show()
    except:
        print("Can't create chart")

def main():
    scores = count_sentiment_score_by_years("./data/trump_tweets.txt", "./data/stop-words.txt", "./data/positive-words.txt", "./data/negative-words.txt")
    print(scores)
    generate_chart(scores)

main()
    

    