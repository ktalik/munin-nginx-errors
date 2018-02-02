#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""nginx_client_errors -- Munin plugin to report the number of Nginx client errors other than 40X

The access log defaults to `/var/log/nginx/access.log`. This may be
customized with the following stanza in your munin plugin conf:

[nginx_client_other_errors]
env.access_log /path/to/access.log
"""
#%# family=auto
#%# capabilities=autoconf

import nginx_errors

from nginx_errors import *

"""
counters += [(
    "errors_4x",
    "4XX Client Errors",
    re.compile(r'" (4[0-9][0-9]) '),
    defaultdict(lambda: 0))]
"""

counters += [(
    "errors_%s" % code,
    "%s %s" % (code, reason),
    re.compile(r'" (%s) ' % code),
    defaultdict(lambda: 0))
    for code, reason in [
        (410, 'Gone'),
        (411, 'Length Required'),
        (412, 'Precondition Failed'),
        (413, 'Payload Too Large'),
        (414, 'Request-URI Too Long'),
        (415, 'Unsupported Media Type'),
        (416, 'Requested Range Not Satisfiable'),
        (417, 'Expectation Failed'),
        (418, "I'm a teapot"),
        (421, 'Misdirected Request'),
        (422, 'Unprocessable Entity'),
        (423, 'Locked'),
        (424, 'Failed Dependency'),
        (426, 'Upgrade Required'),
        (428, 'Precondition Required'),
        (429, 'Too Many Requests'),
        (431, 'Request Header Fields Too Large'),
        (444, 'Connection Closed Without Response'),
        (451, 'Unavailable For Legal Reasons'),
        (494, 'Request Header Too Large'),
        (495, 'SSL Certificate Error'),
        (496, 'SSL Certificate Required'),
        (497, 'HTTP Request Sent to HTTPS Port'),
        (499, 'Client Closed Request'),]]

nginx_errors.GRAPH_TITLE = "Nginx Client Other Errors"

if __name__ == '__main__':
    main()
