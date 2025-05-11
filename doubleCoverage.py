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
    Recursively generates all candidate branches starting from the given candidate.

    Parameters:
      candidate: Starting word (a string).
      value: Weight associated with this candidate.
      words: Current available words list.
      reservoirDF: DataFrame representing the current reservoir state.
      usedLettersDF: DataFrame representing the used letters.
      width: Number of candidate options to consider at each branch node.
      depth: Remaining branch depth (when depth == 1 the branch is complete).

    Returns:
      A list of tuples: (branch, cumulative_weight), where branch is a list of words.
    """
    # Initialize the branch with the candidate.
    branch = [candidate]
    cumulative_weight = value

    # Use deep copies to ensure each branch works with independent state.
    local_words = copy.deepcopy(words)
    if candidate in local_words:
        local_words.remove(candidate)
    local_usedLettersDF = copy.deepcopy(usedLettersDF)
    local_reservoirDF = copy.deepcopy(reservoirDF)

    # Update the state based on the characters in the candidate word.
    for pos, letter in enumerate(candidate):
        local_usedLettersDF.at[letter, pos] += 1
        local_reservoirDF.at[letter, pos] -= 1

    # Immediately check: if every position in usedLettersDF is now covered (i.e. no zeros), then terminate.
    if 0 not in local_usedLettersDF.values:
        return [(branch, cumulative_weight)]

    # Base case: if no further depth is allowed, return the current branch.
    if depth == 1:
        return [(branch, cumulative_weight)]

    # Filter the available words based on the updated usedLettersDF.
    local_words = leaveOnlyZeroLetteredWords(local_words, local_usedLettersDF)
    weightedWords, min_value, min_keys = sortWorda(local_reservoirDF, local_usedLettersDF, local_words)
    if not weightedWords:
        return [(branch, cumulative_weight)]

    # From the current weightedWords, take the last `width` candidates to extend the branch.
    candidate_options = dict(list(weightedWords.items())[-width:])
    all_branches = []
    for cand, cand_value in candidate_options.items():
        # Recursively compute extensions for each candidate.
        extensions = candidate_branch(
            cand,
            cand_value,
            copy.deepcopy(local_words),
            copy.deepcopy(local_reservoirDF),
            copy.deepcopy(local_usedLettersDF),
            width,
            depth - 1
        )
        for ext_branch, ext_weight in extensions:
            all_branches.append((branch + ext_branch, cumulative_weight + ext_weight))
    return all_branches


def doubleCoverageWithBranching2(words: list[str],
                                reservoirDF: pd.DataFrame,
                                width: int = 4,
                                depth: int = 3):
    """
    Instead of pre-selecting the first word, this function starts branching
    right away from the available candidates. In each iteration, it filters, weights,
    and then uses the last 'width' candidates to spawn candidate branches concurrently.
    The branch with the lowest cumulative weight is chosen to update the global state.

    The process continues until there are no zeros left in usedLettersDF.
    """
    usedLettersDF = wordOperations.createEmptyDF()
    usedWords = []
    weightedWords = wordOperations.assignValues(words, reservoirDF, True)

    while 0 in usedLettersDF.values:
        # Update available words based on the current usedLettersDF.
        words = leaveOnlyZeroLetteredWords(words, usedLettersDF)
        weightedWords, min_value, min_keys = sortWorda(reservoirDF, usedLettersDF, words)
        if not weightedWords:
            break

        # Instead of a fixed first word, consider the last 'width' candidates.
        candidates = dict(list(weightedWords.items())[-width:])
        print("Candidates at current iteration:", candidates)

        # Set up arguments for each candidate branch using deepcopy.
        params = []
        for candidate, value in candidates.items():
            params.append((
                candidate,
                value,
                copy.deepcopy(words),
                copy.deepcopy(reservoirDF),
                copy.deepcopy(usedLettersDF),
                width,
                depth
            ))

        # Use a multiprocessing Pool to concurrently compute candidate branches.
        with multiprocessing.Pool() as pool:
            candidate_branches_list = pool.starmap(candidate_branch, params)

        # Flatten the list of candidate branches.
        all_candidate_branches = []
        for branch_list in candidate_branches_list:
            all_candidate_branches.extend(branch_list)

        if not all_candidate_branches:
            break

        # Choose the branch with the lowest cumulative weight.
        chosen_branch, branch_weight = min(all_candidate_branches, key=lambda x: x[1])
        print("Chosen branch:", chosen_branch, branch_weight)

        # Update the global state with each word from the chosen branch.
        for candidate_word in chosen_branch:
            usedWords.append(candidate_word)
            if candidate_word in words:
                words.remove(candidate_word)
            for pos, letter in enumerate(candidate_word):
                usedLettersDF.at[letter, pos] += 1
                reservoirDF.at[letter, pos] -= 1

        # print(usedWords)


        # print("Updated usedLettersDF:\n", usedLettersDF)
        # print("Updated reservoirDF:\n", reservoirDF)

    print("Used words:", usedWords)
    print("Total used words count:", len(usedWords))
