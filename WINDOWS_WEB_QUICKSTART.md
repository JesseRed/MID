# Windows Web Version - Quick Start

## 🌐 **Einfache Browser-Version (FUNKTIONIERT!)**

Die neue `mid_web.html` Version ist viel einfacher und funktioniert zuverlässig auf Windows.

---

## 🚀 **Schnellstart (2 Methoden)**

### **Methode 1: Direkt im Browser (Einfachste)**

1. **Öffnen Sie** `mid_web.html` im Browser:
   - **Doppelklick** auf `mid_web.html`
   - ODER Rechtsklick → "Öffnen mit" → Chrome/Firefox/Edge

2. **Experiment startet automatisch!**

---

### **Methode 2: Mit lokalem Server (Empfohlen)**

```cmd
# 1. Öffnen Sie die Eingabeaufforderung im MID-Ordner
cd C:\Ihr\MID\Ordner

# 2. Starten Sie den Server
python -m http.server 8000

# 3. Öffnen Sie im Browser:
http://localhost:8000/mid_web.html
```

---

## ✅ **Was Sie sehen sollten**

1. **"Laden..."** erscheint kurz
2. **Dialog-Fenster** erscheint:
   - Teilnehmer ID eingeben
   - Session (Standard: 001)
   - "Start" klicken
3. **Experiment startet**:
   - Titel-Bildschirm
   - Anweisungen
   - Trials beginnen

---

## 🎮 **Wie man spielt**

1. **Fixationskreuz (+)** erscheint
2. **Cue-Bild** zeigt möglichen Gewinn
3. **Warten...**
4. **Zielbild** erscheint → **LEERTASTE DRÜCKEN!**
5. **Feedback**: Treffer oder Fehler
6. **Geld-Feedback**: +30 Cent, +3 Cent, oder +0 Cent

---

## 📊 **Daten speichern**

Am Ende des Experiments:
- **CSV-Datei wird automatisch heruntergeladen**
- Dateiname: `MID_WEB_<teilnehmer>_<session>_<zeitstempel>.csv`
- Speicherort: Ihr Downloads-Ordner

---

## 🔧 **Fehlerbehebung**

### **Problem: Schwarzer Bildschirm, nichts passiert**
✅ **Lösung**: Verwenden Sie Methode 2 (lokaler Server)

### **Problem: Bilder werden nicht geladen**
✅ **Lösung**: 
- Stellen Sie sicher, dass der `images/` Ordner vorhanden ist
- Verwenden Sie lokalen Server (Methode 2)

### **Problem: Tasten funktionieren nicht**
✅ **Lösung**:
- Klicken Sie auf das Browser-Fenster, um es zu fokussieren
- Versuchen Sie es mit Chrome oder Firefox
- Aktualisieren Sie die Seite (F5)

### **Problem: Python nicht gefunden**
✅ **Lösung**:
- Installieren Sie Python von: https://www.python.org/downloads/
- Oder verwenden Sie einfach Methode 1 (kein Python nötig)

---

## 🌐 **Empfohlene Browser**

| Browser | Version | Status |
|---------|---------|--------|
| **Chrome** | 90+ | ✅ Beste Wahl |
| **Firefox** | 88+ | ✅ Sehr gut |
| **Edge** | 90+ | ✅ Sehr gut |
| **Safari** | 14+ | ✅ Gut |

---

## 📁 **Benötigte Dateien**

Stellen Sie sicher, dass diese Dateien im selben Ordner sind:

```
C:\MID\
├── mid_web.html          ← Diese Datei öffnen!
├── mid_web.js
├── mid_config.yml
├── text_content.yml
└── images\
    ├── Cue00.png
    ├── Cue03.png
    ├── Cue30.png
    ├── Target.png
    ├── PerformanceFeedbackPositiv.png
    ├── PerformanceFeedbackNegativ.png
    └── schatztruhebw.png
```

---

## 🎯 **Testlauf**

### **Schneller Test:**
1. Doppelklick auf `mid_web.html`
2. Teilnehmer: `test`
3. Session: `001`
4. Start klicken
5. Beliebige Taste drücken (Anweisungen)
6. Leertaste bei Ziel drücken
7. Experiment läuft!

---

## ⚡ **Vorteile dieser Version**

- ✅ **Keine Installation nötig**
- ✅ **Funktioniert sofort**
- ✅ **Einfach zu bedienen**
- ✅ **Zuverlässige Tastenerkennung**
- ✅ **Automatischer CSV-Download**
- ✅ **Funktioniert auf jedem Computer**

---

## 🆚 **Unterschied zu mid_psychojs.html**

| Feature | mid_web.html | mid_psychojs.html |
|---------|--------------|-------------------|
| **Funktioniert?** | ✅ Ja, sofort | ❌ Probleme |
| **Installation** | ❌ Keine | ❌ Keine |
| **Komplexität** | ✅ Einfach | ❌ Komplex |
| **Empfohlen** | ✅✅✅ JA | ❌ Nein |

**→ Verwenden Sie `mid_web.html`!**

---

## 🎉 **Los geht's!**

```cmd
# Einfachste Methode:
1. Doppelklick auf mid_web.html
2. Dialog ausfüllen
3. Start!

# Beste Methode:
cd C:\Ihr\MID\Ordner
python -m http.server 8000
# Dann im Browser: http://localhost:8000/mid_web.html
```

**Viel Erfolg mit dem Experiment!** 🚀

