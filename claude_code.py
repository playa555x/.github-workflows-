import os
import requests
import json

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

def process_code_files():
    """
    Verarbeitet Code-Dateien im Repository und lässt Claude Verbesserungen vorschlagen
    """
    # Hier Code zum Durchsuchen des Repos nach bestimmten Dateien
    code_files = ["example.py", "app.js"]  # Beispiel
    
    for file_path in code_files:
        if os.path.exists(file_path):
            with open(file_path, "r") as file:
                code_content = file.read()
            
            # Claude nach Verbesserungen fragen
            prompt = f"""
            Hier ist ein Code aus unserer Codebasis. Bitte analysiere ihn und schlage Verbesserungen vor:
            
            ```
            {code_content}
            ```
            
            Gib deine Antwort im JSON-Format zurück mit den Schlüsseln 'analysis' und 'improved_code'.
            """
            
            claude_response = ask_claude(prompt)
            
            try:
                # Antwort parsen
                response_data = json.loads(claude_response)
                
                # Verbesserungen in eine Datei schreiben
                with open(f"{file_path}_improved.txt", "w") as output_file:
                    output_file.write(f"Analyse:\n{response_data['analysis']}\n\n")
                    output_file.write(f"Verbesserter Code:\n{response_data['improved_code']}")
                
                print(f"Verarbeitung von {file_path} abgeschlossen")
            
            except json.JSONDecodeError:
                print(f"Fehler beim Parsen der Claude-Antwort für {file_path}")
                with open(f"{file_path}_raw_response.txt", "w") as output_file:
                    output_file.write(claude_response)

if __name__ == "__main__":
    if not ANTHROPIC_API_KEY:
        raise ValueError("ANTHROPIC_API_KEY Umgebungsvariable nicht gesetzt")
    
    process_code_files()
