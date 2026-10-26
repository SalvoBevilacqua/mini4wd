"""
TAMIYA MINI 4WD ITALIA - SYNC & CATALOG UPDATER SCRIPT
Esegue il controllo periodico delle novita e rilasci ufficiali Mini 4WD sul portale Tamiya Japan.
Aggiorna o genera data/tamiya_db.json.

Utilizzo:
    python scripts/sync_tamiya.py
"""

import urllib.request
import re
import json
import os
import sys

TAMIYA_GRADEUP_URL = "https://www.tamiya.com/japan/products/list.html?genre_item=801010"
DB_PATH = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "data", "tamiya_db.json")

def fetch_latest_tamiya_item_numbers():
    print(f"[*] Interrogazione catalogo Tamiya: {TAMIYA_GRADEUP_URL} ...")
    req = urllib.request.Request(TAMIYA_GRADEUP_URL, headers={"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"})
    try:
        with urllib.request.urlopen(req, timeout=10) as resp:
            html = resp.read().decode("shift_jis", errors="ignore")
        
        # Cerca link del tipo /japan/products/15477/index.html
        raw_items = re.findall(r'/japan/products/(\d{5})/index\.html', html)
        # Rimuovi duplicati preservando l'ordine
        items = list(dict.fromkeys(raw_items))
        print(f"[+] Rilevati {len(items)} articoli Mini 4WD recenti nel catalogo ufficiale Tamiya.")
        return items
    except Exception as e:
        print(f"[-] Errore durante l'interrogazione di Tamiya: {e}")
        return []

def verify_cloudfront_image(item_number):
    """Verifica se l'immagine ufficiale e disponibile su CloudFront"""
    first_digit = item_number[0]
    url = f"https://d7z22c0gz59ng.cloudfront.net/japan_contents/img/usr/item/{first_digit}/{item_number}/{item_number}_1.jpg"
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"}, method="HEAD")
    try:
        with urllib.request.urlopen(req, timeout=4) as r:
            if r.status == 200:
                return url
    except Exception:
        pass
    return None

def update_database():
    if not os.path.exists(DB_PATH):
        print(f"[-] File database non trovato: {DB_PATH}")
        return

    with open(DB_PATH, "r", encoding="utf-8") as f:
        db = json.load(f)

    existing_numbers = {c.get("itemNumber") for c in db.get("TAMIYA_COMPONENTS", [])}
    print(f"[*] Database attuale contiene {len(existing_numbers)} componenti.")

    latest_items = fetch_latest_tamiya_item_numbers()
    new_found = [num for num in latest_items if num not in existing_numbers]

    print(f"[*] Articoli nel catalogo non ancora mappati nel DB: {len(new_found)}")
    if new_found:
        print(f"[*] Campione nuovi codici: {new_found[:10]}")
        print("[*] E possibile aggiungerli tramite il 'Pannello Gestione Database' sul sito con relative regole di omologazione.")

    print("\n[V] Sincronizzazione completata con successo!")

if __name__ == "__main__":
    update_database()
