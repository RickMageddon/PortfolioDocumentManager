#!/usr/bin/env python3
"""
Portfolio Document Program - Flet Version
Een programma voor het beheren van portfolio items voor het TI S4 verantwoordingsdocument.
"""
import flet as ft
import json
import os
import sys
import datetime
import webbrowser
import markdown
import weasyprint
from typing import Dict, List, Optional


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
                # Feedback pages
                "feedback_add_title": "Feedback Toevoegen",
                "feedback_add_subtitle": "Voeg feedback toe aan een bestaand portfolio item",
                "no_portfolio_items_title": "Feedback Toevoegen",
                "no_portfolio_items_msg": "Er zijn nog geen portfolio items om feedback aan toe te voegen.",
                "no_portfolio_items_hint": "Voeg eerst een portfolio item toe voordat je feedback kunt geven.",
                "select_portfolio_item": "Selecteer portfolio item",
                "select_learning_outcomes_feedback": "Selecteer leeruitkomsten voor deze feedback:",
                "feedback_from_label": "Feedback van (naam docent/begeleider) *",
                "feedback_text_label": "Feedback tekst *",
                "save_feedback_btn": "Feedback Opslaan",
                "select_portfolio_item_error": "⚠️ Selecteer een portfolio item!",
                "select_min_one_lo_feedback": "⚠️ Selecteer minimaal één leeruitkomst voor de feedback!",
                "feedback_saved_success": "✅ Feedback succesvol toegevoegd!",
                "portfolio_item_label": "Portfolio Item:",
                "add_feedback_to_item": "Voeg feedback toe aan dit portfolio item",
                # All Feedback page
                "all_feedback_title": "Alle Feedback Overzicht",
                "total_items_with_feedback": "Totaal {} portfolio item(s) met feedback",
                "no_feedback_found": "Geen Feedback Gevonden",
                "no_feedback_msg": "Er is nog geen feedback toegevoegd aan portfolio items.",
                "no_feedback_hint": "Voeg eerst feedback toe via de 'Feedback Toevoegen' knop.",
                "feedback_from": "Van:",
                "feedback_date": "Datum:",
                "unknown": "Onbekend",
                # Document Submission page
                "submit_document_title": "Document Inleveren",
                "reflection_questions": "Reflectie Vragen",
                "proud_of_label": "Waar ik het meest trots op ben:",
                "struggled_with_label": "Waar ik de afgelopen periode moeite mee heb gehad en welke actie ik heb ondernomen:",
                "want_to_learn_label": "Wat ik nog graag wil leren en welke actie ik wil gaan ondernemen:",
                "confirm_complete": "Ik bevestig dat mijn portfolio compleet is en klaar voor inlevering",
                "generate_markdown": "Ook markdown (.md) bestand genereren",
                "generate_document_btn": "Document Genereren",
                "fill_reflection_error": "⚠️ Vul alle reflectie vragen in!",
                "confirm_complete_error": "⚠️ Bevestig dat je portfolio compleet is!",
                "document_generated_success": "✅ Document succesvol gegenereerd!",
                "document_generation_failed": "❌ Document generatie mislukt:",
                # Delete confirmation
                "delete_portfolio_item": "Portfolio Item Verwijderen",
                "delete_confirmation": "Weet je zeker dat je '{}' wilt verwijderen?",
                "delete_warning": "Deze actie kan niet ongedaan worden gemaakt.",
                "delete_btn": "Verwijderen",
                # First time setup
                "first_time_setup": "Eerste Installatie",
                "welcome_msg": "Welkom bij de Portfolio Document Manager!",
                "fill_basic_info": "Vul eerst je basisgegevens in:",
                "ok_btn": "OK",
                # Tooltips
                "edit_tooltip": "Bewerken",
                "add_feedback_tooltip": "Feedback Toevoegen",
                "delete_tooltip": "Verwijderen",
                # Learning Outcomes page
                "learning_outcomes_title": "Leeruitkomsten Informatie",
                "learning_outcomes_subtitle": "Detailinformatie over alle leeruitkomsten",
                "description_label_lo": "Beschrijving:",
                "indicators_label": "Indicatoren:",
                "examples_label": "Voorbeelden van opdrachten:",
                # About page
                "about_title": "Over Portfolio Document Manager",
                "version_label": "Versie: 1.5.14",
                "about_description": "Een moderne desktop applicatie voor het beheren van portfolio documenten",
                "developed_by": "Ontwikkeld door:",
                "copyright": "© 2025 Rick van der Voort - Portfolio Document Manager",
                # Feedback Info page
                "feedback_info_title": "Feedback over de App",
                "improve_app": "Verbeter de Portfolio Document Manager!",
                "feedback_help": "Jouw feedback helpt ons de app te verbeteren. Deel je ervaringen, suggesties en bug reports.",
                "how_to_give_feedback": "Hoe kan je feedback geven?",
                "share_experience": "• Deel je ervaring met de app",
                "report_bugs": "• Rapporteer bugs of problemen", 
                "suggest_features": "• Suggereer nieuwe functies",
                "ux_tips": "• Geef tips voor betere gebruikerservaring",
                "feedback_categories": "Feedback categorieën:",
                "bug_report": "🐛 Bug Report - Meld een probleem",
                "feature_request": "💡 Feature Request - Suggereer een nieuwe functie",
                "documentation": "📖 Documentatie - Verbeter de handleiding",
                "ui_ux": "🎨 UI/UX - Design en gebruiksvriendelijkheid",
                "performance": "⚡ Performance - Snelheid en prestaties",
                "give_feedback": "Geef feedback:",
                "feedback_github_link": "📝 Feedback Geven via GitHub Issues",
                "thanks_msg": "Bedankt voor je bijdrage aan het verbeteren van de app!",
                # GitHub setup
                "github_integration": "GitHub Integratie",
                "feature_development": "Functie in Ontwikkeling",
                "github_under_development": "GitHub integratie is momenteel nog in ontwikkeling.",
                "feature_future_version": "Deze functie wordt toegevoegd in een toekomstige versie.",
                # Additional UI text
                "no_title": "Geen titel",
                "no_date": "Geen datum",
                "no_feedback": "Geen feedback",
                # Additional error messages and status texts
                "document_generate_btn": "Document Genereren",
                "document_generated": "Document gegenereerd",
                "error_occurred": "Er is een fout opgetreden",
                "data_exported": "Data geëxporteerd",
                "data_imported": "Data geïmporteerd",
                # Additional feedback view texts
                "feedback_for_item": "Feedback voor item:",
                "add_feedback_specific": "Voeg feedback toe aan dit item",
                "feedback_overview": "Feedback overzicht",
                "items_count": "items",
                "with_feedback": "met feedback",
                # Learning Outcome Tab Header
                "learning_outcome": "Leeruitkomst"
            },
            "en": {
                "app_title": "Portfolio Document Manager - TI",
                "menu_about": "About",
                "menu_feedback": "Feedback",
                "menu_main": "Main Menu",
                "menu_student_info": "Change student information",
                "menu_github": "🚧 GitHub credentials (under development)",
                "menu_github_tooltip": "Feature under development",
                "menu_export": "Export data",
                "menu_import": "Import data",
                "btn_learning_outcomes": "Learning Outcomes Info",
                "btn_all_feedback": "All Feedback",
                "btn_add_item": "Add New Portfolio Item",
                "btn_add_feedback": "Add Feedback",
                "btn_submit_document": "Submit Document",
                "tooltip_theme": "Toggle Dark/Light Mode",
                "tooltip_language": "Switch Language",
                "table_title": "Title",
                "table_learning_outcomes": "Learning Outcomes",
                "table_type": "Type",
                "table_date": "Date",
                "table_feedback": "Feedback",
                "table_actions": "Actions",
                "btn_back": "Back to Overview",
                "portfolio_items_title": "Portfolio Items",
                "attention_items_without_feedback_single": "You still have {} portfolio item without feedback!",
                "attention_items_without_feedback_multiple": "You still have {} portfolio items without feedback!",
                "attention_all_items_have_feedback": "✅ All portfolio items have feedback!",
                "type_personal": "Personal",
                "type_group": "Group",
                "important": "IMPORTANT",
                # Student Info page
                "student_info_title": "Student Information",
                "student_info": "Student Information",
                "name_label": "Student name",
                "student_number_label": "Student number",
                "semester_label": "Semester (2-8)",
                "milestone_label": "Milestone (1-4)",
                "save_btn": "Save",
                "cancel_btn": "Cancel",
                "required_fields_error": "⚠️ Please fill in all fields!",
                # Portfolio Item page
                "portfolio_item_add_title": "Add Portfolio Item",
                "portfolio_item_edit_title": "Edit Portfolio Item",
                "title_label": "Title *",
                "select_learning_outcomes": "Select learning outcomes:",
                "assignment_type": "Assignment type:",
                "assignment_personal": "Personal",
                "assignment_group": "Group work",
                "group_members_label": "Group members (one per line)",
                "github_link_label": "GitHub link *",
                "description_label": "Brief explanation of what you did *",
                "select_min_one_lo": "⚠️ Select at least one learning outcome!",
                "fill_required_fields": "⚠️ Please fill in all required fields (*)!",
                # Feedback pages
                "feedback_add_title": "Add Feedback",
                "feedback_add_subtitle": "Add feedback to an existing portfolio item",
                "no_portfolio_items_title": "Add Feedback",
                "no_portfolio_items_msg": "There are no portfolio items yet to add feedback to.",
                "no_portfolio_items_hint": "Please add a portfolio item first before you can give feedback.",
                "select_portfolio_item": "Select portfolio item",
                "select_learning_outcomes_feedback": "Select learning outcomes for this feedback:",
                "feedback_from_label": "Feedback from (teacher/supervisor name) *",
                "feedback_text_label": "Feedback text *",
                "save_feedback_btn": "Save Feedback",
                "select_portfolio_item_error": "⚠️ Please select a portfolio item!",
                "select_min_one_lo_feedback": "⚠️ Select at least one learning outcome for the feedback!",
                "feedback_saved_success": "✅ Feedback successfully added!",
                "portfolio_item_label": "Portfolio Item:",
                "add_feedback_to_item": "Add feedback to this portfolio item",
                # All Feedback page
                "all_feedback_title": "All Feedback Overview",
                "total_items_with_feedback": "Total {} portfolio item(s) with feedback",
                "no_feedback_found": "No Feedback Found",
                "no_feedback_msg": "No feedback has been added to portfolio items yet.",
                "no_feedback_hint": "Please add feedback first via the 'Add Feedback' button.",
                "feedback_from": "From:",
                "feedback_date": "Date:",
                "unknown": "Unknown",
                # Document Submission page
                "submit_document_title": "Submit Document",
                "reflection_questions": "Reflection Questions",
                "proud_of_label": "What I am most proud of:",
                "struggled_with_label": "What I struggled with during this period and what action I took:",
                "want_to_learn_label": "What I still want to learn and what action I want to take:",
                "confirm_complete": "I confirm that my portfolio is complete and ready for submission",
                "generate_markdown": "Also generate markdown (.md) file",
                "generate_document_btn": "Generate Document",
                "fill_reflection_error": "⚠️ Please answer all reflection questions!",
                "confirm_complete_error": "⚠️ Please confirm that your portfolio is complete!",
                "document_generated_success": "✅ Document successfully generated!",
                "document_generation_failed": "❌ Document generation failed:",
                # Delete confirmation
                "delete_portfolio_item": "Delete Portfolio Item",
                "delete_confirmation": "Are you sure you want to delete '{}'?",
                "delete_warning": "This action cannot be undone.",
                "delete_btn": "Delete",
                # First time setup
                "first_time_setup": "First Time Setup",
                "welcome_msg": "Welcome to the Portfolio Document Manager!",
                "fill_basic_info": "Please fill in your basic information first:",
                "ok_btn": "OK",
                # Tooltips
                "edit_tooltip": "Edit",
                "add_feedback_tooltip": "Add Feedback",
                "delete_tooltip": "Delete",
                # Learning Outcomes page
                "learning_outcomes_title": "Learning Outcomes Information",
                "learning_outcomes_subtitle": "Detailed information about all learning outcomes",
                "description_label_lo": "Description:",
                "indicators_label": "Indicators:",
                "examples_label": "Examples of assignments:",
                # About page
                "about_title": "About Portfolio Document Manager",
                "version_label": "Version: 1.5.14",
                "about_description": "A modern desktop application for managing portfolio documents",
                "developed_by": "Developed by:",
                "copyright": "© 2025 Rick van der Voort - Portfolio Document Manager",
                # Feedback Info page
                "feedback_info_title": "Feedback about the App",
                "improve_app": "Improve the Portfolio Document Manager!",
                "feedback_help": "Your feedback helps us improve the app. Share your experiences, suggestions and bug reports.",
                "how_to_give_feedback": "How can you give feedback?",
                "share_experience": "• Share your experience with the app",
                "report_bugs": "• Report bugs or problems",
                "suggest_features": "• Suggest new features",
                "ux_tips": "• Give tips for better user experience",
                "feedback_categories": "Feedback categories:",
                "bug_report": "🐛 Bug Report - Report a problem",
                "feature_request": "💡 Feature Request - Suggest a new feature",
                "documentation": "📖 Documentation - Improve the manual",
                "ui_ux": "🎨 UI/UX - Design and usability",
                "performance": "⚡ Performance - Speed and performance",
                "give_feedback": "Give feedback:",
                "feedback_github_link": "📝 Give Feedback via GitHub Issues",
                "thanks_msg": "Thank you for your contribution to improving the app!",
                # GitHub setup
                "github_integration": "GitHub Integration",
                "feature_development": "Feature in Development",
                "github_under_development": "GitHub integration is currently under development.",
                "feature_future_version": "This feature will be added in a future version.",
                # Additional UI text
                "no_title": "Geen titel",
                "no_date": "Geen datum",
                "no_feedback": "Geen feedback",
                # Additional error messages and status texts
                "document_generate_btn": "Document Genereren",
                "document_generated": "Document gegenereerd",
                "error_occurred": "Er is een fout opgetreden",
                "data_exported": "Data geëxporteerd",
                "data_imported": "Data geïmporteerd",
                # Additional feedback view texts
                "feedback_for_item": "Feedback voor item:",
                "add_feedback_specific": "Voeg feedback toe aan dit item",
                "feedback_overview": "Feedback overzicht",
                "items_count": "items",
                "with_feedback": "met feedback",
                # Learning Outcome Tab Header
                "learning_outcome": "Leeruitkomst"
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
        
        # UI Components
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
            self.first_time_setup()

    def setup_gui(self):
        """Setup the main GUI interface"""
        # App bar with menu on the left and info buttons on the right
        self.page.appbar = ft.AppBar(
            title=ft.Text(self.get_text("app_title")),
            bgcolor=ft.Colors.BLUE_700,
            color=ft.Colors.WHITE,
            leading=ft.PopupMenuButton(
                items=[
                    ft.PopupMenuItem(text=self.get_text("menu_main"), on_click=lambda e: self.show_main_view()),
                    ft.PopupMenuItem(),  # Separator
                    ft.PopupMenuItem(text=self.get_text("menu_about"), on_click=self.show_about),
                    ft.PopupMenuItem(text=self.get_text("menu_feedback"), on_click=self.show_feedback_info),
                    ft.PopupMenuItem(),  # Separator
                    ft.PopupMenuItem(text=self.get_text("menu_student_info"), on_click=self.show_student_info_view),
                    ft.PopupMenuItem(text=self.get_text("menu_github"), on_click=self.setup_github),
                    ft.PopupMenuItem(),  # Separator
                    ft.PopupMenuItem(text=self.get_text("menu_export"), on_click=self.export_data),
                    ft.PopupMenuItem(text=self.get_text("menu_import"), on_click=self.import_data),
                ],
                icon=ft.Icons.MENU
            ),
            actions=[
                ft.TextButton(
                    text=self.get_text("btn_learning_outcomes"),
                    on_click=self.show_learning_outcomes_info,
                    style=ft.ButtonStyle(color=ft.Colors.WHITE)
                ),
                ft.PopupMenuButton(
                    items=[
                        ft.PopupMenuItem(
                            text="🇳🇱 Nederlands",
                            on_click=lambda e: self.change_language("nl")
                        ),
                        ft.PopupMenuItem(
                            text="🇬🇧 English", 
                            on_click=lambda e: self.change_language("en")
                        ),
                    ],
                    icon=ft.Icons.LANGUAGE,
                    icon_color=ft.Colors.WHITE,
                    tooltip=self.get_text("tooltip_language")
                ),
                ft.IconButton(
                    icon=ft.Icons.LIGHT_MODE if self.page.theme_mode == ft.ThemeMode.DARK else ft.Icons.DARK_MODE,
                    tooltip=self.get_text("tooltip_theme"),
                    on_click=self.toggle_theme_mode,
                    icon_color=ft.Colors.WHITE
                )
            ]
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
        
        # Check if first time setup is needed
        if not self.student_info:
            self.show_student_info_view()

    def show_main_view(self):
        """Show the main portfolio overview"""
        self.current_view = "main"
        
        # Main content
        main_content = ft.Column([
            # Student info card - centered
            ft.Container(
                content=ft.Card(
                    content=ft.Container(
                        content=ft.Column([
                            ft.Text(self.get_text("student_info"), size=16, weight=ft.FontWeight.BOLD),
                            self.info_text
                        ], horizontal_alignment=ft.CrossAxisAlignment.CENTER),
                        padding=20
                    ),
                    margin=ft.margin.only(bottom=10)
                ),
                alignment=ft.alignment.center
            ),
            
            # Attention card - centered
            ft.Container(
                content=self.attention_card,
                margin=ft.margin.only(bottom=10, top=10),
                alignment=ft.alignment.center
            ),
            
            # Action buttons - centered
            ft.Container(
                content=ft.Row([
                    ft.ElevatedButton(
                        text=self.get_text("btn_add_item"),
                        icon=ft.Icons.ADD,
                        on_click=self.show_add_portfolio_item_view,
                        style=ft.ButtonStyle(
                            bgcolor=ft.Colors.GREEN_600,
                            color=ft.Colors.WHITE
                        )
                    ),
                    ft.ElevatedButton(
                        text=self.get_text("btn_add_feedback"),
                        icon=ft.Icons.FEEDBACK,
                        on_click=self.show_add_feedback_view,
                        style=ft.ButtonStyle(
                            bgcolor=ft.Colors.BLUE_600,
                            color=ft.Colors.WHITE
                        )
                    ),
                    ft.ElevatedButton(
                        text=self.get_text("btn_all_feedback"),
                        icon=ft.Icons.LIST_ALT,
                        on_click=self.show_all_feedback_view,
                        style=ft.ButtonStyle(
                            bgcolor=ft.Colors.PURPLE_600,
                            color=ft.Colors.WHITE
                        )
                    ),
                    ft.ElevatedButton(
                        text=self.get_text("btn_submit_document"),
                        icon=ft.Icons.UPLOAD_FILE,
                        on_click=self.show_submit_document_view,
                        style=ft.ButtonStyle(
                            bgcolor=ft.Colors.ORANGE_600,
                            color=ft.Colors.WHITE
                        )
                    ),
                ], spacing=10, alignment=ft.MainAxisAlignment.CENTER),
                alignment=ft.alignment.center,
                padding=ft.padding.symmetric(vertical=10)
            ),
            
            # Portfolio items list - centered
            ft.Container(
                content=ft.Card(
                    content=ft.Container(
                        content=ft.Column([
                            ft.Container(
                                content=ft.Text(self.get_text("portfolio_items_title"), size=16, weight=ft.FontWeight.BOLD),
                                alignment=ft.alignment.center,
                                padding=ft.padding.only(bottom=10)
                            ),
                            ft.Container(
                                content=self.portfolio_data_table,
                                height=400,
                                alignment=ft.alignment.top_center
                            )
                        ]),
                        padding=20
                    ),
                    margin=ft.margin.only(top=20)
                ),
                alignment=ft.alignment.center
            )
        ], scroll=ft.ScrollMode.AUTO, horizontal_alignment=ft.CrossAxisAlignment.CENTER)
        
        # Wrap main content in centered container for better layout
        centered_content = ft.Container(
            content=main_content,
            alignment=ft.alignment.top_center,
            expand=True
        )
        
        self.content_container.content = centered_content
        self.update_display()

    def show_back_button(self):
        """Create a back button"""
        # Check if student info is complete
        student_info_complete = bool(self.student_info and 
                                   self.student_info.get("name") and 
                                   self.student_info.get("student_number"))
        
        return ft.ElevatedButton(
            text=f"← {self.get_text('btn_back')}",
            icon=ft.Icons.ARROW_BACK,
            on_click=lambda e: self.show_main_view() if student_info_complete else None,
            disabled=not student_info_complete,
            style=ft.ButtonStyle(
                bgcolor=ft.Colors.GREY_600 if student_info_complete else ft.Colors.GREY_300,
                color=ft.Colors.WHITE if student_info_complete else ft.Colors.GREY_500
            )
        )

    def center_content(self, content):
        """Helper function to center any content consistently"""
        if isinstance(content, ft.Column):
            content.horizontal_alignment = ft.CrossAxisAlignment.CENTER
        
        centered_content = ft.Container(
            content=content,
            alignment=ft.alignment.top_center,
            expand=True
        )
        return centered_content

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
                # Simple error handling without dialog
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
            self.show_back_button(),
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
                            icon=ft.Icons.SAVE,
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
        
        self.content_container.content = self.center_content(content)
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
        
        # Learning outcomes checkboxes with tooltips
        lo_checkboxes = {}
        lo_controls = []
        
        for lo_num, lo_data in self.learning_outcomes.items():
            # Create tooltip text with description and examples
            tooltip_text = f"Beschrijving: {lo_data['description']}\n\nVoorbeelden: {', '.join(lo_data['examples'])}"
            
            checkbox = ft.Checkbox(
                label=f"LU{lo_num}: {lo_data['title']}",
                value=lo_num in existing_item.get('learning_outcomes', []) if existing_item else False,
                tooltip=tooltip_text
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
        
        # Group members (conditionally shown)
        group_members_field = ft.TextField(
            label=self.get_text("group_members_label"),
            multiline=True,
            min_lines=3,
            max_lines=5,
            value="\n".join(existing_item.get('group_members', [])) if existing_item and existing_item.get('group_members') else '',
            width=600,
            visible=existing_item.get('is_group_work', False) if existing_item else False
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
        
        def toggle_group_options(e):
            group_members_field.visible = assignment_type.value == "group"
            self.page.update()
        
        assignment_type.on_change = toggle_group_options
        
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
            
            if assignment_type.value == "group" and group_members_field.value:
                item_data["group_members"] = [member.strip() for member in group_members_field.value.split("\n") if member.strip()]
            
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
            self.show_back_button(),
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
                        group_members_field,
                        github_field,
                        description_field,
                        ft.Row([
                            ft.ElevatedButton(
                                text=self.get_text("save_btn"),
                                icon=ft.Icons.SAVE,
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
        
        self.content_container.content = self.center_content(content)
        self.page.update()

    def show_add_feedback_view(self, e=None):
        """Show add feedback view"""
        self.current_view = "add_feedback"
        
        # Portfolio item selection
        if not self.portfolio_items:
            content = ft.Column([
                self.show_back_button(),
                ft.Card(
                    content=ft.Container(
                        content=ft.Column([
                            ft.Text(self.get_text("feedback_add_title"), size=20, weight=ft.FontWeight.BOLD),
                            ft.Icon(ft.Icons.INFO, color=ft.Colors.BLUE, size=48),
                            ft.Text(self.get_text("no_portfolio_items_msg"), 
                                   size=16, text_align=ft.TextAlign.CENTER),
                            ft.Text(self.get_text("no_portfolio_items_hint"), 
                                   color=ft.Colors.GREY_600, text_align=ft.TextAlign.CENTER),
                        ], spacing=20, horizontal_alignment=ft.CrossAxisAlignment.CENTER),
                        padding=40
                    )
                )
            ])
            
            self.content_container.content = self.center_content(content)
            self.page.update()
            return
        
        # Create dropdown options for portfolio items
        portfolio_options = []
        for i, item in enumerate(self.portfolio_items):
            portfolio_options.append(
                ft.dropdown.Option(
                    key=str(i),
                    text=f"{item.get('title', self.get_text('no_title'))} (LU: {', '.join([str(lo) for lo in item.get('learning_outcomes', [])])})"
                )
            )
        
        portfolio_dropdown = ft.Dropdown(
            label=self.get_text("select_portfolio_item"),
            options=portfolio_options,
            width=600
        )
        
        # Learning outcomes radio group for the selected item  
        lo_radio_group = ft.RadioGroup(content=ft.Column([], spacing=5))
        
        def update_learning_outcomes(e):
            """Update learning outcomes based on selected portfolio item"""
            if not portfolio_dropdown.value:
                lo_radio_group.content.controls.clear()
                self.page.update()
                return
            
            selected_index = int(portfolio_dropdown.value)
            selected_item = self.portfolio_items[selected_index]
            available_los = selected_item.get('learning_outcomes', [])
            
            lo_radio_group.content.controls.clear()
            
            for lo_num in available_los:
                lo_data = self.learning_outcomes[lo_num]
                # Create tooltip text with description and examples
                tooltip_text = f"Beschrijving: {lo_data['description']}\n\nVoorbeelden: {', '.join(lo_data['examples'])}"
                
                radio = ft.Radio(
                    value=str(lo_num),
                    label=f"LU{lo_num}: {lo_data['title']}",
                    tooltip=tooltip_text
                )
                lo_radio_group.content.controls.append(radio)
            
            self.page.update()
        
        portfolio_dropdown.on_change = update_learning_outcomes
        
        # Feedback fields
        feedback_from_field = ft.TextField(
            label=self.get_text("feedback_from_label"),
            width=600
        )
        
        feedback_text_field = ft.TextField(
            label=self.get_text("feedback_text_label"),
            multiline=True,
            min_lines=4,
            max_lines=8,
            width=600
        )
        
        error_text = ft.Text("", color=ft.Colors.RED, visible=False)
        success_text = ft.Text("", color=ft.Colors.GREEN, visible=False)
        
        def save_feedback(e):
            if not portfolio_dropdown.value:
                error_text.value = self.get_text("select_portfolio_item_error")
                error_text.visible = True
                success_text.visible = False
                self.page.update()
                return
            
            selected_lo = lo_radio_group.value
            if not selected_lo:
                error_text.value = "⚠️ Selecteer een leeruitkomst voor de feedback!"
                error_text.visible = True
                success_text.visible = False
                self.page.update()  
                return
            
            if not feedback_from_field.value or not feedback_text_field.value:
                error_text.value = "⚠️ Vul alle verplichte velden (*) in!"
                error_text.visible = True
                success_text.visible = False
                self.page.update()
                return
            
            # Add feedback to the selected portfolio item
            selected_index = int(portfolio_dropdown.value)
            
            feedback_entry = {
                "from": feedback_from_field.value.strip(),
                "text": feedback_text_field.value.strip(),
                "learning_outcomes": [int(selected_lo)],  # Only one learning outcome now
                "date": datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
            }
            
            # Initialize feedback list if it doesn't exist
            if 'feedback' not in self.portfolio_items[selected_index]:
                self.portfolio_items[selected_index]['feedback'] = []
            
            self.portfolio_items[selected_index]['feedback'].append(feedback_entry)
            
            self.save_data()
            
            error_text.visible = False
            success_text.value = "✅ Feedback succesvol toegevoegd!"
            success_text.visible = True
            
            # Clear form
            feedback_from_field.value = ""
            feedback_text_field.value = ""
            portfolio_dropdown.value = None
            lo_radio_group.content.controls.clear()
            lo_radio_group.value = None
            
            self.page.update()
        
        content = ft.Column([
            self.show_back_button(),
            ft.Card(
                content=ft.Container(
                    content=ft.Column([
                        ft.Text(self.get_text("feedback_add_title"), size=20, weight=ft.FontWeight.BOLD),
                        ft.Text(self.get_text("feedback_add_subtitle"), 
                               size=14, color=ft.Colors.GREY_600),
                        error_text,
                        success_text,
                        portfolio_dropdown,
                        ft.Text("Selecteer een leeruitkomst voor deze feedback:", weight=ft.FontWeight.BOLD),
                        ft.Container(
                            content=lo_radio_group,
                            height=150,
                            bgcolor=ft.Colors.GREY_50,
                            border_radius=5,
                            padding=10
                        ),
                        feedback_from_field,
                        feedback_text_field,
                        ft.Row([
                            ft.ElevatedButton(
                                text="Feedback Opslaan",
                                icon=ft.Icons.SAVE,
                                on_click=save_feedback,
                                style=ft.ButtonStyle(
                                    bgcolor=ft.Colors.BLUE_600,
                                    color=ft.Colors.WHITE
                                )
                            )
                        ])
                    ], spacing=15),
                    padding=20
                )
            )
        ], scroll=ft.ScrollMode.AUTO)
        
        self.content_container.content = self.center_content(content)
        self.page.update()

    def show_add_feedback_for_item_view(self, item_index):
        """Show add feedback view for a specific portfolio item"""
        self.current_view = "add_feedback_item"
        
        selected_item = self.portfolio_items[item_index]
        available_los = selected_item.get('learning_outcomes', [])
        
        # Learning outcomes radio buttons for the selected item with tooltips
        radio_buttons = []
        for lo_num in available_los:
            lo_data = self.learning_outcomes[lo_num]
            # Create tooltip text with description and examples
            tooltip_text = f"Beschrijving: {lo_data['description']}\n\nVoorbeelden: {', '.join(lo_data['examples'])}"
            
            radio = ft.Radio(
                value=str(lo_num),
                label=f"LU{lo_num}: {lo_data['title']}",
                tooltip=tooltip_text
            )
            radio_buttons.append(radio)
        
        lo_radio_group = ft.RadioGroup(
            content=ft.Column(radio_buttons, spacing=5)
        )
        
        # Feedback fields
        feedback_from_field = ft.TextField(
            label=self.get_text("feedback_from_label"),
            width=600
        )
        
        feedback_text_field = ft.TextField(
            label=self.get_text("feedback_text_label"),
            multiline=True,
            min_lines=4,
            max_lines=8,
            width=600
        )
        
        error_text = ft.Text("", color=ft.Colors.RED, visible=False)
        success_text = ft.Text("", color=ft.Colors.GREEN, visible=False)
        
        def save_feedback(e):
            selected_lo = lo_radio_group.value
            if not selected_lo:
                error_text.value = "⚠️ Selecteer een leeruitkomst voor de feedback!"
                error_text.visible = True
                success_text.visible = False
                self.page.update()
                return
            
            if not feedback_from_field.value or not feedback_text_field.value:
                error_text.value = "⚠️ Vul alle verplichte velden (*) in!"
                error_text.visible = True
                success_text.visible = False
                self.page.update()
                return
            
            # Add feedback to the selected portfolio item
            feedback_entry = {
                "from": feedback_from_field.value.strip(),
                "text": feedback_text_field.value.strip(),
                "learning_outcomes": [int(selected_lo)],  # Only one learning outcome now
                "date": datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
            }
            
            # Initialize feedback list if it doesn't exist
            if 'feedback' not in self.portfolio_items[item_index]:
                self.portfolio_items[item_index]['feedback'] = []
            
            self.portfolio_items[item_index]['feedback'].append(feedback_entry)
            
            self.save_data()
            
            error_text.visible = False
            success_text.value = "✅ Feedback succesvol toegevoegd!"
            success_text.visible = True
            
            # Clear form
            feedback_from_field.value = ""
            feedback_text_field.value = ""
            lo_radio_group.value = None
            
            self.page.update()
        
        content = ft.Column([
            self.show_back_button(),
            ft.Card(
                content=ft.Container(
                    content=ft.Column([
                        ft.Text("Feedback Toevoegen", size=20, weight=ft.FontWeight.BOLD),
                        ft.Text(f"{self.get_text('portfolio_item_label')} {selected_item.get('title', self.get_text('no_title'))}", 
                               size=16, weight=ft.FontWeight.BOLD, color=ft.Colors.BLUE_700),
                        ft.Text(self.get_text("add_feedback_to_item"), 
                               size=14, color=ft.Colors.GREY_600),
                        error_text,
                        success_text,
                        ft.Text("Selecteer een leeruitkomst voor deze feedback:", weight=ft.FontWeight.BOLD),
                        lo_radio_group,
                        feedback_from_field,
                        feedback_text_field,
                        ft.Row([
                            ft.ElevatedButton(
                                text="Feedback Opslaan",
                                icon=ft.Icons.SAVE,
                                on_click=save_feedback,
                                style=ft.ButtonStyle(
                                    bgcolor=ft.Colors.BLUE_600,
                                    color=ft.Colors.WHITE
                                )
                            )
                        ])
                    ], spacing=15),
                    padding=20
                )
            )
        ], scroll=ft.ScrollMode.AUTO)
        
        self.content_container.content = self.center_content(content)
        self.page.update()

    def show_all_feedback_view(self, e=None):
        """Show all feedback from all portfolio items in an overview"""
        self.current_view = "all_feedback"
        
        feedback_cards = []
        
        # Collect all feedback from all portfolio items
        for item_idx, item in enumerate(self.portfolio_items):
            feedback_list = item.get('feedback', [])
            if feedback_list:
                # Create card for this portfolio item's feedback
                item_feedback_card = ft.Card(
                    content=ft.Container(
                        content=ft.Column([
                            ft.Text(f"Portfolio Item: {item['title']}", 
                                   size=18, weight=ft.FontWeight.BOLD, color=ft.Colors.BLUE_700),
                            ft.Text(f"Datum: {item.get('date', 'Onbekend')}", 
                                   size=12, color=ft.Colors.GREY_600),
                            ft.Divider(),
                            
                            # Show all feedback for this item
                            ft.Column([
                                ft.Container(
                                    content=ft.Column([
                                        ft.Row([
                                            ft.Text(f"Van: {feedback.get('from', 'Onbekend')}", 
                                                   weight=ft.FontWeight.BOLD, color=ft.Colors.GREEN_700),
                                            ft.Text(f"Datum: {feedback.get('date', 'Onbekend')}", 
                                                   color=ft.Colors.GREY_600, size=12)
                                        ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
                                        ft.Row([
                                            ft.Text(f"LU: {', '.join([f'{lo}' for lo in feedback.get('learning_outcomes', [])])}", 
                                                   color=ft.Colors.BLUE_600, size=12)
                                        ]),
                                        ft.Text(feedback.get('text', ''), 
                                               size=14, color=ft.Colors.BLACK87)
                                    ], spacing=5),
                                    bgcolor=ft.Colors.GREY_50,
                                    padding=10,
                                    border_radius=5,
                                    margin=ft.margin.only(bottom=10)
                                ) for feedback in feedback_list
                            ], spacing=5)
                        ], spacing=10),
                        padding=20
                    ),
                    margin=ft.margin.only(bottom=15)
                )
                feedback_cards.append(item_feedback_card)
        
        if not feedback_cards:
            # No feedback found
            content = ft.Column([
                self.show_back_button(),
                ft.Card(
                    content=ft.Container(
                        content=ft.Column([
                            ft.Icon(ft.Icons.FEEDBACK_OUTLINED, size=64, color=ft.Colors.GREY_400),
                            ft.Text(self.get_text("no_feedback_found"), size=20, weight=ft.FontWeight.BOLD),
                            ft.Text(self.get_text("no_feedback_msg"), 
                                   size=14, color=ft.Colors.GREY_600, text_align=ft.TextAlign.CENTER),
                            ft.Text(self.get_text("no_feedback_hint"), 
                                   size=14, color=ft.Colors.GREY_600, text_align=ft.TextAlign.CENTER)
                        ], spacing=15, horizontal_alignment=ft.CrossAxisAlignment.CENTER),
                        padding=40
                    )
                )
            ], scroll=ft.ScrollMode.AUTO)
        else:
            # Show all feedback
            content = ft.Column([
                self.show_back_button(),
                ft.Card(
                    content=ft.Container(
                        content=ft.Column([
                            ft.Text(self.get_text("all_feedback_title"), size=24, weight=ft.FontWeight.BOLD),
                            ft.Text(f"Totaal {len(feedback_cards)} portfolio item(s) met feedback", 
                                   size=14, color=ft.Colors.GREY_600),
                            ft.Divider()
                        ], spacing=10),
                        padding=20
                    ),
                    margin=ft.margin.only(bottom=10)
                ),
                ft.Column(feedback_cards, spacing=0)
            ], scroll=ft.ScrollMode.AUTO)
        
        self.content_container.content = self.center_content(content)
        self.page.update()

    def show_submit_document_view(self, e=None):
        """Show document submission view"""
        self.current_view = "submit_document"
        
        proud_field = ft.TextField(
            label=self.get_text("proud_of_label"),
            multiline=True,
            min_lines=4,
            value=self.reflection_data.get('proud_of', ''),
            width=600
        )
        
        struggled_field = ft.TextField(
            label=self.get_text("struggled_with_label"),
            multiline=True,
            min_lines=4,
            value=self.reflection_data.get('struggled_with', ''),
            width=600
        )
        
        learn_field = ft.TextField(
            label=self.get_text("want_to_learn_label"),
            multiline=True,
            min_lines=4,
            value=self.reflection_data.get('want_to_learn', ''),
            width=600
        )
        
        # Always start unchecked for security
        complete_checkbox = ft.Checkbox(
            label=self.get_text("confirm_complete"),
            value=False
        )
        
        generate_md_checkbox = ft.Checkbox(
            label=self.get_text("generate_markdown"),
            value=False
        )
        
        error_text = ft.Text("", color=ft.Colors.RED, visible=False)
        success_text = ft.Text("", color=ft.Colors.GREEN, visible=False)
        
        # Create the generate button (initially disabled)
        generate_button = ft.ElevatedButton(
            text="Document Genereren",
            icon=ft.Icons.DESCRIPTION,
            disabled=True,
            style=ft.ButtonStyle(
                bgcolor=ft.Colors.GREY_400,
                color=ft.Colors.WHITE
            )
        )
        
        def update_button_state(e=None):
            """Update button state based on checkbox"""
            if complete_checkbox.value:
                generate_button.disabled = False
                generate_button.style = ft.ButtonStyle(
                    bgcolor=ft.Colors.ORANGE_600,
                    color=ft.Colors.WHITE
                )
            else:
                generate_button.disabled = True
                generate_button.style = ft.ButtonStyle(
                    bgcolor=ft.Colors.GREY_400,
                    color=ft.Colors.WHITE
                )
            self.page.update()
        
        def generate_document(e):
            if not proud_field.value or not struggled_field.value or not learn_field.value:
                error_text.value = "⚠️ Vul alle reflectie vragen in!"
                error_text.visible = True
                success_text.visible = False
                self.page.update()
                return
            
            if not complete_checkbox.value:
                error_text.value = "⚠️ Bevestig dat je portfolio compleet is!"
                error_text.visible = True
                success_text.visible = False
                self.page.update()
                return
            
            self.reflection_data = {
                "proud_of": proud_field.value.strip(),
                "struggled_with": struggled_field.value.strip(),
                "want_to_learn": learn_field.value.strip(),
                "is_complete": True,
                "generate_markdown": generate_md_checkbox.value,
                "submission_date": datetime.datetime.now().isoformat()
            }
            self.save_data()
            
            # Generate documents
            try:
                self.generate_documents()
                error_text.visible = False
                success_text.value = "✅ Document succesvol gegenereerd!"
                success_text.visible = True
                self.page.update()
            except Exception as ex:
                error_text.value = f"❌ Document generatie mislukt: {str(ex)}"
                error_text.visible = True
                success_text.visible = False
                self.page.update()
        
        # Set the checkbox change handler and button click handler
        complete_checkbox.on_change = update_button_state
        generate_button.on_click = generate_document
        
        content = ft.Column([
            self.show_back_button(),
            ft.Card(
                content=ft.Container(
                    content=ft.Column([
                        ft.Text("Document Inleveren", size=20, weight=ft.FontWeight.BOLD),
                        ft.Text("Reflectie Vragen", size=16, weight=ft.FontWeight.BOLD),
                        error_text,
                        success_text,
                        proud_field,
                        struggled_field,
                        learn_field,
                        complete_checkbox,
                        generate_md_checkbox,
                        generate_button
                    ], spacing=15),
                    padding=20
                )
            )
        ], scroll=ft.ScrollMode.AUTO)
        
        self.content_container.content = self.center_content(content)
        self.page.update()

    def update_display(self):
        """Update the display with current data"""
        # Update student info
        if self.student_info:
            semester = self.student_info.get('semester', '')
            info_text = f"Naam: {self.student_info.get('name', '')} | " \
                       f"Studentnummer: {self.student_info.get('student_number', '')} | " \
                       f"Semester: {semester} | " \
                       f"Peilmoment: {self.student_info.get('milestone', '')}"
            self.info_text.value = info_text
            
            # Update window title
            if semester:
                self.page.title = f"Portfolio Document Manager - TI S{semester}"
        
        # Only update portfolio data if we're in main view
        if self.current_view != "main":
            self.page.update()
            return
        
        # Update attention message for feedback
        items_without_feedback = self.count_items_without_feedback()
        if items_without_feedback > 0:
            if items_without_feedback == 1:
                attention_text = self.get_text("attention_items_without_feedback_single").format(items_without_feedback)
            else:
                attention_text = self.get_text("attention_items_without_feedback_multiple").format(items_without_feedback)
            
            self.attention_card.content = ft.Container(
                content=ft.Row([
                    ft.Icon(ft.Icons.WARNING, color=ft.Colors.RED),
                    ft.Text(self.get_text("important"), weight=ft.FontWeight.BOLD, color=ft.Colors.RED),
                    ft.Text(attention_text, color=ft.Colors.RED)
                ], wrap=True),
                padding=20,
                bgcolor=ft.Colors.RED_50
            )
            self.attention_card.visible = True
        else:
            if self.portfolio_items:  # Only show if there are items
                self.attention_card.content = ft.Container(
                    content=ft.Row([
                        ft.Icon(ft.Icons.CHECK_CIRCLE, color=ft.Colors.GREEN),
                        ft.Text(self.get_text("attention_all_items_have_feedback"), color=ft.Colors.GREEN)
                    ], wrap=True),
                    padding=20,
                    bgcolor=ft.Colors.GREEN_50
                )
                self.attention_card.visible = True
            else:
                self.attention_card.visible = False
        
        # Update portfolio items table
        self.portfolio_data_table.rows.clear()
        
        for i, item in enumerate(self.portfolio_items):
            learning_outcomes_text = ", ".join([f"LU{lo}" for lo in item.get('learning_outcomes', [])])
            item_type = self.get_text("type_group") if item.get('is_group_work', False) else self.get_text("type_personal")
            feedback_count = len(item.get('feedback', []))
            
            self.portfolio_data_table.rows.append(
                ft.DataRow(
                    cells=[
                        ft.DataCell(ft.Text(item.get('title', 'Geen titel'))),
                        ft.DataCell(ft.Text(learning_outcomes_text)),
                        ft.DataCell(ft.Text(item_type)),
                        ft.DataCell(ft.Text(item.get('date_added', ''))),
                        ft.DataCell(ft.Text(f"({feedback_count})")),
                        ft.DataCell(
                            ft.Row([
                                ft.IconButton(
                                    icon=ft.Icons.EDIT,
                                    tooltip="Bewerken",
                                    on_click=lambda e, idx=i: self.edit_portfolio_item(idx)
                                ),
                                ft.IconButton(
                                    icon=ft.Icons.FEEDBACK,
                                    tooltip="Feedback Toevoegen",
                                    on_click=lambda e, idx=i: self.show_add_feedback_for_item_view(idx)
                                ),
                                ft.IconButton(
                                    icon=ft.Icons.DELETE,
                                    tooltip="Verwijderen",
                                    on_click=lambda e, idx=i: self.delete_portfolio_item(idx)
                                )
                            ], tight=True)
                        )
                    ]
                )
            )
        
        self.page.update()

    def first_time_setup(self):
        """First time setup dialog"""
        name_field = ft.TextField(label="Naam student", width=350)
        number_field = ft.TextField(label="Studentnummer", width=350)
        semester_dropdown = ft.Dropdown(
            label="Semester (2-8)",
            options=[ft.dropdown.Option(str(i)) for i in range(2, 9)],
            value="4",
            width=350
        )
        milestone_dropdown = ft.Dropdown(
            label="Peilmoment (1-4)",
            options=[ft.dropdown.Option(str(i)) for i in range(1, 5)],
            value="1",
            width=350
        )
        
        def save_and_close(e):
            if not name_field.value or not number_field.value:
                self.show_error_dialog("Fout", "Vul alle velden in!")
                return
            
            self.student_info = {
                "name": name_field.value.strip(),
                "student_number": number_field.value.strip(),
                "semester": semester_dropdown.value,
                "milestone": milestone_dropdown.value
            }
            self.save_data()
            self.update_display()
            self.close_dialog(dialog)
            self.page.update()
        
        dialog = ft.AlertDialog(
            modal=True,
            title=ft.Text("Eerste Installatie"),
            content=ft.Container(
                content=ft.Column([
                    ft.Text("Welkom bij de Portfolio Document Manager!", 
                           size=18, weight=ft.FontWeight.BOLD),
                    ft.Text("Vul eerst je basisgegevens in:", size=14),
                    name_field,
                    number_field,
                    semester_dropdown,
                    milestone_dropdown,
                ], spacing=15),
                width=450,
                height=400
            ),
            actions=[
                ft.TextButton("Annuleren", on_click=lambda e: setattr(dialog, 'open', False)),
                ft.ElevatedButton("OK", on_click=save_and_close)
            ]
        )
        
        self.page.dialog = dialog
        dialog.open = True
        self.page.update()

    def edit_student_info(self, e):
        """Edit student information"""
        name_field = ft.TextField(label="Naam student", value=self.student_info.get("name", ""), width=350)
        number_field = ft.TextField(label="Studentnummer", value=self.student_info.get("student_number", ""), width=350)
        semester_dropdown = ft.Dropdown(
            label="Semester (2-8)",
            options=[ft.dropdown.Option(str(i)) for i in range(2, 9)],
            value=self.student_info.get("semester", "2"),
            width=350
        )
        milestone_dropdown = ft.Dropdown(
            label="Peilmoment (1-4)",
            options=[ft.dropdown.Option(str(i)) for i in range(1, 5)],
            value=self.student_info.get("milestone", "1"),
            width=350
        )
        
        def save_and_close(e):
            self.student_info = {
                "name": name_field.value.strip(),
                "student_number": number_field.value.strip(),
                "semester": semester_dropdown.value,
                "milestone": milestone_dropdown.value
            }
            self.save_data()
            self.update_display()
            self.close_dialog(dialog)
            self.page.update()
        
        dialog = ft.AlertDialog(
            modal=True,
            title=ft.Text("Student Gegevens Wijzigen"),
            content=ft.Container(
                content=ft.Column([
                    name_field,
                    number_field,
                    semester_dropdown,
                    milestone_dropdown,
                ], spacing=15),
                width=450,
                height=300
            ),
            actions=[
                ft.TextButton("Annuleren", on_click=lambda e: setattr(dialog, 'open', False)),
                ft.ElevatedButton("Opslaan", on_click=save_and_close)
            ]
        )
        
        self.page.dialog = dialog
        dialog.open = True
        self.page.update()

    def add_portfolio_item(self, e):
        """Add a new portfolio item"""
        self.show_add_portfolio_item_view()

    def edit_portfolio_item(self, index):
        """Edit existing portfolio item"""
        self.show_add_portfolio_item_view(existing_item=self.portfolio_items[index], index=index)

    def delete_portfolio_item(self, index):
        """Delete portfolio item with inline confirmation"""
        self.current_view = "delete_confirm"
        
        item = self.portfolio_items[index]
        
        def confirm_delete(e):
            del self.portfolio_items[index]
            self.save_data()
            self.show_main_view()
        
        def cancel_delete(e):
            self.show_main_view()
        
        content = ft.Column([
            self.show_back_button(),
            ft.Card(
                content=ft.Container(
                    content=ft.Column([
                        ft.Text("Portfolio Item Verwijderen", size=20, weight=ft.FontWeight.BOLD),
                        ft.Icon(ft.Icons.WARNING, color=ft.Colors.RED, size=48),
                        ft.Text(f"Weet je zeker dat je '{item.get('title', 'dit item')}' wilt verwijderen?", 
                               size=16, text_align=ft.TextAlign.CENTER),
                        ft.Text("Deze actie kan niet ongedaan worden gemaakt.", 
                               color=ft.Colors.RED, text_align=ft.TextAlign.CENTER),
                        ft.Row([
                            ft.ElevatedButton(
                                text="Annuleren",
                                icon=ft.Icons.CANCEL,
                                on_click=cancel_delete,
                                style=ft.ButtonStyle(
                                    bgcolor=ft.Colors.GREY_600,
                                    color=ft.Colors.WHITE
                                )
                            ),
                            ft.ElevatedButton(
                                text="Verwijderen",
                                icon=ft.Icons.DELETE,
                                on_click=confirm_delete,
                                style=ft.ButtonStyle(
                                    bgcolor=ft.Colors.RED_600,
                                    color=ft.Colors.WHITE
                                )
                            )
                        ], alignment=ft.MainAxisAlignment.CENTER, spacing=20)
                    ], spacing=20, horizontal_alignment=ft.CrossAxisAlignment.CENTER),
                    padding=40
                )
            )
        ])
        
        self.content_container.content = self.center_content(content)
        self.page.update()

    def close_dialog(self, dialog):
        """Close dialog and update page"""
        dialog.open = False
        self.page.update()

    def manage_portfolio_items(self, e):
        """Open portfolio items management (simplified as edit is now inline)"""
        if not self.portfolio_items:
            self.show_info_dialog("Info", "Er zijn nog geen portfolio items toegevoegd.")
            return
        # For now, just show info since we have inline editing
        self.show_info_dialog("Portfolio Items Beheren", "Je kunt portfolio items bewerken en verwijderen via de actieknoppen in de tabel.")

    def submit_document(self, e):
        """Submit the document - collect reflection data and generate markdown/PDF"""
        self.show_submit_document_view()

    def open_submission_dialog(self):
        """Open submission dialog"""
        proud_field = ft.TextField(
            label="Waar ik het meest trots op ben:",
            multiline=True,
            min_lines=4,
            value=self.reflection_data.get('proud_of', ''),
            width=550
        )
        
        struggled_field = ft.TextField(
            label="Waar ik de afgelopen periode moeite mee heb gehad en welke actie ik heb ondernomen:",
            multiline=True,
            min_lines=4,
            value=self.reflection_data.get('struggled_with', ''),
            width=550
        )
        
        learn_field = ft.TextField(
            label="Wat ik nog graag wil leren en welke actie ik wil gaan ondernemen:",
            multiline=True,
            min_lines=4,
            value=self.reflection_data.get('want_to_learn', ''),
            width=550
        )
        
        complete_checkbox = ft.Checkbox(
            label="Ik bevestig dat mijn portfolio compleet is en klaar voor inlevering",
            value=self.reflection_data.get('is_complete', False)
        )
        
        generate_md_checkbox = ft.Checkbox(
            label="Ook markdown (.md) bestand genereren",
            value=False
        )
        
        error_text = ft.Text("", color=ft.Colors.RED, visible=False)
        success_text = ft.Text("", color=ft.Colors.GREEN, visible=False)
        
        def generate_document(e):
            if not proud_field.value or not struggled_field.value or not learn_field.value:
                error_text.value = "⚠️ Vul alle reflectie vragen in!"
                error_text.visible = True
                success_text.visible = False
                self.page.update()
                return
            
            if not complete_checkbox.value:
                error_text.value = "⚠️ Bevestig dat je portfolio compleet is!"
                error_text.visible = True
                success_text.visible = False
                self.page.update()
                return
            
            self.reflection_data = {
                "proud_of": proud_field.value.strip(),
                "struggled_with": struggled_field.value.strip(),
                "want_to_learn": learn_field.value.strip(),
                "is_complete": True,
                "generate_markdown": generate_md_checkbox.value,
                "submission_date": datetime.datetime.now().isoformat()
            }
            self.save_data()
            
            # Generate documents
            try:
                self.generate_documents()
                error_text.visible = False
                success_text.value = "✅ Document succesvol gegenereerd!"
                success_text.visible = True
                self.page.update()
            except Exception as ex:
                error_text.value = f"❌ Document generatie mislukt: {str(ex)}"
                error_text.visible = True
                success_text.visible = False
                self.page.update()
        
        content = ft.Column([
            self.show_back_button(),
            ft.Card(
                content=ft.Container(
                    content=ft.Column([
                        ft.Text("Document Inleveren", size=20, weight=ft.FontWeight.BOLD),
                        ft.Text("Reflectie Vragen", size=16, weight=ft.FontWeight.BOLD),
                        error_text,
                        success_text,
                        proud_field,
                        struggled_field,
                        learn_field,
                        complete_checkbox,
                        generate_md_checkbox,
                        ft.ElevatedButton(
                            text="Document Genereren",
                            icon=ft.Icons.DESCRIPTION,
                            on_click=generate_document,
                            style=ft.ButtonStyle(
                                bgcolor=ft.Colors.ORANGE_600,
                                color=ft.Colors.WHITE
                            )
                        )
                    ], spacing=15),
                    padding=20
                )
            )
        ], scroll=ft.ScrollMode.AUTO)
        
        self.content_container.content = self.center_content(content)
        self.page.update()

    def generate_documents(self):
        """Generate markdown and PDF documents"""
        try:
            # Generate markdown content
            markdown_content = self.generate_markdown_document()
            
            # Save markdown file temporarily for PDF generation
            timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
            temp_markdown_filename = f"temp_verantwoordingsdocument_{timestamp}.md"
            
            with open(temp_markdown_filename, 'w', encoding='utf-8') as f:
                f.write(markdown_content)
            
            generated_files = []
            
            # Generate PDF (always)
            try:
                self.generate_pdf(temp_markdown_filename)
                pdf_filename = temp_markdown_filename.replace('.md', '.pdf')
                final_pdf_filename = f"Verantwoordingsdocument_{self.student_info.get('name', 'Student')}_{timestamp}.pdf"
                os.rename(pdf_filename, final_pdf_filename)
                generated_files.append(f"PDF: {final_pdf_filename}")
            except Exception as e:
                self.show_error_dialog("PDF Generatie", f"PDF generatie is mislukt: {str(e)}")
                # Clean up temp file
                if os.path.exists(temp_markdown_filename):
                    os.remove(temp_markdown_filename)
                return
            
            # Generate markdown file if requested
            if self.reflection_data.get('generate_markdown', False):
                final_markdown_filename = f"Verantwoordingsdocument_{self.student_info.get('name', 'Student')}_{timestamp}.md"
                os.rename(temp_markdown_filename, final_markdown_filename)
                generated_files.append(f"Markdown: {final_markdown_filename}")
            else:
                # Remove temp markdown file if not needed
                if os.path.exists(temp_markdown_filename):
                    os.remove(temp_markdown_filename)
            
            # Show success message
            files_text = "\\n".join(generated_files)
            self.show_info_dialog("Succes", f"Document succesvol gegenereerd!\\n\\n{files_text}")
            
        except Exception as e:
            self.show_error_dialog("Fout", f"Document generatie mislukt: {str(e)}")

    def generate_markdown_document(self):
        """Generate the complete markdown document (restored to main.py style)"""
        content = []
        # Header
        content.append("![logo](https://www.hu.nl/-/media/hu/afbeeldingen/algemeen/hu-logo.ashx) [](logo-id)\n")
        content.append("# Verantwoordingsdocument[](title-id) <!-- omit in toc -->\n")
        semester = self.student_info.get('semester', '4')
        content.append("### Inhoud[](toc-id)\n")
        content.append(f"- [Portfolio Technische Informatica (TI) semester {semester} (S{semester})](#portfolio-technische-informatica-ti-semester-{semester}-s{semester})")
        content.append("- [Algemeen](#algemeen)")
        content.append("- [Leeruitkomsten](#leeruitkomsten)")
        for i in range(1, 10):
            content.append(f"  - [Leeruitkomst {i} {self.learning_outcomes[i]['title']}](#leeruitkomst-{i}-{self.learning_outcomes[i]['title'].lower()})")
        content.append("")
        content.append("---\n")
        content.append("**v1.0.5 [](version-id)** Gegenereerd door Portfolio Document Manager[](author-id).\n")
        content.append("---\n")
        semester = self.student_info.get('semester', '4')
        content.append(f"<h2 class='portfolio-header'>Portfolio Technische Informatica (TI) semester {semester} (S{semester})</h2>\n")
        content.append("Onderwerp | Graag invullen | Opmerking")
        content.append("--- | --- | ---")
        content.append(f"*Peilmoment* | `peilmoment {self.student_info.get('milestone', '')}` | ")
        content.append(f"*Naam student* | `{self.student_info.get('name', '')}` | ")
        content.append(f"*Studentnummer* | `{self.student_info.get('student_number', '')}` | ")
        content.append(f"*Semester* | `semester {semester}` | ")
        content.append(f"*Datum* | `{datetime.datetime.now().strftime('%d-%m-%Y')}` | dd-mm-jjjj\n")
        content.append("## Algemeen\n")
        content.append(f"*Waar ik het meest trots op ben:*\n")
        content.append(f"    {self.reflection_data.get('proud_of', '--')}\n")
        content.append(f"*Waar ik de afgelopen periode moeite mee heb gehad en welke actie ik heb ondernomen:*\n")
        content.append(f"    {self.reflection_data.get('struggled_with', '--')}\n")
        content.append(f"*Wat ik nog graag wil leren en welke actie ik wil gaan ondernemen:*\n")
        content.append(f"    {self.reflection_data.get('want_to_learn', '--')}\n")
        content.append("---\n")
        content.append("## Leeruitkomsten\n")
        for lo_num in range(1, 10):
            lo = self.learning_outcomes[lo_num]
            content.append(f"### Leeruitkomst {lo_num} {lo['title']}\n")
            content.append(f"*{lo['description']}*\n")
            content.append("")
            content.append("**Indicatoren:**")
            content.append("")
            content.append('<ul class="indicators-list">')
            for indicator in lo['indicators']:
                content.append(f"<li>{indicator}</li>")
            content.append("</ul>")
            content.append("")
            content.append("---\n")
            personal_items = [item for item in self.portfolio_items 
                            if lo_num in item.get('learning_outcomes', []) and not item.get('is_group_work', False)]
            group_items = [item for item in self.portfolio_items 
                         if lo_num in item.get('learning_outcomes', []) and item.get('is_group_work', False)]
            if personal_items or group_items:
                if personal_items:
                    content.append(f"**Leeruitkomst {lo_num} Persoonlijke opdrachten:**\n")
                    content.append("| Portfolio-item     | Beschrijving                                           | Bewijslast               |")
                    content.append("|--------------------|--------------------------------------------------------|--------------------------|")
                    for item in personal_items:
                        content.append(f"| {item.get('title', 'Portfolio-item')} | {item.get('description', 'Beschrijving niet beschikbaar')} | [link naar {item.get('github_link', 'repository')}]({item.get('github_link', 'http://')}) |")
                    content.append("")
                    for item in personal_items:
                        relevant_feedback = [feedback for feedback in item.get('feedback', []) 
                                           if lo_num in feedback.get('learning_outcomes', [])]
                        if relevant_feedback:
                            content.append(f"**Feedback op {item.get('title')} voor Leeruitkomst {lo_num}:**")
                            content.append('<div class="feedback-section">')
                            for feedback in relevant_feedback:
                                content.append(f'<div class="feedback-item">')
                                content.append(f'<strong>{feedback.get("from", "Onbekend")}</strong> ({feedback.get("date", "Geen datum")}):')
                                content.append(f'<p>{feedback.get("text", "")}</p>')
                                content.append(f'</div>')
                            content.append('</div>')
                            content.append("")
                if group_items:
                    content.append(f"**Leeruitkomst {lo_num} Groepsopdrachten:**\n")
                    content.append("| Portfolio-item     | Beschrijving                                           | Bewijslast               |")
                    content.append("|--------------------|--------------------------------------------------------|--------------------------|")
                    for item in group_items:
                        content.append(f"| {item.get('title', 'Portfolio-item')} | {item.get('description', 'Beschrijving niet beschikbaar')} | [link naar {item.get('github_link', 'repository')}]({item.get('github_link', 'http://')}) |")
                    content.append("")
                    for item in group_items:
                        relevant_feedback = [feedback for feedback in item.get('feedback', []) 
                                           if lo_num in feedback.get('learning_outcomes', [])]
                        if relevant_feedback:
                            content.append(f"**Feedback op {item.get('title')} voor Leeruitkomst {lo_num}:**")
                            content.append('<div class="feedback-section">')
                            for feedback in relevant_feedback:
                                content.append(f'<div class="feedback-item">')
                                content.append(f'<strong>{feedback.get("from", "Onbekend")}</strong> ({feedback.get("date", "Geen datum")}):')
                                content.append(f'<p>{feedback.get("text", "")}</p>')
                                content.append(f'</div>')
                            content.append('</div>')
                            content.append("")
            else:
                content.append("<div class='no-portfolio-item'>Student heeft nog geen portfolio item ingeleverd voor deze leeruitkomst.</div>\n")
            content.append("---\n")
        return "\n".join(content)

    def generate_pdf(self, markdown_filename):
        """Generate PDF from markdown using weasyprint (restored to main.py style)"""
        with open(markdown_filename, 'r', encoding='utf-8') as f:
            markdown_content = f.read()
        html_content = markdown.markdown(markdown_content, extensions=['tables'])
        html_with_css = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset=\"UTF-8\">
            <style>
                body {{ font-family: Arial, sans-serif; margin: 40px; line-height: 1.6; }}
                h1, h2, h3 {{ color: #333; }}
                h2.portfolio-header {{ font-size: 1.3em; }}
                table {{ border-collapse: collapse; width: 100%; margin: 20px 0; }}
                th, td {{ border: 1px solid #ddd; padding: 8px; text-align: left; }}
                th {{ background-color: #f2f2f2; }}
                code {{ background-color: #f4f4f4; padding: 2px 4px; border-radius: 3px; }}
                pre {{ background-color: #f4f4f4; padding: 10px; border-radius: 5px; overflow-x: auto; }}
                .no-portfolio-item {{ color: red; font-weight: bold; }}
                h3 + p em {{ font-style: italic; font-size: 0.9em; color: #666; }}
                p strong:contains(\"Indicatoren:\") {{ font-weight: bold; }}
                .indicators-list {{ font-style: normal; font-size: 1em; color: #333; margin-top: 0.5em; }}
                .indicators-list li {{ margin: 0.2em 0; }}
                .feedback-section {{ margin: 10px 0; }}
                .feedback-item {{ margin-bottom: 15px; padding: 10px; background-color: #f9f9f9; border-left: 3px solid #ddd; }}
                .feedback-item strong {{ color: #555; }}
                .feedback-item p {{ margin: 5px 0 0 0; line-height: 1.4; }}
            </style>
        </head>
        <body>
        {html_content}
        </body>
        </html>
        """
        pdf_filename = markdown_filename.replace('.md', '.pdf')
        weasyprint.HTML(string=html_with_css).write_pdf(pdf_filename)

    def load_data(self):
        """Load data from JSON file"""
        if os.path.exists(self.data_file):
            try:
                with open(self.data_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                
                self.student_info = data.get("student_info", {})
                self.portfolio_items = data.get("portfolio_items", [])
                self.reflection_data = data.get("reflection_data", {})
                self.current_language = data.get("language", "nl")  # Default to Dutch
            except Exception as e:
                print(f"ERROR: Laden van data mislukt: {str(e)}")

    def save_data(self):
        """Save data to JSON file"""
        try:
            data = {
                "student_info": self.student_info,
                "portfolio_items": self.portfolio_items,
                "reflection_data": self.reflection_data,
                "language": self.current_language
            }
            with open(self.data_file, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
        except Exception as e:
            print(f"ERROR: Opslaan van data mislukt: {str(e)}")

    def export_data(self, e):
        """Export data to file"""
        try:
            data = {
                "student_info": self.student_info,
                "portfolio_items": self.portfolio_items,
                "reflection_data": self.reflection_data
            }
            filename = f"portfolio_export_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
            print(f"INFO: Data geëxporteerd naar {filename}")
        except Exception as e:
            print(f"ERROR: Exporteren mislukt: {str(e)}")

    def import_data(self, e):
        """Import data from file"""
        filename = "portfolio_data.json"
        try:
            if os.path.exists(filename):
                with open(filename, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                
                self.student_info = data.get("student_info", {})
                self.portfolio_items = data.get("portfolio_items", [])
                self.reflection_data = data.get("reflection_data", {})
                
                self.save_data()
                self.show_main_view()
                print(f"INFO: Data geïmporteerd van {filename}")
            else:
                print(f"ERROR: Bestand {filename} niet gevonden")
        except Exception as e:
            print(f"ERROR: Importeren mislukt: {str(e)}")

    def count_items_without_feedback(self):
        """Count portfolio items that have no feedback"""
        count = 0
        for item in self.portfolio_items:
            # Check if item has any feedback
            if not item.get('feedback') or len(item.get('feedback', [])) == 0:
                count += 1
        return count

    def show_error_dialog(self, title, message):
        """Show error as inline message (simplified)"""
        print(f"ERROR: {title} - {message}")

    def show_info_dialog(self, title, message):
        """Show info as inline message (simplified)"""
        print(f"INFO: {title} - {message}")

    def setup_github(self, e):
        """Setup GitHub credentials"""
        # Show a dialog that this feature is under development
        dialog = ft.AlertDialog(
            modal=True,
            title=ft.Text(self.get_text("github_integration")),
            content=ft.Container(
                content=ft.Column([
                    ft.Icon(ft.Icons.CONSTRUCTION, size=64, color=ft.Colors.ORANGE),
                    ft.Text(self.get_text("feature_development"), size=18, weight=ft.FontWeight.BOLD),
                    ft.Text(self.get_text("github_under_development"), size=14),
                    ft.Text(self.get_text("feature_future_version"), size=14, color=ft.Colors.GREY_600),
                ], spacing=15, horizontal_alignment=ft.CrossAxisAlignment.CENTER),
                width=400,
                height=200
            ),
            actions=[
                ft.ElevatedButton(self.get_text("ok_btn"), on_click=lambda e: setattr(dialog, 'open', False))
            ]
        )
        
        self.page.dialog = dialog
        dialog.open = True
        self.page.update()

    def show_learning_outcomes_info(self, e):
        """Show learning outcomes info in the main content area"""
        self.current_view = "learning_outcomes"
        
        # Create tabs for different learning outcomes
        tabs = []
        for lo_num, lo_data in self.learning_outcomes.items():
            # Create content for this learning outcome
            content = ft.Column([
                ft.Text(f"Leeruitkomst {lo_num}: {lo_data['title']}", 
                       size=18, weight=ft.FontWeight.BOLD),
                ft.Divider(),
                ft.Text(self.get_text("description_label_lo"), size=16, weight=ft.FontWeight.BOLD),
                ft.Text(lo_data['description'], size=14),
                ft.Divider(),
                ft.Text(self.get_text("indicators_label"), size=16, weight=ft.FontWeight.BOLD),
                ft.Column([
                    ft.Text(f"• {indicator}", size=14) 
                    for indicator in lo_data['indicators']
                ]),
                ft.Divider(),
                ft.Text(self.get_text("examples_label"), size=16, weight=ft.FontWeight.BOLD),
                ft.Column([
                    ft.Text(f"• {example}", size=14)
                    for example in lo_data['examples']
                ])
            ], spacing=10, scroll=ft.ScrollMode.AUTO)
            
            tab = ft.Tab(
                text=f"LU{lo_num}",
                content=ft.Container(
                    content=content,
                    padding=20
                )
            )
            tabs.append(tab)
        
        # Create main content with tabs
        main_content = ft.Column([
            self.show_back_button(),
            ft.Card(
                content=ft.Container(
                    content=ft.Column([
                        ft.Text(self.get_text("learning_outcomes_title"), size=24, weight=ft.FontWeight.BOLD),
                        ft.Text(self.get_text("learning_outcomes_subtitle"), 
                               size=14, color=ft.Colors.GREY_600),
                        ft.Divider(),
                        ft.Container(
                            content=ft.Tabs(
                                tabs=tabs,
                                selected_index=0
                            ),
                            height=500
                        )
                    ], spacing=15),
                    padding=20
                )
            )
        ], scroll=ft.ScrollMode.AUTO)
        
        self.content_container.content = self.center_content(main_content)
        self.page.update()

    def show_about(self, e=None):
        """Show about information"""
        self.current_view = "about"
        
        content = ft.Column([
            self.show_back_button(),
            ft.Card(
                content=ft.Container(
                    content=ft.Column([
                        ft.Text(self.get_text("about_title"), size=24, weight=ft.FontWeight.BOLD),
                        ft.Divider(),
                        ft.Text(self.get_text("version_label"), size=16, weight=ft.FontWeight.BOLD),
                        ft.Text(self.get_text("about_description"), size=14),
                        ft.Divider(),
                        ft.Text(self.get_text("developed_by"), size=16, weight=ft.FontWeight.BOLD),
                        ft.Text("• Rick van der Voort", size=14, weight=ft.FontWeight.BOLD, color=ft.Colors.BLUE_700),
                        ft.TextButton(
                            text="🔗 GitHub: @RickMageddon",
                            url="https://github.com/RickMageddon",
                            style=ft.ButtonStyle(
                                color=ft.Colors.BLUE_600,
                                bgcolor=ft.Colors.BLUE_50
                            )
                        ),
                        ft.Divider(),
                        ft.Text(self.get_text("copyright"), size=12, color=ft.Colors.GREY_600)
                    ], spacing=15),
                    padding=30
                )
            )
        ], scroll=ft.ScrollMode.AUTO)
        
        self.content_container.content = self.center_content(content)
        self.page.update()

    def show_feedback_info(self, e=None):
        """Show feedback about the app (for giving feedback on the app itself)"""
        self.current_view = "feedback_info"
        
        import webbrowser
        
        def open_feedback_link(e):
            webbrowser.open("https://github.com/RickMageddon/PortfolioDocumentManager/issues")
        
        content = ft.Column([
            self.show_back_button(),
            ft.Card(
                content=ft.Container(
                    content=ft.Column([
                        ft.Text(self.get_text("feedback_info_title"), size=24, weight=ft.FontWeight.BOLD),
                        ft.Divider(),
                        ft.Text(self.get_text("improve_app"), size=18, weight=ft.FontWeight.BOLD),
                        ft.Text(self.get_text("feedback_help"), size=14),
                        ft.Divider(),
                        ft.Text(self.get_text("how_to_give_feedback"), size=16, weight=ft.FontWeight.BOLD),
                        ft.Text(self.get_text("share_experience"), size=14),
                        ft.Text(self.get_text("report_bugs"), size=14),
                        ft.Text(self.get_text("suggest_features"), size=14),
                        ft.Text(self.get_text("ux_tips"), size=14),
                        ft.Divider(),
                        ft.Text(self.get_text("feedback_categories"), size=16, weight=ft.FontWeight.BOLD),
                        ft.Text(self.get_text("bug_report"), size=14),
                        ft.Text(self.get_text("feature_request"), size=14),
                        ft.Text(self.get_text("documentation"), size=14),
                        ft.Text(self.get_text("ui_ux"), size=14),
                        ft.Text(self.get_text("performance"), size=14),
                        ft.Divider(),
                        ft.Text(self.get_text("give_feedback"), size=16, weight=ft.FontWeight.BOLD),
                        ft.TextButton(
                            text=self.get_text("feedback_github_link"),
                            on_click=open_feedback_link,
                            style=ft.ButtonStyle(
                                color=ft.Colors.BLUE_700,
                                bgcolor=ft.Colors.BLUE_50
                            )
                        ),
                        ft.Divider(),
                        ft.Row([
                            ft.Icon(ft.Icons.FAVORITE, color=ft.Colors.RED),
                            ft.Text(self.get_text("thanks_msg"), 
                                   color=ft.Colors.RED, weight=ft.FontWeight.BOLD)
                        ])
                    ], spacing=15),
                    padding=30
                )
            )
        ], scroll=ft.ScrollMode.AUTO)
        
        self.content_container.content = self.center_content(content)
        self.page.update()

    def toggle_theme_mode(self, e=None):
        """Toggle between light and dark theme"""
        if self.page.theme_mode == ft.ThemeMode.LIGHT:
            self.page.theme_mode = ft.ThemeMode.DARK
            e.control.icon = ft.Icons.LIGHT_MODE
        else:
            self.page.theme_mode = ft.ThemeMode.LIGHT
            e.control.icon = ft.Icons.DARK_MODE
        self.page.update()

    def get_text(self, key):
        """Get translated text for current language"""
        return self.translations.get(self.current_language, {}).get(key, key)

    def refresh_table_headers(self):
        """Refresh the data table headers with current language"""
        self.portfolio_data_table.columns = [
            ft.DataColumn(ft.Text(self.get_text("table_title"))),
            ft.DataColumn(ft.Text(self.get_text("table_learning_outcomes"))),
            ft.DataColumn(ft.Text(self.get_text("table_type"))),
            ft.DataColumn(ft.Text(self.get_text("table_date"))),
            ft.DataColumn(ft.Text(self.get_text("table_feedback"))),
            ft.DataColumn(ft.Text(self.get_text("table_actions"))),
        ]

    def change_language(self, language_code):
        """Change language to specified language code"""
        if language_code in ["nl", "en"]:
            self.current_language = language_code
            
            # Update page title
            self.page.title = self.get_text("app_title")
            
            # Save language preference
            self.save_data()
            
            # Refresh table headers
            self.refresh_table_headers()
            
            # Update only the appbar with new translations
            self.page.appbar = ft.AppBar(
                title=ft.Text(self.get_text("app_title")),
                bgcolor=ft.Colors.BLUE_700,
                color=ft.Colors.WHITE,
                leading=ft.PopupMenuButton(
                    items=[
                        ft.PopupMenuItem(text=self.get_text("menu_main"), on_click=lambda e: self.show_main_view()),
                        ft.PopupMenuItem(),  # Separator
                        ft.PopupMenuItem(text=self.get_text("menu_about"), on_click=self.show_about),
                        ft.PopupMenuItem(text=self.get_text("menu_feedback"), on_click=self.show_feedback_info),
                        ft.PopupMenuItem(),  # Separator
                        ft.PopupMenuItem(text=self.get_text("menu_student_info"), on_click=self.show_student_info_view),
                        ft.PopupMenuItem(text=self.get_text("menu_github"), on_click=self.setup_github),
                        ft.PopupMenuItem(),  # Separator
                        ft.PopupMenuItem(text=self.get_text("menu_export"), on_click=self.export_data),
                        ft.PopupMenuItem(text=self.get_text("menu_import"), on_click=self.import_data),
                    ],
                    icon=ft.Icons.MENU
                ),
                actions=[
                    ft.TextButton(
                        text=self.get_text("btn_learning_outcomes"),
                        on_click=self.show_learning_outcomes_info,
                        style=ft.ButtonStyle(color=ft.Colors.WHITE)
                    ),
                    ft.PopupMenuButton(
                        items=[
                            ft.PopupMenuItem(
                                text="🇳🇱 Nederlands",
                                on_click=lambda e: self.change_language("nl")
                            ),
                            ft.PopupMenuItem(
                                text="🇬🇧 English", 
                                on_click=lambda e: self.change_language("en")
                            ),
                        ],
                        icon=ft.Icons.LANGUAGE,
                        icon_color=ft.Colors.WHITE,
                        tooltip=self.get_text("tooltip_language")
                    ),
                    ft.IconButton(
                        icon=ft.Icons.LIGHT_MODE if self.page.theme_mode == ft.ThemeMode.DARK else ft.Icons.DARK_MODE,
                        tooltip=self.get_text("tooltip_theme"),
                        on_click=self.toggle_theme_mode,
                        icon_color=ft.Colors.WHITE
                    )
                ]
            )
            
            # Refresh the main view to show translated buttons only if we're on main view
            if self.current_view == "main":
                self.show_main_view()
            
            # Update the page
            self.page.update()

    def toggle_language(self, e=None):
        """Toggle between Dutch and English (kept for compatibility)"""
        new_language = "en" if self.current_language == "nl" else "nl"
        self.change_language(new_language)


def main(page: ft.Page):
    """Main entry point for the Flet application"""
    try:
        # Force window to be visible and properly configured
        page.window_visible = True
        page.window_prevent_close = True
        page.window_always_on_top = False
        page.window_focused = True
        
        # Set window icon - try multiple methods for Linux compatibility
        icon_paths = [
            "icon.png",
            "assets/icon.png",
            "/home/rick/Documents/Code/PortfolioDocumentManager/icon.png",
            os.path.join(os.path.dirname(__file__), "icon.png") if hasattr(sys, '_MEIPASS') else "icon.png",
            os.path.join(sys._MEIPASS, "icon.png") if hasattr(sys, '_MEIPASS') else None
        ]
        
        icon_set = False
        for icon_path in icon_paths:
            if icon_path and os.path.exists(icon_path):
                try:
                    page.window_icon = icon_path
                    print(f"Window icon set to: {icon_path}")
                    icon_set = True
                    break
                except Exception as e:
                    print(f"Failed to set icon {icon_path}: {e}")
                    continue
        
        if not icon_set:
            print("Warning: Could not set window icon")
        
        # Ensure the window appears on screen (window_center not available in this Flet version)
        
        print("Initializing Portfolio Manager...")
        
        # Initialize the application
        app = PortfolioManager(page)
        
        # Try to set window properties after initialization for Linux
        if os.name == 'posix':  # Linux/Unix
            try:
                # Set additional window properties for better Linux integration
                page.window_title_bar_hidden = False
                page.window_title_bar_buttons_hidden = False
                
                # Force window class name for better desktop integration
                if hasattr(page, 'window_class_name'):
                    page.window_class_name = "PortfolioManager"
                
                # Try setting icon again after initialization
                if os.path.exists("icon.png"):
                    page.window_icon = "icon.png"
                elif os.path.exists("/home/rick/Documents/Code/PortfolioDocumentManager/icon.png"):
                    page.window_icon = "/home/rick/Documents/Code/PortfolioDocumentManager/icon.png"
                    
                page.update()
                print("Linux-specific window properties set")
            except Exception as e:
                print(f"Could not set Linux window properties: {e}")
        
        # Handle window close event
        def on_window_event(e):
            if e.data == "close":
                print("Application closing...")
                page.window_destroy()
        
        page.window_on_event = on_window_event
        
        # Force update to ensure window is visible
        page.update()
        
        print("Portfolio Manager initialized successfully!")
        
    except Exception as e:
        print(f"Error initializing app: {e}")
        import traceback
        traceback.print_exc()
        
        # Create a simple error page that's definitely visible
        page.title = "Portfolio Document Manager - Error"
        page.window_visible = True
        # page.window_center() not available in this Flet version
        page.clean()
        
        error_text = ft.Text(
            f"Error starting application:\n{str(e)}\n\nCheck the console for more details.", 
            color=ft.Colors.RED,
            size=16,
            selectable=True
        )
        
        page.add(ft.Container(
            content=ft.Column([
                ft.Text("Portfolio Document Manager", size=24, weight=ft.FontWeight.BOLD),
                ft.Divider(),
                error_text,
                ft.ElevatedButton(
                    "Close Application",
                    on_click=lambda e: page.window_close()
                )
            ], spacing=20),
            padding=20,
            alignment=ft.alignment.center,
            expand=True
        ))
        page.update()

def check_environment():
    """Check if the environment is suitable for running the app"""
    import platform
    
    system = platform.system()
    print(f"Running on {system} {platform.release()}")
    
    if system == "Linux":
        # Check for display
        display = os.environ.get('DISPLAY')
        if not display:
            print("Warning: No DISPLAY environment variable set")
            print("Setting DISPLAY=:0")
            os.environ['DISPLAY'] = ':0'
        else:
            print(f"DISPLAY is set to: {display}")
        
        # Check for Wayland
        wayland_display = os.environ.get('WAYLAND_DISPLAY')
        if wayland_display:
            print(f"Wayland display detected: {wayland_display}")
        
        # Check XDG session type
        session_type = os.environ.get('XDG_SESSION_TYPE', 'unknown')
        print(f"Session type: {session_type}")
    
    return True


if __name__ == "__main__":
    # Single startup guard to prevent loops
    if hasattr(sys.modules[__name__], '_app_started'):
        sys.exit(0)
    sys.modules[__name__]._app_started = True
    
    print("=" * 50)
    print("Portfolio Document Manager v1.5.13")
    print("=" * 50)
    
    try:
        # Check environment first
        check_environment()
        
        # Set environment variables for better Flet compatibility
        os.environ["FLET_WEB_APP_PATH"] = ""
        os.environ["FLET_SERVER_PORT"] = "0"  # Use random available port
        
        print("Starting desktop application...")
        
        # Only use desktop mode for better PyInstaller compatibility
        ft.app(
            target=main,
            view=ft.AppView.FLET_APP,  # Force desktop app only
            assets_dir="assets" if os.path.exists("assets") else None,
            port=0,  # Use random available port
            web_renderer="html"  # Use HTML renderer for better compatibility
        )
        
    except KeyboardInterrupt:
        print("\nApplication interrupted by user.")
        sys.exit(0)
        
    except ImportError as e:
        print(f"\nIMPORT ERROR: {e}")
        print("\nRequired Python packages are missing.")
        print("Please ensure all dependencies are installed:")
        print("pip install flet flet-core markdown weasyprint")
        sys.exit(1)
        
    except Exception as e:
        print(f"\nAPPLICATION ERROR: {e}")
        
        error_str = str(e).lower()
        if "libmpv" in error_str or "cannot open shared object file" in error_str:
            print("\nSystem library missing: libmpv")
            print("Install with: sudo apt install libmpv1")
        elif "display" in error_str or "x11" in error_str:
            print("\nDisplay server connection failed.")
            print("Make sure you're running in a desktop environment.")
        elif "name 'exit' is not defined" in error_str:
            print("\nInternal error in Flet framework detected.")
            print("This is a known compatibility issue.")
            # Don't attempt fallback - just exit cleanly
            print("Application cannot start with current configuration.")
        elif "address already in use" in error_str:
            print("\nPort conflict detected.")
            print("Please close any other instances of the application.")
        else:
            print(f"\nUnexpected error occurred.")
            print(f"Error details: {str(e)}")
        
        print("\nApplication cannot start.")
        sys.exit(1)