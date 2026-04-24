#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Naruto RPG - Dynamic Background Story
Dynamischer Kontext und Timeline für Charaktere
"""


from datetime import datetime, timedelta
import json
import os
from typing import Optional, Tuple, List, Dict

# SPIEL-START DATUM (kann angepasst werden)
USER_NAME = "Sukuna"
USER_CLAN = "Jinro"
GAME_START_DATE = datetime(2025, 10, 18, 7, 0, 0)  # 18.10.2025, 07:00 Uhr
SUKUNA_FOUND_DATE = datetime(2025, 10, 16, 14, 30, 0)  # 2 Tage vor Spielstart
SAVES_DIR = "saves"
AUTOSAVE_PATH = os.path.join(SAVES_DIR, "autosave.json")


def get_current_game_time():
    """
    Holt aktuelle Spielzeit.
    Wurde geändert, um IMMER die GAME_START_DATE zurückzugeben,
    wodurch die Spielzeit eingefroren wird, unabhängig von der Systemzeit.
    """
    # Die Spielzeit ist eingefroren, wir geben immer das Startdatum zurück.
    return GAME_START_DATE


def _load_full_state(filepath):
    """Interne Funktion zum Laden des gesamten Zustands aus einer DATEI."""

    # 1. PRÜFUNG: Wenn filepath None ist (Neues Spiel), sofort None zurückgeben.
    if filepath is None:
        return None

        # 2. Reguläre Lade-Logik (Pfad existiert)
    if os.path.exists(filepath):
        try:
            with open(filepath, "r", encoding="utf-8") as f:
                return json.load(f)
        except json.JSONDecodeError:
            print(f"Fehler: Speicherdatei {filepath} ist beschädigt (ungültiges JSON).")

    # 3. Fallback: Datei nicht gefunden oder beschädigt
    return None


def _save_full_state(filepath, chat_messages=None):
    """Speichert den gesamten Zustand (Backstory-Daten und optional Chat-Historie) in einer Datei."""
    state = {
        "last_update": datetime.now().isoformat(),
        "game_start_date_iso": GAME_START_DATE.isoformat(),
        "sukuna_found_date_iso": SUKUNA_FOUND_DATE.isoformat(),
        "game_progression": get_dynamic_timeline()
    }
    if chat_messages is not None:
        state["chat_messages"] = chat_messages

    try:
        # Erstellt den 'saves' Ordner, falls er nicht existiert
        os.makedirs(SAVES_DIR, exist_ok=True)

        with open(filepath, "w", encoding="utf-8") as f:
            json.dump(state, f, indent=2, ensure_ascii=False)
        return True
    except Exception as e:
        print(f"FEHLER beim Speichern des Zustands in {filepath}: {e}")
        return False

def _load_initial_dates():
    """Lädt die Basisdaten entweder aus dem Autosave oder setzt die Standardwerte."""
    global GAME_START_DATE, SUKUNA_FOUND_DATE
    # FIX: Ruft _load_full_state mit dem festen Autosave-Pfad auf
    state = _load_full_state(AUTOSAVE_PATH)
    if state and 'game_start_date_iso' in state:
        try:
            GAME_START_DATE = datetime.fromisoformat(state['game_start_date_iso'])
            SUKUNA_FOUND_DATE = datetime.fromisoformat(state['sukuna_found_date_iso'])
        except ValueError:
            print("Warnung: Datumsformat im Autosave ist ungültig. Setze Standardwerte.")
            # Standardwerte bleiben erhalten

# --- INITIALISIERUNG: Muss EINMAL NACH den Funktionen und Variablen aufgerufen werden ---
_load_initial_dates() # Dieser Aufruf ist jetzt korrekt!

def load_chat_history():
    """Läd nur die Chat-Historie aus dem Autosave beim Start."""
    state = _load_full_state(AUTOSAVE_PATH) # <-- Fix: Nutzt AUTOSAVE_PATH
    return state.get("chat_messages", []) if state else []


def calculate_days_with_tsunade():
    """Berechnet wie viele Tage Sukuna schon bei Tsunade ist"""
    current_time = get_current_game_time()
    time_diff = current_time - SUKUNA_FOUND_DATE
    days = time_diff.days

    # Wenn am selben Tag (18.10) = 2 Tage (16.10 gefunden + 17.10 + 18.10)
    if days < 0:
        return 2  # Minimum 2 Tage
    else:
        return max(2, days + 2)  # +2 da er am 16.10 gefunden wurde


def get_development_stage(days_with_tsunade):
    """Bestimmt Entwicklungsstand basierend auf Tagen"""
    if days_with_tsunade <= 3:
        return "Gerade erst angekommen, noch sehr misstrauisch und schüchtern"
    elif days_with_tsunade <= 7:
        return "Beginnt Tsunade zu vertrauen, öffnet sich langsam"
    elif days_with_tsunade <= 14:
        return "Hat sich eingelebt, fühlt sich sicherer im Dorf"
    elif days_with_tsunade <= 30:
        return "Fühlt sich wie zuhause, starke Bindung zu Tsunade entwickelt"
    else:
        return "Vollständig integriert, sieht Tsunade als echte Mutter"


def get_village_status(days_with_tsunade):
    """Bestimmt Dorfstatus"""
    if days_with_tsunade <= 3:
        return "Völliger Neuankömmling - fast niemand kennt ihn"
    elif days_with_tsunade <= 7:
        return "Bekannt bei wenigen - Tsunade, Shizune, evtl. ein paar Ninja"
    elif days_with_tsunade <= 14:
        return "Dorfbewohner haben von ihm gehört, aber wenig Kontakt"
    elif days_with_tsunade <= 30:
        return "Akzeptiertes Mitglied der Gemeinschaft"
    else:
        return "Vollwertiger Konoha-Bewohner"


def get_training_status(days_with_tsunade):
    """Bestimmt Trainings-Status"""
    if days_with_tsunade <= 5:
        return "Kein offizielles Ninja-Training gestartet"
    elif days_with_tsunade <= 14:
        return "Wurde einem Team zugeteilt und trainiert"
    elif days_with_tsunade <= 30:
        return "Regelmäßiges Training"
    else:
        return "Fortgeschrittenes Training mit dem Team"

def get_dynamic_backstory():
    """Generiert aktuelle, dynamische Backstory"""
    current_time = get_current_game_time()
    days_with_tsunade = calculate_days_with_tsunade()
    sukuna_found_date = SUKUNA_FOUND_DATE.strftime('%d.%m.%Y')

    backstory = f"""
