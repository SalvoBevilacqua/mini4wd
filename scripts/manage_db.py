#!/usr/bin/env python3
"""
TAMIYA MINI 4WD ITALIA - DATABASE MANAGER & BUILD SYSTEM
========================================================
Strumento di gestione centralizzata del database Tamiya Mini 4WD Italia.
Mantiene in sincronia 'data/tamiya_db.json' e il file frontend 'js/data.js'.

Tutte le modifiche (aggiunta pezzi, modifica regolamenti, build, sync Tamiya)
vengono gestite esclusivamente da questo script, garantendo che il sito web
pubblico sia sicuro, veloce e privo di pannelli di amministrazione esposti.

Utilizzo:
    python scripts/manage_db.py list [--category CAT] [--search QUERY]
    python scripts/manage_db.py add
    python scripts/manage_db.py remove <itemNumber_o_id>
    python scripts/manage_db.py validate
    python scripts/manage_db.py build
    python scripts/manage_db.py sync
"""

import os
import sys
import json
import re
import argparse
import urllib.request

ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(ROOT_DIR, "data")
JS_DIR = os.path.join(ROOT_DIR, "js")
DB_JSON_PATH = os.path.join(DATA_DIR, "tamiya_db.json")
JS_DATA_PATH = os.path.join(JS_DIR, "data.js")

CATEGORIES_LIST = ["chassis", "motor", "plate", "damper", "roller", "wheel", "brake", "gear", "accessory"]
CHASSIS_TYPES = ["universal", "single", "double"]
CLASSES_LIST = ["bmax", "open", "tuned", "boxstock", "expert", "street"]

def load_db():
    if not os.path.exists(DB_JSON_PATH):
        raise FileNotFoundError(f"Database JSON non trovato: {DB_JSON_PATH}")
    with open(DB_JSON_PATH, "r", encoding="utf-8") as f:
        return json.load(f)

def save_db(db):
    os.makedirs(DATA_DIR, exist_ok=True)
    with open(DB_JSON_PATH, "w", encoding="utf-8") as f:
        json.dump(db, f, indent=2, ensure_ascii=False)
    print(f"[V] Database salvato con successo in {os.path.relpath(DB_JSON_PATH, ROOT_DIR)}")
    build_js_data(db)

def build_js_data(db=None):
    if db is None:
        db = load_db()

    categories = db.get("MINI4WD_CATEGORIES", {})
    components = db.get("TAMIYA_COMPONENTS", [])
    recommended_builds = db.get("RECOMMENDED_BUILDS", {})
    paddock_tips = db.get("CATEGORY_PADDOCK_TIPS", {})

    content = []
    content.append("/**")
    content.append(" * TAMIYA MINI 4WD ITALIA - DATABASE CATEGORIE E COMPONENTI")
    content.append(" * Generato automaticamente da scripts/manage_db.py")
    content.append(" * ")
    content.append(" * NOTA: Questo file e di sola lettura nel frontend.")
    content.append(" * Le modifiche devono essere eseguite tramite: python scripts/manage_db.py")
    content.append(" */")
    content.append("")
    content.append("const MINI4WD_CATEGORIES = " + json.dumps(categories, indent=2, ensure_ascii=False) + ";")
    content.append("")
    content.append("/**")
    content.append(" * COMPONENT DATABASE")
    content.append(" * Verified Tamiya items with official item numbers, descriptions, specs, images, and category legality rules.")
    content.append(" */")
    content.append("const TAMIYA_COMPONENTS = " + json.dumps(components, indent=2, ensure_ascii=False) + ";")
    content.append("")
    content.append("/**")
    content.append(" * RECOMMENDED BUILDS & PRESETS (BY CATEGORY)")
    content.append(" */")
    content.append("const RECOMMENDED_BUILDS = " + json.dumps(recommended_builds, indent=2, ensure_ascii=False) + ";")
    content.append("")
    content.append("/**")
    content.append(" * CATEGORY PADDOCK TIPS & TECHNICAL SECRETS")
    content.append(" */")
    content.append("const CATEGORY_PADDOCK_TIPS = " + json.dumps(paddock_tips, indent=2, ensure_ascii=False) + ";")
    content.append("")

    with open(JS_DATA_PATH, "w", encoding="utf-8") as f:
        f.write("\n".join(content))
    print(f"[V] Compilato 'js/data.js' con {len(components)} componenti e {len(categories)} categorie.")

