#!/usr/bin/env python
# -*- coding: utf-8 -*-
""" Toma datos de suc.php y los adapta a scripts hechos en python"""
import cgitb; cgitb.enable()
import os
import cgi
import Cookie
def main():
    """Toma datos de suc.php y los adapta a Cookie de Python"""
    form = cgi.FieldStorage()
    sesion = Cookie.SimpleCookie(os.environ.get("HTTP_COOKIE",""))
    if "deposito_id" in form:
        nuevo_deposito_id = form.getvalue("deposito_id")
    else:
        if "deposito_id" in sesion:
            nuevo_deposito_id = sesion["deposito_id"].value
        else:
            nuevo_deposito_id = 1
    sesion["deposito_id"] = str(nuevo_deposito_id)
    print('Content-Type: text/html; charset=utf-8')
    print(sesion)
    print("\n\n")
    print('<META HTTP-EQUIV="Refresh" CONTENT="1;URL=geined.py">')
    #print('<head>')
    #print('</head><body>')
    #print("</body></head>")
if __name__ == "__main__":
    main()
