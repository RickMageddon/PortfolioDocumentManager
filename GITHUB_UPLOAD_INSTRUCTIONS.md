# 🚀 GitHub Upload Instructies

## Stap 1: Repository maken op GitHub

1. Ga naar [github.com](https://github.com) en log in
2. Klik op "New repository" 
3. Repository naam: `portfolio-document-manager`
4. Beschrijving: `Cross-platform desktop applicatie voor het beheren van portfolio items en genereren van verantwoordingsdocumenten voor TI studenten`
5. Selecteer "Public"
6. **NIET** aanvinken: "Add a README file", "Add .gitignore", "Choose a license" (we hebben deze al)
7. Klik "Create repository"

## Stap 2: Remote toevoegen en pushen

```bash
# In de project directory:
git remote add origin https://github.com/JOUW-GEBRUIKERSNAAM/portfolio-document-manager.git
git branch -M main
git push -u origin main
```

## Stap 3: Eerste release maken

1. Ga naar je GitHub repository
2. Klik op "Releases" → "Create a new release"
3. Tag: `v1.0.0`
4. Release title: `Portfolio Document Manager v1.0.0`
5. Beschrijving:
```markdown
🎉 Eerste officiële release van Portfolio Document Manager!

## 🌟 Features
- Cross-platform desktop applicatie (Windows, macOS, Linux)
- Portfolio items beheer met leeruitkomsten
- Feedback systeem voor docenten en experts
- Automatische PDF/Markdown document generatie
- Moderne GUI interface

## 📦 Downloads

### Voor Eindgebruikers (Aanbevolen)
Kies het juiste **executable bestand** voor jouw platform:
- **Windows**: Download `PortfolioManager-windows.exe`
- **macOS**: Download `PortfolioManager-macos`
- **Linux**: Download `PortfolioManager-linux`

### Voor Developers
- **Source code (zip)**: Volledige broncode in ZIP formaat
- **Source code (tar.gz)**: Volledige broncode in TAR.GZ formaat

## 🚀 Installatie

### Executable (Eindgebruikers)
1. Download het juiste executable bestand voor jouw platform
2. Op macOS/Linux: `chmod +x PortfolioManager-*`
3. Start de applicatie - klaar!

### Vanuit Source Code (Developers)
1. Download en extract de source code
2. `pip install -r requirements.txt`
3. `python main.py`

Zie de [README](https://github.com/JOUW-GEBRUIKERSNAAM/portfolio-document-manager/blob/main/README.md) voor volledige documentatie.
```

6. Klik "Publish release"

## Stap 4: Monitor de automatische builds

1. **Onmiddellijk na het maken van de release:**
   - Ga naar: Repository → **Actions** tab
   - Je ziet een nieuwe workflow run genaamd "Build and Release"
   - Deze start binnen 10-30 seconden

2. **Voortgang volgen:**
   - Klik op de workflow run om details te zien
   - 3 parallelle jobs draaien (Windows, macOS, Linux)
   - Elke job duurt ~3-5 minuten

3. **Wanneer klaar:**
   - Ga terug naar je **Releases** pagina
   - De executable bestanden zijn automatisch toegevoegd!
   - Gebruikers kunnen nu downloaden

### ⏱️ Verwachte timing:

Na het maken van de v1.0.0 tag zal GitHub Actions **onmiddellijk** automatisch:
- Builds maken voor Windows, macOS en Linux (duurt ~5-15 minuten totaal)
- Executables toevoegen aan de release
- Gebruikers kunnen direct downloaden!

### ⏱️ Timing van de builds:
- **Start**: Binnen 10-30 seconden na het maken van de tag
- **Windows build**: ~3-5 minuten
- **macOS build**: ~3-5 minuten  
- **Linux build**: ~2-4 minuten
- **Release update**: ~1 minuut
- **Totaal**: Ongeveer 5-15 minuten voor alle platforms

Je kunt de voortgang volgen via: Repository → Actions tab

**Let op**: GitHub voegt automatisch ook source code archives toe (ZIP + TAR.GZ). Dit is normaal gedrag en handig voor developers. Eindgebruikers moeten de executable bestanden downloaden, niet de source code archives.

## Stap 5: Testen

1. Ga naar je release pagina
2. Download de executable voor jouw platform
3. Test of deze werkt
4. Deel de link met gebruikers!

## 🎯 Resultaat

Gebruikers zien in de GitHub release:

### ✅ **Download deze bestanden (voor eindgebruikers):**
- `PortfolioManager-windows.exe` ← Windows gebruikers
- `PortfolioManager-macos` ← macOS gebruikers  
- `PortfolioManager-linux` ← Linux gebruikers

### ℹ️ **GitHub voegt automatisch toe (voor developers):**
- `Source code (zip)` ← Automatisch toegevoegd door GitHub
- `Source code (tar.gz)` ← Automatisch toegevoegd door GitHub

**Eindgebruikers hoeven alleen de executable bestanden te downloaden!**

Gebruikers hoeven nu alleen maar:
1. Naar je GitHub releases gaan
2. De juiste **executable** downloaden (niet source code!)
3. Het bestand starten
4. Klaar! ✨

**Repository URL**: `https://github.com/JOUW-GEBRUIKERSNAAM/portfolio-document-manager`
**Releases URL**: `https://github.com/JOUW-GEBRUIKERSNAAM/portfolio-document-manager/releases`
