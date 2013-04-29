import time
import requests
import csv
import random


def pause(min_length=1):
  """ 
  Pauses for a random amount of time.

  Args:
    min_length: the minimum pause length, in seconds.

  """
  pause_length = min_length + abs(random.normalvariate(0, 3))
  print "Pausing for " + str(int(pause_length)) + " seconds"
  time.sleep(pause_length)


def request_page(url, headers={'User-Agent' : 'Mozilla/4.0 (compatible; MSIE 6.1; Windows XP)'}):
  """ 
  Wrapper for requests.get().  

  Args:
    url: the url to request.
    headers: headers to pass to requests.get().   
  Returns:
    Page content if request succeeds, None otherwise.

  """
  r = requests.get(url, headers=headers)
  if r.status_code != 200:
    return None
  else:
    return r.content


def load_chart(year, resolved=False, dir='data/'):
  """ 
  Loads the content of a yearly box office chart. 

  Args:
    year: year of chart.
    resolved: whether or not to load the resolved version of the chart.
    dir: a path to the directory where the charts are located.
  Returns:
    A list of dictionaries, each containing data for a row in the chart.

  """
  if resolved:
    file_name = '%schart-%d-resolved.csv' % (dir, year)
  else:
    file_name = '%schart-%d.csv' % (dir, year)
  f = open(file_name, 'r')
  reader = csv.reader(f)
  chart = []
  rownum = 0
  header = []
  for row in reader:
    if rownum == 0:
      header = row
    else:
      chart_entry = {}
      for i in range(0, len(row)):
        chart_entry[header[i]] = row[i]
      chart += [chart_entry]
    rownum += 1
  f.close()
  return chart