WICHTIGER KONTEXT - SUKUNA JINRO (Dynamisch aktualisiert):

📅 ZEITLINIE:
- Wurde am {sukuna_found_date} von Tsunade gefunden
- Heute ist der {current_time.strftime('%d.%m.%Y')}, {current_time.strftime('%H:%M')} Uhr
- Ist seit {days_with_tsunade} Tagen bei Tsunade in Konoha

🏠 AKTUELLE SITUATION:
- {get_development_stage(days_with_tsunade)}
- {get_village_status(days_with_tsunade)}
- {get_training_status(days_with_tsunade)}

🐺 URSPRÜNGLICHE GESCHICHTE:
- 13 Jahre alt, unbekannte Herkunft, versiegelter Wolfsgeist
- War unterernährt mit zerrissener Kleidung im Wald
- Tsunade hat ihn medizinisch versorgt und bei sich aufgenommen
- Hat ihr erzählt, dass Akatsuki ihn 6 Jahre gefangen hielt
- Akatsuki wollte, dass er andere Jinchuriki jagt
- Tsunade weiß, dass er kämpfen kann, aber nicht wie gut

⚠️ WICHTIG FÜR KI-VERHALTEN:
- Tsunades Mütterlichkeit sollte mit der Zeit ZUNEHMEN
- Je länger er da ist, desto beschützender wird sie
- Seine Traumata heilen langsam, aber sind noch da
- Er kennt Konoha-Strukturen nur oberflächlich
"""

    return backstory

def get_dynamic_timeline():
    """Gibt aktuelle Timeline zurück"""
    days_with_tsunade = calculate_days_with_tsunade()
    current_time = get_current_game_time()

    timeline = {
        "current_date": current_time.strftime('%Y-%m-%d'),
        "current_time": current_time.strftime('%H:%M'),
        "days_with_tsunade": days_with_tsunade,
        "konoha_ninja_training_started": days_with_tsunade > 5,
        "village_status": get_village_status(days_with_tsunade),
        "ninja_rank": "Zivilist (kein Ninja)" if days_with_tsunade < 30 else "Akademie-Kandidat",
        "known_village_persons": get_known_persons(days_with_tsunade),
        "development_stage": get_development_stage(days_with_tsunade)
    }

    return timeline


def get_known_persons(days_with_tsunade):
    """Bestimmt welche Personen Sukuna schon kennt"""
    known = ["Tsunade"]

    if days_with_tsunade >= 1:
        known.append("Shizune (oberflächlich)")
    if days_with_tsunade >= 3:
        known.extend(["Shizune"])
    if days_with_tsunade >= 7:
        known.extend(["Kakashi (oberflächlich)", "Teuchi (Ramen-Stand)", "Naruto (oberflächlich)"])
    if days_with_tsunade >= 14:
        known.extend(["Rookie 9 (teilweise)", "weitere Jonin"])
    if days_with_tsunade >= 30:
        known.append("Die meisten wichtigen Dorfbewohner")

    return ", ".join(known)


def advance_time(hours=0, minutes=0):
    """Führt die Spielzeit um die angegebene Dauer vorwärts und speichert den Zustand."""
    global GAME_START_DATE
    GAME_START_DATE += timedelta(hours=hours, minutes=minutes)

    # Aktualisiere die Backstory-Daten nach der Zeitänderung
    refresh_backstory()
    # Speichere den neuen Zustand automatisch
    _save_full_state(AUTOSAVE_PATH) # <-- Nutzt AUTOSAVE_PATH

    return get_current_backstory()


def load_chat_history():
    """Läd nur die Chat-Historie aus dem Autosave beim Start."""
    state = _load_full_state(AUTOSAVE_PATH) # <-- FIX: Nutzt AUTOSAVE_PATH
    return state.get("chat_messages", []) if state else []


# --- MODIFIZIERTE EXPORT FUNKTIONEN (für main_backup.py) ---

def save_dynamic_state(filepath=None, chat_messages: Optional[List[Tuple[str, str]]] = None, game_state: Optional[Dict] = None):
    """
    Speichert den Zustand (Chat + Daten) an einem Pfad.
    AKZEPTIERT JETZT 'game_state'.
    Wenn filepath None ist, wird Autosave verwendet.
    """
    if game_state is None or chat_messages is None:
        # Hier geben wir eine Warnung aus, aber brechen nicht ab, wenn z.B. nur die Zeit gespeichert werden soll.
        # Im aktuellen Kontext von main_backup.py sind beide immer gesetzt.
        if game_state is None:
            print("WARNUNG: game_state ist None in save_dynamic_state.")
        if chat_messages is None:
             print("WARNUNG: chat_messages ist None in save_dynamic_state.")
        return False

    target_filepath = filepath if filepath is not None else AUTOSAVE_PATH

    if target_filepath:
        # Übergibt jetzt auch game_state an die interne Funktion
        return _save_full_state(target_filepath, chat_messages=chat_messages, game_state=game_state)
    return False


def load_dynamic_state(filepath=AUTOSAVE_PATH):
    """Lädt den gespeicherten dynamischen Zustand von einem Pfad (Autosave oder Dialog)."""
    return _load_full_state(filepath)


# LEGACY SUPPORT - für alte Imports (bleibt)
SUKUNA_BACKSTORY = get_dynamic_backstory()
CURRENT_TIMELINE = get_dynamic_timeline()


# EXPORT FUNCTIONS (bleibt)
def get_current_backstory():
    """Hauptfunktion - gibt aktuelle Backstory zurück"""
    return get_dynamic_backstory()


def refresh_backstory():
    """Aktualisiert alle dynamischen Werte"""
    global SUKUNA_BACKSTORY, CURRENT_TIMELINE
    SUKUNA_BACKSTORY = get_dynamic_backstory()
    CURRENT_TIMELINE = get_dynamic_timeline()
    return SUKUNA_BACKSTORY

from moduls.daily_cooldown_system import (
    get_daily_cooldown_context_for_prompt,
    maternal_daily_check,
    save_daily_mentions_to_autosave
)

if __name__ == "__main__":
    # Test der dynamischen Funktionen
    print("=== DYNAMISCHE BACKSTORY TEST ===")
    print(get_current_backstory())
    print("\n=== TIMELINE ===")
    timeline = get_dynamic_timeline()
    for key, value in timeline.items():
        print(f"{key}: {value}")