# 🔧 Lokale DLL Fix voor Windows

## Probleem
De .exe kan de GTK3 DLLs niet vinden, zelfs als ze geïnstalleerd zijn in `C:\Program Files\GTK3-Runtime Win64\bin`.

## Oplossing: Kopieer DLLs naast de .exe

### Stap 1: Kopieer alle GTK3 DLLs
Open PowerShell en run dit commando:

```powershell
# Ga naar de folder waar je .exe staat
cd "pad\naar\je\exe\folder"

# Kopieer alle DLLs van GTK3 naar de huidige folder
Copy-Item "C:\Program Files\GTK3-Runtime Win64\bin\*.dll" -Destination . -Force
```

### Stap 2: Test de .exe
Dubbelklik op `PortfolioDocumentManager.exe` en probeer een PDF te genereren.

## Welke DLLs zijn nodig?

De belangrijkste DLLs die WeasyPrint nodig heeft:
- `libgobject-2.0-0.dll` ✅ (al toegevoegd)
- `libglib-2.0-0.dll`
- `libcairo-2.0.dll`
- `libcairo-gobject-2.0.dll`
- `libpango-1.0-0.dll`
- `libpangocairo-1.0-0.dll`
- `libpangoft2-1.0-0.dll`
- `libpangowin32-1.0-0.dll`
- `libfontconfig-1.dll`
- `libfreetype-6.dll`
- `libpixman-1-0.dll`
- `libpng16-16.dll`
- `zlib1.dll`
- En alle dependencies...

**TIP**: Kopieer gewoon ALLE .dll bestanden van de GTK3 bin folder. Het zijn er ~60, maar dan weet je zeker dat alles werkt!

## Wat doet de nieuwe code?

De aangepaste `main.py` zoekt nu op deze locaties naar GTK3 DLLs:

1. **Dezelfde folder als de .exe** 👈 BESTE OPTIE!
2. `<exe folder>/gtk-runtime/bin` (voor subfolder)
3. Dezelfde folder als het script
4. `<script folder>/gtk-runtime/bin`
5. `C:\Program Files\GTK3-Runtime Win64\bin` (systeeminstallatie)

## In de volgende GitHub release

De GitHub Actions workflow zal automatisch:
1. Alle GTK3 DLLs installeren via Chocolatey
2. Alle DLLs kopiëren naar de dist folder (naast de .exe)
3. Ook `main.py` + `requirements.txt` meepakken als fallback
4. Alles inpakken in een zip

Gebruikers hoeven dan alleen de zip uit te pakken en de .exe te starten! 🎉
