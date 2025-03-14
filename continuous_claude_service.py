import os
import time
import requests
import json
import signal
import sys
import subprocess

# Globale Variable für den Laufstatus
running = True

def signal_handler(sig, frame):
    """Behandelt Ctrl+C oder andere Signale zum Beenden des Dienstes"""
    global running
    print("\nBeende den Claude-Service...")
    running = False
    sys.exit(0)

# Signal-Handler für SIGINT (Ctrl+C) registrieren
signal.signal(signal.SIGINT, signal_handler)

# Anthropic API-Konfiguration
ANTHROPIC_API_KEY = os.environ.get("ANTHROPIC_API_KEY")
API_URL = "https://api.anthropic.com/v1/messages"

def ask_claude(prompt, model="claude-3-7-sonnet-20250219"):
    """
    Sendet eine Anfrage an die Claude API und gibt die Antwort zurück
    """
    headers = {
        "x-api-key": ANTHROPIC_API_KEY,
        "anthropic-version": "2023-06-01",
        "content-type": "application/json"
    }
    
    data = {
        "model": model,
        "max_tokens": 4000,
        "messages": [{"role": "user", "content": prompt}]
    }
    
    response = requests.post(API_URL, headers=headers, json=data)
    
    if response.status_code == 200:
        return response.json()["content"][0]["text"]
    else:
        raise Exception(f"Fehler bei der API-Anfrage: {response.status_code}, {response.text}")

def extract_code_from_response(response, language=None):
    """
    Extrahiert Code aus Claude's Antwort, sucht nach Markdown-Code-Blöcken
    """
    import re
    
    # Wenn eine bestimmte Sprache angegeben ist
    if language:
        pattern = r"```" + language + r"\n([\s\S]*?)```"
        matches = re.findall(pattern, response)
        if matches:
            return matches[0]
    
    # Allgemeine Code-Blöcke suchen
    pattern = r"```(?:\w+)?\n([\s\S]*?)```"
    matches = re.findall(pattern, response)
    if matches:
        return matches[0]
    
    # Falls kein Code-Block gefunden wurde, gesamte Antwort zurückgeben
    return response

def write_file(file_path, content):
    """
    Schreibt Inhalt in eine Datei und erstellt Verzeichnisse bei Bedarf
    """
    os.makedirs(os.path.dirname(os.path.abspath(file_path)), exist_ok=True)
    with open(file_path, 'w') as file:
        file.write(content)
    print(f"Datei geschrieben: {file_path}")

def run_tests(file_path):
    """
    Führt Tests für die generierte Datei aus
    """
    file_extension = os.path.splitext(file_path)[1].lower()
    
    try:
        if file_extension == '.py':
            # Python-Tests
            result = subprocess.run(['python', file_path], capture_output=True, text=True)
            return result.returncode == 0, result.stdout, result.stderr
        
        elif file_extension in ['.cs', '.csproj']:
            # C#/.NET Tests
            if file_path.endswith('.csproj'):
                result = subprocess.run(['dotnet', 'test', file_path], capture_output=True, text=True)
            else:
                result = subprocess.run(['dotnet', 'run', '--project', find_csproj_for_file(file_path)], capture_output=True, text=True)
            return result.returncode == 0, result.stdout, result.stderr
        
        elif file_extension in ['.cpp', '.cc', '.h', '.hpp']:
            # C++ Tests - hier wird erwartet, dass ein Makefile vorhanden ist
            result = subprocess.run(['make', 'test'], capture_output=True, text=True)
            return result.returncode == 0, result.stdout, result.stderr
        
        elif file_extension in ['.js', '.ts']:
            # JavaScript/TypeScript Tests
            if os.path.exists('package.json'):
                result = subprocess.run(['npm', 'test'], capture_output=True, text=True)
                return result.returncode == 0, result.stdout, result.stderr
            else:
                result = subprocess.run(['node', file_path], capture_output=True, text=True)
                return result.returncode == 0, result.stdout, result.stderr
        
        else:
            return False, "", f"Keine Test-Methode für Dateityp {file_extension} verfügbar"
            
    except Exception as e:
        return False, "", f"Fehler beim Ausführen der Tests: {str(e)}"

