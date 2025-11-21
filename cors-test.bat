@echo off
setlocal enabledelayedexpansion

set /p ASAL_ORIGIN="Masukkan domain/sub-domain (contoh: http://api.example.com): "

if "%ASAL_ORIGIN%"=="" (
    echo Domain tidak boleh kosong!
    pause
    exit /b 1
)

set /p PATHS_INPUT="Masukkan URL paths yang ingin di-test, dipisahkan koma (contoh: /api,/api/data,/v1/users): "

if "%PATHS_INPUT%"=="" (
    echo Minimal satu path harus diinput!
    pause
    exit /b 1
)

echo.
echo ============================================================
echo Tool Pengujian CORS untuk: %ASAL_ORIGIN%
echo URL paths: %PATHS_INPUT%
echo ============================================================
echo.

setlocal enabledelayedexpansion
set idx=0
set titik_akhir[0]=%ASAL_ORIGIN%
set /a idx=1

for /f "tokens=1* delims=," %%a in ("%PATHS_INPUT%") do (
    set path=%%a
    set path=!path: =!
    if not "!path!"=="" (
        set titik_akhir[!idx!]=%ASAL_ORIGIN%!path!
        set /a idx=!idx!+1
    )
)

set /a total_endpoints=!idx!
if !total_endpoints! lss 2 (
    echo Minimal satu path harus diinput!
    pause
    exit /b 1
)

for /L %%i in (0,1,!total_endpoints!) do (
    set url=!titik_akhir[%%i]!
    if defined url (
        echo.
        echo ============================================================
        echo Testing CORS untuk: !url!
        echo ============================================================
        
        curl -s -i -X OPTIONS "!url!" ^
            -H "Origin: %ASAL_ORIGIN%" ^
            -H "Access-Control-Request-Method: GET" ^
            -H "Access-Control-Request-Headers: Content-Type"
        
        echo.
        echo ============================================================
        echo Testing GET request ke: !url!
        echo ============================================================
        
        curl -s -i -X GET "!url!" ^
            -H "Origin: %ASAL_ORIGIN%"
        
        echo.
    )
)

echo ============================================================
echo Pengujian CORS Selesai
echo ============================================================
echo.

pause
