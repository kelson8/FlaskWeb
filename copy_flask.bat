@REM This is a basic script to copy my Python Flask website to the remote host (ubuntu-server.lan)
@REM Should make Docker development a bit easier.

@echo off
@REM Define source and destination
set SOURCE=ubu_flaskweb:
set DEST=D:\linode\FlaskWeb

@REM Run rclone to copy the Flask program excluding the venv folder
rclone copy %DEST% %SOURCE% --exclude "venv/**"  --exclude ".git/**"

echo Copy completed!
pause