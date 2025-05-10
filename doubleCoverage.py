# Wstawiane są słowa o najmniejszym przekryciu z DFem słów już użytych oraz z najmniejszym przekryciem z DFem słów nieużytych (poza analizowanym słowe)
import pandas as pd
import wordOperations


# min_value = min(d.values())
# min_keys = [k for k in d if d[k] == min_value]


def leaveOnlyZeroLetteredWords(words: list[str], usedLettersDF: pd.DataFrame) -> list[str]:
    acceptedWords = []

    for word in words:
        addToList = False
        for pos, letter in enumerate(word):
            if usedLettersDF.loc[letter, pos] == 0:
                addToList = True
                break

        if addToList:
            acceptedWords.append(word)

    return acceptedWords


def doubleCoverage(words: list[str], reservoirDF: pd.DataFrame):
    usedLettersDF = wordOperations.createEmptyDF()
    weightedWords = wordOperations.assignValues(words, reservoirDF, True)

    usedWords = []

    top = weightedWords.popitem()
    topWord, topValue = top[0], top[1]
    usedWords.append(topWord)
    print(top)
    words.remove(topWord)

    for pos, letter in enumerate(topWord):
        usedLettersDF.at[letter, pos] += 1
        reservoirDF.at[letter, pos] -= 1

    print(usedLettersDF.values)

    print(usedLettersDF.eq(0).any().any())

    print(reservoirDF)

    # for _ in range(10):
    while 0 in usedLettersDF.values:

        words = leaveOnlyZeroLetteredWords(words, usedLettersDF)

        # print(0 in usedLettersDF.values)
        weightedWords = wordOperations.assignValues(words, usedLettersDF, True)
        min_value = min(weightedWords.values())
        min_keys = [k for k in weightedWords if weightedWords[k] == min_value]

        # print(weightedWords)

        weightedWords = wordOperations.assignValues(min_keys, reservoirDF, True)

        # print(weightedWords.keys())

        top = weightedWords.popitem()
        topWord, topValue = top[0], top[1]
        usedWords.append(topWord)
        print(top, min_value, len(min_keys))
        words.remove(topWord)

        for pos, letter in enumerate(topWord):
            usedLettersDF.at[letter, pos] += 1
            reservoirDF.at[letter, pos] -= 1
            # reservoirDF.loc[letter, pos] *= 2

        # print(usedLettersDF)

        # print(f'{len(usedWords)=}')

    print(usedWords)

    print(len(usedWords))
