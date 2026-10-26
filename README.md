# TAMIYA MINI 4WD ITALIA - Configurator & Rules Engine

Piattaforma web pubblica interattiva per la configurazione, verifica di conformità tecnica e consultazione dei regolamenti ufficiali Mini 4WD Italia (B-Max GP, Open Class, Tuned / TMEC, Box Stock, Expert Classica R.U.M. e Street Mini 4WD).

---

## Architettura & Sicurezza

Il frontend del sito è **100% statico e pubblico**:
- **Nessuna gestione database o pannello admin esposto nel browser**.
- **Nessun override locale**: il catalogo viene servito direttamente da [`js/data.js`](file:///c:/Users/numot/OneDrive/Coding/progetti%20ai/mini4wd/js/data.js), generato e compilato a partire dal database sorgente [`data/tamiya_db.json`](file:///c:/Users/numot/OneDrive/Coding/progetti%20ai/mini4wd/data/tamiya_db.json).

---

## Gestione Database via Script CLI (`scripts/manage_db.py`)

Tutte le operazioni sul database vengono effettuate da riga di comando tramite Python. Ogni modifica aggiorna automaticamente [`data/tamiya_db.json`](file:///c:/Users/numot/OneDrive/Coding/progetti%20ai/mini4wd/data/tamiya_db.json) e ricompila [`js/data.js`](file:///c:/Users/numot/OneDrive/Coding/progetti%20ai/mini4wd/js/data.js).

### 1. Elencare i componenti del catalogo
```bash
# Tutti i componenti
python scripts/manage_db.py list

# Filtra per categoria (chassis, motor, plate, damper, roller, wheel, brake, gear, accessory)
python scripts/manage_db.py list --category motor

# Cerca per testo o item number
python scripts/manage_db.py list --search "Mach-Dash"
```

### 2. Aggiungere un nuovo componente Tamiya
```bash
# Modalità guidata interattiva
python scripts/manage_db.py add

# Oppure tramite argomenti
python scripts/manage_db.py add --item 15530 --name "HG Carbon Wide Rear Plate (1.5mm)" --category plate --chassis universal --price 11.90
```
> Lo script interroga automaticamente i server CDN Tamiya CloudFront per verificare la presenza dell'immagine ufficiale in alta risoluzione.

### 3. Rimuovere un componente
```bash
python scripts/manage_db.py remove 15530
```

### 4. Validare l'integrità del catalogo
```bash
python scripts/manage_db.py validate
```
Controlla:
- Univocità di ID e codici articolo Tamiya.
- Correttezza delle categorie e tipi di telaio.
- Integrità delle classi di omologazione e preset.

### 5. Compilare il database per il frontend
```bash
python scripts/manage_db.py build
```
Legge [`data/tamiya_db.json`](file:///c:/Users/numot/OneDrive/Coding/progetti%20ai/mini4wd/data/tamiya_db.json) e genera [`js/data.js`](file:///c:/Users/numot/OneDrive/Coding/progetti%20ai/mini4wd/js/data.js).

### 6. Sincronizzazione con le novità Tamiya Japan
```bash
python scripts/manage_db.py sync
# oppure
python scripts/sync_tamiya.py
```
Controlla il portale ufficiale Tamiya Japan Grade-Up Parts e rileva eventuali nuovi codici non ancora inseriti.
