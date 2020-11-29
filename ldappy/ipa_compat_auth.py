#!/usr/bin/env python
import sys

import ldap

from pprint import pprint

if __name__ == "__main__": 
    (_, host, binduser, bindpass) = sys.argv
    conn = ldap.initialize("ldap://{}:389".format(host))
    conn.set_option(ldap.OPT_REFERRALS, 0)
    
    conn.simple_bind_s(binduser, bindpass)
    res = conn.search_s(binduser, ldap.SCOPE_SUBTREE)
    pprint(res)
    print(conn.whoami_s())
    conn.unbind()
