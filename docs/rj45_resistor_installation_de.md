🛠️ Anleitung: Abschlusswiderstand in RJ45-Stecker einbauen (Modbus RTU)



✅ Hintergrund

Ein korrekt platzierter 120-Ohm-Abschlusswiderstand ist für stabile Modbus-Kommunikation über RS-485 essenziell. Bei deinem Setup mit einem X1 Mini Inverter, RJ45-Direktanschluss und Modbus via USB-Stick bei 9600 Baud und ca. 15 m Kabellänge ist der Abschlusswiderstand besonders wichtig – vor allem, wenn es keine weiteren Geräte in der Linie gibt.



🎯 Ziel

Einbau eines 120-Ohm-Widerstands zwischen Pin 4 (Modbus A/+) und Pin 5 (Modbus B/–) in einem RJ45-Stecker – auf möglichst kurzem Raum, damit der IP65-Deckel wieder schließt.



🧰 Du brauchst

\- 1x RJ45-Stecker (8P8C, ungeschirmt oder geschirmt – je nach Kabel)

\- 1x 120-Ohm-Widerstand (idealerweise ¼ W, axial)

\- 1x Netzwerkkabel (z. B. Patchkabel)

\- Crimpzange für RJ45

\- Seitenschneider / Abisolierzange

\- Schrumpfschlauch (optional)

\- Multimeter (optional zur Kontrolle)



🔌 Pinbelegung Modbus über RJ45

| Pin | Signal       | Funktion         |

|-----|--------------|------------------|

| 4   | Modbus A / D+ | Datenleitung +   |

| 5   | Modbus B / D– | Datenleitung –   |



🧱 Schritt-für-Schritt-Anleitung

1\. Widerstand vorbereiten

\- Schneide die Beinchen des Widerstands auf ca. 1 cm.

\- Winkle die Enden leicht an, sodass sie direkt in Pin 4 und Pin 5 gesteckt werden können.



2\. Kabel vorbereiten

\- Entferne ca. 2–3 cm der Außenisolierung des RJ45-Kabels.

\- Isoliere die Adern für Pin 4 (blau) und Pin 5 (blau-weiß) ca. 5 mm ab.



3\. Widerstand einfügen

\- Löte oder klemme den Widerstand direkt zwischen die Adern für Pin 4 und 5 oder

\- Führe die Widerstandsbeinchen direkt in die dafür vorgesehenen Kanäle im RJ45-Stecker (siehe dein Foto oben).



4\. Schrumpfschlauch anbringen (optional)

\- Isoliere den Widerstand mit etwas Schrumpfschlauch oder Isolierband, falls die Beinchen Kontakt zu anderen Pins haben könnten.



5\. RJ45 crimpen

\- Achte darauf, dass die Adern korrekt liegen und der Widerstand straff, aber nicht gequetscht im Stecker sitzt.

\- Stecke den Stecker in die Crimpzange (8P-Port) und presse fest durch.



📏 Kontrolle (optional)

\- Multimeter im Widerstandsmessmodus

\- Messe zwischen Pin 4 und Pin 5 (im Stecker): ca. 120 Ω anzeigen → alles richtig!



📦 Einsatz

\- Stecke den RJ45-Stecker in den Anschluss deines Wechselrichters (X1 Mini).

\- Der IP65-Deckel sollte ohne größeren Druck schließbar sein.

\- Starte Modbus-Kommunikation neu und prüfe Logs/Verbindungen.



💬 Tipp

Wenn du jemals die Linie verlängerst oder weitere Geräte einbindest, beachte:

\- Genau zwei Abschlusswiderstände in einem RS-485-Bus! → je einer am Anfang und am Ende der Linie.



📎 GitHub-Issue (Referenz)

https://github.com/wills106/homeassistant-solax-modbus/issues/1510

