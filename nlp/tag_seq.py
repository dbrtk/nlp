

import nltk
from nltk.corpus import brown

suffix_fdist = nltk.FreqDist()
for word in brown.words():
    word = word.lower()
    suffix_fdist[word[-1:]] += 1
    suffix_fdist[word[-2:]] += 1
    suffix_fdist[word[-3:]] += 1


common_suffixes = [suffix for (suffix, count) in suffix_fdist.most_common(100)]

print(common_suffixes)
