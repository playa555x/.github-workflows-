/*
BRAWLER-CHARAKTERE - SPEZIFIKATION

Implementiere die folgenden Brawler-Charaktere mit ihren einzigartigen Eigenschaften:

1. SHARPSHOOTER (Fernkämpfer)
   - Name: "Bolt"
   - Gesundheit: 3600
   - Geschwindigkeit: Normal (720)
   - Primärangriff: "Dual Shots"
     * Zwei schnelle Projektile mit mittlerer Reichweite
     * Schaden: 420 pro Schuss
     * Feuerrate: Hoch (0.3s Cooldown)
     * Reichweite: 8 Tiles
   - Super-Fähigkeit: "Bullet Storm"
     * Feuert eine Salve von 12 Projektilen in Fächerform
     * Jedes Projektil verursacht 320 Schaden
     * Durchdringt keine Wände
   - Besonderheit: Hohe Angriffsgeschwindigkeit, gute für Distanzkämpfe

2. TANK (Nahkämpfer)
   - Name: "Bulldozer"
   - Gesundheit: 7200
   - Geschwindigkeit: Langsam (650)
   - Primärangriff: "Heavy Swing"
     * Weitreichender Nahkampfangriff mit Flächenwirkung
     * Schaden: 980 pro Schlag
     * Feuerrate: Langsam (0.8s Cooldown)
     * Reichweite: 2.5 Tiles
   - Super-Fähigkeit: "Rampage"
     * Erhält 40% Schadensreduktion für 5 Sekunden
     * Erhöhte Bewegungsgeschwindigkeit für die Dauer
     * Verursacht 600 Schaden beim Zusammenstoß mit Gegnern
   - Besonderheit: Hohe Überlebensfähigkeit, gut zum Verteidigen von Zielen

3. SUPPORT (Unterstützer)
   - Name: "Helix"
   - Gesundheit: 4200
   - Geschwindigkeit: Normal (720)
   - Primärangriff: "Healing Pulse"
     * Mittlere Reichweite, heilt Verbündete für 840
     * Verursacht 560 Schaden an Gegnern
     * Feuerrate: Mittel (0.5s Cooldown)
     * Reichweite: 6 Tiles
   - Super-Fähigkeit: "Regeneration Field"
     * Erzeugt eine Zone (Radius: 4 Tiles), die 5 Sekunden bestehen bleibt
     * Verbündete in der Zone erhalten 600 HP/Sekunde
     * Gegner in der Zone werden um 20% verlangsamt
   - Besonderheit: Team-Support, ideal für objektbasierte Spielmodi

4. ASSASSIN (Schneller Angreifer)
   - Name: "Phantom"
   - Gesundheit: 3200
   - Geschwindigkeit: Sehr schnell (820)
   - Primärangriff: "Quick Strike"
     * Schneller Nahkampfangriff
     * Schaden: 1680 bei vollständiger Aufladung
     * Automatisches Aufladen über 1.5 Sekunden
     * Reichweite: 2 Tiles
   - Super-Fähigkeit: "Shadow Dash"
     * Teleportiert sich 6 Tiles in Blickrichtung
     * Hinterlässt eine Schatten-Kopie, die nach 1 Sekunde explodiert (900 Schaden)
     * Wird für 1 Sekunde nach dem Teleport unsichtbar
   - Besonderheit: Hohe Mobilität, gut für Hinterhalte und schnelle Ausschaltungen

5. THROWER (Werfer)
   - Name: "Bombarda"
   - Gesundheit: 3400
   - Geschwindigkeit: Normal (720)
   - Primärangriff: "Bouncing Bomb"
     * Wirft eine Bombe, die beim Aufprall zweimal springt
     * Schaden: 800 beim ersten Aufprall, 600 beim zweiten, 400 beim dritten
     * Feuerrate: Mittel (0.6s Cooldown)
     * Reichweite: 7 Tiles
   - Super-Fähigkeit: "Minefield"
     * Verstreut 8 Minen in einem Gebiet (5x5 Tiles)
     * Jede Mine verursacht 860 Schaden und verlangsamt Gegner
     * Minen bleiben 10 Sekunden oder bis zur Auslösung
   - Besonderheit: Kann Gegner hinter Wänden angreifen, starke Gebietskontrolle

Balancing-Hinweise:
- Alle Schadenswerte sind für Level 1 angegeben
- Gesundheit und Schaden steigen mit jedem Level um ca. 5%
- Cooldowns und Geschwindigkeiten bleiben konstant über alle Level

Visuelle Elemente:
- Jeder Brawler sollte eine eindeutige Silhouette haben
- Angriffe sollten visuell zur Persönlichkeit des Brawlers passen
- Farbcodierung: Sharpshooter (Blau), Tank (Rot), Support (Grün), Assassin (Lila), Thrower (Orange)

Implementiere diese Charaktere als abgeleitete Klassen von der Basis-Brawler-Klasse
mit ihren einzigartigen Fähigkeiten und Eigenschaften.
*/
