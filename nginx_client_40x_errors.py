#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""nginx_client_errors -- Munin plugin to report the number of Nginx 40X client errors

The access log defaults to `/var/log/nginx/access.log`. This may be
customized with the following stanza in your munin plugin conf:

[nginx_client_40x_errors]
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
        (400, 'Bad Request'),
        (401, 'Unauthorized'),
        (402, 'Payment Required'),
        (403, 'Forbidden'),
        (404, 'Not Found'),
        (405, 'Method Not Allowed'),
        (406, 'Not Acceptable'),
        (407, 'Proxy Authentication Required'),
        (408, 'Request Timeout'),
        (409, 'Conflict'),]]

nginx_errors.GRAPH_TITLE = "Nginx Client 40X Errors"

if __name__ == '__main__':
    main()
