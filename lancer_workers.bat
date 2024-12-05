@echo off
setlocal enabledelayedexpansion

:: Vérifie si un nombre d'arguments est donné
if "%~1"=="" (
    echo Utilisation : lancer_workers.bat [nombre_de_workers]
    exit /b
)

:: Nombre de workers à lancer
set N=%~1

:: Port de base
set BASE_PORT=25545

:: Boucle pour ouvrir les workers
for /L %%i in (0,1,%N%) do (
    set /A PORT=!BASE_PORT! + %%i
    echo Lancement du WorkerSocket sur le port !PORT!...
    start cmd /k "java -XX:ActiveProcessorCount=32 -XX:+UseNUMA -XX:+UseParallelGC -XX:ParallelGCThreads=32 -cp bin src.WorkerSocket_old !PORT!"
)

:: Fin
echo %N% workers ont ete lances.
pause
