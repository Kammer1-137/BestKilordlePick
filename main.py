import loading
import wordOperations

import time

if __name__ == '__main__':
    words = loading.loadWords()

    # start = time.time()
    # weights = wordOperations.createWeightmap(words)
    # end = time.time()
    # print(f'Stara wersja: {end - start}')
    #
    # start = time.time()
    # weights = wordOperations.createWeightmapOptimized(words)
    # end = time.time()
    # print(f'Npwa wersja: {end - start}')

    weights = wordOperations.createWeightmapOptimized(words)
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
