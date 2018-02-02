#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""nginx_server_errors -- Munin plugin to report the number of Nginx server errors

The access log defaults to `/var/log/nginx/access.log`. This may be
customized with the following stanza in your munin plugin conf:

[nginx_server_errors]
env.access_log /path/to/access.log
"""
#%# family=auto
#%# capabilities=autoconf

import nginx_errors

from nginx_errors import *


"""
counters += [(
    "errors_5x",
    "5XX Server Errors",
    re.compile(r'" (5[0-9][0-9]) '),
    defaultdict(lambda: 0))]
"""

counters += [(
    "errors_%s" % code,
    "%s %s" % (code, reason),
    re.compile(r'" (%s) ' % code),
    defaultdict(lambda: 0))
    for code, reason in [
        (500, 'Internal Server Error'),
        (501, 'Not Implemented'),
        (502, 'Bad Gateway'),
        (503, 'Service Unavailable'),
        (504, 'Gateway Timeout'),
        (505, 'HTTP Version Not Supported'),
        (506, 'Variant Also Negotiates'),
        (507, 'Insufficient Storage'),
        (508, 'Loop Detected'),
        (510, 'Not Extended'),
        (511, 'Network Authentication Required'),
        (599, 'Network Connect Timeout Error'),]]

nginx_errors.GRAPH_TITLE = "Nginx Server Errors"

if __name__ == '__main__':
    main()
