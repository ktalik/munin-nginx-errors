#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""Python wrapper for Munin plugin reporting the number of errors in Nginx access log.
"""
#%# family=auto
#%# capabilities=autoconf

import os
import datetime as dt
import re
from collections import deque, defaultdict


GRAPH_TITLE = "Nginx errors"

date_cp = re.compile(r'''
\[
  (?P<day>\d+)
  /
  (?P<month>\w+)
  /
  (?P<year>\d+)
  :
  (?P<hour>\d+)
  :
  (?P<minute>\d+)
  :
  (?P<second>\d+)
  \              # Space
  [^\]]+
\]''', re.VERBOSE)

error_cp = re.compile(r'" ([4,5][0-9][0-9]) ')

counters = []

month_num = {
    'Jan': 1,
    'Feb': 2,
    'Mar': 3,
    'Apr': 4,
    'May': 5,
    'Jun': 6,
    'Jul': 7,
    'Aug': 8,
    'Sep': 9,
    'Oct': 10,
    'Nov': 11,
    'Dec': 12,
    }


def values():
    error_lines = deque()
    server_error_lines = deque()
    client_error_lines = deque()

    access_log = os.path.abspath(os.path.expanduser(os.environ.get('access_log', '/var/log/nginx/access.log')))
    if not os.path.exists(access_log):
        return

    with open(access_log) as fi:
        for line in fi:
            match = error_cp.search(line)
            if match is not None:
                error_lines.append((match.group(1), line.strip()))

    now = dt.datetime.now()
    d5m = now - dt.timedelta(minutes=5)

    for code, line in reversed(error_lines):
        match = date_cp.search(line)
        if match is not None:
            data = match.groupdict()
            date = dt.datetime(
                int(data['year'], base=10),
                month_num[data['month']],
                int(data['day'], base=10),
                int(data['hour'], base=10),
                int(data['minute'], base=10),
                int(data['second'], base=10),
                )

            if date < d5m:
                break

            for name, label, regex, by_second in counters:

                match = regex.search(line)
                if match is not None:
                    by_second[date] += 1

    for name, label, regex, by_second in counters:
        print '%s.value' % name, sum(by_second.itervalues()) if by_second else 0


def config():
    print "graph_title", GRAPH_TITLE
    print "graph_category webserver"
    print "graph_vlabel Errors per 5 minutes"

    for name, label, regex, by_second in counters:
        print '%s.label' % name, label


def main():
    from optparse import OptionParser
    parser = OptionParser()
    (options, args) = parser.parse_args()
    if len(args) > 1:
        parser.error('Too many arguments.')
    elif len(args) < 1:
        values()
    elif args[0] == 'config':
        config()

if __name__ == '__main__':
    main()
