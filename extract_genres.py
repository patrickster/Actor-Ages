import sys
import os
import csv
import re
from functions import *
from BeautifulSoup import BeautifulSoup


def get_genres(film_id):
  """
  Returns a list of genres ascribed to an IMDb title.

  Args:
    film_id: the id of the IMDb title.

  """
  genre_re = re.compile('genre/(.+)\?ref')
  with open('%s%s.html' % (HTML_DIR, film_id)) as f:
    soup = BeautifulSoup(f.read())
    try:
      genres = [span.text for span in soup.findAll('span', {'itemprop' : 'genre'})]
    except:
      genres = []
  return genres


def main():
  files = [f for f in os.listdir('html') if '.html' in f]
  film_ids = [f.replace('.html', '') for f in files]
  with open('%s/genres.csv' % DATA_DIR, 'w') as f:
    w = csv.writer(f)
    for film_id in film_ids:
      genres = get_genres(film_id)
      row = [film_id] + genres
      print row
      w.writerow(row)


if __name__ == '__main__':
  sys.exit(main())