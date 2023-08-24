# NoSQL-Scripts
## Requirements
Zur Vorbereitung der Umgebung sowie zum Ausführen der Skripte ist die Installation von `Python3` sowie `PIP(3)` notwendig.
Welche Schritte hierzu auf Ihrem System durchgeführt werden müssen, entnehmen Sie bitte dem Handbuch des Betriebssystems.

## Python - Virtual Environment
Zur Erzeugung der Umgebung öffnen Sie bitte eine Eingabeaufforderung/Shell und wechseln Sie in den Ordner "Project".
Dort erzeugen Sie zunächst das Virtuelle Environment und aktivieren dieses
> $ python -m venv NoSQL
> 
> $ source NoSQL/bin/activate

Anschließend laden Sie die erforderlichen Bibliotheken nach:
> $ pip install -r requirements.txt

## Nuztung der Scripte
Für die initale Befüllung der Datenbank müssen zunächst Kunden erzeugt und hochgeladen werden.
Hierzu geben Sie an, wieviele Customer sie erzeugen wollen und wieviel Hotspots sie haben wollen.
Das Script erzeugt eine CSV mit dem Namen __customer.csv__

> $ DataImport.py -c \<customers\> -s \<hotspots\>(0-3)

**Die Erzeugung dauert sehr lange. Es ist ggf zweckmäßiger die Datenbank mit einer Datei aus dem Ordner __Samples__ zu befüllen.**

Die Daten werden mit dem Script DataImport in die Datenbank geladen. Als InputFile ist die erzeugte CSV anzugeben. Die Collection ist in diesem Fall: **__Customer__**

> $ DataImport.py -i \<inputfile\> -r \<remote_server\> -d \<database\> -c \<collection\>

Wenn die Datenbank Kundendaten enthält können die Bestellungen erzeugt werden. Die Datenbank muss hierbei angegeben werden um die Kundendaten laden zu können um die Bestellungen den Kunden zuordnen zu können. Das Script erzeugt eine CSV mit dem Namen __orders.csv__

> $ OrderGenerator.py -r \<remote_server\> -d \<database\>

Auch die im letztem Schritt erzeugte CSV muss in die Datenbank importiert werden. Die passende Collection heißt: **__Orders__**

> $ DataImport.py -i \<inputfile\> -r \<remote_server\> -d \<database\> -c \<collection\>
