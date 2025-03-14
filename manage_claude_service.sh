#!/bin/bash

function start_service() {
    echo "Starting Claude continuous service..."
    if [ -z "$ANTHROPIC_API_KEY" ]; then
        echo "ERROR: ANTHROPIC_API_KEY is not set!"
        echo "Please set your API key first:"
        echo "export ANTHROPIC_API_KEY=your_api_key_here"
        exit 1
    fi
    
    # Docker-Compose verwenden, falls vorhanden
    if command -v docker-compose &> /dev/null; then
        docker-compose up -d
        echo "Service started in Docker container. Check logs with 'docker-compose logs -f'"
    else
        # Direkte Python-Ausführung
        echo "Docker Compose not found, running directly with Python..."
        nohup python continuous_claude_service.py > claude_service.log 2>&1 &
        echo $! > claude_service.pid
        echo "Service started with PID $(cat claude_service.pid). Logs in claude_service.log"
        echo ""
        echo "Um Claude Code schreiben zu lassen, erstelle eine .spec-Datei im Projektverzeichnis:"
        echo "- Für C#: create dateiname.spec.cs"
        echo "- Für Python: create dateiname.spec.py"
        echo "- Für C++: create dateiname.spec.cpp"
        echo "- Für JavaScript: create dateiname.spec.js"
        echo ""
        echo "Schreibe in die Spec-Datei eine Beschreibung dessen, was programmiert werden soll."
        echo "Der Dienst erkennt neue/geänderte Spec-Dateien automatisch und generiert Code + Tests."
    fi
}

function stop_service() {
    echo "Stopping Claude continuous service..."
    
    # Docker-Compose verwenden, falls vorhanden
    if command -v docker-compose &> /dev/null; then
        docker-compose down
        echo "Service stopped."
    else
        # Direkte Python-Ausführung stoppen
        if [ -f claude_service.pid ]; then
            PID=$(cat claude_service.pid)
            if ps -p $PID > /dev/null; then
                kill $PID
                echo "Service with PID $PID stopped."
            else
                echo "Service not running."
            fi
            rm claude_service.pid
        else
            echo "No PID file found. Service might not be running."
        fi
    fi
}

function service_status() {
    # Docker-Compose verwenden, falls vorhanden
    if command -v docker-compose &> /dev/null; then
        STATUS=$(docker-compose ps | grep claude-service)
        if [[ -n "$STATUS" ]]; then
            echo "Service is running in Docker container."
            docker-compose ps
        else
            echo "Service is not running in Docker container."
        fi
    else
        # Direkte Python-Ausführung prüfen
        if [ -f claude_service.pid ]; then
            PID=$(cat claude_service.pid)
            if ps -p $PID > /dev/null; then
                echo "Service is running with PID $PID."
            else
                echo "Service is not running (stale PID file)."
            fi
        else
            echo "Service is not running (no PID file)."
        fi
    fi
}

case "$1" in
    start)
        start_service
        ;;
    stop)
        stop_service
        ;;
    restart)
        stop_service
        sleep 2
        start_service
        ;;
    status)
        service_status
        ;;
    *)
        echo "Usage: $0 {start|stop|restart|status}"
        exit 1
        ;;
esac

exit 0
