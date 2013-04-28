
import sys
import csv
import re
from BeautifulSoup import BeautifulSoup
from functions import *


def search_imdb(title, year=None):
  query = re.sub('\s', '+', title)
  if year is not None:
     query += '%28' + str(year) + '%29'
  print 'Searching imdb for %s' % query
  url = 'http://www.imdb.com/find?q=%s&s=all' % query
  page = request_page(url)
  if page is None:
    return None
  info = ['', '']
  try:  
    soup = BeautifulSoup(page)
    results_table = soup.find('table', {'class' : 'findList'})
    top_hit = results_table.find('tr')
    title = top_hit.text
    link = top_hit.find('a')['href']
    movie_id = link.split('/')[2]
    info = [title.encode('utf-8'), movie_id]
    print info
    return info
  except:
    pass
  return info


def resolve_chart(year):
  chart = load_chart(year)
  with open('./data/chart-%d-resolved.csv' % year, 'w') as f:
    w = csv.writer(f)
    w.writerow(['year', 'film', 'gross', 'date', 'imdb-title', 'id'])
    for film in chart:
      film_info = [film['year'], film['title'], film['gross'], film['date']]
      search_result = search_imdb(film['title'], film['year'])
      w.writerow(film_info + search_result)
      pause()


def main(argv=None):
  if argv is None:
    argv = sys.argv
  print argv
  if len(argv) == 2:
    year = int(argv[1])
    resolve_chart(year) 
  if len(argv) > 2:
    year1 = int(argv[1])
    year2 = int(argv[2])
    for year in range(year1, year2 + 1):
      resolve_chart(year)


if __name__ == '__main__':
  sys.exit(main())