def check_cloudfront_image(item_number):
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

def cmd_list(args):
    db = load_db()
    items = db.get("TAMIYA_COMPONENTS", [])
    
    if args.category:
        items = [i for i in items if i.get("category") == args.category]
    if args.search:
        q = args.search.lower()
        items = [i for i in items if q in i.get("name", "").lower() or q in i.get("itemNumber", "").lower()]

    print(f"\n=== CATALOGO MINI 4WD TAMIYA ({len(items)} articoli visualizzati) ===")
    print(f"{'Idx':<4} | {'Cat':<10} | {'Item #':<7} | {'Prezzo':<7} | {'Nome Componente'}")
    print("-" * 75)
    for idx, item in enumerate(items, 1):
        cat = item.get("category", "")
        num = item.get("itemNumber", "")
        price = f"EUR {item.get('price', 0):.2f}"
        name = item.get("name", "")
        print(f"{idx:<4} | {cat:<10} | {num:<7} | {price:<7} | {name}")
    print("-" * 75 + "\n")

def cmd_validate(args=None):
    db = load_db()
    items = db.get("TAMIYA_COMPONENTS", [])
    categories = db.get("MINI4WD_CATEGORIES", {})
    builds = db.get("RECOMMENDED_BUILDS", {})

    print("[*] Esecuzione validazione integrita del database...")
    errors = []
    warnings = []

    item_numbers = {}
    item_ids = set()

    classes_available = list(categories.keys())
    for idx, item in enumerate(items):
        i_id = item.get("id")
        i_num = item.get("itemNumber")
        name = item.get("name")

        if not i_id:
            errors.append(f"Articolo #{idx} privo di 'id'")
        elif i_id in item_ids:
            errors.append(f"ID duplicato: '{i_id}' in '{name}'")
        else:
            item_ids.add(i_id)

        if not i_num:
            errors.append(f"Articolo '{i_id}' privo di 'itemNumber'")
        else:
            if i_num in item_numbers:
                warnings.append(f"Attenzione: itemNumber #{i_num} usato piu volte: '{item_numbers[i_num]}' e '{name}'")
            else:
                item_numbers[i_num] = name

        cat = item.get("category")
        if cat not in CATEGORIES_LIST:
            errors.append(f"Articolo #{i_num} '{name}' ha una categoria non valida: '{cat}'")

        chassis = item.get("chassisType")
        if chassis not in CHASSIS_TYPES:
            errors.append(f"Articolo #{i_num} '{name}' ha un chassisType non valido: '{chassis}'")

        allowed = item.get("allowedCategories", [])
        for c in allowed:
            if c not in classes_available:
                errors.append(f"Articolo #{i_num} fa riferimento alla classe inesistente: '{c}'")

    # Verifica presets
    for b_key, build in builds.items():
        for p_id in build.get("parts", []):
            if p_id not in item_ids:
                warnings.append(f"Preset '{b_key}' fa riferimento all'id '{p_id}' non trovato nei componenti")

    print(f"[*] Totale componenti verificati: {len(items)}")
    print(f"[*] Totale categorie verificate: {len(categories)}")

    if errors:
        print(f"\n[-] RILEVATI {len(errors)} ERRORI CRITICI:")
        for err in errors:
            print(f"  - {err}")
    else:
        print("\n[V] Nessun errore critico rilevato.")

    if warnings:
        print(f"\n[!] {len(warnings)} AVVISI:")
        for w in warnings:
            print(f"  - {w}")
    else:
        print("[V] Nessun avviso.")

    return len(errors) == 0

