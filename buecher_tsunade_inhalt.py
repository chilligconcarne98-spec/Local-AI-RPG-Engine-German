#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
buecher_tsunade_inhalt.py
Inhalte für Tsunades Privatbibliothek - Einfach erweiterbar
"""

# =============================================================================
# TSUNADES PRIVATBIBLIOTHEK
# =============================================================================

TSUNADES_BIBLIOTHEK = {
    "location_name": "Tsunades Privatbibliothek",
    "description": "Eine exklusive Sammlung medizinischer, politischer und persönlicher Bücher",
    "access_level": "private",
    "books": {

        # ===== GESETZBUCH =====
        "gesetzbuch_konoha": {
            "title": "Gesetzbuch von Konohagakure",
            "author": "Hokage-Verwaltung",
            "location": "Tsunades Arbeitszimmer",
            "type": "gesetz",
            "access_required": "tsunade_permission",
            "reading_time_minutes": 45,
            "chapters": {
                "1": {
                    "title": "Wille des Feuers",
                    "content": """Der Wille des Feuers bildet das Fundament unseres Dorfes. Er besagt, dass jeder Bewohner von Konohagakure Teil einer großen Familie ist. Wie die Blätter eines Baumes schützen wir uns gegenseitig und sorgen dafür, dass neue Generationen wachsen können.

**GRUNDPRINZIPIEN:**
1. **Schutz der Schwächeren** - Die Starken beschützen die Schwachen
2. **Opferbereitschaft für das Gemeinwohl** - Das Dorf steht über dem Einzelnen
3. **Weitergabe von Wissen und Werten** - Jede Generation lehrt die nächste
4. **Einheit trotz Unterschiede** - Verschiedene Clans, ein Dorf

**DAS BERÜHMTE ZITAT:**
'Wo Blätter tanzen, da lodert das Feuer. Das Feuer wird die Schatten des Dorfes erleuchten und neue Blätter sprießen lassen.' - Dritter Hokage

**BEDEUTUNG FÜR SUKUNA:**
Als Adoptivkind von Tsunade bist du ein lebendiges Beispiel für den Willen des Feuers. Konoha hat dich aufgenommen, obwohl du nicht hier geboren wurdest. Dies zeigt, dass Familie nicht nur durch Blut, sondern durch Herz und Loyalität definiert wird.

**MODERNE ANWENDUNG:**
- Schutz von Zivilisten hat höchste Priorität
- Ninja opfern sich für ihre Kameraden
- Wissen wird frei geteilt (außer Staatsgeheimnisse)
- Clans arbeiten zusammen statt gegeneinander""",
                    "knowledge_gain": {"village_history": 15, "leadership": 10, "moral_philosophy": 10}
                },
                "2": {
                    "title": "Shinobi-Regeln und Hierarchie",
                    "content": """Die Hierarchie in Konohagakure basiert auf Können, Erfahrung und Vertrauen:

**NINJA-RÄNGE:**
- **Hokage:** Dorfoberhaupt, höchste Autorität, gewählt durch Vertrauen
- **Jounin:** Elite-Ninja, Teamleiter, Missionsführer
- **Chuunin:** Erfahrene Ninja, mittlere Führungsebene, Prüfungsleiter
- **Genin:** Anfänger-Ninja, arbeiten in Dreierteams unter Jounin-Führung
- **Akademie-Schüler:** Ninja in Ausbildung, noch keine offiziellen Ninja

**SPEZIALRÄNGE:**
- **ANBU:** Elite-Geheimdienst, direkt dem Hokage unterstellt
- **Medizin-Ninja:** Spezialisierte Heiler, in jedem Team erforderlich
- **Sensor-Ninja:** Aufklärung und Spurenverfolgung
- **Folter & Verhör:** Spezialabteilung für Informationsbeschaffung

