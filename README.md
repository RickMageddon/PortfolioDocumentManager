# 📚 Portfolio Document Manager

Een moderne, cross-platform desktop applicatie voor het beheren van portfolio items en het genereren van verantwoordingsdocumenten voor Technisc### 📋 Vereisten

### Systeem Vereisten
- **Windows**: Windows 10 of hoger
  - **⚠️ BELANGRIJK voor .exe gebruikers**: Voor PDF generatie heb je GTK3-Runtime nodig
  - Download en installeer: [GTK3-Runtime Win64](https://github.com/tschoonj/GTK-for-Windows-Runtime-Environment-Installer/releases)
  - Zonder GTK3 kun je de app gebruiken, maar geen PDFs genereren
- **macOS**: macOS 10.14 of hoger  
- **Linux**: Ubuntu 18.04+ / vergelijkbare distributies

### Voor Development
- Python 3.11 of hoger
- Tkinter (meestal pre-installed met Python)
- Zie `Release_version/requirements.txt` voor alle dependencies

### Dependencies
De applicatie gebruikt:
- **Tkinter**: Voor de betrouwbare cross-platform UI
- **Markdown**: Voor document conversie
- **WeasyPrint**: Voor PDF generatie (vereist GTK3 op Windows)
- **Andere**: Zie `Release_version/requirements.txt` voor complete lijstdenten van de Hogeschool Utrecht.

![Platform Support](https://img.shields.io/badge/platform-Windows%20%7C%20macOS%20%7C%20Linux-blue)
![Python Version](https://img.shields.io/badge/python-3.11%2B-blue)
![License](https://img.shields.io/badge/license-MIT-green)
![Version](https://img.shields.io/badge/version-2.0-brightgreen)
![Visitors](https://visitor-badge.laobi.icu/badge?page_id=RickMageddon.PortfolioDocumentManager)

> **⚠️ Belangrijke opmerking**: De Flet-versie is **on hold / gestopt**. De **Tkinter-versie** (in `Release_version/`) is nu de **aanbevolen en actief ondersteunde versie**.


## ✨ Features

### 📋 Portfolio Beheer
- **Portfolio Items Toevoegen**: Voeg eenvoudig nieuwe portfolio items toe met titel, beschrijving en GitHub links
- **Leeruitkomsten Selectie**: Kies uit 9 leeruitkomsten per semester met beschrijvingen
- **Type Onderscheid**: Onderscheid tussen persoonlijke opdrachten en groepswerk
- **Groepsbeheer**: Beheer groepsleden voor groepsopdrachten
- **Semester Ondersteuning**: Dynamische leeruitkomsten voor Semester 2, 3 en 4

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
- **Betrouwbare Interface**: Stabiele GUI gebouwd met Tkinter
- **Cross-platform**: Werkt naadloos op Windows, macOS en Linux
- **Data Persistentie**: Automatisch opslaan in JSON formaat
- **Import/Export**: Backup en herstel functionaliteit
- **Instellingenmenu**: Eenvoudig je semester wijzigen

## 🚀 Quick Start

### Download & Installatie

#### 🎯 Voor Eindgebruikers (Aanbevolen)

1. **Ga naar de [Releases pagina](https://github.com/RickMageddon/portfolio-document-manager/releases)**

2. **Download het archief voor jouw platform:**
   - **Windows**: `PortfolioDocumentManager-tkinter-windows.zip`
   - **macOS**: `PortfolioDocumentManager-tkinter-macos.tar.gz`  
   - **Linux**: `PortfolioDocumentManager-tkinter-linux.tar.gz`

3. **⚠️ Windows gebruikers: Installeer GTK3-Runtime (alleen voor PDF generatie):**
   - Download: [GTK3-Runtime Win64 Installer](https://github.com/tschoonj/GTK-for-Windows-Runtime-Environment-Installer/releases)
   - Installeer de nieuwste versie
   - Dit is **alleen nodig voor PDF generatie** - de rest van de app werkt zonder GTK3

4. **Installeer de applicatie:**
   - Pak het archief uit
   - Open een terminal in de uitgepakte map
   - Installeer dependencies:
     ```bash
     pip install -r requirements.txt
     ```

5. **Start de applicatie:**
   ```bash
   python Release_version/main.py
   ```

6. **Eerste keer opstarten:**
   - Vul je studentgegevens in (inclusief semester)
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
   pip install -r Release_version/requirements.txt
   ```

3. **Start de applicatie:**
   ```bash
   python Release_version/main.py
   ```

## 🆕 Nieuw in v2.0 - Back to the Roots

### 🔄 Terug naar Tkinter
- **Betrouwbare Basis**: Terug naar de stabiele en beproefde Tkinter GUI
- **Flet on Hold**: De Flet-versie is gestopt voor nu, focus op stabiliteit
- **Production Ready**: Volledig geteste en betrouwbare interface

### 📚 Dynamische Leeruitkomsten per Semester
- **Semester 2 Ondersteuning**: Volledige leeruitkomsten voor semester 2
- **Semester 3 Ondersteuning**: Volledige leeruitkomsten voor semester 3
- **Semester 4 Ondersteuning**: Volledige leeruitkomsten voor semester 4
- **Automatische Selectie**: Kies je semester en krijg automatisch de juiste leeruitkomsten

### ⚙️ Instellingenmenu
- **Semester Selectie**: Wijzig je semester via het nieuwe Instellingen menu
- **Direct Effect**: Leeruitkomsten worden direct bijgewerkt na wijziging
- **Persistent**: Je semesterkeuze wordt opgeslagen

### ✨ Verbeteringen
- **Verbeterde Stabiliteit**: Robuuste tkinter-based interface
- **Better Error Handling**: Uitgebreide foutafhandeling
- **Enhanced UI**: Geoptimaliseerde gebruikersinterface
- **Automated Releases**: Volledig geautomatiseerde build en release pipeline voor alle platforms

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
├── Release_version/         # Actieve Tkinter versie (v2.0)
│   ├── main.py             # Hoofd applicatie
│   ├── requirements.txt    # Python dependencies
│   └── ...                 # Overige bestanden
├── Legacy/                 # Oude versie (v1.0)
├── main_flet.py            # Flet versie (ON HOLD)
├── README.md               # Deze documentatie
├── CHANGELOG.md            # Versie geschiedenis
└── .github/workflows/      # GitHub Actions CI/CD
```

### Versie Informatie
- **Actief**: `Release_version/` - Tkinter versie 2.0 (aanbevolen)
- **On Hold**: `main_flet.py` - Flet versie (gestopt)
- **Legacy**: `Legacy/` - Oude Tkinter versie 1.0

## 📋 Vereisten

### Systeem Vereisten
- **Windows**: Windows 10 of hoger
- **macOS**: macOS 10.14 of hoger  
- **Linux**: Ubuntu 18.04+ / vergelijkbare distributies

### Voor Development
- Python 3.11 of hoger
- Tkinter (meestal pre-installed met Python)
- Zie `Release_version/requirements.txt` voor alle dependencies

### Dependencies
De applicatie gebruikt:
- **Tkinter**: Voor de betrouwbare cross-platform UI
- **Markdown**: Voor document conversie
- **WeasyPrint**: Voor PDF generatie
- **Andere**: Zie `Release_version/requirements.txt` voor complete lijst


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

- TI docenten voor feedback en requirements
- Alle studenten die de applicatie testen en feedback geven

---

**Gemaakt met ❤️ voor HU studenten**

*Versie 2.0 - Back to the Roots - Powered by Tkinter - Ontwikkeld door Rick van der Voort*
