from configparser import ConfigParser
import sqlite3
import os

# Pfad zur DB-Datei
db_path = "/config/solar_logbook.db"

# Verbindung zur SQLite-Datenbank herstellen
conn = sqlite3.connect(db_path)
cur = conn.cursor()

# Update-Befehl ausführen
cur.execute("UPDATE solar_log_v2 SET modules1 = 760 WHERE modules1 = 2")
updated_rows = cur.rowcount

# Änderungen speichern und Verbindung schließen
conn.commit()
conn.close()

print(f"✅ Updated {updated_rows} rows: modules1 = 2 → 760")

# Pfad zur .conf-Datei
conf_path = "solar_logbook.conf"

# Config laden
config = ConfigParser()
config.read(conf_path)

# Prüfen & ersetzen
if config.has_section("system") and config.has_option("system", "modules1"):
    old_value = config.get("system", "modules1")
    config.set("system", "modules1", "760")
    print(f"✅ modules1 updated from {old_value} to 760")
else:
    print("⚠️ 'modules1' not found in [system] section. Nothing changed.")

# Zurückschreiben
with open(conf_path, "w") as configfile:
    config.write(configfile)
    print(f"📝 Changes saved to {conf_path}")