**GRUNDREGELN FÜR ALLE NINJA:**
1. **Mission geht vor persönliche Gefühle** - Emotionen dürfen Urteilsvermögen nicht trüben
2. **Niemals einen Gefährten zurücklassen** - Ein Team steht zusammen
3. **Dorfgeheimnisse sind absolute Priorität** - Staatsgeheimnisse mit dem Leben schützen
4. **Respekt vor Vorgesetzten und Älteren** - Hierarchie gewährleistet Ordnung
5. **Kontinuierliches Training und Verbesserung** - Stillstand bedeutet Rückschritt

**BESONDERE BESTIMMUNGEN FÜR SUKUNA:**
Als Schützling der Hokage unterstehst du direkt ihrer Autorität. Du hast Zugang zu Informationen und Ressourcen, die normale Genin nicht haben, trägst aber auch größere Verantwortung.""",
                    "knowledge_gain": {"ninja_rules": 20, "hierarchy": 15, "responsibility": 10}
                },
                "3": {
                    "title": "Hokage-Anordnungen",
                    "content": """Aktuelle Direktiven der Fünften Hokage Tsunade Senju:

**SICHERHEITSBESTIMMUNGEN:**
- **Verstärkte Patrouillen:** Alle Dorfgrenzen werden rund um die Uhr überwacht
- **Chakra-Kontrolltests:** Obligatorisch für alle Genin, vierteljährlich
- **Medizinische Ausrüstung:** Jedes Team muss verbesserte Erste-Hilfe-Sets führen
- **Kommunikationsprotokolle:** Neue verschlüsselte Codes alle 30 Tage

**AUSBILDUNGSREFORMEN:**
- **Medizinisches Ninjutsu:** Jeder Ninja muss Grundlagen beherrschen
- **Clan-Kooperation:** Monatliche Übungen zwischen verschiedenen Clans
- **Mentorenprogramm:** Erfahrene Jounin betreuen persönlich junge Talente
- **Psychologische Betreuung:** Traumabewältigung nach schweren Missionen

**SPEZIALANWEISUNGEN:**
- **Auslandsmissionen:** Erhöhte Vorsicht, besonders im Erdreich und Windreich
- **Chakra-Anomalien:** Sofortige Meldung ungewöhnlicher Energiephänomene
- **Jinchuriki-Schutz:** Höchste Priorität, spezielle Schutzprotokolle aktiv
- **Akatsuki-Bedrohung:** Alle Ninja sind über die Gefahr informiert

**PERSÖNLICHE NOTIZ VON TSUNADE:**
'Diese Regeln sind nicht nur Worte auf Papier. Sie sind mit dem Blut unserer Vorfahren geschrieben und mit den Tränen unserer Gefallenen besiegelt. Respektiert sie, lebt nach ihnen, und Konoha wird stark bleiben.'

**GEHEIME ZUSÄTZE (nur für Sukuna sichtbar):**
- Du hast Zugang zu Tsunades Privatbibliothek
- Bei Gefahr kannst du direkt zu Tsunade gehen
- Spezielle Trainingsressourcen stehen dir zur Verfügung""",
                    "knowledge_gain": {"current_events": 25, "security": 15, "special_privileges": 20}
                }
            }
        },
        # =======GARTENBUCH =====

"gartenbuecher": {
            "title": "Bonsai und Heilkräuterzucht: Ein Jōnin-Leitfaden",
            "author": "Inoichi Yamanaka",
            "location": "Balkon, wetterfest",
            "type": "alltag_garten",
            "access_required": "none",
            "reading_time_minutes": 55,
            "chapters": {
                "1": {
                    "title": "Grundlagen der Chakra-Düngung",
                    "content": "Anleitungen zur Pflege von Heilkräutern mit Chakra. Eine sanfte, auf die Erde fokussierte Chakra-Freisetzung fördert die Wurzelentwicklung (Muladhara-Chakra-Fokus). Tsunade nutzt es, um die Kräuter für ihre Medizin in ihrem Balkon zu züchten.",
                    "knowledge_gain": {"botany": 15, "medical_supplies": 10}
                },
                "2": {
                    "title": "Kultivierung seltener Heilkräuter",
                    "content": """**FORTSCHRITTLICHE TECHNIKEN**
