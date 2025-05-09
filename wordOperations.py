import pandas as pd
import numpy as np


def createWeightmap(words: list[str]) -> pd.DataFrame:
    column_labels = [0, 1, 2, 3, 4]
    row_labels = [
        "a", "b", "c", "d", "e", "f", "g", "h", "i", "j",
        "k", "l", "m", "n", "o", "p", "q", "r", "s", "t",
        "u", "v", "w", "x", "y", "z"
    ]

    df = pd.DataFrame(
        np.zeros(
            (
                len(row_labels),
                len(column_labels)
            )
        ), index=row_labels, columns=column_labels
    )
    df = df.astype(int)

    # word = words[0]

    for word in words:

        # print(word)
        for i, letter in enumerate(word):
            df.loc[letter, i] += 1
            # print(f"{i}. letter is {letter}")

    print(df)

    return df


def assignValues(words: list[str], weights: pd.DataFrame) -> dict[str, int]:
    valueDict = {}

    for word in words:
        value = 0
        for i, letter in enumerate(word):
            value += weights.loc[letter, i]

        valueDict.update({word: int(value)})

    valueDict = dict(sorted(valueDict.items(), key=lambda item: item[1]))
    # print(valueDict)

    return valueDict


def alignWeights(word: str, weights: pd.DataFrame) -> pd.DataFrame:
    for i, letter in enumerate(word):
        weights.loc[letter, i] = 0

    return weights
