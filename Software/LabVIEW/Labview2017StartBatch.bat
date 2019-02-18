@echo off
echo LabVIEW startet gleich...
echo Bitte bestaetig die Evaluation sofort.
echo Terminal schliesst inerhalb von 25 sec von selbst.
echo Bitte nicht inerhalb dieser Zeit abbrechen.
echo Sonst veraendert sich die Systemzeit dauerhaft.
SET STR=%DATE%
date 10.03.2018
start "" "C:\Program Files\National Instruments\LabVIEW 2017\LabVIEW.exe"
ping -n 25 localhost>nul
date %STR%
:end
exit