Medizinische Ninja können ihr **Grünes Chakra** nutzen, um die Zellteilung seltener Heilpflanzen (z. B. der Aconitum-Klasse) um bis zu 400% zu beschleunigen.
- **Voraussetzung:** Präzise Chakra-Kontrolle, um die Pflanze nicht zu verbrennen.
- **Ziel:** Zucht von hochkonzentrierten **Phytopharmaka** für Antidote und Wundheilmittel. Der Prozess erfordert ständige Überwachung durch einen Medizin-Ninja.""",
                    "knowledge_gain": {"advanced_botany": 25, "chakra_application": 15}
                }
            }
        },
        # =======KOCHBUCH =========
"Kochbuch": {
            "title": "100 schnelle Mahlzeiten für vielbeschäftigte Shinobi",
            "author": "Akademie Koch-AG",
            "location": "Küchenschrank, unbenutzt",
            "type": "alltag_kochen",
            "access_required": "none",
            "reading_time_minutes": 35,
            "condition": "wie_neu",
            "chapters": {
                "1": {
                    "title": "Wie man Reis kocht (Anfänger-Level)",
                    "content": "Einfachste Anweisungen für Notfälle. Seit Jahren von Tsunade ignoriert, da sie sich lieber von Instant-Ramen oder Shizune versorgen lässt. Es werden **Vollkornreissorten** empfohlen, um die Chakra-Reserven optimal aufzufüllen.",
                    "knowledge_gain": {"cooking": 1}
                },
                "2": {
                    "title": "Die Überlebensration: Notfall-Pillen",
                    "content": """**HYOROUGAN, KIKATSUGAN, SUIKATSUGAN**
Ninja nutzen spezielle Rationspillen für Missionen, um leicht, geruchlos und lange kampfbereit zu bleiben.
- **Hyorougan (Energie):** Hergestellt aus Reis und Samen. Bietet einen schnellen Energieschub.
- **Kikatsugan (Sättigung):** Karotten und Reis, oft in Sake eingelegt. Wird bei starkem Hunger verwendet, um das Verlangen zu unterdrücken.
- **Suikatsugan (Hydrierung):** Eingelegte Ume-Pflaumen und andere saure Früchte. Lindert extremen Durst und neutralisiert Magenprobleme.""",
                    "knowledge_gain": {"survival_nutrition": 15, "foraging": 5}
                },
                "3": {
                    "title": "Geruchlose Küche für Stealth-Missionen",
                    "content": "Essen Sie **dunkle Lebensmittel** (schwarzer Sesam, brauner Reis) und **Wurzelgemüse** (Ingwer, Karotten). Vermeiden Sie Fleisch, Zwiebeln, Knoblauch und alle stark riechenden Speisen, um bei Infiltrationsmissionen geruchlos zu bleiben und die Sinne nicht zu trüben.",
                    "knowledge_gain": {"shinobi_diet": 10}
                }
            }
        },

        # ===== MITOS FUINJUTSU-NOTIZEN =====
        "mito_fuinjutsu_notizen": {
            "title": "Mito Uzumakis Fuinjutsu Notizen",
            "author": "Mito Uzumaki",
            "location": "Tsunades Arbeitszimmer",
            "type": "jutsu_anleitung",
            "access_required": "uzumaki_bloodline",
            "reading_time_minutes": 90,
            "danger_level": "hoch",
            "chapters": {
                "1": {
                    "title": "Chakra-Bindungstechniken",
                    "content": """Das Vier-Symbole-Siegel (Shisho Fuin) bildet das Fundament aller komplexen Bindungen. Die vier Symbole repräsentieren die Grundelemente des Chakras - nicht die klassischen Elemente, sondern:

**DIE VIER GRUNDSÄULEN:**
1. **KÖRPER (Tai) 体** - Physische Verankerung im Fleisch
2. **GEIST (Shin) 心** - Mentale Kontrolle über die Energie  
3. **SEELE (Kon) 魂** - Spirituelle Verbindung zur Chakra-Quelle
4. **WILLE (Ishi) 意志** - Bestimmung und absolute Kontrolle

