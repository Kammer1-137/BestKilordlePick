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

def candidate_branch(candidate,
                     value: int,
                     words: list,
                     reservoirDF: pd.DataFrame,
                     usedLettersDF: pd.DataFrame,
                     width: int,
                     depth: int) -> list:
    """
    Recursively computes all candidate branches starting from the given candidate.

    Parameters:
      candidate: the starting word or branch (list of words).
                 If a list is provided, the last element is the word used for state updates.
      value: the weight associated with the candidate.
      words: current available words list.
      reservoirDF: DataFrame representing the current reservoir state.
      usedLettersDF: DataFrame representing used letters.
      width: number of candidate choices to consider at each step.
      depth: remaining branch depth (if depth==1, the branch is complete).

    Returns:
      A list of tuples. Each tuple is (branch, cumulative_weight) where branch is a list
      of words representing one complete branch.
    """
    # If candidate is already a branch (a list), extract its last element as the current candidate word.
    if isinstance(candidate, list):
        candidate_word = candidate[-1]
        branch = candidate[:]  # copy the branch
    else:
        candidate_word = candidate
        branch = [candidate_word]

    # Initialize the cumulative weight.
    cumulative_weight = value

    # Work on copies of state so that each branch is independent.
    local_words = words.copy()
    if candidate_word in local_words:
        local_words.remove(candidate_word)
    local_usedLettersDF = usedLettersDF.copy()
    local_reservoirDF = reservoirDF.copy()

    # Update the DataFrames for the current candidate word.
    # Here we assume that candidate_word is a string, so that iterating over it gives characters.
    for pos, letter in enumerate(candidate_word):
        local_usedLettersDF.at[letter, pos] += 1
        local_reservoirDF.at[letter, pos] -= 1

    # Base case: if depth == 1, no further branching.
    if depth == 1:
        return [(branch, cumulative_weight)]

    # Update available words, then recalc weighted words.
    local_words = leaveOnlyZeroLetteredWords(local_words, local_usedLettersDF)
    weightedWords, min_value, min_keys = sortWorda(local_reservoirDF, local_usedLettersDF, local_words)
    if not weightedWords:
        return [(branch, cumulative_weight)]

    all_branches = []
    # Get candidate options from the last `width` items.
    candidate_options = dict(list(weightedWords.items())[-width:])

    # Process each candidate option recursively.
    for cand, cand_value in candidate_options.items():
        extensions = candidate_branch(cand, cand_value,
                                      local_words, local_reservoirDF, local_usedLettersDF,
                                      width, depth - 1)
        for ext_branch, ext_weight in extensions:
            all_branches.append((branch + ext_branch, cumulative_weight + ext_weight))

    return all_branches


def doubleCoverageWithBranching2(words: list[str],
                                 reservoirDF: pd.DataFrame,
                                 width: int = 12,
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

    # print("Initial usedLettersDF:\n", usedLettersDF.values)
    # print("Initial reservoirDF:\n", reservoirDF)

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
            params.append(
                (
                    candidate,
                    value,
                    copy.deepcopy(words),
                    copy.deepcopy(reservoirDF),
                    copy.deepcopy(usedLettersDF),
                    width,
                    depth)
            )

        # Use the multiprocessing Pool to compute candidate branches concurrently.
        with multiprocessing.Pool() as pool:
            candidate_branches_list = pool.starmap(candidate_branch, params)

        # candidate_branches_list is a list of lists (each from one candidate call).
        # Flatten them into one list of branch tuples.
        all_candidate_branches = []
        for cand_branches in candidate_branches_list:
            all_candidate_branches.extend(cand_branches)

        # Choose the branch with the lowest cumulative weight.
        if all_candidate_branches:
            chosen_branch, branch_weight = min(all_candidate_branches, key=lambda x: x[1])
            print("Chosen branch:", chosen_branch)

            # Update the global state using the chosen branch.
            for candidate_word in chosen_branch:
                usedWords.append(candidate_word)
                if candidate_word in words:
                    words.remove(candidate_word)
                # Update the DataFrames based on the candidate word.
                for pos, letter in enumerate(candidate_word):
                    usedLettersDF.at[letter, pos] += 1
                    reservoirDF.at[letter, pos] -= 1

        # print("Updated usedLettersDF:\n", usedLettersDF)
        # print("Updated reservoirDF:\n", reservoirDF)

    print("Used words:", usedWords)
    print("Total used words count:", len(usedWords))
