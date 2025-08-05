#!/usr/bin/env python3
"""
Portfolio Document Manager - Standalone Version
Minimal implementation without Flet auto-installation issues
"""
import sys
import os
import json
import datetime
import webbrowser
import subprocess
import tempfile
from pathlib import Path

# Prevent any automatic package installation
os.environ['PIP_DISABLE_PIP_VERSION_CHECK'] = '1'
os.environ['PIP_NO_CACHE_DIR'] = '1'
os.environ['PIP_NO_INPUT'] = '1'

class PortfolioManagerStandalone:
    def __init__(self):
        self.version = "1.5.10"
        self.data_file = "portfolio_data.json"
        self.student_info = {}
        self.portfolio_items = []
        self.load_data()
    
    def load_data(self):
        """Load data from JSON file"""
        try:
            if os.path.exists(self.data_file):
                with open(self.data_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    self.student_info = data.get('student_info', {})
                    self.portfolio_items = data.get('portfolio_items', [])
        except Exception as e:
            print(f"Error loading data: {e}")
    
    def save_data(self):
        """Save data to JSON file"""
        try:
            data = {
                'student_info': self.student_info,
                'portfolio_items': self.portfolio_items
            }
            with open(self.data_file, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
        except Exception as e:
            print(f"Error saving data: {e}")
    
    def show_menu(self):
        """Show main menu"""
        while True:
            print("\n" + "="*60)
            print(f"Portfolio Document Manager v{self.version}")
            print("="*60)
            
            if self.student_info:
                print(f"Student: {self.student_info.get('name', 'Unknown')}")
                print(f"Nummer: {self.student_info.get('student_number', 'Unknown')}")
                print(f"Semester {self.student_info.get('semester', '?')} - Peilmoment {self.student_info.get('milestone', '?')}")
            else:
                print("Geen studentgegevens ingesteld")
            
            print(f"\nPortfolio items: {len(self.portfolio_items)}")
            items_with_feedback = sum(1 for item in self.portfolio_items if item.get('feedback'))
            print(f"Items met feedback: {items_with_feedback}")
            
            print("\nMenu opties:")
            print("1. Student gegevens instellen/wijzigen")
            print("2. Portfolio item toevoegen")
            print("3. Portfolio items bekijken")
            print("4. Feedback toevoegen")
            print("5. Alle feedback bekijken")
            print("6. Document genereren")
            print("7. Data exporteren/importeren")
            print("8. Web versie starten (als Flet werkt)")
            print("0. Afsluiten")
            
            choice = input("\nKies een optie (0-8): ").strip()
            
            if choice == '0':
                print("Afsluiten...")
                break
            elif choice == '1':
                self.setup_student_info()
            elif choice == '2':
                self.add_portfolio_item()
            elif choice == '3':
                self.view_portfolio_items()
            elif choice == '4':
                self.add_feedback()
            elif choice == '5':
                self.view_all_feedback()
            elif choice == '6':
                self.generate_document()
            elif choice == '7':
                self.data_management()
            elif choice == '8':
                self.try_web_version()
            else:
                print("Ongeldige keuze!")
    
    def setup_student_info(self):
        """Setup student information"""
        print("\n" + "="*40)
        print("Student Gegevens")
        print("="*40)
        
        name = input(f"Naam [{self.student_info.get('name', '')}]: ").strip()
        if name:
            self.student_info['name'] = name
        
        number = input(f"Studentnummer [{self.student_info.get('student_number', '')}]: ").strip()
        if number:
            self.student_info['student_number'] = number
        
        semester = input(f"Semester (2-8) [{self.student_info.get('semester', '2')}]: ").strip()
        if semester and semester.isdigit() and 2 <= int(semester) <= 8:
            self.student_info['semester'] = semester
        
        milestone = input(f"Peilmoment (1-4) [{self.student_info.get('milestone', '1')}]: ").strip()
        if milestone and milestone.isdigit() and 1 <= int(milestone) <= 4:
            self.student_info['milestone'] = milestone
        
        self.save_data()
        print("✅ Student gegevens opgeslagen!")
    
    def add_portfolio_item(self):
        """Add portfolio item"""
        print("\n" + "="*40)
        print("Portfolio Item Toevoegen")
        print("="*40)
        
        title = input("Titel: ").strip()
        if not title:
            print("❌ Titel is verplicht!")
            return
        
        print("\nLeeruitkomsten (1-9, gescheiden door komma's):")
        print("1=Analyseren, 2=Ontwerpen, 3=Adviseren, 4=Realiseren, 5=Beheren")
        print("6=Toekomstgericht organiseren, 7=Doelgericht interacteren, 8=Persoonlijk leiderschap, 9=Onderzoek")
        
        los_input = input("Leeruitkomsten: ").strip()
        try:
            learning_outcomes = [int(x.strip()) for x in los_input.split(',') if x.strip().isdigit() and 1 <= int(x.strip()) <= 9]
        except:
            learning_outcomes = []
        
        if not learning_outcomes:
            print("❌ Selecteer minimaal één leeruitkomst!")
            return
        
        is_group = input("Groepswerk? (j/n): ").strip().lower() == 'j'
        group_members = []
        if is_group:
            members_input = input("Groepsleden (gescheiden door komma's): ").strip()
            if members_input:
                group_members = [x.strip() for x in members_input.split(',') if x.strip()]
        
        github_link = input("GitHub link: ").strip()
        if not github_link:
            print("❌ GitHub link is verplicht!")
            return
        
        description = input("Beschrijving: ").strip()
        if not description:
            print("❌ Beschrijving is verplicht!")
            return
        
        item = {
            'title': title,
            'learning_outcomes': learning_outcomes,
            'is_group_work': is_group,
            'group_members': group_members,
            'github_link': github_link,
            'description': description,
            'date_added': datetime.datetime.now().strftime("%Y-%m-%d"),
            'feedback': []
        }
        
        self.portfolio_items.append(item)
        self.save_data()
        print("✅ Portfolio item toegevoegd!")
    
    def view_portfolio_items(self):
        """View all portfolio items"""
        if not self.portfolio_items:
            print("\n❌ Geen portfolio items gevonden!")
            return
        
        print("\n" + "="*80)
        print("Portfolio Items")
        print("="*80)
        
        for i, item in enumerate(self.portfolio_items, 1):
            print(f"\n{i}. {item.get('title', 'Geen titel')}")
            print(f"   Leeruitkomsten: {', '.join(map(str, item.get('learning_outcomes', [])))}")
            print(f"   Type: {'Groepswerk' if item.get('is_group_work') else 'Persoonlijk'}")
            print(f"   Datum: {item.get('date_added', 'Onbekend')}")
            print(f"   Feedback items: {len(item.get('feedback', []))}")
            print(f"   GitHub: {item.get('github_link', 'Geen link')}")
            print(f"   Beschrijving: {item.get('description', 'Geen beschrijving')[:100]}...")
    
    def add_feedback(self):
        """Add feedback to portfolio item"""
        if not self.portfolio_items:
            print("\n❌ Geen portfolio items om feedback aan toe te voegen!")
            return
        
        print("\n" + "="*40)
        print("Feedback Toevoegen")
        print("="*40)
        
        print("Portfolio items:")
        for i, item in enumerate(self.portfolio_items, 1):
            print(f"{i}. {item.get('title', 'Geen titel')}")
        
        try:
            choice = int(input("\nSelecteer item nummer: ")) - 1
            if choice < 0 or choice >= len(self.portfolio_items):
                print("❌ Ongeldig item nummer!")
                return
        except:
            print("❌ Ongeldig nummer!")
            return
        
        selected_item = self.portfolio_items[choice]
        available_los = selected_item.get('learning_outcomes', [])
        
        print(f"\nBeschikbare leeruitkomsten voor '{selected_item.get('title', 'Geen titel')}':")
        for lo in available_los:
            print(f"{lo}. Leeruitkomst {lo}")
        
        try:
            lo_choice = int(input("Selecteer leeruitkomst nummer: "))
            if lo_choice not in available_los:
                print("❌ Ongeldige leeruitkomst!")
                return
        except:
            print("❌ Ongeldig nummer!")
            return
        
        feedback_from = input("Feedback van (naam docent/begeleider): ").strip()
        if not feedback_from:
            print("❌ Naam is verplicht!")
            return
        
        feedback_text = input("Feedback tekst: ").strip()
        if not feedback_text:
            print("❌ Feedback tekst is verplicht!")
            return
        
        feedback_entry = {
            'from': feedback_from,
            'text': feedback_text,
            'learning_outcomes': [lo_choice],
            'date': datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
        }
        
        if 'feedback' not in selected_item:
            selected_item['feedback'] = []
        
        selected_item['feedback'].append(feedback_entry)
        self.save_data()
        print("✅ Feedback toegevoegd!")
    
    def view_all_feedback(self):
        """View all feedback"""
        feedback_found = False
        
        print("\n" + "="*80)
        print("Alle Feedback")
        print("="*80)
        
        for item in self.portfolio_items:
            if item.get('feedback'):
                feedback_found = True
                print(f"\n📁 {item.get('title', 'Geen titel')}")
                print("-" * 60)
                
                for feedback in item['feedback']:
                    print(f"   Van: {feedback.get('from', 'Onbekend')}")
                    print(f"   Datum: {feedback.get('date', 'Onbekend')}")
                    print(f"   Leeruitkomst: {', '.join(map(str, feedback.get('learning_outcomes', [])))}")
                    print(f"   Feedback: {feedback.get('text', 'Geen tekst')}")
                    print()
        
        if not feedback_found:
            print("\n❌ Geen feedback gevonden!")
    
    def generate_document(self):
        """Generate portfolio document"""
        print("\n" + "="*40)
        print("Document Genereren")
        print("="*40)
        print("Deze functie is beschikbaar in de volledige Flet versie.")
        print("Voor nu kun je de data exporteren en handmatig een document maken.")
    
    def data_management(self):
        """Data export/import"""
        print("\n" + "="*40)
        print("Data Beheer")
        print("="*40)
        print(f"Data bestand: {os.path.abspath(self.data_file)}")
        print("Je kunt dit bestand kopiëren naar een andere computer.")
        
        if os.path.exists(self.data_file):
            print(f"Bestand grootte: {os.path.getsize(self.data_file)} bytes")
        
        choice = input("\nWil je de data directory openen? (j/n): ").strip().lower()
        if choice == 'j':
            try:
                if sys.platform == 'linux':
                    subprocess.run(['xdg-open', os.path.dirname(os.path.abspath(self.data_file))])
                elif sys.platform == 'darwin':
                    subprocess.run(['open', os.path.dirname(os.path.abspath(self.data_file))])
                elif sys.platform == 'win32':
                    subprocess.run(['explorer', os.path.dirname(os.path.abspath(self.data_file))])
            except:
                print("Kon directory niet openen")
    
    def try_web_version(self):
        """Try to start web version if Flet works"""
        print("\n" + "="*40)
        print("Web Versie Proberen")
        print("="*40)
        print("Dit probeert de volledige Flet versie te starten...")
        
        try:
            # Try importing Flet in a subprocess to avoid crashing this process
            result = subprocess.run([
                sys.executable, '-c', 
                'import flet as ft; print("Flet werkt!"); '
                'ft.app(lambda page: page.add(ft.Text("Test")), view=ft.AppView.WEB_BROWSER, port=8551)'
            ], capture_output=True, text=True, timeout=10)
            
            if result.returncode == 0:
                print("✅ Flet werkt! Web versie zou moeten starten...")
            else:
                print("❌ Flet werkt niet correct")
                print(f"Error: {result.stderr}")
        except subprocess.TimeoutExpired:
            print("⚠️ Flet reageert niet binnen 10 seconden")
        except Exception as e:
            print(f"❌ Kon Flet niet testen: {e}")

def main():
    print("Portfolio Document Manager - Standalone Mode")
    print("Dit is een tekstgebaseerde versie die altijd werkt!")
    print("De volledige GUI versie heeft helaas compatibiliteitsproblemen op Linux.")
    
    app = PortfolioManagerStandalone()
    
    try:
        app.show_menu()
    except KeyboardInterrupt:
        print("\n\nAfgebroken door gebruiker.")
    except Exception as e:
        print(f"\nOnverwachte fout: {e}")
    
    print("Bedankt voor het gebruiken van Portfolio Document Manager!")

if __name__ == "__main__":
    main()
