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


###########################

def doubleCoverageWithBranching(
        words: list[str],
        reservoirDF: pd.DataFrame,
        width: int = 4,
        depth: int = 3
):
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

    print(reservoirDF)

    # for _ in range(10):
    while 0 in usedLettersDF.values:
        currentDepth = 0
        branchDict = {}
        while currentDepth < depth:

            words = leaveOnlyZeroLetteredWords(words, usedLettersDF)

            weightedWords, min_value, min_keys = sortWorda(reservoirDF, usedLettersDF, words)

            # print(weightedWords.keys())
            lastElements = dict(list(weightedWords.items())[-width:])
            print(lastElements)

            for word, value in enumerate(lastElements.items()):
                print(word, value)
                weightedWords.pop(
                    word
                )

            top = weightedWords.popitem()
            topWord, topValue = top[0], top[1]
            usedWords.append(topWord)
            print(top, min_value, len(min_keys))
            words.remove(topWord)

            for pos, letter in enumerate(topWord):
                usedLettersDF.at[letter, pos] += 1
                reservoirDF.at[letter, pos] -= 1

            # print(usedLettersDF)
            # print(f'{len(usedWords)=}')

            currentDepth += 1

    print(usedWords)

    print(len(usedWords))


def sortWorda(reservoirDF: pd.DataFrame, usedLettersDF: pd.DataFrame, words: list[str]) -> (
        tuple)[dict[str, int], int, list[str]]:
    weightedWords = wordOperations.assignValues(words, usedLettersDF, True)
    min_value = min(weightedWords.values())
    min_keys = [k for k in weightedWords if weightedWords[k] == min_value]
    weightedWords = wordOperations.assignValues(min_keys, reservoirDF, True)
    return weightedWords, min_value, min_keys


import copy
import multiprocessing


# These helper functions must be defined in your code base.
# For example:
# def leaveOnlyZeroLetteredWords(words, usedLettersDF):
#     # ... filter words according to usedLettersDF ...
#     return filtered_words
#
# def sortWorda(reservoirDF, usedLettersDF, words):
#     # ... compute a dictionary mapping words to weights, plus maybe min_value and keys
#     # For example, return sortedWeightedWords, min_value, min_keys
#     return sorted_weighted_dict, min_value, min_keys

def candidate_branch(candidate: str,
                     value: int,
                     words: list,
                     reservoirDF: pd.DataFrame,
                     usedLettersDF: pd.DataFrame,
                     width: int,
                     depth: int) -> list:
    """
    Computes a branch (a list of candidate words) starting from a given candidate.
    This function works on copies of the input state (words, reservoirDF, usedLettersDF) so that each branch is independent.

    The branch is built by repeatedly filtering the available words and picking a candidate from
    the last `width` elements of the weighted dictionary (as computed by sortWorda).
    The recursion stops after 'depth' steps (or if no further candidate is found).
    """
    branch = [candidate]

    # Remove the candidate and update the state for this branch:
    local_words = words.copy()
    if candidate in local_words:
        local_words.remove(candidate)
    local_usedLettersDF = usedLettersDF.copy()
    local_reservoirDF = reservoirDF.copy()
    for pos, letter in enumerate(candidate):
        local_usedLettersDF.at[letter, pos] += 1
        local_reservoirDF.at[letter, pos] -= 1

    current_depth = 1
    # Continue branching until the desired depth has been reached.
    while current_depth < depth:
        local_words = leaveOnlyZeroLetteredWords(local_words, local_usedLettersDF)
        weightedWords, min_value, min_keys = sortWorda(local_reservoirDF, local_usedLettersDF, local_words)
        if not weightedWords:
            break

        # Select the candidate branch from the last width items
        new_candidates = dict(list(weightedWords.items())[-width:])
        print(new_candidates)
        # For simplicity, here we choose the first candidate from new_candidates.
        # (You could choose by another criterion.)
        top_candidate, top_value = list(new_candidates.items())[0]
        branch.append(top_candidate)

        if top_candidate in local_words:
            local_words.remove(top_candidate)
        for pos, letter in enumerate(top_candidate):
            local_usedLettersDF.at[letter, pos] += 1
            local_reservoirDF.at[letter, pos] -= 1

        current_depth += 1

    return branch


def doubleCoverageWithBranching2(words: list[str],
                                 reservoirDF: pd.DataFrame,
                                 width: int = 4,
                                 depth: int = 3):
    """
    This function first initializes the state by picking a top word (from the weighted dictionary),
    updating the used letters and the reservoir. Then, while there remain zeros in usedLettersDF,
    it computes candidate branches in parallel using multiprocessing. The branching is done over the
    last `width` of the weighted dictionary, recursing for `depth` steps.

    Note: The helper functions `leaveOnlyZeroLetteredWords` and `sortWorda` (as well as
    the wordOperations functions) are assumed to be defined.
    """
    usedLettersDF = wordOperations.createEmptyDF()
    weightedWords = wordOperations.assignValues(words, reservoirDF, True)
    usedWords = []

    # Initial selection: take the top value from weightedWords
    top = weightedWords.popitem()
    topWord, topValue = top[0], top[1]
    usedWords.append(topWord)
    if topWord in words:
        words.remove(topWord)

    for pos, letter in enumerate(topWord):
        usedLettersDF.at[letter, pos] += 1
        reservoirDF.at[letter, pos] -= 1

    print("Initial usedLettersDF:\n", usedLettersDF.values)
    print("Initial reservoirDF:\n", reservoirDF)

    # Main loop: continue until there are no zeros left in usedLettersDF.
    while 0 in usedLettersDF.values:
        # Update the words list by keeping only those words that have zeros in the usedLettersDF.
        words = leaveOnlyZeroLetteredWords(words, usedLettersDF)
        weightedWords, min_value, min_keys = sortWorda(reservoirDF, usedLettersDF, words)
        if not weightedWords:
            break

        # Take the last `width` elements from weightedWords as candidates.
        candidates = dict(list(weightedWords.items())[-width:])
        print("Candidates at current iteration:", candidates)

        # Set up arguments for each candidate branch.
        params = []
        for candidate, value in candidates.items():
            # Pass copies of the state to each candidate branch so that changes in one branch don’t affect another.
            params.append((candidate, value, words.copy(), reservoirDF.copy(), usedLettersDF.copy(), width, depth))

        # Use the multiprocessing Pool to compute each candidate branch concurrently.
        with multiprocessing.Pool() as pool:
            candidate_branches = pool.starmap(candidate_branch, params)

        # For demonstration, choose the first candidate branch.
        print(candidate_branches)
        chosen_branch = candidate_branches[0]
        print("Chosen branch:", chosen_branch)

        # Update the global state with every candidate in the chosen branch.
        for candidate_word in chosen_branch:
            usedWords.append(candidate_word)
            if candidate_word in words:
                words.remove(candidate_word)
            for pos, letter in enumerate(candidate_word):
                usedLettersDF.at[letter, pos] += 1
                reservoirDF.at[letter, pos] -= 1

        # print("Updated usedLettersDF:\n", usedLettersDF)
        # print("Updated reservoirDF:\n", reservoirDF)

    print("Used words:", usedWords)
    print("Total used words count:", len(usedWords))
