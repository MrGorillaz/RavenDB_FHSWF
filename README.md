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
Hierzu muss zunächst die Standardkonfiguration im Grafana durchgeführt werden, sodass sich anschließend im Admin-Bereich angemeldet werden kann.

![img|524x808,50%](https://raw.githubusercontent.com/MrGorillaz/RavenDB_FHSWF/main/screenshots/add_datasource_1.png)
