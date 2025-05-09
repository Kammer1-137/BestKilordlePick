# Best Kilordle (word) Pick(er)

Yes, I should come up with a better name.

The idea ot this script is heavily inspired by [Kilordle](https://jonesnxt.github.io/kilordle/), a variant of Wordle with a whooping **1000** words to guess. The catch? You don't have to write every single word: if you, by make all letters for a given word green, then this word is autocompleted.

This is basically what this sprits does -- it finds _the best_ word. Such _the-best-ness_ is being determinated by values of letters in analysed word: script takes into consideration position of letter and how many given letter is found in all words from [words.txt](words.txt) and provides one with the highest score (currently there are two modes for scores of letters available: addictive and multiplicative).
Then values of used letters are discarded and new best word is found. And da capo, until all possible combinations of letters and positions are exhausted.

I used word list from [this gist](https://gist.github.com/dracos/dd0668f281e685bad51479e5acaadb93).

I think I should point out this doesn't solve Kilordle: given the provided set of words, it gives a best pick for a word. There's a cahnce for Kilordle to use such a exotic set of words that this script gives completely misleading words.