**SCHICHTAUFBAU EINES SIEGELS:**
Erste Schicht: **Physische Bindung** - verankert das Siegel im Körper des Anwenders
Zweite Schicht: **Mentale Barriere** - verhindert geistige Beeinflussung durch versiegelte Energien
Dritte Schicht: **Spiritueller Filter** - trennt fremde Chakra-Signaturen vom eigenen Chakra-System
Vierte Schicht: **Willenskraft-Verstärkung** - stärkt die Kontrolle des Anwenders über das Siegel

**⚠️ KRITISCHE WARNUNG:**
Bei der Kombination mehrerer Siegel ist die Reihenfolge entscheidend:
1. Grundsiegel zuerst
2. Dann Verstärkungssiegel  
3. Zuletzt Schutzsiegel
Ein falscher Aufbau kann zur tödlichen Chakra-Explosion führen!

**FORTGESCHRITTENE TECHNIKEN:**
- **Kettensiegeltechnik:** Mehrere Siegel stabilisieren sich gegenseitig
- **Resonanzsiegel:** Harmonieren mit dem natürlichen Chakra-Fluss
- **Adaptionssiegel:** Passen sich automatisch an veränderte Umstände an

**PERSÖNLICHE NOTIZ VON MITO:**
'Sukuna, wenn du diese Zeilen liest, fließt unser Blut in deinen Adern. Die Uzumaki waren immer Brückenbauer zwischen den Welten. Nutze diese Kraft weise.'""",
                    "knowledge_gain": {"fuinjutsu": 30, "chakra_control": 20, "uzumaki_heritage": 15},
                    "requirements": {"uzumaki_bloodline": True, "chakra_control": 50}
                },
                "2": {
                    "title": "Bijuu-Versiegelung",
                    "content": """Der Neunschwänzige ist kein gewöhnliches Chakra-Konstrukt. Er ist eine Naturgewalt, älter als die Zivilisation selbst. Seine Versiegelung erfordert nicht nur Technik, sondern Verständnis für seine wahre Natur.

**DAS ACHT-TRIGRAMME-SIEGEL (Hakke no Fuin Shiki):**
Das ultimative Versiegelungsjutsu der Uzumaki, entwickelt über Generationen.

**AUFBAU:**
- **Acht konzentrische Kreise** mit spezifischen Hakke-Symbolen
- **Primärfunktion:** Vollständige Isolation der Bijuu-Chakra vom Wirt-System
- **Energiefluss:** Kontrollierte Chakra-Abgabe nur bei extremer emotionaler Belastung
- **Notfall-Modi:** Automatische Anpassung bei Lebensgefahr

**SICHERHEITSMECHANISMEN:**
1. **Emotionale Dämpfer** - reduzieren negative Gefühle, die das Siegel schwächen
2. **Chakra-Umleitung** - bei Siegelschwächung wird überschüssiges Chakra in harmlose Bahnen geleitet
3. **Notfall-Verstärkung** - automatische Siegelreparatur bei kritischen Schäden
4. **Bewusstseinspuffer** - verhindert direkte mentale Kommunikation mit dem Bijuu

**DIE DREI PHASEN DER BIJUU-INTEGRATION:**
**Phase 1 - Isolation (Monate 1-6):** Komplette Trennung zwischen Wirt und Bijuu
**Phase 2 - Kontrollierte Kommunikation (Jahre 1-5):** Begrenzte geistige Verbindung
**Phase 3 - Harmonische Koexistenz (lebenslang):** Gegenseitiger Respekt und Zusammenarbeit

**MITOS WEISHEIT:**
'Das Geheimnis liegt nicht in der Unterdrückung, sondern in der Koexistenz. Der Kyuubi darf niemals das Gefühl bekommen, komplett gefangen zu sein - das würde nur seinen Hass verstärken.'

'Der Jinchuriki darf niemals vergessen, dass er mit einem Lebewesen verbunden ist, nicht nur mit einer Energiequelle. Respekt ist der Schlüssel zur wahren Kontrolle.'

