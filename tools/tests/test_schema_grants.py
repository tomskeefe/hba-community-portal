"""schema.sql must carry every column-level grant from the migration history. It once dropped them all, so on a
fresh project saving a newsletter PDF or publishing a volunteer task failed with a permission error."""
import os
import re
from pathlib import Path

SUPA = Path(__file__).resolve().parents[2] / "supabase"
# Statements may span lines (schema.sql is auto-formatted), so whitespace includes newlines.
TABLE_GRANT = re.compile(r"^grant\s+([A-Z,\s]+?)\s+on\s+(?:table\s+)?(public\.\w+)\s+to\s+(\w+)", re.I | re.M)
GRANT = re.compile(r"grant\s+[a-z,\s]*?\b(update|insert|select)\s*\(([^)]*)\)\s*on\s+(?:table\s+)?([\w.]+)\s+to\s+(\w+)", re.I)


def read(path):
    """Read a file even from a checkout deep enough to pass Windows' 260-character path limit."""
    name = "\\\\?\\" + str(path.resolve()) if os.name == "nt" else path
    with open(name, encoding="utf-8") as f:
        return f.read()


def column_grants(text):
    out = set()
    for priv, cols, table, role in GRANT.findall(text):
        table = table if "." in table else "public." + table
        out |= {(priv.lower(), c.strip().lower(), table.lower(), role.lower()) for c in cols.split(",")}
    return out


def test_schema_keeps_column_grants_from_migration_history():
    history = set()
    for f in sorted((SUPA / "migrations-history").glob("*.sql")):
        history |= column_grants(read(f))
    assert history, "expected column grants in the migration history"
    schema = read(SUPA / "schema.sql")
    whole = {(p.strip().lower(), t.lower(), r.lower()) for privs, t, r in TABLE_GRANT.findall(schema) for p in privs.split(",")}
    missing = {g for g in history - column_grants(schema) if (g[0], g[2], g[3]) not in whole}
    assert not missing, "schema.sql lacks: " + ", ".join(f"{p}({c}) on {t} to {r}" for p, c, t, r in sorted(missing))
