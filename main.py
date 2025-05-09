import loading
import wordOperations

if __name__ == '__main__':
    words = loading.loadWords()

    weights = wordOperations.createWeightmap(words)
    weightedWords = wordOperations.assignValues(words, weights)

    wordCount = 0

    for _ in words:
        wordCount += 1
        top = weightedWords.popitem()
        topWord, topValue = top[0], top[1]
        print(f'{topWord}\t{topValue}')

        if topValue == 0:
            break

        weights = wordOperations.alignWeights(topWord, weights)
        weightedWords = wordOperations.assignValues(words, weights)

    print(f'{wordCount=}')