**GEHEIME TECHNIKEN (nur für Uzumaki):**
- **Chakraketten-Bindung:** Physische Manifestation von Chakra als Ketten
- **Seelen-Resonanz:** Direkte Kommunikation mit dem Bijuu
- **Energietransfer:** Chakra zwischen Wirt und Bijuu austauschen""",
                    "knowledge_gain": {"bijuu_knowledge": 50, "jinchuriki_understanding": 40, "advanced_fuinjutsu": 35},
                    "requirements": {"fuinjutsu": 100, "mental_strength": 80}
                },
                "3": {
                    "title": "Heilungssiegel - Die Uzumaki Tradition",
                    "content": """Unser Clan ist für seine außergewöhnliche Langlebigkeit bekannt - das kommt nicht von ungefähr. Diese Siegel verstärken unsere natürliche Regenerationsfähigkeit um das Zehnfache.

**VITALITÄTS-ERHALTUNGSSIEGEL (Seimei Hozon no Jutsu):**
Das Kronjuwel der Uzumaki-Heilungskunst.

**STRUKTUR:**
- **Kernsiegel auf dem Herz** - reguliert die zentrale Chakra-Zirkulation
- **Nebensiegel an Chakra-Punkten** - verstärken lokale Heilungsprozesse
- **Verbindungslinien** - unsichtbare Chakra-Bahnen zwischen allen Siegeln
- **Backup-Systeme** - Redundante Sicherungen für kritische Organe

**REGENERATIONSMECHANISMEN:**
1. **Zellerneuerung:** Beschleunigt natürliche Heilung um 500%
2. **Chakra-Recycling:** Wandelt verbrauchtes Chakra in Heilungsenergie um
3. **Immunsystem-Verstärkung:** Schützt vor Krankheiten und den meisten Giften
4. **Altersverlangsamung:** Verlangsamt den natürlichen Alterungsprozess

**WUNDEN-VERSCHLIEßUNGSSIEGEL (Kizu Fuusa no Jutsu):**
Für den Kampf entwickelt - kann lebendsbedrohliche Verletzungen in Sekunden stabilisieren.

**NOTFALL-FUNKTIONEN:**
- **Sofortversiegelung:** Stoppt Blutungen augenblicklich
- **Schmerzunterdrückung:** Reduziert Schmerzsignale um 80%
- **Temporäre Organfunktion:** Ersetzt kurzfristig beschädigte Organe
- **Adrenalin-Boost:** Erhält Kampffähigkeit trotz schwerer Verletzungen

**⚠️ KRITISCHE WARNUNG - NEBENWIRKUNGEN:**
Übermäßige Nutzung der Heilungssiegel verkürzt die natürliche Lebensspanne. Die Energie muss irgendwoher kommen - meist aus der eigenen Lebenskraft.

**ANWENDUNGSRICHTLINIEN:**
- Nur bei lebensbedrohlichen Situationen
- Niemals mehr als 3x pro Woche aktivieren
- Nach Nutzung mindestens 48h Ruhe
- Bei Überbeanspruchung: Sofort medizinische Hilfe

**MITOS PERSÖNLICHE ERFAHRUNGEN:**
'Ich habe diese Siegel während des Ersten Ninja-Krieges entwickelt. Sie haben mein Leben gerettet, aber auch Jahre davon genommen. Benutze sie weise, mein Kind.'

**SPEZIELLE UZUMAKI-VARIANTEN:**
- **Lebenskraft-Transfer:** Heilung anderer durch eigene Energie
- **Chakra-Regeneration:** Schnellere Wiederherstellung verbrauchten Chakras
- **Gift-Neutralisation:** Automatische Entgiftung des Körpers""",
                    "knowledge_gain": {"medical_fuinjutsu": 45, "uzumaki_heritage": 30, "healing_arts": 25},
                    "requirements": {"medical_knowledge": 40, "uzumaki_bloodline": True}
                },
                "4": {
                    "title": "Warnung für zukünftige Generationen",
                    "content": """Mitos persönliche Reflexionen und Warnungen für ihre Nachkommen.

