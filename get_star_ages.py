

import sys
import csv
import re
from functions import *
from BeautifulSoup import BeautifulSoup


def load_actor_ids(file, dir='data/'):
  f = open(dir + file, 'r')
  reader = csv.reader(f)
  actor_ids = []
  rownum = 0
  id_col = None
  for row in reader:
    if rownum == 0:
      colnum = 0
      for col in row:
        if col == 'actor-id':
          id_col = colnum
          break
        colnum += 1
    else:
      actor_ids += [row[id_col]]
    rownum += 1
  f.close()
  return actor_ids


def get_actor_info(actor_id):
  url = 'http://www.imdb.com/name/%s' % actor_id
  headers = { 'User-Agent' : 'Mozilla/4.0 (compatible; MSIE 6.1; Windows XP)' }
  page = request_page(url)
  if page == None:
    return
  soup = BeautifulSoup(page)

  (name, birth_date, gender) = ('', '', '')

  try:
    name = soup.find('h1', {'itemprop':'name'}).next
    name = re.sub('\n', '', name)
  except:
    pass

  try:
    birth_date = soup.find('time', {'itemprop' : 'birthDate'})['datetime']
  except:
    pass

  try:
    actor_count = page.count('Actor')
    actress_count = page.count('Actress')
    if actor_count > actress_count:
      gender = 'male'
    if actor_count < actress_count:
      gender = 'female'
  except:
    pass

  return [actor_id, name, birth_date, gender]


def get_cast_info(year):
  print 'Looking up info for '
  have_info = load_actor_ids('actor-info.csv')
  actor_list = load_actor_ids('cast-%d.csv' % year)
  need_info = list(set(actor_list) - set(have_info))
  print '%d actors in cast list' % len(actor_list)
  print 'Need info for %d' % len(need_info)
  with open('./data/actor-info.csv', 'a') as f:
    w = csv.writer(f)
    counter = 0
    for actor_id in need_info:
      try:
        actor_info = get_actor_info(actor_id)
      except:
        actor_info = [actor_id, '', '', '']
      print actor_info
      w.writerow(actor_info)
      # except:
      #   print actor_id + " FAILED"
      # counter += 1
      pause()


def main(argv=None):
  if argv is None:
    argv = sys.argv
  print argv
  if len(argv) == 2:
    year = int(argv[1])
    get_cast_info(year) 
  if len(argv) > 2:
    year1 = int(argv[1])
    year2 = int(argv[2])
    for year in range(year1, year2 + 1):
      get_cast_info(year)


if __name__ == "__main__":
  sys.exit(main())


