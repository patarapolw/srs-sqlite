# srs-sqlite

A simple SRS app using Markdown/HandsOnTable/SQLite.

## Usage

The app can be invoke from the command line, or from Python.

```commandline
$ srs --help
Usage: srs [OPTIONS] FILENAME

Options:
  --host TEXT
  --port INTEGER
  --debug
  --help          Show this message and exit.
```

Or, in a Python script.

```python
from srs_sqlite import load_srs


if __name__ == '__main__':
    load_srs('srs.db')
```

## SRS usage

You have to get the server running first. After that, in Jupyter Notebook:

```python
>>> import os
>>> os.environ['DATABASE_URI'] = 'srs.db'
>>> from srs_sqlite.flashcards import iter_quiz
>>> from srs_sqlite import db
>>> quiz = iter_quiz()
>>> card = next(quiz)
>>> card.hide()
An HTML-rendered front of the card is shown.
>>> card.show()
An HTML-rendered back of the card is shown.
>>> card.get_more_sentences()
Add more sentences to the card, if the number of example sentences is too few.
>>> card.wrong()
Mark the card as wrong.
>>> card.right()
Mark the card as right.
>>> card.mark()
Add the tag "marked" to the card.
>>> card.unmark()
Remove the tag "marked" from the card.
>>> db.session.commit()
Commit changes.
```

## Screenshots

<img src="https://raw.githubusercontent.com/patarapolw/srs-sqlite/master/screenshots/0.png" />

## Related projects

- [HanziLevelUp](https://github.com/patarapolw/HanziLevelUp) - the project in which I embed the srs-sqlite.
- [jupyter-flashcards](https://github.com/patarapolw/jupyter-flashcards) - a flashcard app with SRS, working with an Excel file.
- [gflashcards](https://github.com/patarapolw/gflashcards) - a flashcard app, working with Google Sheets, but SRS is not yet implemented.
- [simplecel](https://github.com/patarapolw/simplecel) - HandsOnTable-based Excel with viewer, that can view Markdown and images.
