# Changelog

Alle belangrijke wijzigingen aan dit project worden gedocumenteerd in dit bestand.

Het formaat is gebaseerd op [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
en dit project volgt [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [2.0.0] - 2025-10-09

### 🔄 Belangrijke Wijzigingen
- **Back to Tkinter**: Terug naar de betrouwbare en stabiele Tkinter GUI
- **Flet versie on hold**: De Flet-versie is gestopt voor nu, focus op stabiliteit en betrouwbaarheid
- **Production Ready**: Volledig geteste en robuuste interface

### ✨ Added
- 📚 **Dynamische leeruitkomsten per semester**: Volledige ondersteuning voor Semester 2, 3 en 4
- ⚙️ **Instellingenmenu**: Nieuw menu om je semester te wijzigen
- 🎯 **Semester-specifieke leeruitkomsten**: Elke semester heeft zijn eigen set van 9 leeruitkomsten met competenties
- 🔄 **Automatische leeruitkomsten laden**: Bij wijziging van semester worden direct de juiste leeruitkomsten geladen
- 📝 **Semester in document**: Het gekozen semester wordt getoond in het gegenereerde document
- 🚀 **Automated GitHub Actions**: Volledig geautomatiseerde build en release pipeline voor Windows, Linux en macOS

### 🎨 Changed
- **UI Framework**: Van experimentele Flet terug naar stabiele Tkinter
- **Semester Selectie**: Nu prominent aanwezig in instellingen en studentgegevens
- **Leeruitkomsten Structuur**: Gerefactored voor betere ondersteuning van meerdere semesters
- **Menu Structuur**: Toegevoegd Instellingen menu naast Help, Feedback en Leeruitkomsten Info

### 🔧 Technical Details
- Python 3.11+ ondersteuning
- Tkinter GUI framework (stable en betrouwbaar)
- Markdown library voor document conversie
- WeasyPrint voor PDF generatie
- JSON voor data opslag
- Semester-based learning outcomes system met dynamische loading
- GitHub Actions voor cross-platform builds

### 📚 Semester Leeruitkomsten
**Semester 2**: 9 leeruitkomsten gericht op IoT en samenwerking
**Semester 3**: 9 leeruitkomsten gericht op hybride systemen en vermogens
**Semester 4**: 9 leeruitkomsten gericht op Digital Twins en professionalisering

### 🐛 Fixed
- Verbeterde error handling bij ontbrekende data
- Correcte initialisatie van GUI componenten
- Mainloop startup issues opgelost
- Semester persistentie bij herstart van de applicatie

### 🗑️ Deprecated
- Flet versie (`main_flet.py`) is on hold / gestopt
- Oude semester-specifieke hardcoded leeruitkomsten

## [1.0.0] - 2025-07-09

### Added
- 🎉 Eerste release van Portfolio Document Manager
- 📋 Portfolio items beheer (toevoegen, bewerken, verwijderen)
- 🎯 9 leeruitkomsten voor TI S4 met beschrijvingen en voorbeelden
- 💬 Feedback systeem voor elk portfolio item
- 📄 PDF en Markdown document generatie
- 👥 Ondersteuning voor groepsopdrachten met groepsleden beheer
- ⚠️ "BELANGRIJK" waarschuwingen voor items zonder feedback
- 🎨 Professionele GUI met Tkinter
- 💾 JSON data persistentie
- 📤 Import/Export functionaliteit
- 🖥️ Cross-platform ondersteuning (Windows, macOS, Linux)
- 🔧 PyInstaller executable generatie
- 📚 Uitgebreide documentatie en README
- 🏷️ Tooltips voor leeruitkomsten met voorbeelden
- 🎨 Mooie PDF styling met CSS
- 🔄 Automatische data opslag
- ✅ Validatie van verplichte velden
- 🎯 Feedback counter per portfolio item
- 📱 Responsive interface design

### Technical Details
- Python 3.8+ ondersteuning
- Tkinter GUI framework
- Markdown library voor document conversie
- WeasyPrint voor PDF generatie
- JSON voor data opslag
- PyInstaller voor executable packaging

### Known Issues
- Geen bekende issues in deze release

## [Unreleased]

### Planned Features
- 🔐 GitHub integratie voor automatische link validatie
- 📊 Portfolio voortgang dashboard
- 🔄 Automatische backup functionaliteit
- 📧 Email export van documenten
- 📚 Uitbreiden naar meer semesters (5-8)
- 🎨 Verdere UI verbeteringen in Tkinter

---

Voor oudere versies of meer details, zie de [GitHub releases](https://github.com/rickmageddon/portfolio-document-manager/releases).
