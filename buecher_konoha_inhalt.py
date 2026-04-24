#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Naruto RPG - Konoha Bibliothek Inhalte
Alle Bücher und Texte für die öffentliche Bibliothek von Konoha
"""


def get_konoha_library():
    """Gibt die komplette Konoha Bibliothek zurück"""

    return {
        "location_name": "Konoha Öffentliche Bibliothek",
        "description": "Die große Bibliothek von Konohagakure mit öffentlich zugänglichen Büchern über Geschichte, Kultur und Grundlagen-Jutsu.",
        "access_level": "public",
        "opening_hours": "06:00 - 22:00",
        "librarian": "Mizuki Tanaka",

        "books": {
            # --------------------------------------------------#
            # --------RECHTSABTEILUNG---------------------------#
            # --------------------------------------------------#
            "gesetzbuch_konoha": {
                "title": "Gesetzbuch von Konohagakure",
                "author": "Rat der Hokage",
                "location": "Rechtsabteilung, Regal A1",
                "type": "recht_politik",
                "access_required": "none",
                "reading_time_minutes": 45,
                "popularity": "hoch",
                "condition": "gut",
                "chapters": {
                    "1": {
                        "title": "Grundgesetze des Dorfes",
                        "content": """**GRUNDGESETZE VON KONOHAGAKURE**

    **Artikel 1 - Dorfschutz:**
    Das oberste Gesetz besagt, dass der Schutz des Dorfes und seiner Bewohner über allem steht. Jeder Shinobi schwört beim Erhalt seines Stirnbands, sein Leben für Konoha zu geben.

    **Artikel 2 - Hokage-Autorität:**
    Der Hokage ist die höchste Autorität in allen Belangen. Seine Entscheidungen sind endgültig, außer bei Abstimmung des Ältestenrats mit 2/3 Mehrheit.

    **Artikel 3 - Ninja-Rangordnung:**
    - Akademie-Schüler
    - Genin (Niedrigrangige Ninja)
    - Chūnin (Mittlere Ninja) 
    - Jōnin (Hochrangige Ninja)
    - ANBU (Spezialeinheiten)
    - Sannin (Legendäre Drei)
    - Hokage (Dorfanführer)

    **Artikel 4 - Verbotene Techniken:**
    Jutsu der S-Klasse sind ohne ausdrückliche Genehmigung des Hokage verboten. Zuwiderhandlung wird mit Verbannung oder Hinrichtung bestraft.

    **Artikel 5 - Behandlung von Gefangenen:**
    Kriegsgefangene sind menschlich zu behandeln. Folter ist nur bei direkter Bedrohung des Dorfes erlaubt.

    Diese Gesetze bilden das Fundament unserer Gesellschaft seit der Gründung durch den Ersten Hokage, Hashirama Senju.""",
                        "knowledge_gain": {"politics": 15, "village_law": 20}
                    },
                    "2": {
                        "title": "Missionsrichtlinien",
                        "content": """**MISSIONSRICHTLINIEN UND PROTOKOLLE**

    **D-Rang Missionen:**
    - Einfache Aufgaben ohne Kampf
    - Gartenarbeit, Haustiersitting, kleine Reparaturen
    - Vergütung: 500-1.000 Ryō
    - Für Genin-Teams geeignet

    **C-Rang Missionen:**
    - Eskorte-Aufgaben in sicheren Gebieten
    - Banditen-Bekämpfung (kleine Gruppen)
    - Informationsbeschaffung
    - Vergütung: 15.000-50.000 Ryō

    **B-Rang Missionen:**
    - Kampf gegen andere Ninja möglich
    - Eskorte wichtiger Persönlichkeiten
    - Infiltration feindlicher Gebiete
    - Vergütung: 80.000-200.000 Ryō

    **A-Rang Missionen:**
    - Hochgefährliche Aufträge
    - Kampf gegen Jōnin-level Gegner
    - Diplomatische Missionen
    - Vergütung: 150.000-1.000.000 Ryō

    **S-Rang Missionen:**
    - Staatsgeheimnisse betroffen
    - Kampf gegen Kage-level Gegner
    - Nur für Elite-Ninja
    - Vergütung: 1.000.000+ Ryō

    **MISSION PROTOKOLL:**
    1. Briefing beim Missions-Schalter
    2. Team-Zusammenstellung durch Jōnin-Sensei
    3. Ausrüstung abholen
    4. Mission durchführen
    5. Bericht beim Hokage abgeben

    **NOTFALL-CODES:**
    - Code Rot: Dorfdestruction droht
    - Code Orange: Kage in Gefahr
    - Code Gelb: Feindliche Infiltration
    - Code Grün: Standard-Alarm""",
                        "knowledge_gain": {"mission_knowledge": 25, "village_operations": 15}
                    },
                    "3": {
                        "title": "Allianzen und Verträge",
                        "content": """**KONOHAS ALLIANZEN UND VERTRÄGE**

    **AKTUELLE ALLIANZEN:**

    **Sunagakure (Sandgakure):**
    - Friedensvertrag seit dem Ende des Dritten Shinobi-Weltkriegs
    - Handelsabkommen für seltene Mineralien
    - Gegenseitiger Beistandspakt bei Invasionen
    - Austauschprogramm für Chūnin-Prüfungen

    **Kirigakure (Nebeldorf):**
    - Waffenstillstand nach den Blutigen Nebel-Jahren
    - Begrenztes Handelsabkommen
    - Informationsaustausch über feindliche Organisationen

    **EHEMALIGE KONFLIKTE:**

    **Iwagakure (Steindorf):**
    - Traditioneller Rivale
    - Häufige Grenzstreitigkeiten
    - Konkurrierende Ansprüche auf Ressourcen
    - Vorsichtiger Waffenstillstand

    **Kumogakure (Wolkendorf):**
    - Gespannte Beziehungen nach Hyūga-Zwischenfall
    - Versuchte Entführung von Hinata Hyūga
    - Kompensationszahlungen geleistet
    - Überwachung ihrer ANBU-Aktivitäten

    **NEUTRALE NATIONEN:**
    - Land des Eisens (Samurai-Nation)
    - Kleinere Dörfer unter Konohas Schutz
    - Handelsrouten-Sicherheitsverträge

    **FEINDLICHE ORGANISATIONEN:**
    - Akatsuki (höchste Bedrohungsstufe)
    - Verschiedene Banditengruppen
    - Abtrünnige Ninja aller Nationen

    **DIPLOMATISCHE GRUNDSÄTZE:**
    1. Stärke durch Einheit
    2. Verhandlung vor Gewalt
    3. Schutz der Schwächeren
    4. Bewahrung des Friedens""",
                        "knowledge_gain": {"diplomacy": 20, "international_relations": 18}
                    }
                }
            },
            # -------------------------------------------------#
            # -------SOZIOLOGIE--------------------------------#
            # -------------------------------------------------#
            "konoha_clan_guide": {
                "title": "Clans von Konoha - Ein Überblick",
                "author": "Chōza Akimichi & Shikaku Nara",
                "location": "Soziologie, Regal D2",
                "type": "kultur_gesellschaft",
                "access_required": "none",
                "reading_time_minutes": 50,
                "popularity": "hoch",
                "condition": "gut",
                "chapters": {
                    "1": {
                        "title": "Die Großen Clans",
                        "content": """**DIE GROSSEN CLANS VON KONOHA**

    **UCHIHA-CLAN:**
    - Kekkei Genkai: Sharingan
    - Spezialität: Feuer-Jutsu und Genjutsu
    - Geschichte: Mitgründer des Dorfes, später Tragödie
    - Aktuelle Mitglieder: Sasuke Uchiha (letzter bekannter)
    - Clan-Symbol: Uchiwa (Fächer)

    **HYŪGA-CLAN:**
    - Kekkei Genkai: Byakugan  
    - Spezialität: Jūken (Sanfte Faust)
    - Struktur: Haupt- und Nebenfamilie
    - Philosophie: Schicksal und Tradition
    - Anführer: Hiashi Hyūga

    **NARA-CLAN:**
    - Spezialität: Schatten-Jutsu
    - Charakteristik: Hohe Intelligenz, strategisches Denken
    - Tradition: Hirsch-Zucht und Medizin-Herstellung
    - Berühmte Mitglieder: Shikaku, Shikamaru Nara
    - Motto: "Was für ein Drag..."

    **AKIMICHI-CLAN:**
    - Spezialität: Körpererweiterungs-Jutsu
    - Charakteristik: Große Körper, noch größere Herzen
    - Tradition: Besondere Diätpillen und Restaurants
    - Berühmte Mitglieder: Chōza, Chōji Akimichi
    - Philosophie: Kraft kommt aus Freundschaft

    **YAMANAKA-CLAN:**
    - Spezialität: Geistes-Jutsu
    - Geschäft: Blumenladen (Tarnung für Spionage)
    - Fähigkeiten: Gedankenlesen, Körper-Übernahme
    - Berühmte Mitglieder: Inoichi, Ino Yamanaka
    - Tradition: Blumen als Kommunikationsmittel

    **INO-SHIKA-CHŌ FORMATION:**
    Diese drei Clans arbeiten seit Generationen zusammen:
    - Perfekte Kampftaktiken
    - Generationsübergreifende Freundschaften
    - Komplementäre Fähigkeiten
    - Stärkste Team-Formation in Konoha""",
                        "knowledge_gain": {"clan_knowledge": 30, "village_sociology": 20}
                    },
                    "2": {
                        "title": "Mittlere und kleinere Clans",
                        "content": """**MITTLERE UND KLEINERE CLANS**

    **SARUTOBI-CLAN:**
    - Berühmtes Mitglied: Hiruzen Sarutobi (3. Hokage)
    - Spezialität: Vielseitigkeit in allen Jutsu-Arten
    - Charakteristik: Natürliche Führungsqualitäten
    - Tradition: Viele Hokage und Anbu-Mitglieder

    **HATAKE-CLAN:**
    - Berühmtes Mitglied: Kakashi Hatake
    - Charakteristik: Außergewöhnliche Ninja-Talente
    - Geschichte: Kleiner, aber einflussreicher Clan
    - Besonderheit: Weiße Haare als Erkennungsmerkmal

    **INUZUKA-CLAN:**
    - Spezialität: Partnerschaft mit Ninja-Hunden
    - Charakteristik: Scharfe Sinne, wilde Kampfart
    - Tradition: Familienhunde als Kampfpartner
    - Berühmte Mitglieder: Tsume, Kiba Inuzuka

    **ABURAME-CLAN:**
    - Spezialität: Insekten-Jutsu
    - Charakteristik: Ruhig, analytisch, geheimnisvoll
    - Tradition: Symbiotische Beziehung zu Käfern
    - Kampfstil: Aufklärung und Gift-Attacken

    **LEE-Familie:**
    - Spezialität: Taijutsu (Körpertechniken)
    - Philosophie: Harte Arbeit überwindet Talent
    - Training: Extremes körperliches Training
    - Berühmte Mitglieder: Might Guy, Rock Lee

    **TENTEN'S FAMILIE:**
    - Spezialität: Waffen-Jutsu
    - Geschäft: Ninja-Werkzeug Laden
    - Charakteristik: Präzision und Vielseitigkeit
    - Training: Alle Arten von Ninja-Waffen

    **INTEGRATION NEUER MITGLIEDER:**
    Konoha hat auch Platz für:
    - Einzelne Ninja ohne Clan-Zugehörigkeit
    - Flüchtlinge aus anderen Dörfern
    - Adoptierte Waisen (wie Naruto)
    - Ehemalige Feinde, die Schutz suchen

    **CLAN-SYSTEM VORTEILE:**
    - Spezialisierte Jutsu-Vererbung
    - Starke Familienbande und Unterstützung
    - Traditionelles Wissen und Techniken
    - Politische Stabilität im Dorf""",
                        "knowledge_gain": {"clan_knowledge": 25, "village_structure": 18}
                    }
                }
            },
            # ------------------------------------------------------#
            # -------------MEDIZIN---------------------------------#
            # -----------------------------------------------------#
            "tenketsu_punkte_verstehen": {
                "title": "Medizin: Tenketsu Punkte verstehen",
                "author": "Medic-Nin des Konoha-Krankenhauses",
                "locatlion": "Medizin & Biologie, Regal C3",
                "type": "jutsu_medizin",
                "access_required": "none",
                "reading_time_minutes": 55,
                "popularity": "mittel",
                "condition": "neu",
                "chapters": {
                    "1": {
                        "title": "Was sind Tenketsu-Punkte?",
                        "content": """Die Tenketsu sind 361 winzige Löcher auf der Keirakurai, den Chakra-Bahnen.
                            Durch diese Löcher kann man Chakra ausströmen lassen. Wenn man einen dieser winzigen Löcher
                             gezielt trifft, kann kein Chakra mehr hindurch fließen.Jedoch ist es schon sehr schwer ein Loch
                              auf der Keirakurai zu treffen, da sie kleiner sind als Stecknadelköpfe. Die meisten Ninja können
                               Tenkutsu nur an ihren Händen verwenden, um Chakra in den zwölf grundlegenden Handsiegeln zu formen. """
                    },
                    "2": {
                        "title": "Organ-Tenketsu und acht Tore",
                        "content": """Im Körperinneren gibt es acht Stellen, an denen die Tenketsu sehr nahe an die Organe
                            geknüpft sind. Diese sogenannten acht Tore stärken durch das Öffnen selbiger den Chakra-Fluss, 
                            jedoch zu Lasten des eigenen Körpers. Sie heißen der Reihe nach:
                            - Kaimon (Tor der Öffnung)
                            - Kyumon (Tor der Ruhe)
                            - Seimon (Tor des Lebens)
                            - Shomon (Tor des Schmerzes)
                            - Tomon (Tor der Grenze)
                            - Keimon (Tor der Sicht)
                            - Kyomon (Tor des Schockes)
                            - Shimon (Tor des Todes)
                            Man nennt sie zusammen Hachimon. Wenn man alle acht Tore geöffnet hat, befindet man sich in einem
                            Zustand, den man Hachimon Tonkou no Jin nennt. In diesem Zustand ist man unglaublich stark, aber
                            nach Öffnen der acht Tore und Durchführung eines Angriffes wird man unweigerlich sterben.""",
                        "knowledge_gain": {"chakra_theory": 10}
                    }
                }
            },
            "medizin_ninjutsu": {
                "title": "Medizin-Ninjutsu: Theorie und Praxis",
                "author": "Tsunade Senju (unter Pseudonym)",
                "location": "Medizin & Biologie, Regal C2",
                "type": "jutsu_medizin",
                "access_required": "none",
                "reading_time_minutes": 30,
                "popularity": "mittel",
                "condition": "neu",
                "chapters": {
                    "1": {
                        "title": "Chakra-Anwendung in der Heilung",
                        "content": """**MEDIZINISCHES CHAKRA**
        Medizinisches Ninjutsu erfordert die präziseste Chakra-Kontrolle. Das Chakra muss als Grün visualisiert und mit sanftem, 
        aber festem Willen durch die **Tenketsu** des Patienten geleitet werden.
        - **Heilungs-Prozess:** Die Energie stimuliert die Zellregeneration.
        - **Erste Hilfe:** Die Wunde reinigen und den Blutfluss mit Chakra stoppen.
        - **Gefahr:** Falsch angewandtes Chakra kann mehr Schaden als Nutzen anrichten.""",
                        "knowledge_gain": {"medical_ninjutsu": 20, "chakra_control": 10}
                    },
                    "2": {
                        "title": "Die Mystische Hand-Technik",
                        "content": """**MYSTICAL PALM TECHNIQUE (SHŌSEN JUTSU)**
        Dies ist die grundlegendste chirurgische Heilungstechnik. Der Anwender konzentriert Chakra auf seine Handflächen und 
        lässt es als grüne, heilende Aura austreten.
        - **Anwendung:** Schneiden (feine Chakra-Skalpell) und Heilen (regenerativer Fluss).
        - **Voraussetzung:** Extrem hohes medizinisches Wissen, um die **Anatomie** des Patienten zu verstehen und die Chakra-Kanäle zu visualisieren.
        - **Training:** Fünf Jahre ununterbrochenes Training in Chakra-Kontrolle sind die Mindestanforderung.""",
                        "knowledge_gain": {"medical_ninjutsu": 25, "chakra_application": 15}
                    }
                }
            },

            "heilkräuter_des_feuerreichs": {
                "title": "Heilkräuter des Feuerreichs",
                "author": "Konoha Medi-Nin Gesellschaft",
                "location": "Medizin & Biologie, Regal C9",
                "type": "jutsu_heilkraeuter",
                "access_required": "none",
                "reading_time_minutes": 30,
                "popularity": "mittel",
                "condition": "neu",
                "chapters": {
                    "1": {
                        "title": "Häufige Heilpflanzen",
                        "content": """Konoha Gras: Wächst überall im Dorf. Lindert Kopfschmerzen und kleine Wunden.
                                                Einfach zerkauen oder als Tee aufbrühen.
                                  Feuer-Lilie: Rote Blüten mit heilender Wirkung. Hilft bei Verbrennungen und Fieber.
                                               Nur die Blütenblätter verwenden - die Wurzel ist giftig!
                                  Schafgarbe:  Diese Pflanze wächst in den umliegenden Wäldern und an Feldrändern und
                                               hilft bei Magen-Darm-Beschwerden. Schafgarben-Tee hat eine leicht
                                               beruhigende Wirkung.
                                   Löwenzahn:  Löwenzahn wächst eigentlich überall wie Unkraut. Jedoch hat auch diese
                                               Pflanze heilende Eigenschaften. Frische Löwenzahnblätter stärken das 
                                               Immunsystem und Löwenzahn-Tee hilft bei Gelenkentzündungen. 

                                   """,
                    },
                    "2": {
                        "title": "Seltene Heilkräuter",
                        "content": """Chakra-Moos: Sehr seltenes Moos, das auf chakra-reichen Bäumen wächst. Stellt 
                                                verbrauchtes Chakra wieder her.
                              Ewigkeits-Blume: Blüht nur alle 10 Jahre. Ein Blütenblatt kann tödliche Verletzungen
                                                heilen.
                                 Hinata-Momo: Wächst an Südhängen, hilft bei Verbrennungen und Hautverletzungen.
                                Akane-Wurzel: Eine rote Wurzel die in schattigen Waldgebieten wächst. Wirkt 
                                              blutstillend.""",
                    }
                }
            },
            "grundlagen_der_feldmedizin": {
                "title": "Grundlagen der Feldmedizin",
                "author": "Konoha Medi-Nin Gesellschaft",
                "location": "Medizin & Biologie, Regal C4",
                "type": "medizin",
                "access_required": "none",
                "reading_time_minutes": 25,
                "popularity": "sehr_hoch",
                "condition": "gut",
                "chapters": {
                    "1": {
                        "title": "Erste Hilfe im Kampf",
                        "content": """Die ersten Minuten entscheiden über Leben und Tod. Auch ohne medizinische 
                        Ninjutsu kann jeder Ninja Leben retten:
                        1. Blutungen stoppen: Druckverband anlegen, niemals Fremdkörper entfernen!
                        2. Atemwege freihalten: Bewusstlose in stabile Seitenlage bringen
                        3. Schock verhindern: Beine hochlagern, warm halten, beruhigen."""

                    },
                    "2": {
                        "title": "Chakra-Erschöpfung",
                        "content": """Häufigste Ursachen für Ninja-Todesfälle nach Kampfhandlungen. Symptome: 
                                      Schwäche, Verwirrung, kalter Schweiß.
                                      Behandlung: Soldatenpillen, Ruhe, warme Decken. Bei schwerem Chakra-Verlust:
                                      Sofort zum Medizin-Nin!"""
                    },
                    "3": {
                        "title": "Improvisierte Heilmittel",
                        "content": """In der Wildnis muss man erfinderisch sein: 
                                      - Spinnweben als Wundauflage(stoppt Blutungen)
                                      - Baumrinde als Schiene bei Knochenbrüchen
                                      - Urin zur Wundreinigung(ACHTUNG: Wirklich NUR im äußersten Notfall!)
                                      - Lehm und Spucke gegen Insektenstiche"""
                    }
                }
            },
            # -------------------------------------------------------#
            # ------------JUTSU-GRUNDLAGEN--------------------------#
            # ------------------------------------------------------#
            "grundlagen_der_chakra_kontrolle": {
                "title": "Grundlagen der Chakra-Kontrolle",
                "author": "Akademie-Instruktoren Kollektiv",
                "location": "Jutsu-Grundlagen, Regal C1",
                "type": "jutsu_theorie",
                "access_required": "none",
                "reading_time_minutes": 40,
                "popularity": "sehr_hoch",
                "condition": "sehr_gut",
                "chapters": {
                    "1": {
                        "title": "Was ist Chakra?",
                        "content": """**CHAKRA - DIE LEBENSENERGIE ALLER NINJA**

    **DEFINITION:**
    Chakra ist die Mischung aus physischer und spiritueller Energie, die alle Lebewesen besitzen. Ninja lernen, diese Energie zu kontrollieren und für Jutsu einzusetzen.

    **DIE ZWEI KOMPONENTEN:**

    **1. KÖRPERLICHE ENERGIE:**
    - Stammt aus jeder Zelle des Körpers
    - Wird durch Training und Kondition gestärkt
    - Regeneriert sich durch Ruhe und Nahrung
    - Bestimmt die Ausdauer eines Ninja

    **2. SPIRITUELLE ENERGIE:**
    - Kommt aus Geist und Seele
    - Wächst durch Erfahrung und Meditation
    - Beeinflusst die Kraft der Jutsu
    - Verbunden mit Willenskraft und Konzentration

    **CHAKRA-BILDUNG:**
    Beide Energien verschmelzen in speziellen Punkten im Körper, genannt Tenketsu. Ein Mensch hat 361 Tenketsu-Punkte, die wie ein Netzwerk verbunden sind.

    **CHAKRA-FARBEN:**
    - Blau: Standard-Chakra (die meisten Ninja)
    - Rot: Chakra mit negativen Emotionen
    - Gelb: Seltene goldene Chakra-Variation
    - Grün: Medizinisches Chakra
    - Weiß: Sehr reine, spirituelle Energie

    **CHAKRA-NATUREN:**
    Jeder Ninja hat eine natürliche Affinität zu einem Element:
    - Katon (Feuer): Aggressive, heiße Techniken
    - Suiton (Wasser): Fließende, anpassbare Jutsu
    - Doton (Erde): Defensive, stabile Techniken
    - Fūton (Wind): Schneidende, scharfe Angriffe
    - Raiton (Blitz): Schnelle, durchdringende Jutsu

    **GRUNDÜBUNGEN:**
    1. Blätter am Körper kleben lassen
    2. Auf Wasser laufen
    3. Bäume hinaufgehen
    4. Chakra sichtbar machen""",
                        "knowledge_gain": {"chakra_theory": 20, "jutsu_basics": 15}
                    },
                    "2": {
                        "title": "Handzeichen und Jutsu-Ausführung",
                        "content": """**HANDZEICHEN - DIE SPRACHE DER JUTSU**

    **GRUNDLAGEN DER HANDZEICHEN:**
    Handzeichen helfen dabei, Chakra zu formen und zu lenken. Jedes Zeichen hat eine spezielle Bedeutung und beeinflusst die Art des Jutsu.

    **DIE 12 GRUND-HANDZEICHEN:**

    1. **Ratte (Ne):** Grundlage für Wasser-Jutsu
    2. **Ochse (Ushi):** Verstärkt Erdtechniken  
    3. **Tiger (Tora):** Basis für Feuer-Jutsu
    4. **Hase (U):** Unterstützt Mond-basierte Techniken
    5. **Drache (Tatsu):** Verstärkt alle Jutsu-Arten
    6. **Schlange (Mi):** Basis für Gift- und Erdtechniken
    7. **Pferd (Uma):** Verstärkt Heilungs-Jutsu
    8. **Ziege (Hitsuji):** Unterstützt Illusions-Techniken
    9. **Affe (Saru):** Basis für Blitz-Jutsu
    10. **Hahn (Tori):** Verstärkt Wind-Techniken
    11. **Hund (Inu):** Unterstützt Erd- und Wasser-Jutsu
    12. **Wildschwein (I):** Verstärkt alle Element-Jutsu

    **JUTSU-AUSFÜHRUNG - DIE DREI SCHRITTE:**

    **1. KONZENTRATION:**
    - Klarer Geist und fokussierte Absicht
    - Visualisierung der gewünschten Wirkung
    - Emotionale Kontrolle und Ruhe

    **2. CHAKRA-FORMUNG:**
    - Korrekte Handzeichen in richtiger Reihenfolge
    - Gleichmäßiger Chakra-Fluss
    - Balance zwischen Geschwindigkeit und Präzision

    **3. FREISETZUNG:**
    - Kontrolle über Richtung und Intensität
    - Timing der Jutsu-Aktivierung
    - Nachkontrolle der Jutsu-Wirkung

    **HÄUFIGE ANFÄNGERFEHLER:**
    - Zu schnelle Handzeichen (Ungenauigkeit)
    - Falsche Chakra-Menge (zu viel/zu wenig)
    - Mangelnde Konzentration (schwache Jutsu)
    - Unvollständige Handzeichen (Jutsu-Versagen)

    **TRAINING-TIPPS:**
    - Übe Handzeichen bis sie unbewusst werden
    - Starte mit einfachen Ein-Handzeichen-Jutsu  
    - Meditiere täglich für bessere Chakra-Kontrolle
    - Trainiere mit einem erfahrenen Sensei""",
                        "knowledge_gain": {"jutsu_execution": 25, "hand_signs": 20}
                    }
                }
            },
            "chakra_arten": {
                "title": "Chakra-Arten: Verstehen und Lernen",
                "author": "Hashirama Senju",
                "Location": "Jutsu-Grundlagen, Regal C9",
                "type": "chakra",
                "access_required": "none",
                "reading_time_minutes": 30,
                "popularity": "mittel",
                "condition": "gut",
                "chapters": {
                    "1": {
                        "title": "Normales Chakra",
                        "content": """Normales Chakra besitzt jeder Shinobi, es ist meist blau. Wenn ein Shinobi sein
                            gesamtes Chakra verbraucht hat, kann er keine Nin- oder Genjutsu mehr wirken. Man kann sein 
                            Chakra trainieren, indem man es im Training des Öfteren vollständig verbraucht. Dadurch wird es
                            gestärkt und der Chakravorrat vergrößert sich ein wenig. Außerdem gilt: Je besser man sein 
                            Chakra unter Kontrolle hat, desto weniger verbraucht man beim Wirken von Nin- und Genjutsus""",
                    },
                    "2": {
                        "title": "Bijuu-Chakra",
                        "content": """Das Bijuu-Chakra ist das Chakra, das die Jinchuuriki mit rotem Chakra umgibt. Es ist
                            noch nicht sehr viel bekannt, aber dieses Chakra scheint rot zu sein.""",
                    },
                    "3": {
                        "title": "Natur-Chakra",
                        "content": """Das Natur-Chakra wird für die Anwendung von Senjutsu benötigt. Das Natur-Chakra fließt
                            überall in der Welt herum und theoretisch kann es jeder benutzen. Ebenfalls theoretisch existiert 
                            davon unendlich viel. Man müsste allerdings erst einmal lernen, dass Natur-Chakra zu sehen, es 
                            zweitens zu sammeln und drittens die richtige Menge anwenden, da man sonst zu Stein wird. Sammeln
                            kann man es nur, wenn man völlig regungslos bleibt. WARNUNG: NIEMALS einfach so SELBST praktizieren!"""
                    }
                }

            },
            # -------------------------------------#
            # ------GESCHICHTE---------------------#
            # ------------------------------------#
            "geschichte_des_feuerreichs": {
                "title": "Geschichte des Feuerreichs",
                "author": "Professor Hiruzen Yamamoto",
                "location": "Geschichte, Regal B3",
                "type": "geschichte",
                "access_required": "none",
                "reading_time_minutes": 60,
                "popularity": "mittel",
                "condition": "abgenutzt",
                "chapters": {
                    "1": {
                        "title": "Die Sengoku-Zeit",
                        "content": """**DIE SENGOKU-ZEIT - ZEITALTER DER KRIEGE**

    Vor der Gründung der versteckten Dörfer herrschte das Zeitalter der permanenten Kriege. Clans kämpften erbittert um Territorien, 
    Ressourcen und Aufträge. Die mächtigsten Clans des Feuerreichs waren:

    **DIE SENJU:**
    - Angeführt von Hashirama Senju
    - Meister des Mokuton (Holz-Release)
    - Bekannt für ihre Heilkräfte und Vitalität
    - "Der Gott der Shinobi" war ihr stärkster Krieger

    **DIE UCHIHA:**
    - Angeführt von Madara Uchiha
    - Besitzer der legendären Sharingan
    - Unübertroffene Feuer-Jutsu Meister
    - Erbitterte Rivalen der Senju

    **ANDERE MÄCHTIGE CLANS:**
    - Hyūga (Byakugan-Nutzer)
    - Nara (Schatten-Techniken)
    - Akimichi (Größenänderungs-Jutsu)
    - Yamanaka (Geistes-Jutsu)

    **DAS ENDE DER SENGOKU-ZEIT:**
    Nach Jahrzehnten des Blutvergießens erkannten Hashirama Senju und Madara Uchiha, dass nur durch Zusammenschluss wahrer Frieden möglich war. 
    Ihre Allianz beendete die ewigen Kriege und legte den Grundstein für Konohagakure.

    **OPFER DER KRIEGSZEIT:**
    - Millionen von Shinobi fielen in sinnlosen Schlachten
    - Ganze Familienlinien starben aus
    - Kinder wurden als Waffen eingesetzt
    - Dörfer wurden regelmäßig überfallen und zerstört

    Die Gründung der versteckten Dörfer war ein revolutionärer Akt des Friedens in einer Welt voller Hass.""",
                        "knowledge_gain": {"ancient_history": 25, "clan_knowledge": 20}
                    },
                    "2": {
                        "title": "Gründung Konohagakures",
                        "content": """**DIE GRÜNDUNG VON KONOHAGAKURE**

    **DAS HISTORISCHE TREFFEN:**
    Im Jahr 0 des Shinobi-Kalenders trafen sich Hashirama Senju und Madara Uchiha im Tal des Endes. Nach einem epischen Kampf, 
    der drei Tage und Nächte dauerte, erkannten beide, dass ihre Kinder in einer Welt ohne ewige Kriege leben sollten.

    **DER FRIEDENSPAKT:**
    - Beide Clans legten ihre Waffen nieder
    - Andere Clans schlossen sich der Allianz an
    - Das Land des Feuers unterstützte das neue Konzept
    - Der erste versteckte Dorf-Staat entstand

    **HASHIRAMA ALS ERSTER HOKAGE:**
    - Gewählt von den vereinten Clans
    - Erschuf das Hokage-System
    - Entwickelte den "Willen des Feuers" als Philosophie
    - Baute die ersten großen Strukturen mit Mokuton

    **MADARAS VERRAT:**
    Obwohl Mitgründer, konnte Madara die Macht der Senju nicht akzeptieren. Er verließ das Dorf und kehrte später zurück, 
    um es zu zerstören. Hashirama war gezwungen, seinen besten Freund zu töten, um Konoha zu schützen.

    **DIE FRÜHEN JAHRE:**
    - Schnelle Expansion und Wachstum
    - Andere Nationen gründeten eigene versteckte Dörfer
    - Entwicklung des modernen Ninja-Systems
    - Erste Chūnin-Prüfungen etabliert

    **VERMÄCHTNIS:**
    Hashiramas Vision lebt bis heute fort. Konoha wurde zum Vorbild für alle anderen versteckten Dörfer und seine Philosophie
     des Schutzes und der Familie prägt noch immer neue Generationen.

    **BERÜHMTE ERSTE BEWOHNER:**
    - Tobirama Senju (Zweiter Hokage)
    - Izuna Uchiha (Madaras Bruder)
    - Die Gründer der Sarutobi, Shimura und anderen Clans""",
                        "knowledge_gain": {"village_history": 30, "founding_knowledge": 25}
                    }
                }
            },
            "weltkriege_chronologie": {
                "title": "Shinobi-Weltkriege: Eine Chronologie",
                "author": "Hiruzen Sarutobi (posthum)",
                "location": "Geschichte, Regal B4",
                "type": "geschichte_krieg",
                "access_required": "none",
                "reading_time_minutes": 75,
                "popularity": "hoch",
                "condition": "gut",
                "chapters": {
                    "1": {
                        "title": "Der Erste Shinobi-Weltkrieg",
                        "content": """**DER ERSTE SHINOBI-WELTKRIEG**
        Nach der Gründung der versteckten Dörfer führte der Machtkampf zwischen den Großmächten zum ersten globalen Konflikt.
        Der Nidaime Hokage, Tobirama Senju, fiel dabei im Kampf gegen die Spezialeinheit von Kumogakure. Zuvor ernannte er
        Hiruzen Sarutobi zum neuen Hokage. Der Krieg endete durch ein Waffenstillstandsabkommen.
        - **Hauptakteure:** Das Land des Feuers gegen das Land des Blitzes und des Windes.
        - **Resultat:** Hohe Verluste, aber der Wille des Feuers bewährte sich. Hashiramas Tod fiel in diese Zeit.
        - **Lektion:** Die Notwendigkeit der Stärke der Kage als primäre Abschreckung.""",
                        "knowledge_gain": {"war_history": 20, "hokage_chronicles": 10}
                    },
                    "2": {
                        "title": "Der Zweite Shinobi-Weltkrieg",
                        "content": """**DER ZWEITE SHINOBI-WELTKRIEG**
        In dieser Zeit gabe es Konflikte zwischen Konohagakure, Sunagakure, Amegakure und Iwagakure. Die Mehrheit der Kämpfe
        dieses Krieges hat in kleineren Ländern wie Amegakure stattgefunden, wodurch diese verwüstet wurden. Das wirtschaftliche
        Gefälle zwischen den Ländern spielte mit in den Grund des zweiten Shinobi-Krieges mit hinein. Die Nationen begannen 
        Fraktionen zu bilden. Unter dem Vorwand faire Rechte auszugeben, begannen die Länder militärische Gewalt anzuwenden,
        um ihre Territorien zu erweitern. So begann der Krieg.
        - **Zeitpunkt:** Circa 20 Jahre nach dem Ersten.
        - **Die Sannin:** Konohas Jiraiya, Tsunade und Orochimaru erlangten in diesem Krieg ihren legendären Status durch ihren Kampf gegen Hanzo von Amegakure.
        - **Wichtige Ereignisse:** Massaker an Clan-Mitgliedern, Entwicklung neuer, tödlicher Jutsu.
        - **Resultat:** Ein ermüdender Waffenstillstand, der nur eine Pause vor dem nächsten Konflikt darstellte.""",
                        "knowledge_gain": {"war_history": 25, "famous_ninja": 15}
                    },
                    "3": {
                        "title": "Der Dritte Shinobi-Weltkrieg",
                        "content": """**DER DRITTE SHINOBI-WELTKRIEG**
        Konohagakure und Iwagakure kämpften innerhalb von Kusagakures Gebiet, nachdem Iwagakure es eingenommen hatte, um bis ins 
        Feuer-Reich vorzurücken. Erst durch den Sieg von Team Minato und der Zerstörung der Kannabi-Brücke konnte Konoha die 
        Schlacht zu ihren Gunsten drehen. Kakashi Hatake erlangte in dieser Schlacht sein Sharingan und wurde im Verlauf des
        Krieges unter dem Namen "Kakashi mit dem Sharingan" und "Kopierninja" berühmt. Minato Namikaze lieferte sich mehrere
        Schlachten mit Shinobi aus Kumogakure mit A und Killer B, wodurch er zu seinem Beinamen "Konohas gelber Blitz" kam.
        - **Ort:** Hauptsächlich an den Grenzen des Feuerreichs, insbesondere gegen Iwagakure.
        - **Konoha-Helden:** Minato Namikaze (Vierter Hokage) brillierte hier und leitete das Ende ein.
        - **Kriegsopfer:** Rin Nohara und Obito Uchiha waren tragische Opfer.
        - **Resultat:** Waffenstillstand, gefolgt von langem Wiederaufbau. Der Vertrag mit Sunagakure wurde nach diesem Krieg unterzeichnet.""",
                        "knowledge_gain": {"war_history": 30, "village_diplomacy": 10}
                    }
                }
            },
            "chroniken_der_hokage": {
                "title": "Chroniken der Hokage",
                "author": "Hiruzen Sarutobi",
                "location": "Geschichte, Regal B7",
                "type": "geschichte_konoha",
                "access_required": "none",
                "reading_time_minutes": 15,
                "popularity": "mittel",
                "conditions": "gut",
                "chapters": {
                    "1": {
                        "title": "Hashirama Senju - der erste Hokage",
                        "content": """Hashirama-sama gründete Konohagakure mit dem Traum vom Frieden. Seine Mokuton-Fähigkeiten
                     waren legendär - er konnte ganze Wälder aus dem Boden wachsen lassen. Sein größter Triumph war der Pakt
                      mit Madara Uchiha. Leider hielt dieser Frieden nicht lange.
                      'Ich träume von einer Welt, in der Kinder nicht mehr als Waffen erzogen werden.' - Hashirama Senju"""
                    },
                    "2": {
                        "title": "Tobirama Senju - der zweite Hokage",
                        "content": """Hashiramas jüngerer Bruder war pragmatischer und entwickelte viele Jutsu, die heute 
                    Standard sind - darunter das Hiraishin und das Kage Bunshin. Er gründete die Ninja-Akademie und das
                    ANBU-System. Starb heldenhaft im Kampf gegen Kumo-Ninja, um seine Schüler zu retten."""

                    },
                    "3": {
                        "title": "Hiruzen Sarutobi - der dritte Hokage",
                        "content": """Als ich das Amt übernahm, war ich jung und voller Ideale. Der zweite Ninja-Weltkrieg lehrte
                    mich die harten Realitäten des Führens. Mein größter Fehler: Das Uchiha-Massaker nicht verhindert zu haben."""
                    },
                    "4": {
                        "title": "Minato Namikaze - der vierte Hokage",
                        "content": """Minato Namikaze war auch als 'der gelbe Blitz von Konoha' bekannt, wegen seinem Hiraishin, also
                    seiner Schnelligkeit. Kein Ninja war schneller, keiner war gerechter. Er opferte sein Leben, um das Dorf 
                    vor dem Kyuubi zu retten."""
                    }

                }
            },
            # ----------------------------------------------------#
            # -----------GEOLOGIE---------------------------------#
            # ----------------------------------------------------#
            "die_fünf_großen_dörfer": {
                "title": "Die fünf großen Dörfer - ein Überblick",
                "author": "Jiraiya",
                "location": "Geologie, Regal F2",
                "type": "geologie",
                "access_required": "none",
                "reading_time_minutes": 15,
                "popularity": "mittel",
                "conditions": "gut",
                "chapters": {
                    "1": {
                        "title": "Konohagakure - Dorf versteckt in den Blättern",
                        "content": """Unser Heimatdorf im Herzen des Feuer-Reichs. Bekannt für den ''Willen des Feuers'' und
                    die stärksten Ninja der Welt. Die großen Clans: Uchiha(fast ausgelöscht), Hyuga, Nara, Akimichi, Yamanaka.
                    Besonderheiten: Ninja-Akademie, Memorial-Stein, Hokage-Monument."""
                    },
                    "2": {
                        "title": "Sunagakure - Dorf versteckt im Sand",
                        "content": """In der Wüste des Wind-Reichs gelegen. Ihre Ninja sind Meister im Umgang mit Sand und Puppen.
                                  Spezialitäten: Puppen-Jutsu, Sand-Manipulation, Wüsten-Überleben"""
                    },
                    "3": {
                        "title": "Kirigakure - Dorf versteckt im Nebel",
                        "content": """Das blutigste der fünf Dörfer. Berüchtigt für die ''Blutigen Prüfungen'', bei denen 
                                  Akademie-Schüler sich gegenseitig töten mussten. Spezialisiert auf Wasser-Jutsu und
                                  lautlose Attentate."""
                    },
                    "4": {
                        "title": "Kumogakure - Dorf versteckt in den Wolken",
                        "content": """Hoch in den Bergen des Blitz-Reichs. Ihre Ninja sind für Geschwindigkeit und Blitz-Jutsu
                                  bekannt. Sehr militärisch organisiert und kriegslüstern.
                                  Besonderheiten: Stärkste Armee."""
                    },
                    "5": {
                        "title": "Iwagakure - Dorf versteckt in den Steinen",
                        "content": """In den Felsen des Erd-Reichs versteckt. Ihre Ninja sind zäh wie Stein und beherrschen 
                                  Erd-Jutsu meisterhaft. Bekannt für Ausdauer und Verteidigung.
                                  Besonderheiten: Uneinnehmbare Festung."""
                    }
                }
            },
            "handelsrouten_zwischen_den_dörfern": {
                "title": "Handelsrouten zwischen den Dörfern",
                "author": "Händler-Gilde",
                "location": "Geologie, Regal F5",
                "type": "geologie",
                "access_required": "none",
                "reading_time_minutes": 15,
                "popularity": "hoch",
                "conditions": "mittel",
                "chapters": {
                    "1": {
                        "title": "Die große Nordroute",
                        "content": """Verbindet Konoha mit Kumo über des Tee-Reich. Dauer: 15-20 Tage je nach Wetter. 
                                  Hauptwaren: Tee, Gewürze, Metallwaren. 
                                  Gefahren: Räuberbanden in den Bergen, wilde Tiere, Steinschläge"""
                    },
                    "2": {
                        "title": "Die Wüstenstraße",
                        "content": """Verläuft von Konoha nach Suna durch das Fluss-Reich. Die gefährlichste Route wegen
                                  der Wüste und häufigen Sandstürmen.
                                  Hauptwaren: Wasser, Konserven, Medizin.
                                  Warnung: Niemals ohne Wüstenführer reisen!"""
                    },
                    "3": {
                        "title": "Die Seestraße",
                        "content": """Seeweg nach Kiri über das Wellen-Reich. Nur für mutige Händler - Piraten und 
                                  Sturm-Ninja machen diese Route extrem gefährlich."""
                    }
                }
            }

        }
    }