basketballcrawler
==================

[![Join the chat at https://gitter.im/andrewgiessel/basketballcrawler](https://badges.gitter.im/Join%20Chat.svg)](https://gitter.im/andrewgiessel/basketballcrawler?utm_source=badge&utm_medium=badge&utm_campaign=pr-badge&utm_content=badge)

This is a python module to scrape [basketball-reference.com](http://www.basketball-reference.com/) and convert various
stats into usable data structures for analysis.

[Here](example_notebook.ipynb) is a link to a
sample IPython Notebook file demonstrating the library.


Requirements
------------

- [Beautiful Soup](http://www.crummy.com/software/BeautifulSoup/bs4/doc/#) >= 4.0
- [pandas](http://pandas.pydata.org/) >= 0.11
- [request](http://docs.python-requests.org/en/master/) >= 2.0


Usage
-----

Still developing the API.  Right now you can get a list of all player overview urls, generate a list of game log urls for
a given player, and convert that list into pandas dataframe.


Notes
-----

`players.json` was generated on 02/11/2016 by `buildPlayerDictionary()` and `savePlayerDictionary()`.
I'd recommend building your own, fresh copy. It takes about 10 minutes to scrape from the site.
To create the most recent `players.json`, you can use as follows.

```python
import basketballCrawler as bc
players = bc.buildPlayerDictionary()
