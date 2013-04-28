
import sys
import csv
from functions import *
from BeautifulSoup import BeautifulSoup


# def load_resolved_chart(year):
#   f = open('./data/chart-%d-resolved.csv' % year, 'r')
#   reader = csv.reader(f)
#   chart = []
#   rownum = 0
#   for row in reader:
#     if rownum > 0:
#       chart += [row]
#     rownum += 1
#   f.close()
#   return chart


def extract_cast(page, max_cast=5):
  soup = BeautifulSoup(page)
  cast_table = soup.find('table', {'class' : 'cast_list'})
  cast_rows = cast_table.findAll('tr')[1:]
  cast = []
  for i in range(0, max_cast):
    if i < len(cast_rows):
      row = cast_rows[i]
      name = row.find('span', {'itemprop' : 'name'}).text
      name = name.encode('utf-8')
      id = row.find('a')['href']
      id = id.split('/')[2]
      print [name, id]
      cast += [[name, id]]
    else:
      break
  return cast


def get_cast(film_id):
  url = 'http://www.imdb.com/title/' + film_id
  page = request_page(url)
  if page == None:
    return []
  try:
    return extract_cast(page)
  except:
    return []


def get_actors(year, dir='data/'):
  chart = load_chart(year, resolved=True)
  with open('%scast-%d.csv' % (dir, year), 'w') as f:
    w = csv.writer(f)
    w.writerow(['film-id', 'rank', 'actor', 'actor-id'])
    counter = 0
    for film in chart:
      film_id = film['id']
      print film_id
      # try:
      cast = get_cast(film_id)
      for i in range(0, len(cast)):
        w.writerow([film_id, i + 1] + cast[i])
      pause()
      # except:
        # print 'Failed to retrieve cast for %s' % film_id
      counter += 1


def main(argv=None):
  if argv is None:
    argv = sys.argv
  print argv
  if len(argv) == 2:
    year = int(argv[1])
    get_actors(year)
  if len(argv) > 2:
    year1 = int(argv[1])
    year2 = int(argv[2])
    for year in range(year1, year2 + 1):
      get_actors(year)


if __name__ == "__main__":
  sys.exit(main())


