# 📚 Portfolio Document Manager

Een professionele desktop applicatie voor het beheren van portfolio items en het genereren van verantwoordingsdocumenten voor Technische Informatica studenten van de Hogeschool Utrecht.

![Platform Support](https://img.shields.io/badge/platform-Windows%20%7C%20macOS%20%7C%20Linux-blue)
![Python Version](https://img.shields.io/badge/python-3.8%2B-blue)
![License](https://img.shields.io/badge/license-MIT-green)

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
- **Intuïtieve Interface**: Moderne GUI gebouwd met Tkinter
- **Data Persistentie**: Automatisch opslaan in JSON formaat
- **Import/Export**: Backup en herstel functionaliteit
- **Cross-platform**: Werkt op Windows, macOS en Linux

## 🚀 Quick Start

### Download & Installatie

#### 🎯 Voor Eindgebruikers (Aanbevolen)

1. **Ga naar de [Releases pagina](https://github.com/RickMageddon/portfolio-document-manager/releases)**

2. **Download de executable voor jouw platform:**
   - **Windows**: `PortfolioManager-windows.exe`
   - **macOS**: `PortfolioManager-macos`  
   - **Linux**: `PortfolioManager-linux`
   
   ⚠️ **Let op**: Download de executable bestanden, niet de "Source code" ZIP/TAR.GZ files (die zijn voor developers)

3. **Start de applicatie:**
   - Windows: Dubbelklik op het .exe bestand
   - macOS/Linux: Maak executable en run via terminal:
     ```bash
     chmod +x PortfolioManager-*
     ./PortfolioManager-*
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
   python main.py
   ```

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
├── main.py                    # Hoofd applicatie
├── requirements.txt           # Python dependencies
├── build.py                  # Build script voor executables
├── .gitignore               # Git ignore regels
├── README.md                # Deze documentatie
└── dist/                    # Gegenereerde executables
```

## 📋 Vereisten

### Systeem Vereisten
- **Windows**: Windows 10 of hoger
- **macOS**: macOS 10.14 of hoger  
- **Linux**: Ubuntu 18.04+ / vergelijkbare distributies

### Voor Development
- Python 3.8 of hoger
- tkinter (meestal standaard geïnstalleerd)
- Zie `requirements.txt` voor alle dependencies

## 🆘 Probleemoplossing

### Veelvoorkomende Problemen

**PDF generatie mislukt**
- Zorg dat alle tekstvelden zijn ingevuld
- Controleer of de reflectievragen zijn beantwoord

**Applicatie start niet**
- Controleer of je de juiste executable hebt gedownload voor je platform
- Op macOS/Linux: zorg dat het bestand executable permissions heeft

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

*Versie 1.0 - Ontwikkeld door Rick van der Voort*
