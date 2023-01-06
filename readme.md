# A Python Wordle

This program uses all in-built Python packages, no need for a virtual environment.

## Usage
Clone repo
```
git clone git@github.com:mjkgarrow/python-wordle.git
```

Play game
```
python3 wordle.py
```

## Word usage

The `words.txt` file is sourced from Donald E. Knuth's [The Stanford GraphBase: A Platform for Combinatorial Computing](https://www-cs-faculty.stanford.edu/~knuth/sgb.html), found [here](https://www-cs-faculty.stanford.edu/~knuth/sgb-words.txt). It contains 5,757 common 5-letter words.

The `words_long.txt` file is a list of the currently used words in the official [Wordle](https://www.nytimes.com/games/wordle/index.html) app. It contains 14,855 words and is a fair bit harder.