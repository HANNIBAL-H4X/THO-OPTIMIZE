@echo off
ipconfig /flushdns
ipconfig /release
ipconfig /renew
netsh winsock reset
exit /b 0
