# 🎮 Local-AI-RPG-Engine

## 📸 Screenshots

| Chat Interface            | Live Status                | Encounter System          |
|
| ![Chat](screenshot1.png) | ![Status](screenshot2.png) | ![Encounter](screenshot3.png) 
<img width="1100" height="700" alt="screenshot1" src="https://github.com/user-attachments/assets/3871dfd8-4889-431f-821f-c044ee01a775" />
<img width="1100" height="700" alt="screenshot2" src="https://github.com/user-attachments/assets/e33e034c-28ef-4aae-b44c-31d255337408" />
<img width="1100" height="700" alt="screenshot3" src="https://github.com/user-attachments/assets/31e35b77-b0ee-4a2f-8d28-452a65f112f5" />




**DE:** Kostenloses lokales AI-RPG, läuft auf 4GB VRAM Laptop.
**EN:** Free local AI-RPG, runs on 4GB VRAM Laptop. For more infos scroll down to **---- EN TRANSLATION---** (156)

> Kein API-Key. Keine Kosten. Keine Cloud. Läuft komplett auf deinem PC.

---

## ✨ Features

- 🧠 **19 aktive Systeme** die miteinander kommunizieren
- 💖 **Dynamisches Relationship System** — NPCs entwickeln sich
- 🕐 **Tageszeit-System** — NPCs reagieren auf Morgen/Abend/Nacht
- 🧬 **Memory System** — NPCs erinnern sich an vergangene Gespräche
- 💭 **Emotional Intelligence** — NPCs erkennen Emotionen
- 🔄 **Regenerate** — Antwort gefällt nicht? Neu generieren
- 💾 **Save/Load** — Spielstand wird gespeichert
- 🎭 **Encounter System** — Zufällige NPC-Begegnungen
- ⚔️ **Combat System** — Kampf & Training
- 👥 **Companion System** — NPCs begleiten dich
- 🔒 **Komplett lokal** — Keine Datenweitergabe

---

## 🖥️ Hardware Anforderungen

| Minimum | Empfohlen |
|---|---|
| 4GB VRAM | 6GB+ VRAM |
| 8GB RAM | 16GB RAM |
| CPU: i5 10th Gen | CPU: i5 12th Gen+ |

> ✅ Getestet auf: RTX 3050 Laptop (4GB), i5-12450H, 16GB RAM

---

## 🚀 Quick Setup

### 1. LM Studio installieren
Download: https://lmstudio.ai

### 2. Modell laden
Empfohlen für 4GB VRAM:
InferenceIllusionist/Meta-Llama-3.1-8B-Claude-iMat-GGUF
→ Datei: Q3_K_M (4.02GB)
Empfohlen für 6GB+ VRAM:
Mistral-7B-Instruct-v0.3 Q4_K_M

### 3. Repository klonen
```bash
git clone https://github.com/chilligconcarne98-spec/Local-AI-RPG-Engine
cd Local-AI-RPG-Engine
pip install -r requirements.txt
```

### 4. Starten
```bash
python main.py
```

---

## ⚙️ Eigenes Setting einrichten

### Charakter definieren
In `moduls/characters.py`:
```python
"dein_charakter": {
    "name": "Name",
    "personality": "Beschreibung",
    "relationship_to_player": "Mentor/Freund/etc"
}
```

### Spielregeln anpassen
In `gamerules.txt` — einfach Text bearbeiten,
keine Programmierkenntnisse nötig.

### Backstory anpassen
In `backstory.py` — deine eigene Geschichte.

---

## 🔧 Modell wechseln

In `main.py`:
```python
LM_STUDIO_MODEL = "dein-modell-name"
```
Fertig. Alle Systeme funktionieren mit jedem
OpenAI-kompatiblen Modell in LM Studio.

---

## PROJEKTSTRUKTUR
Local-AI-RPG-Engine/
├── main.py                    ← Hauptdatei
├── rpg_gui.py                 ← GUI
├── backstory.py               ← Deine Geschichte
├── gamerules.txt              ← Spielregeln
└── moduls/
├── maternal_system.py     ← Relationship Depth
├── advanced_memory_system.py
├── emotional_intelligence_engine.py
├── encounter_system.py
├── environment_system.py
├── companion_system.py
├── advanced_combat_system.py
├── game_time_system.py
├── family_time_system.py
├── secret_system.py
└── ...
---

## 💡 Tipps für beste Ergebnisse

- **Aktionen** in Sternchen schreiben: `*umarmt*`
- **Commands** mit `/help` erkunden
- **Tageszeit** beeinflusst NPC-Verhalten
- **Relationship Level** steigt durch positive Interaktionen
- Bei schlechter Antwort: **🔄 Neu** Button nutzen

