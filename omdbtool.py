#!/usr/bin/env python

from __future__ import print_function
import argparse
import os
import sys
import json

try:
    from urllib.request import urlopen
    from urllib.parse import urlencode
except ImportError:
    from urllib import urlopen, urlencode


parser = argparse.ArgumentParser(description='Get OMDb data for a movie')

parser.add_argument(
    "-t",
    help="Movie title")

parser.add_argument(
    "-y",
    help="Year of release",
    type=int)

parser.add_argument(
    "-i",
    help="IMDb movie id")

parser.add_argument(
    "-r",
    help="Return raw XML/JSON response",
    choices=['JSON', 'XML'])

parser.add_argument(
    "--plot",
    help="Length of plot summary",
    choices=['short', 'full'])

parser.add_argument(
    "--tomatoes",
    help="Include Rotten Tomatoes data too",
    action="store_true")

parser.add_argument(
    "--type",
    help="movie, series, episode",
    choices=['movie', 'series', 'episode'])

parser.add_argument(
    "--season",
    help="season number",
    type=int)

parser.add_argument(
    "--episode",
    help="episode number",
    type=int)

parser.add_argument(
    "--format",
    help="Output formated in html, markdown or csv, leave out for text",
    choices=['html', 'markdown', 'csv'])

parser.add_argument(
    "--apikey",
    help="Your API key (will try to use env var OMDB_API_KEY if omitted)")


args = parser.parse_args()

params = {}
keys = ['t', 'y', 'i', 'plot', 'r', 'tomatoes', 'type', 'season', 'episode']


# prepare query string keyvals (excluding apikey, which is handled below)

for k in keys:
    if args.__getattribute__(k):
        params[k] = args.__getattribute__(k)

if len(params) == 0:
    parser.print_help()
    sys.exit()


# try to get API key, fall back to env var if not passed as argument

if args.__getattribute__('apikey'):
    params['apikey'] = args.__getattribute__('apikey')
elif 'OMDB_API_KEY' in os.environ.keys():
    params['apikey'] = os.environ['OMDB_API_KEY']
else:
    print("Error: API key must be passed via --apikey=YOUR_KEY or set "
          "as OMDB_API_KEY environment variable", file=sys.stderr)
    sys.exit(1)


# call OMDb API

apicall = urlopen('https://www.omdbapi.com/?%s' % urlencode(params), timeout=6)
result = apicall.read()
apicall.close()

# print raw output and exit, if raw output was requested
if args.r:
    print(result)
    sys.exit()
if args.format == 'csv':
    result = result.replace('","', ';')
    chars_to_remove = ['"', '[', ']', '{', '}']
    result = result.translate(None, ''.join(chars_to_remove))
    print(result)
    sys.exit()
# formats data as html
elif args.format == 'html':
    result = result.replace('",', '<br>')
    result = result.replace('{', '<br><br><br><p>')
    chars_to_remove = ['"', '[', ']']
    result = result.translate(None, ''.join(chars_to_remove))
    result = result.replace('}', '</p>')
    print(result)
    sys.exit()

# formats the data as markdown
if args.format == 'markdown':
    result = result.replace('",', '\n')
    result = result.replace('{', '##')
    chars_to_remove = ['"', '[', ']', '}']
    result = result.translate(None, ''.join(chars_to_remove))
    print(result)
    sys.exit()

# Encoding the data from --season option crashes the program
# this prints the data without having to encode it
if args.season:
    chars_to_remove = ['"', '[', ']', '}']
    result = result.translate(None, ''.join(chars_to_remove))
    result = result.replace(',', '\n')
    result = result.replace('{', '\n\n\n')
    print(result)
    sys.exit()

# print requested info
data = json.loads(result.decode('utf-8'))
for k in data:
    print(k.lower() + ":")
    print(data[k])
    print("\n")