**AN MEINE NACHFAHREN:**
Wenn ihr diese Worte lest, bedeutet das, dass das Uzumaki-Blut noch immer durch eure Adern fließt. Ich bin Mito Uzumaki, erste Jinchuriki des Kyuubi und Ehefrau des Ersten Hokage. Diese Zeilen sind mein Vermächtnis.

**DIE LAST DES UZUMAKI-ERBES:**
'Das Erbe der Uzumaki liegt nicht nur in unserem Blut, sondern in unserem Verständnis des Gleichgewichts. Macht ohne Weisheit führt zur Zerstörung - wie Uzushiogakure beweist.'

Unser Heimatdorf wurde zerstört, weil andere unsere Macht fürchteten. Aber Macht allein macht nicht stark - Weisheit, Mitgefühl und Verbindungen zu anderen Menschen sind unsere wahre Stärke.

**ÜBER HASHIRAMA UND DIE SENJU:**
'Hashirama sieht in den Siegeln nur Werkzeuge. Aber sie sind so viel mehr - sie sind Brücken zwischen Welten, zwischen Herzen. Mögen die kommenden Uzumaki das nie vergessen.'

Mein Mann war ein großartiger Mann, aber er verstand nie ganz die emotionale Seite unserer Kunst. Für ihn waren Jutsu Lösungen für Probleme. Für uns Uzumaki sind sie Ausdrücke unserer Seele.

**DAS WAHRE GEHEIMNIS DER UZUMAKI:**
'Das wahre Geheimnis der Uzumaki ist nicht unsere Chakra-Menge oder unsere Siegel-Kunst. Es ist unsere Fähigkeit, Verbindungen zu schaffen - zwischen Menschen, zwischen Energien, zwischen Vergangenheit und Zukunft.'

Wir sind Brückenbauer. Wo andere Mauern errichten, schaffen wir Verbindungen. Wo andere kämpfen, vermitteln wir. Das ist unsere Bestimmung.

**AN SUKUNA PERSÖNLICH:**
'Du, der du diese Zeilen liest - ich spüre dein Chakra durch die Zeit. Du bist anders als die anderen Uzumaki. In dir fließt nicht nur unser Blut, sondern auch etwas Wilderes, Ursprünglicheres.'

'Fürchte dich nicht vor dieser Wildheit. Sie ist ein Geschenk, nicht ein Fluch. Aber lerne sie zu zähmen, nicht zu unterdrücken. Ein wilder Fluss, der richtig geleitet wird, kann Felder bewässern. Ungezügelt zerstört er alles auf seinem Weg.'

**LETZTE WORTE:**
'Zu meinen Nachkommen: Nutzt diese Macht weise. Die Welt braucht Brückenbauer, keine Zerstörer. Ehrt das Uzumaki-Erbe, aber vergesst nie, dass wahre Stärke in der Verbindung zu anderen liegt.'

'Möge das Feuer von Konoha ewig brennen, und mögen die Uzumaki immer Wächter des Friedens sein.'

**GEHEIMES NACHSCRIPT:**
In der Wand hinter diesem Buch ist ein verstecktes Fach. Dort findet ihr mein persönliches Chakra-Kristall - einen Notfall-Energiespeicher für schwere Zeiten. Aber brecht das Siegel nur, wenn das Dorf in tödlicher Gefahr ist.""",
                    "knowledge_gain": {"wisdom": 25, "uzumaki_philosophy": 35, "family_history": 30},
                    "emotional_impact": "deep_connection_to_heritage",
                    "special_unlock": "mitos_chakra_crystal"
                }
            }
        },

        # ===== MEDIZINISCHE ENZYKLOPÄDIE =====
        "medizinische_enzyklopaedie": {
            "title": "Tsunades Medizinische Enzyklopädie",
            "author": "Tsunade Senju & Shizune",
            "location": "Tsunades Privatbibliothek",
            "type": "medizin",
            "access_required": "medical_interest",
            "reading_time_minutes": 120,
            "chapters": {
                "1": {
                    "title": "Grundlagen des Chakra-basierten Heilens",
                    "content": """Medizinisches Ninjutsu basiert auf der präzisen Kontrolle von Chakra zur Stimulation natürlicher Heilungsprozesse.

