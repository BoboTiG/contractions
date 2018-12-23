import time
import os.path
import sqlite3

from bottle import redirect, route, run, static_file, template

__version__ = "0.1.0"
__author__ = "Mickaël Schoentgen"
__copyright__ = """
Copyright (c) 2018, Mickaël 'Tiger-222' Schoentgen

Permission to use, copy, modify, and distribute this software and its
documentation for any purpose and without fee or royalty is hereby
granted, provided that the above copyright notice appear in all copies
and that both that copyright notice and this permission notice appear
in supporting documentation or portions thereof, including
modifications, that you make.
"""

DB_SCHEMA = "contractions.sql"

# Specific to Samuel, need to adapt later
DB_FILE = "contractions-samuel.db"
PORT = 2018


def render(tpl, **kwargs):
    """ Call template() with several common variables. """

    kwargs["version"] = __version__
    return template(tpl, **kwargs)


@route("/assets/<filename:path>")
def send_static(filename):
    """ Get a resource file used by the website. """

    return static_file(filename, root="assets")


@route("/")
def index():
    return render("tpl/index", history=get_contractions())


@route("/add")  # noqa
def index():
    add_contraction()
    time.sleep(1)
    redirect("/")


def add_contraction():
    ensure_db_exists()

    conn = sqlite3.connect(f"file:{DB_FILE}", uri=True)
    c = conn.cursor()
    c.execute("INSERT INTO Contractions (quand) VALUES (datetime('now', 'localtime'))")
    conn.commit()
    conn.close()


def get_contractions():
    ensure_db_exists()

    conn = sqlite3.connect(f"file:{DB_FILE}", uri=True)
    c = conn.cursor()
    data = c.execute("SELECT quand FROM Contractions").fetchall()
    res = "\n".join(d[0] for d in reversed(data))
    conn.commit()
    conn.close()
    return res


def ensure_db_exists():
    if os.path.isfile(DB_FILE):
        return

    with open(DB_SCHEMA) as filei:
        schema_new_dtb = filei.read()
    conn = sqlite3.connect(f"file:{DB_FILE}", uri=True)
    c = conn.cursor()
    c.executescript(schema_new_dtb)
    conn.commit()
    conn.close()


def main():
    """ Main logic. """

    run(host="", port=PORT, reloader=True)


if __name__ == "__main__":
    exit(main())
