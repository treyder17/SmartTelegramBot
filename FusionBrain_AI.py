import requests
import json
import asyncio
import config

# Header Informationen aus der config.py
HEADERS = {
    'X-Key': f'Key {config.API_KEY}',
    'X-Secret': f'Secret {config.SECRET_KEY}',
}

URL = 'https://api-key.fusionbrain.ai/'


async def generate(prompt):
    """
    Sendet einen Prompt an FusionBrain AI und wartet auf das Ergebnis.
    Gibt die Liste der Bild-Dateien (Base64) zurück oder None bei Fehlern.
    """
    params = {
        "type": "GENERATE",
        "style": "PIXEL",
        "numImages": 1,
        "width": 1024,
        "height": 1024,
        "generateParams": {"query": prompt}
    }

    files = {
        'pipeline_id': (None, 'a17740da-e8a0-4816-876a-74326c5c4cef'),
        'params': (None, json.dumps(params), 'application/json')
    }

    # Versuche den ersten Request bis zu 3 Mal bei Netzwerkfehlern/Timeouts
    for attempt_run in range(3):
        try:
            # 1. Schritt: Generierung starten (POST Request)
            # Timeout auf 30 Sekunden erhöht, da die API manchmal träge reagiert
            response = requests.post(
                URL + 'key/api/v1/pipeline/run',
                headers=HEADERS,
                files=files,
                timeout=30
            )

            if response.status_code in [200, 201]:
                break  # Erfolg beim Starten

            print(f"API Start-Fehler: Status {response.status_code}")
            if attempt_run < 2:
                await asyncio.sleep(2)
                continue
            return None

        except (requests.exceptions.Timeout, requests.exceptions.ConnectionError) as e:
            print(f"Verbindungsversuch {attempt_run + 1} fehlgeschlagen: {e}")
            if attempt_run < 2:
                await asyncio.sleep(2)
                continue
            return None
        except Exception as e:
            print(f"Kritischer Fehler beim API-Aufruf: {e}")
            return None

    # Falls wir hier sind, war der POST erfolgreich
    try:
        data = response.json()
        uuid = data.get('uuid')
        if not uuid:
            print(f"Keine UUID in der Antwort gefunden: {data}")
            return None

        attempts = 0
        # 2. Schritt: Status abfragen bis 'DONE' oder 'FAIL'
        while attempts < 60:  # Auf 60 Versuche erhöht für mehr Puffer
            try:
                status_response = requests.get(
                    URL + 'key/api/v1/pipeline/status/' + uuid,
                    headers=HEADERS,
                    timeout=20
                )

                if status_response.status_code == 200:
                    status_data = status_response.json()
                    current_status = status_data.get('status')

                    if current_status == 'DONE':
                        result = status_data.get('result', {})
                        return result.get('files', [])

                    if current_status == 'FAIL':
                        error_msg = status_data.get('errorDescription', 'Unbekannter Fehler')
                        print(f"KI Generierung fehlgeschlagen: {error_msg}")
                        return None
                else:
                    print(f"Status-Abfrage fehlgeschlagen (Code {status_response.status_code})")

            except requests.exceptions.RequestException:
                # Bei kurzen Aussetzern während der Statusabfrage einfach weiter probieren
                pass

            attempts += 1
            await asyncio.sleep(3)

        print("Timeout: Die Bildgenerierung hat zu lange gedauert.")
        return None

    except Exception as e:
        print(f"Ein unerwarteter Fehler ist nach dem Start aufgetreten: {e}")
        return None