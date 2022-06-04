# Lekoradar
Farmaceutyczna baza danych

## Uruchamianie aplikacji po raz pierwszy
Najpierw należy umieścić plik `authentication.py` z własnymi danymi w folderze `database`. 
Szablon tego pliku znajduje się w `database/authentication_temp.py`.

Następnie uruchamiamy komendę
`bash run.sh -ui`
w folderze głównym repozytorium.

Żeby uruchomić serwer postepujemy zgodnie z poniższymi instrukcjami.

## Uruchomienie serwera
Serwer w trybie debug uruchamiamy komendą `bash run.sh`

Można skorzystać z opcji `-r` lub `--run`, żeby uruchomić serwer po wykonaniu innych operacji opisanych poniżej.

## Instalacja bibliotek
`bash run.sh -u` lub `bash run.sh --update`

## Inicjalizacja danych
`bash run.sh -i` lub `bash run.sh --initialize`
