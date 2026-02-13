@echo off
chcp 65001 >nul
setlocal enabledelayedexpansion

:menu
cls
echo ========================================
echo        基金管理系统服务控制
echo ========================================
echo.
echo 1. 启动所有服务
echo 2. 停止所有服务
echo 3. 重启所有服务
echo 4. 查看服务状态
echo 5. 退出
echo.
set /p choice=请选择操作 (1-5):

if "%choice%"=="1" goto start
if "%choice%"=="2" goto stop
if "%choice%"=="3" goto restart
if "%choice%"=="4" goto status
if "%choice%"=="5" goto end
goto menu

:start
echo.
cls
echo ========================================
echo        正在启动服务...
echo ========================================
echo.

echo [1/2] 正在启动后端服务 (端口 8000)...
start "Backend-Service" cmd /k "cd /d %~dp0backend && python run.py"
timeout /t 3 /nobreak >nul

echo [2/2] 正在启动前端服务 (端口 8080)...
start "Frontend-Service" cmd /k "cd /d %~dp0frontend && python -m http.server 8080"
timeout /t 2 /nobreak >nul

echo.
echo ========================================
echo        所有服务启动完成！
echo ========================================
echo.
echo 后端服务: http://localhost:8000
echo 前端服务: http://localhost:8080
echo.
echo 按任意键返回主菜单...
pause >nul
goto menu

:stop
echo.
cls
echo ========================================
echo        正在停止服务...
echo ========================================
echo.

echo 正在查找并停止后端服务 (端口 8000)...
for /f "tokens=5" %%a in ('netstat -ano ^| findstr :8000 ^| findstr LISTENING') do (
    echo 发现进程 PID: %%a
    taskkill /F /PID %%a >nul 2>&1
    if !errorlevel! equ 0 (
        echo 已成功停止后端服务
    ) else (
        echo 停止后端服务失败
    )
)

echo.
echo 正在查找并停止前端服务 (端口 8080)...
for /f "tokens=5" %%a in ('netstat -ano ^|findstr :8080 ^| findstr LISTENING') do (
    echo 发现进程 PID: %%a
    taskkill /F /PID %%a >nul 2>&1
    if !errorlevel! equ 0 (
        echo 已成功停止前端服务
    ) else (
        echo 停止前端服务失败
    )
)

echo.
echo ========================================
echo        服务停止完成！
echo ========================================
echo.
echo 按任意键返回主菜单...
pause >nul
goto menu

:restart
echo.
echo 正在停止所有服务...
call :stop_internal
timeout /t 2 /nobreak >nul
echo.
echo 正在启动所有服务...
call :start_internal
goto menu

:stop_internal
for /f "tokens=5" %%a in ('netstat -ano ^| findstr :8000 ^| findstr LISTENING') do (
    taskkill /F /PID %%a >nul 2>&1
)
for /f "tokens=5" %%a in ('netstat -ano ^| findstr :8080 ^| findstr LISTENING') do (
    taskkill /F /PID %%a >nul 2>&1
)
goto :eof

:start_internal
start "Backend-Service" cmd /k "cd /d %~dp0backend && python run.py"
timeout /t 3 /nobreak >nul
start "Frontend-Service" cmd /k "cd /d %~dp0frontend && python -m http.server 8080"
goto :eof

:status
echo.
cls
echo ========================================
echo        服务状态检查
echo ========================================
echo.

set backend_status=未运行
set frontend_status=未运行

for /f "tokens=5" %%a in ('netstat -ano ^| findstr :8000 ^| findstr LISTENING') do (
    set backend_status=运行中 (PID: %%a)
)

for /f "tokens=5" %%a in ('netstat -ano ^| findstr :8080 ^| findstr LISTENING') do (
    set frontend_status=运行中 (PID: %%a)
)

echo 后端服务 (8000): %backend_status%
echo 前端服务 (8080): %frontend_status%
echo.
echo ========================================
echo.
echo 按任意键返回主菜单...
pause >nul
goto menu

:end
echo.
echo 退出服务控制脚本
exit /b 0