---

## 🛠️ Bekannte Einschränkungen

- 4GB VRAM = Q3_K_M Modell empfohlen
- Erste Antwort kann 5-10 Sekunden dauern
- LM Studio muss im Hintergrund laufen

---

## 📜 License

MIT License — mach damit was du willst.

---

## 🙏 Credits

- [LM Studio](https://lmstudio.ai) — lokale LLM-Infrastruktur
- [CustomTkinter](https://github.com/TomSchimansky/CustomTkinter) — GUI
- [Meta LLaMA](https://llama.meta.com) — Basis-Modell

---

## ⭐ Wenn dir das Projekt gefällt

Gib einen Star auf GitHub —
das hilft anderen das Projekt zu finden! 🚀




**---- EN TRANSLATION---**

> No API-Key. No costs. No Cloud. Runs completely on your own PC.


## ✨ Features

- 🧠 **19 aktive Systems** that communicate with each other
- 💖 **Dynamic Relationship System** — NPCs evolve
- 🕐 **Tageszeit-System** — NPCs react on time: Morning/Evening/Night
- 🧬 **Memory System** — NPCs remember on conversations after a long time
- 💭 **Emotional Intelligence** — NPCs are noticing emotions
- 🔄 **Regenerate** — You don't like the answer? Regenerate a new one
- 💾 **Save/Load** — Your score will be saved
- 🎭 **Encounter System** — Random NPC encounters
- ⚔️ **Combat System** — Fight & Training
- 👥 **Companion System** — NPCs can join you for traveling/changing the location
- 🔒 **Completely local** — No data sharing
---

---

## 🖥️ Hardware Requirements

| Minimum | Recommended |
|---|---|
| 4GB VRAM | 6GB+ VRAM |
| 8GB RAM | 16GB RAM |
| CPU: i5 10th Gen | CPU: i5 12th Gen+ |

> ✅ Tested on: RTX 3050 Laptop (4GB), i5-12450H, 16GB RAM

---

---

## 🚀 Quick Setup

### 1. install LM Studio
Download: https://lmstudio.ai

### 2. Load Model:
recommended for 4GB VRAM:
InferenceIllusionist/Meta-Llama-3.1-8B-Claude-iMat-GGUF
→ File: Q3_K_M (4.02GB)
Recommended for 6GB+ VRAM:
Mistral-7B-Instruct-v0.3 Q4_K_M

### 3. clone repository
```bash
git clone https://github.com/chilligconcarne98-spec/Local-AI-RPG-Engine
cd Local-AI-RPG-Engine
pip install -r requirements.txt
```

### 4. Start
```bash
python main.py
```
---

## ⚙️ Setup own settings

### define your charactes
In `moduls/characters.py`:
```python
"your_character": {
    "name": "Name",
    "personality": "Description",
    "relationship_to_player": "Mentor/Friend/and so on"
}
```

### Customize gamerules
In `gamerules.txt` — just edit the text,
No programming knowledge required

### Customize backstory
In `backstory.py` — your own story

---

## 🔧Changing model
In `main.py`:
```python
LM_STUDIO_MODEL = "your-model-name"
```
Done. Alle systems work with every
OpenAI-compatible model in LM Studio.

---

## PROJECT STRUCTURE
Local-AI-RPG-Engine/
├── main.py                    ← main file
├── rpg_gui.py                 ← GUI
├── backstory.py               ← Your Story
├── gamerules.txt              ← Game rules
└── moduls/
├── maternal_system.py     ← Relationship Depth
├── advanced_memory_system.py
├── emotional_intelligence_engine.py
├── encounter_system.py
├── environment_system.py
├── companion_system.py
├── advanced_combat_system.py
├── game_time_system.py
├── family_time_system.py
├── secret_system.py
└── ...
---

## 💡 Tips for best results

- **Actions** write in */asterisks: `*hugs*`
- **Commands** explore with '/help'
- **Daytime** affects NPC behavior
- **Relationship Level** increases with positive interactions
- If you have a bad answer: use **🔄 Neu** Button 

---

## 🛠️ Known Limitations

- 4GB VRAM = Q3_K_M Model recommended
- First answer can take 10-20 seconds.
- LM Studio needs to run in the background.

---

## 📜 License

WITH License — do what you want with it.

---

## 🙏 Credits

- [LM Studio](https://lmstudio.ai) — local LLM-Infrastructure
- [CustomTkinter](https://github.com/TomSchimansky/CustomTkinter) — GUI
- [Meta LLaMA](https://llama.meta.com) — Base Model

---

## ⭐ If you like the project

Give a Star on GitHub —
this helps others to find the project! 🚀




