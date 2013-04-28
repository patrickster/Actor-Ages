
import sys
import csv
import requests
import time
from BeautifulSoup import BeautifulSoup


def format_date(date):
  try:
    (y, m, d) = date.split('/')
    if len(m) == 1:
      m = '0' + m
    if len(d) == 1:
      d = '0' + d
    date = '%s/%s/%s' % (y, m, d)
  except:
    print 'Could not format date: %s' % date
  return date


def extract_chart(page, year):
  soup = BeautifulSoup(page)
  with open('data/chart-%d.csv' % year, 'w') as f:
    w = csv.writer(f)
    w.writerow(['year', 'title', 'gross', 'date'])
    table = soup.find('table', {'cellpadding' : 5})
    rows = table.findAll('tr')
    for row in rows[2:101]:
      cols = row.findAll('td')
      name = cols[1].text
      gross = cols[3].text
      date = '%d/%s' % (year, cols[7].text)
      date = format_date(date)
      w.writerow([year, name, gross, date])
  print 'Saved chart for %d' % year


def get_chart(year):
  url = 'http://boxofficemojo.com/yearly/chart/?yr=%d' % year
  page = get_page(url)
  if page is None:
    extract_chart(page, year)


def main(argv=None):
  if argv is None:
    argv = sys.argv
  print argv
  if len(argv) == 2:
    year = int(argv[1])
    get_chart(year)
  if len(argv) > 2:
    year1 = int(argv[1])
    year2 = int(argv[2])
    for year in range(year1, year2 + 1):
      get_chart(year)
      time.sleep(3)


if __name__ == '__main__':
  sys.exit(main())


    