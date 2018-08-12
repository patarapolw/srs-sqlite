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

## Screenshots

<img src="https://raw.githubusercontent.com/patarapolw/srs-sqlite/master/screenshots/0.png" />

## Related projects

- [jupyter-flashcards](https://github.com/patarapolw/jupyter-flashcards) - a flashcard app with SRS, working with an Excel file.
- [gflashcards](https://github.com/patarapolw/gflashcards) - a flashcard app, working with Google Sheets, but SRS is not yet implemented.
- [simplecel](https://github.com/patarapolw/simplecel) - HandsOnTable-based Excel with viewer, that can view Markdown and images.
