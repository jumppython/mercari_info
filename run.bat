@echo off

set PS=run.py
python %~dp0%PS%

set RS=p_price.r
set PF=pricelist.csv

set TOPP=20000

for /f "delims=;" %%f in ('dir /a:d /b') do (
	Rscript %~dp0%RS% %~dp0%%f %PF% %TOPP% %date%
)
