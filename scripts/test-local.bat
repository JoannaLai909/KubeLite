@echo off
echo Testing KubeLite services...

echo.
echo [api-gateway] /health
curl http://localhost:5000/health

echo.
echo [calculator-service] /add
curl "http://localhost:5001/add?a=1^&b=2"

echo.
echo [message-service] /message
curl http://localhost:5002/message

echo.
echo Done.
pause