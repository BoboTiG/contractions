import time
import sqlite3
from datetime import datetime, timedelta
from itertools import zip_longest
from pathlib import Path
from typing import Iterator

import bottle  # type: ignore[import-untyped]

__version__ = "0.2.0"
__author__ = "Mickaël Schoentgen"
__copyright__ = f"""
Copyright (c) 2018-2025, {__author__}

Permission to use, copy, modify, and distribute this software and its
documentation for any purpose and without fee or royalty is hereby
granted, provided that the above copyright notice appear in all copies
and that both that copyright notice and this permission notice appear
in supporting documentation or portions thereof, including
modifications, that you make.
"""

HOST = "0.0.0.0"
PORT = time.gmtime().tm_year

ROOT = Path(__file__).parent
DB_SCHEMA = ROOT / "contractions.sql"
DB_FILE = ROOT / "contractions.db"
DATE_FMT = "%Y-%m-%d %H:%M:%S"


def render(tpl: str, **kwargs: str) -> str:
    kwargs["version"] = __version__
    return bottle.template(tpl, **kwargs)


@bottle.route("/")
def home() -> str:
    return render("tpl/index", history=get_contractions())


@bottle.route("/add")
def new_contraction() -> None:
    add_contraction()
    time.sleep(1)
    bottle.redirect("/")


def add_contraction() -> None:
    ensure_db_exists()

    with sqlite3.connect(DB_FILE) as conn:
        conn.execute(
            "INSERT INTO Contractions (quand) VALUES (datetime('now', 'localtime'))"
        )


def get_contractions() -> str:
    ensure_db_exists()

    with sqlite3.connect(DB_FILE) as conn:
        dates = conn.execute("SELECT quand FROM Contractions").fetchall()
    dates = [d[0] for d in reversed(dates)]
    return "\n".join(format_contractions(dates))


def format_contractions(dates: list[str]) -> Iterator[str]:
    for date1, date2 in zip_longest(dates, dates[1:]):
        if not date2:
            yield date1.ljust(28)
        else:
            d1 = datetime.strptime(date1, DATE_FMT)
            d2 = datetime.strptime(date2, DATE_FMT)
            d1_ts = time.mktime(d1.timetuple())
            d2_ts = time.mktime(d2.timetuple())
            diff = timedelta(seconds=d1_ts - d2_ts)
            yield f"{date1} ({str(diff).removeprefix('0:').lstrip('0').rjust(5)})".ljust(
                28
            )


def ensure_db_exists() -> None:
    if DB_FILE.is_file():
        return

    schema_new_dtb = DB_SCHEMA.read_text()
    with sqlite3.connect(DB_FILE) as conn:
        conn.executescript(schema_new_dtb)


def main() -> int:
    bottle.run(host=HOST, port=PORT, reloader=True)
    return 0


if __name__ == "__main__":
    exit(main())
