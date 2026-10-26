#!/usr/bin/env python3
"""
Script di espansione e verifica catalogo Tamiya Mini 4WD Italia
Corregge gli item esistenti e inserisce i nuovi componenti omologati.
"""

import json
import os
import sys

ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT_DIR, "scripts"))
from manage_db import load_db, save_db, check_cloudfront_image

def run_update():
    db = load_db()
    components = db.get("TAMIYA_COMPONENTS", [])

    print(f"[*] Componenti prima dell'aggiornamento: {len(components)}")

    # =========================================================================
    # 1. FIXES SUGLI ITEM ESISTENTI
    # =========================================================================
    for c in components:
        # Fix Mach-Dash PRO (15433)
        if c.get("itemNumber") == "15433":
            c["name"] = "Mach-Dash Motor PRO"
            c["chassisType"] = "double"
            c["description"] = "Il celebre motore ad altissima velocità della serie Dash a doppio pignone per telai MA ed MS. Con un regime oltre i 23.400 giri al minuto e spazzole al carbone, è il re indiscusso delle piste veloci con lunghi rettilinei e curvoni ad ampio raggio."
            c["specs"]["Albero"] = "Doppio pignone (Double Shaft PRO)"
            c["specs"]["Telaio compatibile"] = "MA Chassis, MS Chassis"

        # Fix AR Mass Damper (era con codice errato 15451, in realtà è 15460)
        if c.get("id") == "damp_15451_mass" or (c.get("category") == "damper" and c.get("itemNumber") == "15451"):
            c["id"] = "damp_15460"
            c["itemNumber"] = "15460"
            c["images"] = [
                "https://d7z22c0gz59ng.cloudfront.net/japan_contents/img/usr/item/1/15460/15460_1.jpg",
                "https://d7z22c0gz59ng.cloudfront.net/japan_contents/img/usr/item/1/15460/15460_s.jpg"
            ]
            c["tamiyaUrl"] = "https://www.tamiya.com/japan/products/15460/index.html"
            c["specs"]["Item Ufficiale"] = "Tamiya #15460"

    existing_nums = {c.get("itemNumber") for c in components}

    # =========================================================================
    # 2. NUOVI COMPONENTI DA AGGIUNGERE
    # =========================================================================
    new_items = [
        # --- CHASSIS ---
        {
            "id": "kit_18094",
            "itemNumber": "18094",
            "name": "Neo-VQS (VZ Chassis)",
            "category": "chassis",
            "chassisType": "single",
            "price": 13.90,
            "description": "L'erede moderno della leggendaria serie Vanquish su innovativo telaio VZ. Carrozzeria filante e aggressiva in plastica rigida nera con sticker metallizzati, cerchi a 5 razze e telaio compatto con interasse corto da 80mm che garantisce una maneggevolezza fulminea nelle curve a gomito.",
            "specs": {
                "Telaio": "VZ Chassis (Nero rinforzato)",
                "Trasmissione": "Singolo albero con rinvio",
                "Rapporto di serie": "3.5:1 Super Speed Gear",
                "Interasse": "80 mm",
                "Carrozzeria": "ABS rigido nero lucido aerodinamico",
                "Ruote": "Cerchi neri 5-Spoke e gomme nere low-profile 26mm"
            },
            "images": [
                "https://d7z22c0gz59ng.cloudfront.net/japan_contents/img/usr/item/1/18094/18094_1.jpg",
                "https://d7z22c0gz59ng.cloudfront.net/japan_contents/img/usr/item/1/18094/18094_s.jpg"
            ],
            "tamiyaUrl": "https://www.tamiya.com/japan/products/18094/index.html",
            "allowedCategories": ["bmax", "open", "tuned", "boxstock", "street"],
            "rulesNotes": {
                "bmax": "100% Legale. Carrozzeria rigida conforme, telaio leggero con eccellente flessibilità controllata.",
                "open": "100% Legale. Ottima piattaforma per telai tagliati e Chochin anteriori.",
                "tuned": "100% Legale. Maneggevolezza eccezionale con motori Tuned 2.",
                "boxstock": "100% Legale per gare monomarca Box Stock Neo-VQS.",
                "street": "100% Legale per corse outdoor."
            }
        },
        {
            "id": "kit_18707",
            "itemNumber": "18707",
            "name": "Rowdy Bull (FM-A Chassis)",
            "category": "chassis",
            "chassisType": "single",
            "price": 14.20,
            "description": "Il celebre modello apripista del telaio FM-A a motore anteriore (Front Midship Aero). Con linee muscolose da muscle car americana, sposta il baricentro in avanti consentendo atterraggi stabili e dritti dai dossi, evitando l'impennamento del muso in fase di salto.",
            "specs": {
                "Telaio": "FM-A Chassis (Nero ad alta resistenza)",
                "Trasmissione": "Motore anteriore a singolo albero",
                "Rapporto di serie": "3.5:1 Super Speed Gear",
                "Interasse": "83 mm",
                "Carrozzeria": "ABS rigido finitura argento metallizzato",
                "Ruote": "Cerchi argento Low-Profile e gomme nere A-spoke 26mm"
            },
            "images": [
                "https://d7z22c0gz59ng.cloudfront.net/japan_contents/img/usr/item/1/18707/18707_1.jpg",
                "https://d7z22c0gz59ng.cloudfront.net/japan_contents/img/usr/item/1/18707/18707_s.jpg"
            ],
            "tamiyaUrl": "https://www.tamiya.com/japan/products/18707/index.html",
            "allowedCategories": ["bmax", "open", "tuned", "boxstock", "street"],
            "rulesNotes": {
                "bmax": "100% Legale. Il telaio FM-A con Skid Bar integrata è ideale per piste tecniche B-Max.",
                "open": "100% Legale. Molto usato nelle piste con salti a discesa rapida.",
                "tuned": "100% Legale.",
                "boxstock": "100% Legale in Box Stock.",
                "street": "Eccezionale stabilità su fondi accidentati."
            }
        },
        {
            "id": "kit_18637",
            "itemNumber": "18637",
            "name": "Festa Jaune (MA Chassis)",
            "category": "chassis",
            "chassisType": "double",
            "price": 14.50,
            "description": "Splendida supercar ispirata alle granturismo da competizione moderne. Il telaio MA monoblocco a doppio albero centrale garantisce un allineamento perfetto dei pignoni motore senza dispersioni di potenza e un raffreddamento ottimale grazie ai condotti aerodinamici inferiori.",
            "specs": {
                "Telaio": "MA Chassis (Grigio scuro ad alta rigidità)",
                "Trasmissione": "Doppio albero centrale Double Shaft",
                "Rapporto di serie": "3.5:1 Super Speed",
                "Interasse": "80 mm",
                "Carrozzeria": "ABS rigido giallo brillante stile GT",
                "Ruote": "Cerchi neri Fin Type e gomme a profilo ribassato"
            },
            "images": [
                "https://d7z22c0gz59ng.cloudfront.net/japan_contents/img/usr/item/1/18637/18637_1.jpg",
                "https://d7z22c0gz59ng.cloudfront.net/japan_contents/img/usr/item/1/18637/18637_s.jpg"
            ],
            "tamiyaUrl": "https://www.tamiya.com/japan/products/18637/index.html",
            "allowedCategories": ["bmax", "open", "tuned", "boxstock", "street"],
            "rulesNotes": {
                "bmax": "100% Legale. Telaio rigido monoblocco che preserva l'assetto anche dopo atterraggi duri.",
                "open": "100% Legale.",
                "tuned": "100% Legale.",
                "boxstock": "100% Legale per gare Box Stock Festa Jaune.",
                "street": "100% Legale."
            }
        },
        {
            "id": "kit_19601",
            "itemNumber": "19601",
            "name": "Max Breaker TRF (Super X Chassis)",
            "category": "chassis",
            "chassisType": "single",
            "price": 13.50,
            "description": "Versione TRF da competizione dell'iconica vettura di Gouki Ichimonji. Il telaio Super X si contraddistingue per la carreggiata larga (interasse 84mm), il motore smontabile dal fondo senza rimuovere carrozzeria o ingranaggi e una stabilità sui rettilinei senza eguali.",
            "specs": {
                "Telaio": "Super X Chassis (Policarbonato/ABS ad alta tenacità)",
                "Trasmissione": "Singolo albero con pozzetto motore a sgancio rapido dal basso",
                "Rapporto di serie": "3.5:1",
                "Interasse": "84 mm",
                "Carrozzeria": "ABS rigido con prese d'aria TRF aperte",
                "Ruote": "Cerchi larghi e gomme slick semi-pneumatiche"
            },
            "images": [
                "https://d7z22c0gz59ng.cloudfront.net/japan_contents/img/usr/item/1/19601/19601_1.jpg",
                "https://d7z22c0gz59ng.cloudfront.net/japan_contents/img/usr/item/1/19601/19601_s.jpg"
            ],
            "tamiyaUrl": "https://www.tamiya.com/japan/products/19601/index.html",
            "allowedCategories": ["bmax", "open", "tuned", "boxstock", "expert", "street"],
            "rulesNotes": {
                "bmax": "100% Legale. Ottima stabilità grazie alla carreggiata allargata da 84mm.",
                "open": "100% Legale.",
                "expert": "Tra i telai storici più apprezzati nella categoria Expert / R.U.M. per piste Flat Track veloci.",
                "street": "100% Legale."
            }
        },

        # --- MOTORI ---
        {
            "id": "motor_15438",
            "itemNumber": "15438",
            "name": "Mach-Dash Motor",
            "category": "motor",
            "chassisType": "single",
            "price": 7.20,
            "description": "Il motore a singolo pignone più veloce della celebre gamma Dash Tamiya per telai tradizionali (VZ, FM-A, AR, Super-II, VS). Campana rossa, spazzole metalliche in carbonio ad alta conducibilità e regime fino a 23.400 rpm: devastante sui rettilinei delle gare B-Max veloci.",
            "specs": {
                "Albero": "Singolo pignone (Single Shaft)",
                "Tensione nominale": "2.4 - 3.0 V",
                "Giri/min (RPM sotto carico)": "20.000 - 23.400 rpm",
                "Coppia": "1.3 - 1.8 mN·m",
                "Consumo corrente": "2.0 - 4.0 A",
                "Campana": "Rossa",
                "Spazzole": "Miste carbone ad alto scorrimento"
            },
            "images": [
                "https://d7z22c0gz59ng.cloudfront.net/japan_contents/img/usr/item/1/15438/15438_1.jpg",
                "https://d7z22c0gz59ng.cloudfront.net/japan_contents/img/usr/item/1/15438/15438_s.jpg"
            ],
            "tamiyaUrl": "https://www.tamiya.com/japan/products/15438/index.html",
            "allowedCategories": ["bmax", "open"],
            "rulesNotes": {
                "bmax": "100% Legale. Ideale quando il tracciato presenta lunghi rettilinei e poche curve strette.",
                "open": "100% Legale.",
                "tuned": "VIETATO! Nella categoria Tuned sono ammessi solo motori serie Tuned.",
                "boxstock": "VIETATO! Ammesso solo motore stock di serie.",
                "expert": "Consentito solo nelle manifestazioni Expert libere (altrimenti motori serie Tuned/Sprint)."
            }
        },
        {
            "id": "motor_15318",
            "itemNumber": "15318",
            "name": "Sprint-Dash Motor",
            "category": "motor",
            "chassisType": "single",
            "price": 6.90,
            "description": "Motore a singolo albero progettato esclusivamente per velocità pura e allungo estremo su circuiti pianeggianti o con ampie curve paraboliche. Campana grigio chiaro, spazzole in carbonio e regime massimo fino a 27.200 giri/minuto.",
            "specs": {
                "Albero": "Singolo pignone (Single Shaft)",
                "Tensione nominale": "2.4 - 3.0 V",
                "Giri/min (RPM sotto carico)": "20.700 - 27.200 rpm",
                "Coppia": "1.2 - 1.6 mN·m",
                "Consumo corrente": "2.8 - 3.8 A",
                "Campana": "Grigia",
                "Spazzole": "Carbone da competizione"
            },
            "images": [
                "https://d7z22c0gz59ng.cloudfront.net/japan_contents/img/usr/item/1/15318/15318_1.jpg",
                "https://d7z22c0gz59ng.cloudfront.net/japan_contents/img/usr/item/1/15318/15318_s.jpg"
            ],
            "tamiyaUrl": "https://www.tamiya.com/japan/products/15318/index.html",
            "allowedCategories": ["bmax", "open", "expert"],
            "rulesNotes": {
                "bmax": "100% Legale. Richiede freni molto efficienti per gestire la tremenda velocità d'entrata sui salti.",
                "open": "100% Legale.",
                "tuned": "VIETATO nelle classi Tuned.",
                "expert": "Spesso impiegato nelle gare storiche veloci su Flat Track senza salti."
            }
        },
        {
            "id": "motor_15455",
            "itemNumber": "15455",
            "name": "Light-Dash Motor",
            "category": "motor",
            "chassisType": "single",
            "price": 6.50,
            "description": "L'anello di congiunzione perfetto tra i docili motori Tuned e i potenti Dash. Campana gialla, offre un'erogazione lineare con consumo moderato di corrente, ideale per piste tecniche con molti salti dove un Mach-Dash rischierebbe di decollare fuori pista.",
            "specs": {
                "Albero": "Singolo pignone (Single Shaft)",
                "Tensione nominale": "2.4 - 3.0 V",
                "Giri/min (RPM sotto carico)": "14.600 - 17.800 rpm",
                "Coppia": "1.3 - 1.9 mN·m",
                "Consumo corrente": "1.5 - 2.2 A",
                "Campana": "Gialla",
                "Spazzole": "Miste metallo-carbone"
            },
            "images": [
                "https://d7z22c0gz59ng.cloudfront.net/japan_contents/img/usr/item/1/15455/15455_1.jpg",
                "https://d7z22c0gz59ng.cloudfront.net/japan_contents/img/usr/item/1/15455/15455_s.jpg"
            ],
            "tamiyaUrl": "https://www.tamiya.com/japan/products/15455/index.html",
            "allowedCategories": ["bmax", "open"],
            "rulesNotes": {
                "bmax": "100% Legale. Scelta tattica preferita su piste con ostacoli Dragon Back consecutivi.",
                "open": "100% Legale.",
                "tuned": "VIETATO nelle classi Tuned.",
                "street": "Ottimo per garantire autonomia elevata durante lunghe sessioni all'aperto."
            }
        },
        {
            "id": "motor_15488",
            "itemNumber": "15488",
            "name": "Rev-Tuned 2 Motor PRO",
            "category": "motor",
            "chassisType": "double",
            "price": 5.50,
            "description": "Versione a doppio pignone per telai MA ed MS della serie Tuned 2 orientata all'allungo e agli alti regimi. Campana blu brillante, eroga fino a 15.200 giri/min, perfetta per tracciati TMEC/Tuned veloci con curve ampie.",
            "specs": {
                "Albero": "Doppio pignone (Double Shaft PRO)",
                "Tensione nominale": "2.4 - 3.0 V",
                "Giri/min (RPM sotto carico)": "13.400 - 15.200 rpm",
                "Coppia": "1.2 - 1.5 mN·m",
                "Consumo corrente": "1.5 - 2.0 A",
                "Campana": "Blu brillante",
                "Spazzole": "Metallo speciale a bassa resistenza"
            },
            "images": [
                "https://d7z22c0gz59ng.cloudfront.net/japan_contents/img/usr/item/1/15488/15488_1.jpg",
                "https://d7z22c0gz59ng.cloudfront.net/japan_contents/img/usr/item/1/15488/15488_s.jpg"
            ],
            "tamiyaUrl": "https://www.tamiya.com/japan/products/15488/index.html",
            "allowedCategories": ["bmax", "open", "tuned"],
            "rulesNotes": {
                "bmax": "100% Legale. Ideale per telai MA su piste guidate veloci.",
                "tuned": "100% Legale. Uno dei motori cardine nei campionati italiani TMEC / Tuned Class.",
                "open": "100% Legale."
            }
        },
        {
            "id": "motor_15489",
            "itemNumber": "15489",
            "name": "Atomic-Tuned 2 Motor PRO",
            "category": "motor",
            "chassisType": "double",
            "price": 5.50,
            "description": "Il motore a doppio albero più bilanciato e utilizzato nelle gare Tuned/TMEC italiane ed europee. Campana arancione, coniuga ottima coppia in uscita da curva e velocità di punta costante su ogni sezione del tracciato.",
            "specs": {
                "Albero": "Doppio pignone (Double Shaft PRO)",
                "Tensione nominale": "2.4 - 3.0 V",
                "Giri/min (RPM sotto carico)": "12.700 - 14.900 rpm",
                "Coppia": "1.5 - 2.0 mN·m",
                "Consumo corrente": "1.5 - 2.2 A",
                "Campana": "Arancione",
                "Spazzole": "Metallo speciale"
            },
            "images": [
                "https://d7z22c0gz59ng.cloudfront.net/japan_contents/img/usr/item/1/15489/15489_1.jpg",
                "https://d7z22c0gz59ng.cloudfront.net/japan_contents/img/usr/item/1/15489/15489_s.jpg"
            ],
            "tamiyaUrl": "https://www.tamiya.com/japan/products/15489/index.html",
            "allowedCategories": ["bmax", "open", "tuned"],
            "rulesNotes": {
                "bmax": "100% Legale. Straordinaria costanza di rendimento con calo termico minimo.",
                "tuned": "100% Legale. Il motore PRO più venduto per le gare Tuned di tutta Europa.",
                "open": "100% Legale."
            }
        },

        # --- PIASTRE & STAFFE ---
        {
            "id": "stay_15452_frp",
            "itemNumber": "15452",
            "name": "FRP Wide Rear Plate (for AR Chassis)",
            "category": "plate",
            "chassisType": "universal",
            "price": 4.80,
            "description": "Piastra posteriore larga in fibra di vetro FRP ad alta resistenza. Predisposta con fori multipli per l'installazione di rulli da 9mm, 11mm, 13mm, 17mm e 19mm a larghezza regolamentare di 105mm. Compatibile universalmente con AR, VZ, MA, MS, Super-II, FM-A.",
            "specs": {
                "Materiale": "Fibra FRP nera ad alta densità (1.5 mm)",
                "Posizione montaggio": "Posteriore / Rear Stay",
                "Compatibilità rulli": "9 mm, 11 mm, 13 mm, 17 mm, 19 mm",
                "Viti e distanziali": "Inclusi nel blister originale"
            },
            "images": [
                "https://d7z22c0gz59ng.cloudfront.net/japan_contents/img/usr/item/1/15452/15452_1.jpg",
                "https://d7z22c0gz59ng.cloudfront.net/japan_contents/img/usr/item/1/15452/15452_s.jpg"
            ],
            "tamiyaUrl": "https://www.tamiya.com/japan/products/15452/index.html",
            "allowedCategories": ["bmax", "open", "tuned", "expert", "street"],
            "rulesNotes": {
                "bmax": "100% Legale. La staffa posteriore 'bolt-on' più usata in configurazione doppia.",
                "open": "100% Legale.",
                "tuned": "100% Legale.",
                "street": "100% Legale."
            }
        },
        {
            "id": "stay_15394_frp",
            "itemNumber": "15394",
            "name": "FRP Multi Roller Setting Stay",
            "category": "plate",
            "chassisType": "universal",
            "price": 4.50,
            "description": "La staffa universale in fibra FRP più celebre nella storia delle Mini 4WD. Forma ricurva a banana con predisposizione fori per rulli da 9mm, 13mm e 19mm. Utilizzabile indistintamente all'anteriore e al posteriore per irrobustire qualsiasi paraurti.",
            "specs": {
                "Materiale": "Fibra FRP (1.5 mm)",
                "Posizione montaggio": "Universale (Anteriore / Posteriore)",
                "Compatibilità rulli": "9, 13, 19 mm",
                "Profilo": "Curvo Multi-Roller"
            },
            "images": [
                "https://d7z22c0gz59ng.cloudfront.net/japan_contents/img/usr/item/1/15394/15394_1.jpg",
                "https://d7z22c0gz59ng.cloudfront.net/japan_contents/img/usr/item/1/15394/15394_s.jpg"
            ],
            "tamiyaUrl": "https://www.tamiya.com/japan/products/15394/index.html",
            "allowedCategories": ["bmax", "open", "tuned", "expert", "street"],
            "rulesNotes": {
                "bmax": "100% Legale. Spesso montata come piastra di base sotto il telaio per proteggere le viti.",
                "open": "100% Legale.",
                "tuned": "100% Legale.",
                "street": "Ottima per montare pattini di scorrimento."
            }
        },
        {
            "id": "stay_15242_frp",
            "itemNumber": "15242",
            "name": "FRP Reinforcing Plate Set (Short)",
            "category": "plate",
            "chassisType": "universal",
            "price": 4.20,
            "description": "Set di 2 barrette diritte in fibra FRP corte forate passo standard. Indispensabili per irrigidire i montanti laterali dei mass damper, raccordare piastre o creare ponti di collegamento rigidi nei punti ad alta sollecitazione strutturale.",
            "specs": {
                "Materiale": "Fibra FRP (1.5 mm)",
                "Contenuto": "2 barrette corte forate + minuteria viti/dadi",
                "Posizione": "Rinforzo strutturale e tiranti"
            },
            "images": [
                "https://d7z22c0gz59ng.cloudfront.net/japan_contents/img/usr/item/1/15242/15242_1.jpg",
                "https://d7z22c0gz59ng.cloudfront.net/japan_contents/img/usr/item/1/15242/15242_s.jpg"
            ],
            "tamiyaUrl": "https://www.tamiya.com/japan/products/15242/index.html",
            "allowedCategories": ["bmax", "open", "tuned", "expert", "street"],
            "rulesNotes": {
                "bmax": "100% Legale. Ideale per unire lateralmente le colonne mass damper.",
                "open": "100% Legale.",
                "street": "100% Legale."
            }
        },
        {
            "id": "stay_95155_carbon",
            "itemNumber": "95155",
            "name": "HG Carbon Rear Brake Stay (1.5mm) J-Cup",
            "category": "plate",
            "chassisType": "universal",
            "price": 13.90,
            "description": "La piastra freno in pura fibra di carbonio HG più ambita nei paddock internazionali. Superficie ad ampia area per incollare le spugne freno senza flessioni su salti violenti, serigrafie ufficiali Tamiya J-Cup in tiratura limitata.",
            "specs": {
                "Materiale": "Fibra di Carbonio HG ad alto modulo (1.5 mm)",
                "Finitura": "Tessuto di carbonio satinato con grafiche J-Cup",
                "Funzione": "Supporto rigido spugne freno posteriore",
                "Compatibilità telai": "MA, MS, FM-A, AR, VZ, Super-II"
            },
            "images": [
                "https://d7z22c0gz59ng.cloudfront.net/japan_contents/img/usr/item/9/95155/95155_1.jpg",
                "https://d7z22c0gz59ng.cloudfront.net/japan_contents/img/usr/item/9/95155/95155_s.jpg"
            ],
            "tamiyaUrl": "https://www.tamiya.com/japan/products/95155/index.html",
            "allowedCategories": ["bmax", "open", "tuned", "street"],
            "rulesNotes": {
                "bmax": "100% Legale. La staffa freno definitiva per il posteriore.",
                "open": "100% Legale.",
                "tuned": "100% Legale.",
                "street": "100% Legale."
            }
        },
        {
            "id": "stay_15495_carbon",
            "itemNumber": "15495",
            "name": "HG Carbon Reinforcing Plate (1.5mm / Straight)",
            "category": "plate",
            "chassisType": "universal",
            "price": 10.90,
            "description": "Barretta diritta in fibra di carbonio HG rigida da 1.5mm. Con foratura standard passo 2mm su tutta la lunghezza, è la base universale per rinforzare paraurti, costruire ponti di irrigidimento e sostenere colonne di mass damper senza aggiunta di peso superfluo.",
            "specs": {
                "Materiale": "Fibra di Carbonio HG (1.5 mm)",
                "Lunghezza": "Formato diritto multi-foro",
                "Rigidità": "3 volte superiore alla comune fibra FRP"
            },
            "images": [
                "https://d7z22c0gz59ng.cloudfront.net/japan_contents/img/usr/item/1/15495/15495_1.jpg",
                "https://d7z22c0gz59ng.cloudfront.net/japan_contents/img/usr/item/1/15495/15495_s.jpg"
            ],
            "tamiyaUrl": "https://www.tamiya.com/japan/products/15495/index.html",
            "allowedCategories": ["bmax", "open", "tuned", "street"],
            "rulesNotes": {
                "bmax": "100% Legale. Perfetta come barra di irrigidimento centrale nel B-Max.",
                "open": "100% Legale. La materia prima più usata per tagliare bracci Chochin.",
                "tuned": "100% Legale."
            }
        },
        {
            "id": "stay_95153_carbon",
            "itemNumber": "95153",
            "name": "HG Carbon Front Stay for Fully Cowled (1.5mm) J-Cup",
            "category": "plate",
            "chassisType": "universal",
            "price": 13.50,
            "description": "La piastra anteriore da gara definitiva per telai B-Max. La sagomatura arcuata è appositamente studiata per montare rulli da 9mm, 13mm o 19mm a dima massima senza toccare le carrozzerie integrali (Fully Cowled), evitando tagli vietati dal regolamento.",
            "specs": {
                "Materiale": "Fibra di Carbonio HG (1.5 mm)",
                "Posizione": "Anteriore / Front Stay",
                "Rulli supportati": "9 mm, 13 mm, 19 mm",
                "Edizione": "Japan Cup Limited Edition con serigrafia dorata"
            },
            "images": [
                "https://d7z22c0gz59ng.cloudfront.net/japan_contents/img/usr/item/9/95153/95153_1.jpg",
                "https://d7z22c0gz59ng.cloudfront.net/japan_contents/img/usr/item/9/95153/95153_s.jpg"
            ],
            "tamiyaUrl": "https://www.tamiya.com/japan/products/95153/index.html",
            "allowedCategories": ["bmax", "open", "tuned", "street"],
            "rulesNotes": {
                "bmax": "100% Legale. La staffa anteriore più consigliata in assoluto per carrozzerie avvolgenti.",
                "open": "100% Legale.",
                "tuned": "100% Legale."
            }
        },

        # --- MASS DAMPERS ---
        {
            "id": "damp_15401",
            "itemNumber": "15401",
            "name": "Mass Damper Set (Heavy)",
            "category": "damper",
            "chassisType": "universal",
            "price": 5.80,
            "description": "Il set di zavorre smorzanti cilindriche fondamentali per l'assorbimento dell'energia cinetica verticale. Include pesi cilindrici pesanti in ottone tornito (6.8g e 3.6g) con colonnine filettate e dadi autobloccanti per atterraggi sicuri dopo salti da Table Top.",
            "specs": {
                "Materiale": "Ottone tornito lucido (Brass)",
                "Pesi inclusi": "2x pesi cilindrici pesanti 6.8g + 2x pesi intermedi 3.6g",
                "Montaggio": "Verticale con viti da 2mm e colonnine di scorrimento"
            },
            "images": [
                "https://d7z22c0gz59ng.cloudfront.net/japan_contents/img/usr/item/1/15401/15401_1.jpg",
                "https://d7z22c0gz59ng.cloudfront.net/japan_contents/img/usr/item/1/15401/15401_s.jpg"
            ],
            "tamiyaUrl": "https://www.tamiya.com/japan/products/15401/index.html",
            "allowedCategories": ["bmax", "open", "tuned", "expert", "street"],
            "rulesNotes": {
                "bmax": "100% Legale. Montaggio verticale conforme a dima.",
                "open": "100% Legale.",
                "tuned": "100% Legale.",
                "street": "100% Legale."
            }
        },
        {
            "id": "damp_15479",
            "itemNumber": "15479",
            "name": "Mass Damper Set w/ Ball Heads",
            "category": "damper",
            "chassisType": "universal",
            "price": 5.90,
            "description": "Set di pesi smorzatori con testa semisferica arrotondata. Il profilo a fungo/sfera abbassa ulteriormente il baricentro e minimizza il rischio che le zavorre si impuntino sulle protezioni della pista in caso di ribaltamento parziale o sbandata laterale.",
            "specs": {
                "Materiale": "Ottone ad alta densità",
                "Pesi": "2x pesi a fungo semisferici (circa 4.2g ciascuno)",
                "Colonnine guida": "Viti da 25mm e 30mm con dadi esagonali e boccole"
            },
            "images": [
                "https://d7z22c0gz59ng.cloudfront.net/japan_contents/img/usr/item/1/15479/15479_1.jpg",
                "https://d7z22c0gz59ng.cloudfront.net/japan_contents/img/usr/item/1/15479/15479_s.jpg"
            ],
            "tamiyaUrl": "https://www.tamiya.com/japan/products/15479/index.html",
            "allowedCategories": ["bmax", "open", "tuned", "expert", "street"],
            "rulesNotes": {
                "bmax": "100% Legale.",
                "open": "100% Legale.",
                "tuned": "100% Legale."
            }
        },
        {
            "id": "damp_15490",
            "itemNumber": "15490",
            "name": "MA Chassis Side Mass Damper Set",
            "category": "damper",
            "chassisType": "double",
            "price": 8.50,
            "description": "Set completo studiato appositamente per le paratie laterali dei telai MA. Include piastre in FRP sagomate su misura per i punti di fissaggio laterali MA, pesi smorzatori cilindrici e distanziali per stabilizzare il telaio sui salti della classe B-Max.",
            "specs": {
                "Compatibilità telaio": "Progettato per MA Chassis (adattabile anche su AR e VZ)",
                "Contenuto": "2 piastre FRP laterali sagomate, pesi cilindrici in ottone, boccole e minuteria",
                "Montaggio": "Laterale bolt-on a baricentro ribassato"
            },
            "images": [
                "https://d7z22c0gz59ng.cloudfront.net/japan_contents/img/usr/item/1/15490/15490_1.jpg",
                "https://d7z22c0gz59ng.cloudfront.net/japan_contents/img/usr/item/1/15490/15490_s.jpg"
            ],
            "tamiyaUrl": "https://www.tamiya.com/japan/products/15490/index.html",
            "allowedCategories": ["bmax", "open", "tuned", "street"],
            "rulesNotes": {
                "bmax": "100% Legale. Il kit dumper laterale ufficiale più venduto per telai MA.",
                "open": "100% Legale.",
                "tuned": "100% Legale."
            }
        },
        {
            "id": "damp_15449",
            "itemNumber": "15449",
            "name": "Mass Damper Block (6x6x32mm / 8.3g)",
            "category": "damper",
            "chassisType": "universal",
            "price": 5.50,
            "description": "Blocchetto smorzatore rettangolare monoblocco in ottone massiccio da 8.3 grammi. Montato trasversalmente sul paraurti posteriore o tra le colonnine centrali, offre uno smorzamento piatto ed estremamente bilanciato, azzerando i rimbalzi del treno posteriore.",
            "specs": {
                "Forma": "Parallelepipedo tornito 6 x 6 x 32 mm",
                "Peso": "8.3 grammi",
                "Fori guida": "2 fori verticali standard 2mm"
            },
            "images": [
                "https://d7z22c0gz59ng.cloudfront.net/japan_contents/img/usr/item/1/15449/15449_1.jpg",
                "https://d7z22c0gz59ng.cloudfront.net/japan_contents/img/usr/item/1/15449/15449_s.jpg"
            ],
            "tamiyaUrl": "https://www.tamiya.com/japan/products/15449/index.html",
            "allowedCategories": ["bmax", "open", "tuned", "street"],
            "rulesNotes": {
                "bmax": "100% Legale se montato orizzontalmente su staffa senza toccare terra.",
                "open": "100% Legale.",
                "tuned": "100% Legale."
            }
        },

        # --- RULLI & CUSCINETTI ---
        {
            "id": "roller_15403",
            "itemNumber": "15403",
            "name": "Double Aluminum Rollers (9-8mm)",
            "category": "roller",
            "chassisType": "universal",
            "price": 11.20,
            "description": "Doppi rulli integrati in alluminio di precisione 9-8mm con cuscinetto a sfere 520 centrale. Il rullo inferiore da 9mm guida l'auto sul dritto; quando l'auto si inclina in curva, il rullo superiore da 8mm tocca la sponda creando un forte effetto stabilizzante antiribaltamento.",
            "specs": {
                "Diametro inferiore": "9 mm",
                "Diametro superiore": "8 mm",
                "Cuscinetto": "520 Ball Bearing integrato",
                "Materiale": "Alluminio tornito anodizzato argento"
            },
            "images": [
                "https://d7z22c0gz59ng.cloudfront.net/japan_contents/img/usr/item/1/15403/15403_1.jpg",
                "https://d7z22c0gz59ng.cloudfront.net/japan_contents/img/usr/item/1/15403/15403_s.jpg"
            ],
            "tamiyaUrl": "https://www.tamiya.com/japan/products/15403/index.html",
            "allowedCategories": ["bmax", "open", "tuned", "expert", "street"],
            "rulesNotes": {
                "bmax": "100% Legale. Conta come 1 singolo punto di contatto per lato.",
                "open": "100% Legale.",
                "tuned": "100% Legale.",
                "expert": "Molto usato all'anteriore nelle curve strette a gomito."
            }
        },
        {
            "id": "roller_15529",
            "itemNumber": "15529",
            "name": "Low Friction Plastic Double Rollers (13-12mm)",
            "category": "roller",
            "chassisType": "universal",
            "price": 4.20,
            "description": "Doppi rulli ultraleggeri in speciale plastica tecnica POM a basso coefficiente d'attrito (Low Friction). Pesano circa la metà dei corrispettivi in alluminio, garantendo ottima scorrevolezza e un baricentro anteriore ridotto per categorie entry/mid level.",
            "specs": {
                "Diametro": "13 mm inferiore, 12 mm superiore",
                "Materiale": "Resina POM a basso attrito autolubrificante",
                "Colore": "Nero tecnico",
                "Bronzine": "Bronzine in ottone e tubetti di scorrimento inclusi"
            },
            "images": [
                "https://d7z22c0gz59ng.cloudfront.net/japan_contents/img/usr/item/1/15529/15529_1.jpg",
                "https://d7z22c0gz59ng.cloudfront.net/japan_contents/img/usr/item/1/15529/15529_s.jpg"
            ],
            "tamiyaUrl": "https://www.tamiya.com/japan/products/15529/index.html",
            "allowedCategories": ["bmax", "open", "tuned", "boxstock", "expert", "street"],
            "rulesNotes": {
                "bmax": "100% Legale. Alternativa economica e leggerissima ai rulli in alluminio.",
                "tuned": "100% Legale.",
                "street": "100% Legale."
            }
        },
        {
            "id": "roller_15426",
            "itemNumber": "15426",
            "name": "19mm Aluminum Rollers with Rubber Rings",
            "category": "roller",
            "chassisType": "universal",
            "price": 9.80,
            "description": "Coppia di rulli in alluminio da 19mm dotati di anello perimetrale in gomma ad alto grip. Utilizzati spesso in posizione superiore anteriore o posteriore per fungere da freno di sicurezza sulle pareti delle curve veloci paraboliche e corsie di cambio corsia (Lane Change).",
            "specs": {
                "Diametro": "19 mm",
                "Anello": "Gomma nitrilica ad alta aderenza (sostituibile)",
                "Cuscinetto": "520 Ball Bearing schermato incluso",
                "Funzione": "Freno sulle pareti esterne in curva"
            },
            "images": [
                "https://d7z22c0gz59ng.cloudfront.net/japan_contents/img/usr/item/1/15426/15426_1.jpg",
                "https://d7z22c0gz59ng.cloudfront.net/japan_contents/img/usr/item/1/15426/15426_s.jpg"
            ],
            "tamiyaUrl": "https://www.tamiya.com/japan/products/15426/index.html",
            "allowedCategories": ["bmax", "open", "tuned", "expert", "street"],
            "rulesNotes": {
                "bmax": "100% Legale. Ottimo stabilizzatore antiribaltamento per il Lane Change.",
                "open": "100% Legale.",
                "street": "100% Legale."
            }
        },
        {
            "id": "roller_95540",
            "itemNumber": "95540",
            "name": "HG Lightweight 13mm Aluminum Rollers (5-Spoke)",
            "category": "roller",
            "chassisType": "universal",
            "price": 12.90,
            "description": "I rulli da competizione da 13mm più leggeri prodotti da Tamiya. Il design a 5 razze sagomate al CNC riduce il peso rotante del 30% rispetto alla versione piena, offrendo una risposta immediata nei cambi di traiettoria delle chicane veloci.",
            "specs": {
                "Diametro": "13 mm esatto",
                "Design": "5 razze ultraleggere fresate CNC (5-Spoke)",
                "Bordo": "Profilo Ringless senza gommini",
                "Cuscinetto": "520 Ball Bearing ad alta precisione"
            },
            "images": [
                "https://d7z22c0gz59ng.cloudfront.net/japan_contents/img/usr/item/9/95540/95540_1.jpg",
                "https://d7z22c0gz59ng.cloudfront.net/japan_contents/img/usr/item/9/95540/95540_s.jpg"
            ],
            "tamiyaUrl": "https://www.tamiya.com/japan/products/95540/index.html",
            "allowedCategories": ["bmax", "open", "tuned", "expert", "street"],
            "rulesNotes": {
                "bmax": "100% Legale. La prima scelta dei campioni giapponesi e italiani al posteriore.",
                "open": "100% Legale.",
                "tuned": "100% Legale."
            }
        },
        {
            "id": "bear_15467",
            "itemNumber": "15467",
            "name": "HG 520 Ball Bearings (2 pcs)",
            "category": "roller",
            "chassisType": "universal",
            "price": 6.90,
            "description": "Micro-cuscinetti a sfere ad alta precisione da 5mm esterno x 2mm interno. Sono i cuscinetti di ricambio standard per tutti i rulli in alluminio Tamiya da 13mm, 17mm, 19mm e doppi rulli, ideali dopo sgrassaggio con oli leggeri sintetici.",
            "specs": {
                "Dimensioni": "Diametro esterno 5.0 mm, foro 2.0 mm, spessore 2.5 mm",
                "Contenuto": "2 microcuscinetti di precisione schermati"
            },
            "images": [
                "https://d7z22c0gz59ng.cloudfront.net/japan_contents/img/usr/item/1/15467/15467_1.jpg",
                "https://d7z22c0gz59ng.cloudfront.net/japan_contents/img/usr/item/1/15467/15467_s.jpg"
            ],
            "tamiyaUrl": "https://www.tamiya.com/japan/products/15467/index.html",
            "allowedCategories": ["bmax", "open", "tuned", "expert", "street"],
            "rulesNotes": {
                "bmax": "100% Legale. Ricambio fondamentale per rulli in alluminio.",
                "open": "100% Legale.",
                "expert": "100% Legale."
            }
        },
        {
            "id": "bear_15111",
            "itemNumber": "15111",
            "name": "Round Hole Ball Bearing Set (4 pcs)",
            "category": "roller",
            "chassisType": "universal",
            "price": 8.50,
            "description": "Set di 4 cuscinetti a sfere con foro rotondo (Round Hole) da 6x2mm per gli assali ruota dei telai Mini 4WD. Riduce drasticamente l'attrito volvente rispetto alle bronzine in plastica fornite nei kit di serie, aumentando la scorrevolezza complessiva dell'auto.",
            "specs": {
                "Diametro esterno": "6.0 mm",
                "Foro assale": "2.0 mm",
                "Contenuto": "4 cuscinetti a sfere per i 4 alloggiamenti assale del telaio"
            },
            "images": [
                "https://d7z22c0gz59ng.cloudfront.net/japan_contents/img/usr/item/1/15111/15111_1.jpg",
                "https://d7z22c0gz59ng.cloudfront.net/japan_contents/img/usr/item/1/15111/15111_s.jpg"
            ],
            "tamiyaUrl": "https://www.tamiya.com/japan/products/15111/index.html",
            "allowedCategories": ["bmax", "open", "tuned", "expert", "street"],
            "rulesNotes": {
                "bmax": "100% Legale. Upgrade basilare per qualsiasi vettura da gara.",
                "open": "100% Legale.",
                "tuned": "100% Legale.",
                "expert": "100% Legale."
            }
        },

        # --- RUOTE, GOMME & ASSALI ---
        {
            "id": "shaft_15417",
            "itemNumber": "15417",
            "name": "72mm Reinforced Shafts (Black / 4 pcs)",
            "category": "wheel",
            "chassisType": "universal",
            "price": 3.80,
            "description": "Assali ruota rinforzati da 72mm in acciaio speciale ad altissima resistenza con finitura brunita nera. Essenziali per la tecnica della 'foratura passante' dei cerchi ruota: impediscono ai cerchi di staccarsi o oscillare ad alte velocità.",
            "specs": {
                "Lunghezza": "72 mm (adatti a foratura passante)",
                "Diametro": "2.0 mm calibrato",
                "Materiale": "Acciaio speciale temprato ad alta tenacità",
                "Quantità": "4 assali rinforzati"
            },
            "images": [
                "https://d7z22c0gz59ng.cloudfront.net/japan_contents/img/usr/item/1/15417/15417_1.jpg",
                "https://d7z22c0gz59ng.cloudfront.net/japan_contents/img/usr/item/1/15417/15417_s.jpg"
            ],
            "tamiyaUrl": "https://www.tamiya.com/japan/products/15417/index.html",
            "allowedCategories": ["bmax", "open", "tuned", "expert", "street"],
            "rulesNotes": {
                "bmax": "100% Legale. La foratura passante dei cerchi è esplicitamente consentita nel B-Max.",
                "open": "100% Legale.",
                "tuned": "100% Legale.",
                "expert": "100% Legale."
            }
        },
        {
            "id": "shaft_15297",
            "itemNumber": "15297",
            "name": "60mm Hollow Stainless Steel Shafts (2 pcs)",
            "category": "wheel",
            "chassisType": "universal",
            "price": 3.50,
            "description": "Assali cavi alleggeriti in acciaio inossidabile da 60mm. Circa il 30% più leggeri degli assali pieni tradizionali, riducono il momento d'inerzia rotazionale delle masse non sospese per partenze fulminee nei circuiti tecnici.",
            "specs": {
                "Lunghezza": "60 mm standard",
                "Struttura": "Cava interna (Hollow Lightweight)",
                "Materiale": "Acciaio inossidabile SUS",
                "Quantità": "2 assali cavi"
            },
            "images": [
                "https://d7z22c0gz59ng.cloudfront.net/japan_contents/img/usr/item/1/15297/15297_1.jpg",
                "https://d7z22c0gz59ng.cloudfront.net/japan_contents/img/usr/item/1/15297/15297_s.jpg"
            ],
            "tamiyaUrl": "https://www.tamiya.com/japan/products/15297/index.html",
            "allowedCategories": ["bmax", "open", "tuned", "expert", "street"],
            "rulesNotes": {
                "bmax": "100% Legale.",
                "open": "100% Legale.",
                "tuned": "100% Legale."
            }
        },
        {
            "id": "wheel_95245",
            "itemNumber": "95245",
            "name": "Carbon Reinforced Large Dia. Wheels w/ Soft Tires",
            "category": "wheel",
            "chassisType": "universal",
            "price": 6.80,
            "description": "Cerchi a grande diametro da 31mm stampati in resina speciale caricata con fibra di carbonio. Estremamente rigidi, non si deformano sotto lo stress delle curve a 40 km/h, abbinati a gomme slick morbide ad alta aderenza per piste piatte e Street.",
            "specs": {
                "Diametro ruota": "31 mm (Large Diameter)",
                "Cerchio": "Nylon caricato con fibra di carbonio nero satinato",
                "Gomma": "Slick morbida ad alta trazione"
            },
            "images": [
                "https://d7z22c0gz59ng.cloudfront.net/japan_contents/img/usr/item/9/95245/95245_1.jpg",
                "https://d7z22c0gz59ng.cloudfront.net/japan_contents/img/usr/item/9/95245/95245_s.jpg"
            ],
            "tamiyaUrl": "https://www.tamiya.com/japan/products/95245/index.html",
            "allowedCategories": ["bmax", "open", "tuned", "expert", "street"],
            "rulesNotes": {
                "bmax": "100% Legale.",
                "open": "100% Legale.",
                "street": "Eccellente per ottenere luce da terra rialzata sui percorsi outdoor."
            }
        },
        {
            "id": "wheel_15512",
            "itemNumber": "15512",
            "name": "Hard Low-Profile Tire & Carbon Wheel Set (Y-Spoke)",
            "category": "wheel",
            "chassisType": "universal",
            "price": 6.50,
            "description": "Combinazione ideale per telai da competizione: cerchi a razze Y rinforzati al carbonio abbinati a gomme a profilo ribassato Hard. Gomme a bassa aderenza laterale che riducono il deceleramento durante il rotolamento sulle pareti delle curve.",
            "specs": {
                "Diametro totale": "26 mm (Low-Profile)",
                "Mescola gomma": "Hard (durezza elevata, rimbalzo ridotto)",
                "Cerchi": "Disegno Y-Spoke in resina caricata carbonio",
                "Colore cerchi/gomme": "Cerchi neri, gomme nere con scritta tampografata"
            },
            "images": [
                "https://d7z22c0gz59ng.cloudfront.net/japan_contents/img/usr/item/1/15512/15512_1.jpg",
                "https://d7z22c0gz59ng.cloudfront.net/japan_contents/img/usr/item/1/15512/15512_s.jpg"
            ],
            "tamiyaUrl": "https://www.tamiya.com/japan/products/15512/index.html",
            "allowedCategories": ["bmax", "open", "tuned", "street"],
            "rulesNotes": {
                "bmax": "100% Legale. La misura 26mm Low-Profile è il benchmark assoluto nel B-Max.",
                "open": "100% Legale.",
                "tuned": "100% Legale."
            }
        },

        # --- FRENI & SPUGNE ---
        {
            "id": "brake_15458",
            "itemNumber": "15458",
            "name": "Brake Set (for AR Chassis / Multi-Chassis)",
            "category": "brake",
            "chassisType": "universal",
            "price": 5.50,
            "description": "Kit freno modulare completo con slitta di scorrimento curva e piastra freno posteriore in plastica tecnica a basso attrito. Include spugne freno, viti e distanziali per regolare l'altezza del freno da terra a 1.0mm, 1.5mm o 2.0mm.",
            "specs": {
                "Compatibilità": "AR, MA, MS, VZ, FM-A",
                "Componenti": "Pattino anteriore anti-impuntamento, staffa freno posteriore regolabile, spugne frenanti",
                "Regolazione": "Altezza da 1.0 a 2.5 mm da terra"
            },
            "images": [
                "https://d7z22c0gz59ng.cloudfront.net/japan_contents/img/usr/item/1/15458/15458_1.jpg",
                "https://d7z22c0gz59ng.cloudfront.net/japan_contents/img/usr/item/1/15458/15458_s.jpg"
            ],
            "tamiyaUrl": "https://www.tamiya.com/japan/products/15458/index.html",
            "allowedCategories": ["bmax", "open", "tuned", "expert", "street"],
            "rulesNotes": {
                "bmax": "100% Legale.",
                "open": "100% Legale.",
                "tuned": "100% Legale."
            }
        },
        {
            "id": "brake_15492",
            "itemNumber": "15492",
            "name": "Brake Sponge Set (1/2/3mm Blue - High Friction)",
            "category": "brake",
            "chassisType": "universal",
            "price": 5.20,
            "description": "Fogli di spugna adesiva blu ad altissimo coefficiente d'attrito (frenata potente). Include 3 spessori calibrati (1mm, 2mm, 3mm) che consentono di dosare millimetricamente la forza frenante prima delle rampe di salto.",
            "specs": {
                "Contenuto": "1 foglio 1mm, 1 foglio 2mm, 1 foglio 3mm (50x50 mm cad.)",
                "Mescola": "Blu (Grip e attrito elevatissimi)",
                "Adesivo": "Biadesivo Tamiya a tenuta extra resistente"
            },
            "images": [
                "https://d7z22c0gz59ng.cloudfront.net/japan_contents/img/usr/item/1/15492/15492_1.jpg",
                "https://d7z22c0gz59ng.cloudfront.net/japan_contents/img/usr/item/1/15492/15492_s.jpg"
            ],
            "tamiyaUrl": "https://www.tamiya.com/japan/products/15492/index.html",
            "allowedCategories": ["bmax", "open", "tuned", "street"],
            "rulesNotes": {
                "bmax": "100% Legale. La spugna blu blocca all'istante l'auto se tocca la rampa.",
                "open": "100% Legale.",
                "tuned": "100% Legale."
            }
        },
        {
            "id": "tape_95682",
            "itemNumber": "95682",
            "name": "Mini 4WD Setting Tape (10mm / 15mm Width)",
            "category": "brake",
            "chassisType": "universal",
            "price": 5.50,
            "description": "Nastro adesivo telato tecnico ufficiale Tamiya. Utilizzato da tutti i campioni per mascherare le spugne freno e variarne l'attrito al millimetro, fissare saldamente le batterie al telaio e proteggere la fibra di carbonio dall'abrasione dell'asfalto.",
            "specs": {
                "Lunghezza rotolo": "15 metri",
                "Larghezza": "Altezza 10 mm e 15 mm",
                "Materiale": "Tessuto rinforzato privo di residui gommosi"
            },
            "images": [
                "https://d7z22c0gz59ng.cloudfront.net/japan_contents/img/usr/item/9/95682/95682_1.jpg",
                "https://d7z22c0gz59ng.cloudfront.net/japan_contents/img/usr/item/9/95682/95682_s.jpg"
            ],
            "tamiyaUrl": "https://www.tamiya.com/japan/products/95682/index.html",
            "allowedCategories": ["bmax", "open", "tuned", "expert", "street"],
            "rulesNotes": {
                "bmax": "100% Legale. Il nastro Tamiya originale è ammesso su tutto il telaio per fissare batterie o coprire freni.",
                "open": "100% Legale.",
                "street": "Fondamentale per sigillare il pozzetto ingranaggi da sabbia e polvere."
            }
        },

        # --- TRASMISSIONE & INGRANAGGI ---
        {
            "id": "gear_15432",
            "itemNumber": "15432",
            "name": "Super Speed EX Gear Set (3.7:1 for Super-II/VS/AR)",
            "category": "gear",
            "chassisType": "single",
            "price": 4.50,
            "description": "Rapporto di trasmissione 3.7:1 (Giallo/Azzurro) per telai a singolo albero. Il compromesso perfetto tra accelerazione e velocità di punta per circuiti tecnici ricchi di salti e ripartenze a bassa aderenza.",
            "specs": {
                "Rapporto di riduzione": "3.7:1 Super Speed EX",
                "Colorazione": "Ingranaggio contatore giallo, corona pignone azzurra",
                "Compatibilità": "Super-II, VS, AR, VZ Chassis"
            },
            "images": [
                "https://d7z22c0gz59ng.cloudfront.net/japan_contents/img/usr/item/1/15432/15432_1.jpg",
                "https://d7z22c0gz59ng.cloudfront.net/japan_contents/img/usr/item/1/15432/15432_s.jpg"
            ],
            "tamiyaUrl": "https://www.tamiya.com/japan/products/15432/index.html",
            "allowedCategories": ["bmax", "open", "tuned", "expert", "street"],
            "rulesNotes": {
                "bmax": "100% Legale. Ideale in combinazione con motori Dash su piste tecniche.",
                "open": "100% Legale.",
                "tuned": "100% Legale."
            }
        },
        {
            "id": "shaft_15390",
            "itemNumber": "15390",
            "name": "Fluorine Coated Gear Shafts (Straight / 2 pcs)",
            "category": "gear",
            "chassisType": "universal",
            "price": 3.20,
            "description": "Alberini in acciaio per l'ingranaggio contatore centrale rivestiti con trattamento al fluoro (Fluorine Coated). Il coefficiente d'attrito ultra-basso azzera la resistenza di rotazione dell'ingranaggio anche agli altissimi regimi di oltre 25.000 giri/min.",
            "specs": {
                "Trattamento superficiale": "Rivestimento chimico al fluoro a bassissimo attrito",
                "Diametro": "2.0 mm esatto di precisione",
                "Contenuto": "2 alberini diritti"
            },
            "images": [
                "https://d7z22c0gz59ng.cloudfront.net/japan_contents/img/usr/item/1/15390/15390_1.jpg",
                "https://d7z22c0gz59ng.cloudfront.net/japan_contents/img/usr/item/1/15390/15390_s.jpg"
            ],
            "tamiyaUrl": "https://www.tamiya.com/japan/products/15390/index.html",
            "allowedCategories": ["bmax", "open", "tuned", "expert", "street"],
            "rulesNotes": {
                "bmax": "100% Legale.",
                "open": "100% Legale.",
                "tuned": "100% Legale.",
                "expert": "Consigliatissimo nella classe Expert per azzerare gli attriti."
            }
        },
        {
            "id": "gear_15453",
            "itemNumber": "15453",
            "name": "Carbon Reinforced Gear Set (G13 & 8T Pinions)",
            "category": "gear",
            "chassisType": "universal",
            "price": 3.60,
            "description": "Set di pignoni motore da 8 denti e ingranaggi intermedi G13 stampati in speciale resina caricata al carbonio. Resistono all'usura estrema e non si sgranano sotto la violenta coppia motrice dei motori Dash e Power-Dash.",
            "specs": {
                "Materiale": "Resina nylon caricata con fibre di carbonio ad alta durezza",
                "Contenuto": "4 pignoni motore 8T + 2 ingranaggi corona G13"
            },
            "images": [
                "https://d7z22c0gz59ng.cloudfront.net/japan_contents/img/usr/item/1/15453/15453_1.jpg",
                "https://d7z22c0gz59ng.cloudfront.net/japan_contents/img/usr/item/1/15453/15453_s.jpg"
            ],
            "tamiyaUrl": "https://www.tamiya.com/japan/products/15453/index.html",
            "allowedCategories": ["bmax", "open", "tuned", "expert", "street"],
            "rulesNotes": {
                "bmax": "100% Legale. Evita che il pignone slitti sull'albero motore.",
                "open": "100% Legale.",
                "street": "100% Legale."
            }
        },
        {
            "id": "shaft_15531",
            "itemNumber": "15531",
            "name": "Hollow Propeller Shaft Set (for VZ Chassis)",
            "category": "gear",
            "chassisType": "single",
            "price": 3.80,
            "description": "Albero di rinvio della trazione cavo in acciaio inox specifico per la geometria del telaio VZ. Pesa solo la metà dell'albero di serie in ferro pieno, riducendo l'inerzia rotazionale e aumentando la reattività in frenata e accelerazione.",
            "specs": {
                "Compatibilità": "VZ Chassis specifico",
                "Materiale": "Tubo in acciaio inossidabile cavo con pignoni in resina termosaldata",
                "Peso": "Circa 0.55 grammi (-45% rispetto all'originale pieno)"
            },
            "images": [
                "https://d7z22c0gz59ng.cloudfront.net/japan_contents/img/usr/item/1/15531/15531_1.jpg",
                "https://d7z22c0gz59ng.cloudfront.net/japan_contents/img/usr/item/1/15531/15531_s.jpg"
            ],
            "tamiyaUrl": "https://www.tamiya.com/japan/products/15531/index.html",
            "allowedCategories": ["bmax", "open", "tuned", "street"],
            "rulesNotes": {
                "bmax": "100% Legale.",
                "open": "100% Legale.",
                "tuned": "100% Legale."
            }
        },
        {
            "id": "gear_15355",
            "itemNumber": "15355",
            "name": "High-Speed EX Counter Gear Set (3.7:1 for MS/MA PRO)",
            "category": "gear",
            "chassisType": "double",
            "price": 4.80,
            "description": "Set di ingranaggi contatori intermedi 3.7:1 dedicati alla trasmissione a doppio albero dei telai MS e MA Chassis. Fornisce maggiore coppia in salita rispetto al rapporto lungo 3.5:1 di serie, ottimale per motori Torque e Atomic nelle gare tecniche.",
            "specs": {
                "Rapporto": "3.7:1 High Speed EX",
                "Compatibilità": "MS Chassis, MA Chassis (Doppio pignone)",
                "Cuscinetti supportati": "Predisposto per alloggiare cuscinetto a sfere 520"
            },
            "images": [
                "https://d7z22c0gz59ng.cloudfront.net/japan_contents/img/usr/item/1/15355/15355_1.jpg",
                "https://d7z22c0gz59ng.cloudfront.net/japan_contents/img/usr/item/1/15355/15355_s.jpg"
            ],
            "tamiyaUrl": "https://www.tamiya.com/japan/products/15355/index.html",
            "allowedCategories": ["bmax", "open", "tuned", "street"],
            "rulesNotes": {
                "bmax": "100% Legale su telai MA/MS.",
                "open": "100% Legale.",
                "tuned": "100% Legale."
            }
        },

        # --- ACCESSORI & MINUTERIA ---
        {
            "id": "screw_15510",
            "itemNumber": "15510",
            "name": "Stainless Steel Countersunk Screws Set (10-30mm)",
            "category": "accessory",
            "chassisType": "universal",
            "price": 4.90,
            "description": "Viti svasate in acciaio inox a testa piatta. Permettono il montaggio a filo perfetto sul fondo del telaio e sotto le piastre freno/stay, eliminando le teste delle viti sporgenti che potrebbero grattare o impuntarsi sui bordi delle corsie.",
            "specs": {
                "Tipologia testa": "Svasata piana a filo (Countersunk)",
                "Lunghezze incluse": "10mm, 12mm, 20mm, 25mm, 30mm (2 pezzi cad.)",
                "Materiale": "Acciaio inossidabile SUS ad alta resistenza"
            },
            "images": [
                "https://d7z22c0gz59ng.cloudfront.net/japan_contents/img/usr/item/1/15510/15510_1.jpg",
                "https://d7z22c0gz59ng.cloudfront.net/japan_contents/img/usr/item/1/15510/15510_s.jpg"
            ],
            "tamiyaUrl": "https://www.tamiya.com/japan/products/15510/index.html",
            "allowedCategories": ["bmax", "open", "tuned", "expert", "street"],
            "rulesNotes": {
                "bmax": "100% Legale. La svasatura delle piastre in carbonio è consentita per montare queste viti a filo.",
                "open": "100% Legale.",
                "tuned": "100% Legale.",
                "expert": "100% Legale."
            }
        },
        {
            "id": "nut_15446",
            "itemNumber": "15446",
            "name": "2mm Aluminum Lock Nut Set (5 pcs - Red)",
            "category": "accessory",
            "chassisType": "universal",
            "price": 4.90,
            "description": "Dadi autobloccanti in alluminio ultraleggero anodizzato rosso con inserto filettato in nylon elastico. Non si allentano mai nemmeno dopo decine di giri di pista e violente vibrazioni sui salti, garantendo che le colonnine dei rulli rimangano salde.",
            "specs": {
                "Filettatura": "2.0 mm metrica",
                "Inserto": "Anello in nylon antiallentamento",
                "Materiale": "Alluminio aeronautico anodizzato rosso",
                "Quantità": "5 dadi autobloccanti"
            },
            "images": [
                "https://d7z22c0gz59ng.cloudfront.net/japan_contents/img/usr/item/1/15446/15446_1.jpg",
                "https://d7z22c0gz59ng.cloudfront.net/japan_contents/img/usr/item/1/15446/15446_s.jpg"
            ],
            "tamiyaUrl": "https://www.tamiya.com/japan/products/15446/index.html",
            "allowedCategories": ["bmax", "open", "tuned", "expert", "street"],
            "rulesNotes": {
                "bmax": "100% Legale. Obbligatori per fissare le colonnine dei rulli superiori.",
                "open": "100% Legale.",
                "tuned": "100% Legale.",
                "expert": "100% Legale."
            }
        },
        {
            "id": "ball_15383",
            "itemNumber": "15383",
            "name": "Mini 4WD F-1 Ball Cap / Stabilizer Ball Set",
            "category": "accessory",
            "chassisType": "universal",
            "price": 3.50,
            "description": "Testine e sfere stabilizzatrici in resina fluorescente/nera da avvitare sulla sommità delle colonnine dei rulli anteriori e posteriori. Evitano che la vettura rimanga agganciata con le viti nude alle paratie della pista in caso di sbandata laterale.",
            "specs": {
                "Materiale": "Resina tecnica ad alto scorrimento",
                "Contenuto": "Sfere tonde forate filettabili e terminali a cupola",
                "Funzione": "Anti-aggancio perimetrale alle paratie del circuito"
            },
            "images": [
                "https://d7z22c0gz59ng.cloudfront.net/japan_contents/img/usr/item/1/15383/15383_1.jpg",
                "https://d7z22c0gz59ng.cloudfront.net/japan_contents/img/usr/item/1/15383/15383_s.jpg"
            ],
            "tamiyaUrl": "https://www.tamiya.com/japan/products/15383/index.html",
            "allowedCategories": ["bmax", "open", "tuned", "expert", "street"],
            "rulesNotes": {
                "bmax": "100% Legale. Proteggono le mani dei giudici di gara e la carrozzeria.",
                "open": "100% Legale.",
                "tuned": "100% Legale."
            }
        },
        {
            "id": "tool_95604",
            "itemNumber": "95604",
            "name": "Aluminum Setting Board (Car Inspection Gauge)",
            "category": "accessory",
            "chassisType": "universal",
            "price": 19.90,
            "description": "La piastra di controllo ufficiale Tamiya in alluminio spazzolato con incisioni laser al decimo di millimetro. Permette al pilota di verificare la planarità del telaio, l'altezza da terra delle spugne freno (1mm), la larghezza totale massima (105mm) e la lunghezza massima (165mm) prima delle verifiche tecniche di gara.",
            "specs": {
                "Materiale": "Alluminio aeronautico anodizzato blu scuro con incisioni laser",
                "Dimensioni sagoma": "Dima ufficiale gara 165 mm x 105 mm",
                "Scale incise": "Righello millimetrato e indicatori luce a terra da 1 mm a 3 mm"
            },
            "images": [
                "https://d7z22c0gz59ng.cloudfront.net/japan_contents/img/usr/item/9/95604/95604_1.jpg",
                "https://d7z22c0gz59ng.cloudfront.net/japan_contents/img/usr/item/9/95604/95604_s.jpg"
            ],
            "tamiyaUrl": "https://www.tamiya.com/japan/products/95604/index.html",
            "allowedCategories": ["bmax", "open", "tuned", "boxstock", "expert", "street"],
            "rulesNotes": {
                "bmax": "Strumento indispensabile di paddock per le verifiche tecniche ufficiali.",
                "open": "Indispensabile per verificare l'ingombro massimo di 105mm.",
                "tuned": "Indispensabile per altezza minima da terra 1.0mm.",
                "expert": "Indispensabile per planarità assali e monobarra."
            }
        }
    ]

    added_count = 0
    for item in new_items:
        if item["itemNumber"] not in existing_nums:
            components.append(item)
            existing_nums.add(item["itemNumber"])
            added_count += 1
            print(f"[+] Aggiunto: #{item['itemNumber']} - {item['name']} ({item['category']})")
        else:
            print(f"[*] Gia presente: #{item['itemNumber']}")

    print(f"\n[*] Nuovi componenti aggiunti: {added_count}")
    print(f"[*] Totale componenti ora nel catalogo: {len(components)}")

    db["TAMIYA_COMPONENTS"] = components
    save_db(db)
    print("\n[V] Catalogo aggiornato e sincronizzato sia in data/tamiya_db.json sia in js/data.js!")

if __name__ == "__main__":
    run_update()
