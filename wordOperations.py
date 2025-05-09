import pandas as pd
import numpy as np
from collections import Counter

algoDict = None


def createEmptyDF() -> pd.DataFrame:
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
    return df


def createWeightmap(words: list[str]) -> pd.DataFrame:
    df = createEmptyDF()

    # word = words[0]

    for word in words:

        # print(word)
        for i, letter in enumerate(word):
            df.loc[letter, i] += 1
            # print(f"{i}. letter is {letter}")

    # print(df)

    return df


def createWeightmapOptimized(words: list[str]) -> pd.DataFrame:
    df = createEmptyDF()

    transposed = ["".join(row) for row in zip(*words)]
    # print(len(transposed))

    for column, letters in enumerate(transposed):
        c = Counter(letters)
        # print(c)

        for letter, number in c.items():
            df.loc[letter, column] = number

    # print(df)

    return df


def assignValues(words: list[str], weights: pd.DataFrame) -> dict[str, int]:
    valueDict = {}

    for word in words:
        value = algoDict['border']
        for i, letter in enumerate(word):
            value = algoDict['calculate'](value, weights.loc[letter, i])
            # value += weights.loc[letter, i]

        valueDict.update({word: int(value)})

    valueDict = dict(sorted(valueDict.items(), key=lambda item: item[1]))
    # print(valueDict)

    return valueDict


def alignWeights(word: str, weights: pd.DataFrame) -> pd.DataFrame:
    for i, letter in enumerate(word):
        weights.loc[letter, i] = algoDict['border']

    return weights


def defineMode(symbol: 'str') -> dict:
    if symbol not in ['+', '*']:
        exit(1)

    global algoDict

    match symbol:
        case '+':
            border = 0
            calculate = lambda a, b: a + b
        case '*':
            border = 1
            calculate = lambda a, b: a * b

    algoDict = {
        'border': border,
        'calculate': calculate
    }


def findBestWords(words: list[str], algoSymbol: str = '+') -> int:
    condit = True
    wordCount = 0

    print(algoDict)

    weights = createWeightmapOptimized(words)
    weightedWords = assignValues(words, weights)

    while condit:
        wordCount += 1
        top = weightedWords.popitem()
        topWord, topValue = top[0], top[1]
        print(f'{topWord}\t{topValue}')

        if topValue == algoDict['border']:
            condit = False

        weights = alignWeights(topWord, weights)
        weightedWords = assignValues(words, weights)

    return wordCount
