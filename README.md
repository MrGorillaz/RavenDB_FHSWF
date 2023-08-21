# RavenDB_FHSWF

## Installation

Mittels Docker Compose können die relevanten Container für RavenDB als auch Grafana betrieben werden.
Hierzu müssen zunächst folgende Befehle ausgeführt werden. 

```
  $ git clone https://github.com/MrGorillaz/RavenDB_FHSWF.git 
  $ cd RavenDB_FHSWF  
  $ docker compose build  
  $ docker compose up --detach 

```
## Grafana konfigurieren

Nachdem beide Container erfolgreich erstellt und hochgefahren wurden, ist Grafana über http://localhost:3000 im Webbrowser aufrufbar.
Hierzu muss zunächst die Standardkonfiguration im Grafana durchgeführt werden, sodass sich anschließend in der Admin-Oberfläche angemeldet werden kann.

In der Adminoberfläche muss zunächst die die RavenDB als Datenquelle hinzugefügt werden.

<img src="https://raw.githubusercontent.com/MrGorillaz/RavenDB_FHSWF/main/screenshots/add_datasource_1.png" width="300">
<img src="https://raw.githubusercontent.com/MrGorillaz/RavenDB_FHSWF/main/screenshots/add_datasource_2.png" width="600">
<img src="https://raw.githubusercontent.com/MrGorillaz/RavenDB_FHSWF/main/screenshots/add_datasource_3.png" width="600">
<img src="https://raw.githubusercontent.com/MrGorillaz/RavenDB_FHSWF/main/screenshots/add_datasource_4.png" width="600">
