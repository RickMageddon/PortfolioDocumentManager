# 📚 Portfolio Document Manager

Een moderne, cross-platform desktop applicatie voor het beheren van portfolio items en het genereren van verantwoordingsdocumenten voor Technische Informatica studenten van de Hogeschool Utrecht.

![Platform Support](https://img.shields.io/badge/platform-Windows%20%7C%20macOS%20%7C%20Linux-blue)
![Python Version](https://img.shields.io/badge/python-3.8%2B-blue)
![License](https://img.shields.io/badge/license-MIT-green)
![Version](https://img.shields.io/badge/version-1.5.0-brightgreen)

## ✨ Features

### 📋 Portfolio Beheer
- **Portfolio Items Toevoegen**: Voeg eenvoudig nieuwe portfolio items toe met titel, beschrijving en GitHub links
- **Leeruitkomsten Selectie**: Kies uit 9 voorgedefinieerde leeruitkomsten met tooltips en voorbeelden
- **Type Onderscheid**: Onderscheid tussen persoonlijke opdrachten en groepswerk
- **Groepsbeheer**: Beheer groepsleden voor groepsopdrachten

### 💬 Feedback Systeem
- **Feedback Toevoegen**: Voeg feedback toe van docenten, experts en medestudenten
- **Feedback Beheren**: Bewerk en verwijder bestaande feedback
- **Visuele Indicatoren**: Zie direct hoeveel feedback elk item heeft
- **Belangrijke Meldingen**: Krijg waarschuwingen voor items zonder feedback

### 📄 Document Generatie
- **PDF Generatie**: Automatische generatie van professioneel vormgegeven PDF documenten
- **Markdown Export**: Optionele export naar markdown formaat
- **Styling**: Mooie opmaak met kleuren, borders en typography
- **Template Gebaseerd**: Gebaseerd op officiële HU TI templates

### 🎯 Gebruikersvriendelijk
- **Moderne Interface**: Prachtige GUI gebouwd met Flet (Flutter-gebaseerd framework)
- **Cross-platform Native Look**: Ziet er native uit op elk platform
- **Responsive Design**: Interface past zich aan verschillende schermgroottes aan
- **Data Persistentie**: Automatisch opslaan in JSON formaat
- **Import/Export**: Backup en herstel functionaliteit
- **Cross-platform**: Werkt naadloos op Windows, macOS en Linux

## 🚀 Quick Start

### Download & Installatie

#### 🎯 Voor Eindgebruikers (Aanbevolen)

1. **Ga naar de [Releases pagina](https://github.com/RickMageddon/portfolio-document-manager/releases)**

2. **Download de executable voor jouw platform:**
   - **Windows**: `PortfolioManager-v1.5.0-windows-x64.exe`
   - **macOS**: `PortfolioManager-v1.5.0-macos-x64`  
   - **Linux**: `PortfolioManager-v1.5.0-linux-x64`
   
   ⚠️ **Let op**: Download de executable bestanden, niet de "Source code" ZIP/TAR.GZ files (die zijn voor developers)

3. **Start de applicatie:**
   - **Windows**: Dubbelklik op het .exe bestand
   - **macOS/Linux**: Maak executable en run via terminal:
     ```bash
     chmod +x PortfolioManager-v1.5.0-*
     ./PortfolioManager-v1.5.0-*
     ```

4. **Eerste keer opstarten:**
   - Vul je studentgegevens in
   - Begin met het toevoegen van portfolio items
   - Vraag feedback en genereer je document!

#### 🛠️ Voor Developers (Vanuit Source Code)

1. **Clone de repository:**
   ```bash
   git clone https://github.com/RickMageddon/portfolio-document-manager.git
   cd portfolio-document-manager
   ```

2. **Installeer dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Start de applicatie:**
   ```bash
   python main_flet.py
   ```

## 🆕 Nieuw in v1.5.0

### 🎨 Complete UI Overhaul met Flet
- **Migratie naar Flet**: Volledig herontworpen met Google's Flutter-gebaseerde Flet framework
- **Moderne Look**: Prachtige Material Design interface
- **Native Performance**: Betere prestaties en responsiviteit
- **Cross-platform Consistency**: Identieke ervaring op alle platforms

### ✨ Nieuwe Features
- **Verbeterde Gebruikersinterface**: Intuïtievere navigatie en cleaner design
- **Enhanced Data Management**: Verbeterde data persistentie en error handling
- **Better Feedback System**: Geoptimaliseerde feedback workflows
- **Improved Build System**: Automatische builds voor alle platforms via GitHub Actions

### 🔧 Technische Verbeteringen
- **Moderne Tech Stack**: Van Tkinter naar Flet voor toekomstbestendigheid
- **Better Code Structure**: Gerefactorde codebase voor onderhoudbaarheid
- **Enhanced Error Handling**: Robuustere foutafhandeling
- **Automated Releases**: Volledig geautomatiseerde build en release pipeline

## 📖 Gebruikshandleiding

### 1. Student Gegevens Instellen
Bij eerste gebruik vul je je basisgegevens in:
- Naam
- Studentnummer  
- Semester (2-8)
- Peilmoment (1-4)

### 2. Portfolio Items Toevoegen
1. Klik op "Nieuw Portfolio Item Toevoegen"
2. Vul de titel in
3. Selecteer relevante leeruitkomsten
4. Kies tussen persoonlijk of groepswerk
5. Voeg GitHub link en beschrijving toe
6. Sla op

### 3. Feedback Beheren
1. Ga naar "Portfolio Items Beheren"
2. Selecteer een item en klik "Bewerken"
3. Scroll naar de feedback sectie
4. Voeg feedback toe van docenten/experts
5. Gebruik de feedback in je verantwoording

### 4. Document Genereren
1. Klik op "Document Inleveren"
2. Beantwoord de reflectievragen
3. Bevestig dat je portfolio compleet is
4. Kies optioneel voor markdown export
5. Genereer je document!

## 🎨 Screenshots

*Screenshots komen binnenkort...*

## 🔧 Development

### Build van Source
```bash
# Installeer build dependencies
pip install -r requirements.txt

# Build executable
python build.py
```

### Project Structuur
```
portfolio-document-manager/
├── main_flet.py              # Hoofd applicatie (Flet UI)
├── requirements.txt          # Python dependencies
├── build.py                 # Build script voor executables
├── .gitignore              # Git ignore regels
├── README.md               # Deze documentatie
├── .github/workflows/      # GitHub Actions CI/CD
└── release/                # Gegenereerde executables
```

### Legacy Files
- `main.py`: Oude Tkinter versie (deprecated vanaf v1.5.0)

## 📋 Vereisten

### Systeem Vereisten
- **Windows**: Windows 10 of hoger
- **macOS**: macOS 10.14 of hoger  
- **Linux**: Ubuntu 18.04+ / vergelijkbare distributies

### Voor Development
- Python 3.8 of hoger
- Flet framework voor UI (automatisch geïnstalleerd via requirements.txt)
- Zie `requirements.txt` voor alle dependencies

### Dependencies
De applicatie gebruikt:
- **Flet**: Voor de moderne cross-platform UI
- **PyInstaller**: Voor het bouwen van executables
- **Andere**: Zie `requirements.txt` voor complete lijst

## 🆘 Probleemoplossing

### Veelvoorkomende Problemen

**PDF generatie mislukt**
- Zorg dat alle tekstvelden zijn ingevuld
- Controleer of de reflectievragen zijn beantwoord

**Applicatie start niet**
- Controleer of je de juiste executable hebt gedownload voor je platform
- Download de executable files, niet de source code ZIP
- Op Windows: mogelijk Windows Defender waarschuwing (klik "Meer info" → "Toch uitvoeren")
- Op macOS/Linux: zorg dat het bestand executable permissions heeft (`chmod +x`)

**Flet/UI problemen**
- Zorg dat je een actieve internetverbinding hebt bij eerste start
- Bij problemen: herstart de applicatie
- Controleer of Flet dependencies correct zijn geïnstalleerd

**Data kwijt**
- Data wordt opgeslagen in `portfolio_data.json`
- Maak regelmatig backups via "Data exporteren"

**Groepsleden veld verschijnt niet**
- Selecteer eerst "Groepswerk" bij Type opdracht
- Het veld verschijnt automatisch onder de radiobuttons

## 🤝 Bijdragen

Bijdragen zijn welkom! Volg deze stappen:

1. Fork het project
2. Maak een feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit je wijzigingen (`git commit -m 'Add some AmazingFeature'`)
4. Push naar de branch (`git push origin feature/AmazingFeature`)
5. Open een Pull Request

## 📞 Support & Feedback

- **Developer**: Rick van der Voort
- **Website**: [rickmageddon.com](https://rickmageddon.com)
- **Issues & Support**: [GitHub Issues](https://github.com/RickMageddon/PortfolioDocumentManager/issues)

Voor bugs, feature requests, vragen of feedback - maak een issue aan op GitHub!

## 📄 Licentie

Dit project is gelicentieerd onder de MIT License - zie het [LICENSE](LICENSE) bestand voor details.

## 🙏 Dankbetuigingen

- Hogeschool Utrecht voor de template specificaties
- TI docenten voor feedback en requirements
- Alle studenten die de applicatie testen en feedback geven

---

**Gemaakt met ❤️ voor HU Technische Informatica studenten**

*Versie 1.5.0 - Powered by Flet - Ontwikkeld door Rick van der Voort*