def find_csproj_for_file(cs_file):
    """
    Findet die .csproj-Datei für eine .cs-Datei
    """
    directory = os.path.dirname(os.path.abspath(cs_file))
    
    # Nach oben suchen, bis eine .csproj-Datei gefunden wird
    while directory != '/' and directory != '':
        csproj_files = [f for f in os.listdir(directory) if f.endswith('.csproj')]
        if csproj_files:
            return os.path.join(directory, csproj_files[0])
        directory = os.path.dirname(directory)
    
    # Fallback: Suche nach allen .csproj-Dateien im aktuellen Verzeichnis und dessen Unterverzeichnissen
    for root, _, files in os.walk('.'):
        for file in files:
            if file.endswith('.csproj'):
                return os.path.join(root, file)
    
    return None  # Keine .csproj-Datei gefunden

def generate_code(spec_file):
    """
    Generiert Code basierend auf einer Spezifikationsdatei
    """
    if not os.path.exists(spec_file):
        print(f"Spezifikationsdatei {spec_file} nicht gefunden!")
        return None
    
    # Dateiendung extrahieren für Sprachbestimmung
    _, file_extension = os.path.splitext(spec_file)
    file_extension = file_extension.lower()
    
    # Sprache basierend auf Dateiendung bestimmen
    language_map = {
        '.cs': 'C#',
        '.py': 'Python',
        '.js': 'JavaScript',
        '.ts': 'TypeScript',
        '.cpp': 'C++',
        '.h': 'C++',
        '.hpp': 'C++',
        '.cc': 'C++',
        '.java': 'Java',
        '.rb': 'Ruby',
        '.go': 'Go',
        '.rs': 'Rust'
    }
    
    language = language_map.get(file_extension, "unbekannt")
    
    # Spezifikation lesen
    with open(spec_file, 'r') as file:
        spec_content = file.read()
    
    output_file = spec_file.replace('.spec', '')
    
    # Prompt für die Codegenerierung erstellen
    prompt = f"""
    Bitte generiere {language}-Code basierend auf folgender Spezifikation/Anforderung:
    
    ```
    {spec_content}
    ```
    
    Der generierte Code sollte:
    1. Vollständig funktionsfähig sein
    2. Best Practices für {language} befolgen
    3. Gut dokumentiert sein
    4. Bei Spielentwicklung flüssiges Rendering und gutes Designs berücksichtigen
    
    Gib den vollständigen Code zurück, der in eine Datei {output_file} gespeichert werden kann.
    Verwende keine Markdown-Formatierung außer für den Code-Block selbst.
    """
    
    # Claude anfragen
    response = ask_claude(prompt)
    
    # Code extrahieren
    code = extract_code_from_response(response, language.lower())
    
    if code:
        # Code in Datei schreiben
        write_file(output_file, code)
        
        # Tests ausführen
        success, stdout, stderr = run_tests(output_file)
        
        if success:
            print(f"✅ Tests für {output_file} erfolgreich!")
        else:
            print(f"❌ Tests für {output_file} fehlgeschlagen!")
            print(f"Fehlerausgabe: {stderr}")
            
            # Bei fehlgeschlagenen Tests: Verbesserungsvorschläge holen
            fix_prompt = f"""
            Der folgende {language}-Code hat einen Fehler. Bitte korrigiere ihn:
            
            ```
            {code}
            ```
            
            Fehlerausgabe:
            ```
            {stderr}
            ```
            
            Gib nur den korrigierten Code zurück, ohne Erklärungen.
            """
            
            fix_response = ask_claude(fix_prompt)
            fixed_code = extract_code_from_response(fix_response, language.lower())
            
            if fixed_code:
                print("Versuche, Code zu reparieren...")
                write_file(output_file, fixed_code)
                
                # Reparierte Version testen
                success, stdout, stderr = run_tests(output_file)
                if success:
                    print(f"✅ Code repariert! Tests für {output_file} erfolgreich!")
                else:
                    print(f"❌ Auch reparierte Version fehlgeschlagen. Speichere als {output_file}.broken")
                    write_file(f"{output_file}.broken", fixed_code)
        
        return output_file
    
    return None

