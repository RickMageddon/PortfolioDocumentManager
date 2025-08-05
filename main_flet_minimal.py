#!/usr/bin/env python3
"""
Portfolio Document Program - Minimal Flet Version
Een programma voor het beheren van portfolio items voor het TI S4 verantwoordingsdocument.
Optimized for PyInstaller with minimal icon usage to avoid enum loading issues.
"""

import sys
import os
import json
import datetime
import webbrowser
from typing import Dict, List, Optional

# Set environment variables before Flet import to optimize loading
os.environ['FLET_APP_HIDDEN'] = 'true'
os.environ['FLET_WEB'] = 'false'

# Custom icon constants to avoid loading the full Icons enum
class CustomIcons:
    ADD = "add"
    SAVE = "save"
    DELETE = "delete"
    EDIT = "edit"
    FEEDBACK = "feedback" 
    UPLOAD_FILE = "upload_file"
    LIST_ALT = "list_alt"
    ARROW_BACK = "arrow_back"
    MENU = "menu"
    LANGUAGE = "language"
    LIGHT_MODE = "light_mode"
    DARK_MODE = "dark_mode"
    INFO = "info"

# Try to import Flet with error handling
try:
    import flet as ft
    print("✅ Flet imported successfully")
except Exception as e:
    print(f"❌ Flet import failed: {e}")
    sys.exit(1)

