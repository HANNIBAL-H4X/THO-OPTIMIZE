@echo off
netsh int tcp set global autotuninglevel=normal
netsh int tcp set global chimney=enabled
netsh int tcp set global dca=enabled
netsh int tcp set global ecncapability=enabled
netsh int tcp set global timestamps=disabled
netsh int tcp set heuristics disabled
netsh int tcp set global rss=enabled
netsh int tcp set global fastopen=enabled
netsh int tcp set global nonsackrttresiliency=disabled
netsh int tcp set global initialRto=2000
netsh int tcp set supplemental template=custom icw=10
netsh interface tcp set global congestionprovider=ctcp
ipconfig /flushdns
ipconfig /registerdns
netsh winsock reset
exit /b 0