def generate_test(code_file):
    """
    Generiert Tests für eine Codedatei
    """
    if not os.path.exists(code_file):
        print(f"Codedatei {code_file} nicht gefunden!")
        return None
    
    # Dateiendung extrahieren für Sprachbestimmung
    _, file_extension = os.path.splitext(code_file)
    file_extension = file_extension.lower()
    
    # Sprache und Testframework basierend auf Dateiendung bestimmen
    language_test_map = {
        '.cs': ('C#', 'NUnit oder xUnit'),
        '.py': ('Python', 'unittest oder pytest'),
        '.js': ('JavaScript', 'Jest oder Mocha'),
        '.ts': ('TypeScript', 'Jest oder Mocha'),
        '.cpp': ('C++', 'Google Test oder Catch2'),
        '.h': ('C++', 'Google Test oder Catch2'),
        '.hpp': ('C++', 'Google Test oder Catch2'),
        '.cc': ('C++', 'Google Test oder Catch2'),
        '.java': ('Java', 'JUnit'),
        '.rb': ('Ruby', 'RSpec'),
        '.go': ('Go', 'testing package'),
        '.rs': ('Rust', 'rust test framework')
    }
    
    language, test_framework = language_test_map.get(file_extension, ("unbekannt", "unbekannt"))
    
    # Code lesen
    with open(code_file, 'r') as file:
        code_content = file.read()
    
    # Testdateinamen erstellen
    file_name_without_ext = os.path.splitext(code_file)[0]
    test_file = f"{file_name_without_ext}_test{file_extension}"
    
    # Prompt für die Testgenerierung erstellen
    prompt = f"""
    Bitte generiere Tests für den folgenden {language}-Code mit {test_framework}:
    
    ```
    {code_content}
    ```
    
    Die Tests sollten:
    1. Alle öffentlichen Funktionen/Methoden testen
    2. Edge Cases abdecken
    3. Best Practices für Tests in {language} befolgen
    4. Ausführbar sein
    
    Gib den vollständigen Testcode zurück, der in eine Datei {test_file} gespeichert werden kann.
    """
    
    # Claude anfragen
    response = ask_claude(prompt)
    
    # Testcode extrahieren
    test_code = extract_code_from_response(response, language.lower())
    
    if test_code:
        # Tests in Datei schreiben
        write_file(test_file, test_code)
        print(f"Testdatei {test_file} erstellt")
        return test_file
    
    return None

def watch_directory(directory_path, file_extensions=None, interval=60):
    """
    Überwacht ein Verzeichnis auf .spec-Dateien und generiert Code
    """
    if file_extensions is None:
        file_extensions = [".spec.cs", ".spec.py", ".spec.cpp", ".spec.js"]
    
    # Startzeit der Überwachung ausgeben
    print(f"Überwache Verzeichnis {directory_path} für Spezifikationsdateien mit {', '.join(file_extensions)}...")
    print(f"Drücke Ctrl+C zum Beenden")
    
    # Letzter Änderungszeitpunkt speichern
    file_timestamps = {}
    
    # Initialer Scan aller Dateien
    for root, _, files in os.walk(directory_path):
        for file in files:
            if any(file.endswith(ext) for ext in file_extensions):
                full_path = os.path.join(root, file)
                file_timestamps[full_path] = os.path.getmtime(full_path)
    
    # Kontinuierliche Überwachung
    global running
    while running:
        # Nach neuen oder geänderten Spezifikationsdateien suchen
        for root, _, files in os.walk(directory_path):
            for file in files:
                if any(file.endswith(ext) for ext in file_extensions):
                    full_path = os.path.join(root, file)
                    current_mtime = os.path.getmtime(full_path)
                    
                    # Überprüfen, ob die Datei geändert wurde oder neu ist
                    if full_path not in file_timestamps or current_mtime > file_timestamps[full_path]:
                        print(f"Neue/geänderte Spezifikation erkannt: {full_path}")
                        
                        # Code generieren
                        code_file = generate_code(full_path)
                        
                        if code_file:
                            # Tests generieren
                            generate_test(code_file)
                        
                        file_timestamps[full_path] = current_mtime
        
        # Nach einer bestimmten Zeit erneut prüfen
        time.sleep(interval)

if __name__ == "__main__":
    if not ANTHROPIC_API_KEY:
        raise ValueError("ANTHROPIC_API_KEY Umgebungsvariable nicht gesetzt")
    
    # Konfiguration - ändere diese Werte nach Bedarf
    watch_directory(
        directory_path="./",  # Das zu überwachende Verzeichnis
        file_extensions=[".spec.cs", ".spec.py", ".spec.cpp", ".spec.js"],  # Spec-Dateiendungen
        interval=30  # Überprüfungsintervall in Sekunden
    )