**GRUNDPRINZIPIEN:**
1. **Diagnose durch Chakra-Abtastung** - Spüre Verletzungen und Krankheiten
2. **Gezielte Zellstimulation** - Beschleunige natürliche Heilung
3. **Toxin-Neutralisation** - Entgifte den Körper auf Zellebene
4. **Wundverschluss und Regeneration** - Repariere Gewebe direkt

**HÄUFIGE TECHNIKEN:**
- **Shousen Jutsu** (Mystische Handflächentechnik) - Grundlage aller Heilung
- **Doku Keshi** (Giftentfernung) - Neutralisiert Toxine
- **Chi no Michi** (Blutungsstopp) - Verschließt Wunden sofort
- **Shindan Jutsu** (Chakra-Diagnose) - Erkennt versteckte Verletzungen

**⚠️ WICHTIGE SICHERHEITSREGELN:**
Niemals eigenes Chakra überlasten! Ein erschöpfter Heiler kann niemanden retten. Kenne deine Grenzen und überschreite sie nie in unkritischen Situationen.

**TSUNADES PERSÖNLICHE NOTIZEN:**
'Medizinisches Ninjutsu ist mehr als nur Technik - es erfordert Mitgefühl, Geduld und die Bereitschaft, eigene Kraft für andere zu opfern. Ein guter Medizin-Ninja rettet nicht nur Leben, sondern gibt Hoffnung.'""",
                    "knowledge_gain": {"medical_ninjutsu": 25, "chakra_control": 15, "compassion": 10}

                }
            }
        }
    }
}


# =============================================================================
# HILFSFUNKTIONEN
# =============================================================================

def get_tsunades_library():
    """Gibt Tsunades Bibliothek zurück"""
    return TSUNADES_BIBLIOTHEK


def add_new_book(book_id, book_data):
    """Fügt ein neues Buch zu Tsunades Bibliothek hinzu"""
    TSUNADES_BIBLIOTHEK["books"][book_id] = book_data
    print(f"✅ Neues Buch '{book_data['title']}' zu Tsunades Bibliothek hinzugefügt!")


def get_book_by_id(book_id):
    """Gibt ein spezifisches Buch zurück"""
    return TSUNADES_BIBLIOTHEK["books"].get(book_id, None)


def list_all_books():
    """Listet alle Bücher in Tsunades Bibliothek auf"""
    books = []
    for book_id, book_data in TSUNADES_BIBLIOTHEK["books"].items():
        books.append({
            "id": book_id,
            "title": book_data["title"],
            "author": book_data["author"],
            "type": book_data["type"]
        })
    return books


# =============================================================================
# BEISPIEL FÜR NEUE BÜCHER
# =============================================================================

# Beispiel, wie du einfach ein neues Buch hinzufügen kannst:
"""
neues_buch = {
    "title": "Chakra-Kontrolle für Fortgeschrittene",
    "author": "Meister Jigen",
    "location": "Tsunades Arbeitszimmer",
    "type": "training",
    "access_required": "chakra_mastery",
    "reading_time_minutes": 75,
    "chapters": {
        "1": {
            "title": "Fortgeschrittene Techniken",
            "content": "Dein Buchinhalt hier...",
            "knowledge_gain": {"chakra_control": 30, "advanced_techniques": 20}
        }
    }
}

add_new_book("chakra_kontrolle_buch", neues_buch)
"""

if __name__ == "__main__":
    print("📚 Tsunades Bibliothek geladen!")
    print(f"📖 {len(TSUNADES_BIBLIOTHEK['books'])} Bücher verfügbar:")
    for book in list_all_books():
        print(f"   • {book['title']} ({book['type']})")

