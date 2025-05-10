import loading
import wordOperations
import doubleCoverage

import time

wordOperations.defineMode('+')

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

    start = time.time()
    doubleCoverage.doubleCoverage(words, weights)
    end = time.time()
    print(f'Stara wersja: {end - start}')

    # wordCount = wordOperations.findBestWords(words)
    #
    # print(f'{wordCount=}')