class PortfolioManager:
    def __init__(self, page: ft.Page):
        self.page = page
        self.page.title = "Portfolio Document Manager - TI"
        self.page.theme_mode = ft.ThemeMode.LIGHT
        self.page.window_width = 1400
        self.page.window_height = 1200
        self.page.window_min_width = 1200
        self.page.window_min_height = 900
        
        # Ensure the window is visible and properly configured
        self.page.window_visible = True
        self.page.window_resizable = True
        self.page.window_maximizable = True
        self.page.window_minimizable = True
        
        # Data storage
        self.data_file = "portfolio_data.json"
        self.student_info = {}
        self.portfolio_items = []
        self.reflection_data = {}
        self.current_language = "nl"  # Default to Dutch
        
        # Language translations
        self.translations = {
            "nl": {
                "app_title": "Portfolio Document Manager - TI",
                "menu_about": "Over",
                "menu_feedback": "Feedback", 
                "menu_main": "Hoofdmenu",
                "menu_student_info": "Student gegevens wijzigen",
                "menu_github": "🚧 GitHub inloggegevens (in ontwikkeling)",
                "menu_github_tooltip": "Functie nog in ontwikkeling",
                "menu_export": "Data exporteren",
                "menu_import": "Data importeren",
                "btn_learning_outcomes": "Leeruitkomsten Info",
                "btn_all_feedback": "Alle Feedback",
                "btn_add_item": "Nieuw Portfolio Item Toevoegen",
                "btn_add_feedback": "Feedback Toevoegen",
                "btn_submit_document": "Document Inleveren",
                "tooltip_theme": "Toggle Dark/Light Mode",
                "tooltip_language": "Schakel Taal",
                "table_title": "Titel",
                "table_learning_outcomes": "Leeruitkomsten",
                "table_type": "Type",
                "table_date": "Datum",
                "table_feedback": "Feedback",
                "table_actions": "Acties",
                "btn_back": "Terug naar Overzicht",
                "portfolio_items_title": "Portfolio Items",
                "attention_items_without_feedback_single": "Je hebt nog {} portfolio item zonder feedback!",
                "attention_items_without_feedback_multiple": "Je hebt nog {} portfolio items zonder feedback!",
                "attention_all_items_have_feedback": "✅ Alle portfolio items hebben feedback!",
                "type_personal": "Persoonlijk",
                "type_group": "Groep",
                "important": "BELANGRIJK",
                # Student Info page
                "student_info_title": "Student Gegevens",
                "student_info": "Student Informatie",
                "name_label": "Naam student",
                "student_number_label": "Studentnummer", 
                "semester_label": "Semester (2-8)",
                "milestone_label": "Peilmoment (1-4)",
                "save_btn": "Opslaan",
                "cancel_btn": "Annuleren",
                "required_fields_error": "⚠️ Vul alle velden in!",
                # Portfolio Item page
                "portfolio_item_add_title": "Portfolio Item Toevoegen",
                "portfolio_item_edit_title": "Portfolio Item Bewerken",
                "title_label": "Titel *",
                "select_learning_outcomes": "Selecteer leeruitkomsten:",
                "assignment_type": "Type opdracht:",
                "assignment_personal": "Persoonlijk",
                "assignment_group": "Groepswerk",
                "group_members_label": "Groepsleden (één per regel)",
                "github_link_label": "GitHub link *",
                "description_label": "Korte uitleg van wat je hebt gedaan *",
                "select_min_one_lo": "⚠️ Selecteer minimaal één leeruitkomst!",
                "fill_required_fields": "⚠️ Vul alle verplichte velden (*) in!",
                # About page
                "about_title": "Over Portfolio Document Manager",
                "version_label": "Versie: 1.5.15 (Minimal)",
                "about_description": "Een moderne desktop applicatie voor het beheren van portfolio documenten",
                "developed_by": "Ontwikkeld door:",
                "copyright": "© 2025 Rick van der Voort - Portfolio Document Manager",
            }
        }
        
        # Learning outcomes definitions
        self.learning_outcomes = {
            1: {
                "title": "Analyseren",
                "description": "Student analyseert de vereisten en doelstellingen van de opdrachtgever betreffende een 'Digital Twin' van een bestaand embedded systeem. Op basis hiervan en rekening houdend met de mogelijke gebruikers deduceert de student requirements volgens een voorgeschreven methode.",
                "indicators": ["Requirements analyse", "Stakeholder analyse", "Testplan", "Ontwikkeldocument (eerste deel)"],
                "examples": ["Stakeholder interviews", "Use case diagrammen", "Requirements specification document", "Functional requirements lijst"]
            },
            2: {
                "title": "Ontwerpen", 
                "description": "Student ontwerpt gebaseerd op de requirements en volgens voorgeschreven methoden een 'Digital Twin', inclusief grafische representatie, van een bestaand embedded systeem. Dit ontwerp omvat ook een ontwerp voor teststrategieën.",
                "indicators": ["Testverslag", "Ontwikkeldocument"],
                "examples": ["UML diagrammen", "Architectuur ontwerp", "Database design", "UI/UX mockups", "Testplan ontwerp"]
            },
            3: {
                "title": "Adviseren",
                "description": "Student adviseert de opdrachtgever, na analyse van de vereisten en doelstellingen, over de inzet van een digital twin. Het advies is helder onderbouwd en gepresenteerd, zodat het begrijpelijk is voor alle stakeholders/betrokkenen.",
                "indicators": ["Adviesrapport", "Advies presentatie"],
                "examples": ["Technisch adviesrapport", "Kosten-baten analyse", "Risico analyse", "Implementatie roadmap", "Stakeholder presentaties"]
            },
            4: {
                "title": "Realiseren",
                "description": "Student realiseert vanuit het ontwerp een 'Digital Twin' van een bestaand embedded systeem, inclusief grafische representatie. Hierbij wordt gewerkt volgens een voorgeschreven methode waarin testen centraal staat.",
                "indicators": ["Broncode simulatie", "Projectcode", "Vision opdrachten", "Algoritmiek opdrachten", "C++ STL opdrachten", "C++<->Python opdrachten", "Creational/Structural design pattern opdrachten"],
                "examples": ["Working prototype", "Code repositories", "Unit tests", "Integration tests", "Performance benchmarks", "Design patterns implementatie"]
            },
            5: {
                "title": "Beheren",
                "description": "Student zet een professionele ontwikkelomgeving op voor desktop development. Daarbij houdt hij rekening met de samenwerking tussen verschillende programmeertalen. De desktop debugging wordt op een gestructureerde manier uitgevoerd.",
                "indicators": ["Ontwikkeldocument", "Opdrachten ontwikkelomgeving", "Opdrachten debugging/tooling", "Testverslag"],
                "examples": ["Version control (Git)", "CI/CD pipelines", "Code reviews", "Debugging sessies", "Development environment setup", "Tool configuration"]
            },
            6: {
                "title": "Toekomstgericht organiseren",
                "description": "De student kan een probleem vertalen naar een product door randvoorwaarden en requirements op te stellen in overleg met de opdrachtgever. Het project wordt gestructureerd opgezet, uitgevoerd en opgeleverd.",
                "indicators": ["Ontwikkeldocument", "Scrum board", "Sprintverslagen"],
                "examples": ["Sprint planning", "Daily standups", "Sprint reviews", "Retrospectives", "Product backlog management", "Project roadmap"]
            },
            7: {
                "title": "Doelgericht interacteren",
                "description": "De student onderhoudt actief de relatie met relevante samenwerkingspartners door middel van het geven van weloverwogen presentaties die afgestemd zijn op de doelgroep.",
                "indicators": ["Onderzoeksverslag(deepdive)", "Adviespresentatie", "Sprintverslagen (review)"],
                "examples": ["Stakeholder meetings", "Demo presentaties", "Technical documentation", "Team communication", "Client feedback sessions"]
            },
            8: {
                "title": "Persoonlijk leiderschap",
                "description": "De student bereidt zich voor op studie- en loopbaankeuzes. De student evalueert hierbij persoonlijke ambities en kwaliteiten in relatie tot de gewenste positionering in het werkveld.",
                "indicators": ["Sollicitatiebrief", "Professionaliseringsdocument"],
                "examples": ["Personal development plan", "Career vision document", "Self-reflection reports", "Professional network building", "Skills assessment"]
            },
            9: {
                "title": "Onderzoek probleem oplossen",
                "description": "De student kan een praktijkgericht probleem identificeren en de juiste oplossingsrichting kiezen door wensen van de opdrachtgever centraal te stellen. Gedurende het proces handelt de student onderzoekend.",
                "indicators": ["Onderzoeksverslag (deepdive)", "Ontwikkeldocument"],
                "examples": ["Literature review", "Proof of concept", "Experimental setup", "Data analysis", "Research methodology", "Problem statement definition"]
            }
        }
        
        # UI Components - Initialize with basic structure
        self.info_text = ft.Text("", size=14)
        self.attention_card = ft.Card(visible=False, expand=False)
        self.portfolio_data_table = ft.DataTable(
            columns=[
                ft.DataColumn(ft.Text(self.get_text("table_title"))),
                ft.DataColumn(ft.Text(self.get_text("table_learning_outcomes"))),
                ft.DataColumn(ft.Text(self.get_text("table_type"))),
                ft.DataColumn(ft.Text(self.get_text("table_date"))),
                ft.DataColumn(ft.Text(self.get_text("table_feedback"))),
                ft.DataColumn(ft.Text(self.get_text("table_actions"))),
            ],
            rows=[]
        )
        
        # View management
        self.current_view = "main"
        self.main_content = ft.Column()
        self.content_container = ft.Container(expand=True)
        
        # Load existing data
        self.load_data()
        
        # Initialize GUI
        self.setup_gui()
        
        # Check if first time setup is needed
        if not self.student_info:
            self.show_student_info_view()

    def get_text(self, key: str) -> str:
        """Get translated text for current language"""
        return self.translations.get(self.current_language, {}).get(key, key)
    
    def load_data(self):
        """Load data from JSON file"""
        try:
            if os.path.exists(self.data_file):
                with open(self.data_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    self.student_info = data.get('student_info', {})
                    self.portfolio_items = data.get('portfolio_items', [])
                    self.reflection_data = data.get('reflection_data', {})
                    self.current_language = data.get('current_language', 'nl')
        except Exception as e:
            print(f"Error loading data: {e}")
    
    def save_data(self):
        """Save data to JSON file"""
        try:
            data = {
                'student_info': self.student_info,
                'portfolio_items': self.portfolio_items,
                'reflection_data': self.reflection_data,
                'current_language': self.current_language
            }
            with open(self.data_file, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
        except Exception as e:
            print(f"Error saving data: {e}")

    def setup_gui(self):
        """Setup the main GUI interface with minimal icons"""
        # Simple app bar without complex icons
        self.page.appbar = ft.AppBar(
            title=ft.Text(self.get_text("app_title")),
            bgcolor=ft.Colors.BLUE_700,
            color=ft.Colors.WHITE,
            leading=ft.TextButton(
                text="☰ Menu",
                on_click=self.show_menu,
                style=ft.ButtonStyle(color=ft.Colors.WHITE)
            )
        )
        
        # Initialize main content container
        self.content_container = ft.Container(
            content=self.main_content,
            padding=20,
            expand=True
        )
        
        # Add to page
        self.page.add(self.content_container)
        
        # Show initial view
        self.show_main_view()

    def show_menu(self, e=None):
        """Show simple menu"""
        # Simple menu implementation without PopupMenuButton
        pass

    def show_main_view(self):
        """Show the main portfolio overview with minimal UI"""
        self.current_view = "main"
        
        # Update student info display
        if self.student_info:
            name = self.student_info.get('name', 'Onbekend')
            number = self.student_info.get('student_number', 'Onbekend')
            semester = self.student_info.get('semester', 'Onbekend')
            milestone = self.student_info.get('milestone', 'Onbekend')
            self.info_text.value = f"Naam: {name}\nStudentnummer: {number}\nSemester: {semester}\nPeilmoment: {milestone}"
        else:
            self.info_text.value = "Geen student informatie ingevuld"
        
        # Update portfolio table
        self.update_portfolio_table()
        
        # Main content with simple buttons (no icons to avoid enum loading)
        main_content = ft.Column([
            # Student info card
            ft.Card(
                content=ft.Container(
                    content=ft.Column([
                        ft.Text(self.get_text("student_info"), size=16, weight=ft.FontWeight.BOLD),
                        self.info_text
                    ], horizontal_alignment=ft.CrossAxisAlignment.CENTER),
                    padding=20
                ),
                margin=ft.margin.only(bottom=10)
            ),
            
            # Action buttons without icons
            ft.Row([
                ft.ElevatedButton(
                    text="+ " + self.get_text("btn_add_item"),
                    on_click=self.show_add_portfolio_item_view,
                    style=ft.ButtonStyle(
                        bgcolor=ft.Colors.GREEN_600,
                        color=ft.Colors.WHITE
                    )
                ),
                ft.ElevatedButton(
                    text="⚙ " + self.get_text("menu_student_info"),
                    on_click=self.show_student_info_view,
                    style=ft.ButtonStyle(
                        bgcolor=ft.Colors.BLUE_600,
                        color=ft.Colors.WHITE
                    )
                ),
            ], spacing=10, alignment=ft.MainAxisAlignment.CENTER),
            
            # Portfolio items table
            ft.Card(
                content=ft.Container(
                    content=ft.Column([
                        ft.Text(self.get_text("portfolio_items_title"), size=16, weight=ft.FontWeight.BOLD),
                        self.portfolio_data_table
                    ]),
                    padding=20
                ),
                margin=ft.margin.only(top=20)
            )
        ], scroll=ft.ScrollMode.AUTO)
        
        self.content_container.content = main_content
        self.page.update()

    def update_portfolio_table(self):
        """Update the portfolio table with current data"""
        self.portfolio_data_table.rows.clear()
        
        for i, item in enumerate(self.portfolio_items):
            title = item.get('title', 'Geen titel')[:30] + ('...' if len(item.get('title', '')) > 30 else '')
            los = ', '.join([f"LU{lo}" for lo in item.get('learning_outcomes', [])])
            item_type = "Groep" if item.get('is_group_work', False) else "Persoonlijk"
            date_added = item.get('date_added', 'Onbekend')
            feedback_count = len(item.get('feedback', []))
            
            # Simple text buttons instead of icon buttons
            edit_btn = ft.TextButton(
                text="Edit",
                on_click=lambda e, idx=i: self.edit_portfolio_item(idx)
            )
            delete_btn = ft.TextButton(
                text="Delete",
                on_click=lambda e, idx=i: self.delete_portfolio_item(idx)
            )
            
            row = ft.DataRow(cells=[
                ft.DataCell(ft.Text(title)),
                ft.DataCell(ft.Text(los)),
                ft.DataCell(ft.Text(item_type)),
                ft.DataCell(ft.Text(date_added)),
                ft.DataCell(ft.Text(str(feedback_count))),
                ft.DataCell(ft.Row([edit_btn, delete_btn], spacing=5))
            ])
            
            self.portfolio_data_table.rows.append(row)

    def show_student_info_view(self, e=None):
        """Show student info editing view"""
        self.current_view = "student_info"
        
        name_field = ft.TextField(
            label=self.get_text("name_label"), 
            value=self.student_info.get("name", ""), 
            width=400
        )
        number_field = ft.TextField(
            label=self.get_text("student_number_label"), 
            value=self.student_info.get("student_number", ""), 
            width=400
        )
        semester_dropdown = ft.Dropdown(
            label=self.get_text("semester_label"),
            options=[ft.dropdown.Option(str(i)) for i in range(2, 9)],
            value=self.student_info.get("semester", "2"),
            width=400
        )
        milestone_dropdown = ft.Dropdown(
            label=self.get_text("milestone_label"),
            options=[ft.dropdown.Option(str(i)) for i in range(1, 5)],
            value=self.student_info.get("milestone", "1"),
            width=400
        )
        
        def save_student_info(e):
            if not name_field.value or not number_field.value:
                error_text.value = self.get_text("required_fields_error")
                error_text.visible = True
                self.page.update()
                return
            
            self.student_info = {
                "name": name_field.value.strip(),
                "student_number": number_field.value.strip(),
                "semester": semester_dropdown.value,
                "milestone": milestone_dropdown.value
            }
            self.save_data()
            self.show_main_view()
        
        error_text = ft.Text("", color=ft.Colors.RED, visible=False)
        
        content = ft.Column([
            ft.ElevatedButton(
                text="← " + self.get_text("btn_back"),
                on_click=lambda e: self.show_main_view()
            ),
            ft.Card(
                content=ft.Container(
                    content=ft.Column([
                        ft.Text(self.get_text("student_info_title"), size=20, weight=ft.FontWeight.BOLD),
                        error_text,
                        name_field,
                        number_field,
                        semester_dropdown,
                        milestone_dropdown,
                        ft.ElevatedButton(
                            text=self.get_text("save_btn"),
                            on_click=save_student_info,
                            style=ft.ButtonStyle(
                                bgcolor=ft.Colors.GREEN_600,
                                color=ft.Colors.WHITE
                            )
                        )
                    ], spacing=15),
                    padding=20
                )
            )
        ], scroll=ft.ScrollMode.AUTO)
        
        self.content_container.content = content
        self.page.update()

    def show_add_portfolio_item_view(self, e=None, existing_item=None, index=None):
        """Show add/edit portfolio item view"""
        self.current_view = "add_portfolio_item"
        
        # Title field
        title_field = ft.TextField(
            label="Titel *",
            value=existing_item.get('title', '') if existing_item else '',
            width=600
        )
        
        # Learning outcomes checkboxes
        lo_checkboxes = {}
        lo_controls = []
        
        for lo_num, lo_data in self.learning_outcomes.items():
            checkbox = ft.Checkbox(
                label=f"LU{lo_num}: {lo_data['title']}",
                value=lo_num in existing_item.get('learning_outcomes', []) if existing_item else False
            )
            lo_checkboxes[lo_num] = checkbox
            lo_controls.append(checkbox)
        
        # Assignment type
        assignment_type = ft.RadioGroup(
            content=ft.Column([
                ft.Radio(value="personal", label=self.get_text("assignment_personal")),
                ft.Radio(value="group", label=self.get_text("assignment_group"))
            ]),
            value="group" if existing_item and existing_item.get('is_group_work', False) else "personal"
        )
        
        # GitHub link
        github_field = ft.TextField(
            label=self.get_text("github_link_label"),
            value=existing_item.get('github_link', '') if existing_item else '',
            width=600
        )
        
        # Description
        description_field = ft.TextField(
            label=self.get_text("description_label"),
            multiline=True,
            min_lines=4,
            max_lines=6,
            value=existing_item.get('description', '') if existing_item else '',
            width=600
        )
        
        error_text = ft.Text("", color=ft.Colors.RED, visible=False)
        
        def save_item(e):
            selected_los = [lo_num for lo_num, checkbox in lo_checkboxes.items() if checkbox.value]
            
            if not selected_los:
                error_text.value = self.get_text("select_min_one_lo")
                error_text.visible = True
                self.page.update()
                return
            
            if not title_field.value or not github_field.value or not description_field.value:
                error_text.value = self.get_text("fill_required_fields")
                error_text.visible = True
                self.page.update()
                return
            
            item_data = {
                "title": title_field.value.strip(),
                "learning_outcomes": selected_los,
                "is_group_work": assignment_type.value == "group",
                "github_link": github_field.value.strip(),
                "description": description_field.value.strip(),
                "feedback": existing_item.get('feedback', []) if existing_item else []
            }
            
            if index is not None:
                # Edit existing item - preserve the original date
                item_data['date_added'] = existing_item.get('date_added', datetime.datetime.now().strftime("%Y-%m-%d"))
                self.portfolio_items[index] = item_data
            else:
                # Add new item - set current date
                item_data['date_added'] = datetime.datetime.now().strftime("%Y-%m-%d")
                self.portfolio_items.append(item_data)
            
            self.save_data()
            self.show_main_view()
        
        # Create content
        content = ft.Column([
            ft.ElevatedButton(
                text="← " + self.get_text("btn_back"),
                on_click=lambda e: self.show_main_view()
            ),
            ft.Card(
                content=ft.Container(
                    content=ft.Column([
                        ft.Text(self.get_text("portfolio_item_edit_title" if existing_item else "portfolio_item_add_title"), 
                               size=20, weight=ft.FontWeight.BOLD),
                        error_text,
                        title_field,
                        ft.Text(self.get_text("select_learning_outcomes"), weight=ft.FontWeight.BOLD),
                        ft.Column(lo_controls, spacing=5),
                        ft.Text(self.get_text("assignment_type"), weight=ft.FontWeight.BOLD),
                        assignment_type,
                        github_field,
                        description_field,
                        ft.Row([
                            ft.ElevatedButton(
                                text=self.get_text("save_btn"),
                                on_click=save_item,
                                style=ft.ButtonStyle(
                                    bgcolor=ft.Colors.GREEN_600,
                                    color=ft.Colors.WHITE
                                )
                            )
                        ])
                    ], spacing=15),
                    padding=20
                )
            )
        ], scroll=ft.ScrollMode.AUTO)
        
        self.content_container.content = content
        self.page.update()

    def edit_portfolio_item(self, index):
        """Edit a portfolio item"""
        if 0 <= index < len(self.portfolio_items):
            item = self.portfolio_items[index]
            self.show_add_portfolio_item_view(existing_item=item, index=index)

    def delete_portfolio_item(self, index):
        """Delete a portfolio item"""
        if 0 <= index < len(self.portfolio_items):
            # Simple confirmation without dialog
            if len(self.portfolio_items) > 0:
                self.portfolio_items.pop(index)
                self.save_data()
                self.show_main_view()

    def update_display(self):
        """Update the display"""
        self.page.update()


def show_startup_info():
    """Show startup information"""
    import platform
    import os
    
    print("=" * 50)
    print("Portfolio Document Manager v1.5.15 (Minimal)")
    print("=" * 50)
    print(f"Running on {platform.system()} {platform.release()}")
    
    if platform.system() == "Linux":
        display = os.getenv('DISPLAY', 'Not set')
        session_type = os.getenv('XDG_SESSION_TYPE', 'unknown')
        print(f"DISPLAY is set to: {display}")
        print(f"Session type: {session_type}")
    
    print("Starting minimal desktop application...")
    print("This version uses minimal icons to avoid PyInstaller enum issues.")


def main(page: ft.Page):
    """Main application entry point"""
    try:
        # Set desktop mode
        page.views.clear()
        
        # Create the application
        app = PortfolioManager(page)
        
        print("✅ Application initialized successfully")
        
    except Exception as e:
        print(f"❌ Application initialization failed: {e}")
        import traceback
        traceback.print_exc()
        
        # Show error page
        page.add(
            ft.Container(
                content=ft.Column([
                    ft.Text("Application Error", size=20, weight=ft.FontWeight.BOLD, color=ft.Colors.RED),
                    ft.Text(f"Error: {str(e)}", color=ft.Colors.RED),
                    ft.Text("Please check the console for details.", color=ft.Colors.GREY_600)
                ], horizontal_alignment=ft.CrossAxisAlignment.CENTER),
                alignment=ft.alignment.center,
                expand=True
            )
        )


if __name__ == "__main__":
    try:
        show_startup_info()
        
        # Start the application with desktop view
        ft.app(
            target=main,
            view=ft.AppView.FLET_APP,  # Desktop mode
            assets_dir="assets"
        )
        
    except KeyboardInterrupt:
        print("\n👋 Application stopped by user")
    except Exception as e:
        print(f"❌ Fatal error: {e}")
        import traceback
        traceback.print_exc()
    finally:
        print("Application shutdown")