def cmd_add(args):
    db = load_db()
    items = db.get("TAMIYA_COMPONENTS", [])

    print("\n=== AGGIUNTA NUOVO COMPONENTE TAMIYA ===")
    item_num = args.item if args.item else input("Codice Articolo Tamiya (es. 15499 o 95689): ").strip()
    if not item_num:
        print("[-] Codice articolo obbligatorio.")
        return

    # Controlla se gia presente
    existing = [i for i in items if i.get("itemNumber") == item_num]
    if existing:
        print(f"[!] Attenzione: codice #{item_num} gia presente: '{existing[0].get('name')}'.")
        ans = input("Vuoi comunque procedere? [s/N]: ").strip().lower()
        if ans != 's':
            return

    name = args.name if args.name else input("Nome Ufficiale Componente (Tamiya): ").strip()
    category = args.category if args.category else input(f"Categoria ({', '.join(CATEGORIES_LIST)}): ").strip().lower()
    chassis = args.chassis if args.chassis else input(f"Compatibilita telaio ({', '.join(CHASSIS_TYPES)}): [universal] ").strip().lower() or "universal"
    price = args.price if args.price is not None else float(input("Prezzo indicativo (€): [7.50] ") or 7.50)
    desc = args.desc if args.desc else input("Descrizione e note tecniche: ").strip()

    cf_img = check_cloudfront_image(item_num)
    if cf_img:
        print(f"[+] Immagine ufficiale trovata su Tamiya CloudFront: {cf_img}")
        images = [cf_img]
    else:
        first_digit = item_num[0]
        images = [f"https://d7z22c0gz59ng.cloudfront.net/japan_contents/img/usr/item/{first_digit}/{item_num}/{item_num}_1.jpg"]

    new_item = {
        "id": f"part_{item_num}_{category}",
        "itemNumber": item_num,
        "name": name,
        "category": category,
        "chassisType": chassis,
        "price": round(price, 2),
        "description": desc or f"Componente Tune-Up ufficiale Tamiya Item #{item_num}.",
        "specs": {
            "Categoria": category.upper(),
            "Telaio": chassis.upper()
        },
        "images": images,
        "tamiyaUrl": f"https://www.tamiya.com/japan/products/{item_num}/index.html",
        "allowedCategories": ["bmax", "open", "tuned", "street"],
        "rulesNotes": {
            "bmax": "Verificare il montaggio bolt-on secondo dima 105mm.",
            "open": "100% Legale in Open Class."
        }
    }

    items.append(new_item)
    db["TAMIYA_COMPONENTS"] = items
    save_db(db)
    print(f"[V] Componente #{item_num} - '{name}' aggiunto e compilato con successo!")

def cmd_remove(args):
    db = load_db()
    items = db.get("TAMIYA_COMPONENTS", [])
    target = args.target.strip()

    filtered = [i for i in items if i.get("itemNumber") != target and i.get("id") != target]
    if len(filtered) == len(items):
        print(f"[-] Nessun articolo trovato corrispondente a '{target}'.")
        return

    db["TAMIYA_COMPONENTS"] = filtered
    save_db(db)
    print(f"[V] Rimosso componente '{target}'. Totale componenti rimanenti: {len(filtered)}.")

def cmd_sync(args=None):
    from sync_tamiya import update_database
    update_database()
    # Esegui anche il build
    build_js_data()

def main():
    parser = argparse.ArgumentParser(description="Tamiya Mini 4WD Italia - Gestore Database & Compilatore")
    subparsers = parser.add_subparsers(dest="command", help="Comandi disponibili")

    # List
    p_list = subparsers.add_parser("list", help="Elenca tutti i componenti nel catalogo")
    p_list.add_argument("--category", choices=CATEGORIES_LIST, help="Filtra per categoria")
    p_list.add_argument("--search", help="Cerca per testo o codice articolo")

    # Add
    p_add = subparsers.add_parser("add", help="Aggiunge un nuovo componente")
    p_add.add_argument("--item", help="Codice articolo Tamiya")
    p_add.add_argument("--name", help="Nome componente")
    p_add.add_argument("--category", choices=CATEGORIES_LIST, help="Categoria")
    p_add.add_argument("--chassis", choices=CHASSIS_TYPES, help="Compatibilita telaio")
    p_add.add_argument("--price", type=float, help="Prezzo")
    p_add.add_argument("--desc", help="Descrizione")

    # Remove
    p_rm = subparsers.add_parser("remove", help="Rimuove un componente tramite codice o id")
    p_rm.add_argument("target", help="Item number o ID da rimuovere")

    # Validate
    subparsers.add_parser("validate", help="Valida la correttezza e l'integrita del database")

    # Build
    subparsers.add_parser("build", help="Genera/compila 'js/data.js' a partire da 'data/tamiya_db.json'")

    # Sync
    subparsers.add_parser("sync", help="Interroga Tamiya Japan e aggiorna il catalogo")

    args = parser.parse_args()

    if args.command == "list":
        cmd_list(args)
    elif args.command == "add":
        cmd_add(args)
    elif args.command == "remove":
        cmd_remove(args)
    elif args.command == "validate":
        cmd_validate(args)
    elif args.command == "build":
        build_js_data()
    elif args.command == "sync":
        cmd_sync(args)
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
