import re
import sys

import requests

from . import config

def download(url):
  response = requests.get(url,
    headers= {
      'Authorization': 'Bearer ' + config.get_token(),
      'Content-Type': 'application/json'
    }
  )
  if response.status_code != 200:
    print("Canvas responded with", response.status_code, file=sys.stderr)
    return None
  return response.content

def get(url):
  response = requests.get(url,
    headers= {
      'Authorization': 'Bearer ' + config.get_token()
    }
  )
  if response.status_code != 200:
    print("Canvas responded with", response.status_code, file=sys.stderr)
    return None
  return response.json()

def full_get(url):
  if 'per_page' not in url:
    if '?' in url:
      url += "&per_page=1000"
    else:
      url += "?per_page=1000"
  response = requests.get(url,
    headers= {
      'Authorization': 'Bearer ' + config.get_token()
    }
  )
  if response.status_code != 200:
    print("Canvas responded with", response.status_code, file=sys.stderr)
    return []
  else:
    results = response.json()
    next = get_next_link(response.headers["Link"])
    if next:
      return results + full_get(next)
    else:
      return results

def get_next_link(link_text):
  links = link_text.split(',')
  for link in links:
    match = re.fullmatch(r'\s*<([^>]*)>;\s*rel="([^"]*)"\s*', link)
    if match:
      if match[2] == 'next':
        return match[1]
  return None

def put(url, body):
  response = requests.put(url,
    headers= {
      'Authorization': 'Bearer ' + config.get_token()
    },
    json=body
  )
  if response.status_code != 200:
    print("Canvas responded with", response.status_code, file=sys.stderr)
    return None
  else:
    return response.json()
