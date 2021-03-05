import random

from newutils.wordlist import wordlist


def get_passphrase(n_words: int, sep: str = ' ') -> str:
    return str(sep.join([
        wordlist[random.randint(0, len(wordlist))]
        for _ in range(n_words)
    ]))
