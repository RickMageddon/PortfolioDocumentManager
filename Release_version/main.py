# Start de app als script direct wordt uitgevoerd
#!/usr/bin/env python3
"""
PeilDocument Program
Een programma voor het beheren van portfolio items voor het verantwoordingsdocument.
"""

import tkinter as tk
from tkinter import ttk, messagebox, filedialog, simpledialog
import json
import os
import datetime
import webbrowser
from typing import Dict, List, Optional
import markdown
import subprocess
import sys

class PortfolioManager:
    def open_github_issues(self):
        webbrowser.open_new("https://github.com/RickMageddon/PortfolioDocumentManager/issues")
    def show_help_page(self):
        uitleg = (
            "1. Vul je studentgegevens in via Opties.\n"
            "2. Voeg portfolio items toe met de knop.\n"
            "3. Voeg feedback toe aan items.\n"
            "4. Gebruik 'Document Inleveren' om je PDF te genereren.\n"
            "5. Bekijk alle feedback en leeruitkomsten via de knoppen bovenin.\n"
            "6. Gebruik het Help-menu voor meer uitleg en info."
        )
        messagebox.showinfo("Uitleg: Hoe werkt de app?", uitleg)
    def show_app_info(self):
        self.show_about()
    def show_help(self):
        messagebox.showinfo("Help", "Welkom bij de Portfolio Document Manager!\n\nGebruik de knoppen en menu's bovenin om portfolio items te beheren, feedback te bekijken en leeruitkomsten te raadplegen.")
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("PeilDocument Manager")
        self.root.geometry("1050x700")
        
        # Data storage
        self.data_file = "portfolio_data.json"
        self.student_info = {}
        self.portfolio_items = []
        self.reflection_data = {}
        
        # Leeruitkomsten per semester
        self.semester_learning_outcomes = {
            "2": {
                1: {"title": "Analyseren", "description": "Student analyseert de met de opdrachtgever afgestemde functionaliteit en hoofdlijnen van de (eenvoudige) IoT oplossing en stelt aan de hand hiervan requirements op.", "indicators": [], "examples": [], "competentie": "Analyseren"},
                2: {"title": "Ontwerpen", "description": "Student zet de requirements om in logische onderdelen voor de oplossing, onderzoekt de toepasbaarheid van componenten, maakt bewuste keuzes in de samenstelling en ontwerpt hiermee de IoT-oplossing.", "indicators": [], "examples": [], "competentie": "Ontwerpen"},
                3: {"title": "Realiseren", "description": "Student realiseert vanuit een ontwerp een eenvoudige toekomstbestendige IoT oplossing in zowel hard- als software waarbij integratie van componenten via software een onderdeel is.", "indicators": [], "examples": [], "competentie": "Realisatie"},
                4: {"title": "Samenwerken", "description": "Student werkt doelgericht en met verantwoordelijkheid samen door zich aan afspraken te houden, taken op te pakken en uit te voeren, teamleden op de hoogte te houden, feedback te geven, feedback te ontvangen en waar nodig om hulp te vragen en aan te bieden.", "indicators": [], "examples": [], "competentie": "Samenwerken"},
                5: {"title": "Communiceren", "description": "Student deelt een boodschap helder met het team en opdrachtgever en is in staat om diens werk te presenteren aan peers en opdrachtgever en vraagt door om onduidelijkheden weg te nemen.", "indicators": [], "examples": [], "competentie": "Communiceren"},
                6: {"title": "Reflecteren / Verbeteren / Evalueren", "description": "Student evalueert eigen gedrag en eigen leerontwikkeling, kijkt kritisch terug op eigen handelen en de invloed daarvan op de teamprestaties/leerontwikkeling, herkent hierin de eigen sterktes en verbeterpunten, en kan deze vervolgens vertalen naar concrete acties.", "indicators": [], "examples": [], "competentie": "Reflecteren / Verbeteren / Evalueren"},
                7: {"title": "Testen / Evalueren", "description": "Student voert eenvoudige tests uit in strikte overeenstemming met gecommuniceerde instructies en evalueert de resultaten om uitspraken te kunnen doen over de kwaliteit van de code en het systeem.", "indicators": [], "examples": [], "competentie": "Testen / Evalueren"},
                8: {"title": "Plannen", "description": "Student is in staat om een eenvoudige planning voor zichzelf en/of voor het team op te stellen door grote taken op te delen in kleinere (deel)taken om zodoende het gestelde doel te bereiken en zich daaraan te kunnen houden. Naar aanleiding van (gecontroleerde) gebeurtenissen kan de student zijn planning aanpassen en deze aanpassingen toelichten.", "indicators": [], "examples": [], "competentie": "Plannen"},
                9: {"title": "Opleveren / Documenteren", "description": "Student levert, in een daarvoor ingerichte versiebeheeromgeving, de producten en diensten op zodanig dat de opdrachtgever en peers verder kunnen met de doorontwikkeling van de resultaten waarvan een bijdrage aan de documentatie een wezenlijk onderdeel is.", "indicators": [], "examples": [], "competentie": "Opleveren / Documenteren"}
            },
            "3": {
                1: {"title": "Analyseren", "description": "Student analyseert de vereisten en doelstellingen van de opdrachtgever betreffende een hybride systeem met een real-time embedded subsysteem en een frontend/backend/database subsysteem. Op basis hiervan en rekening houdend met de mogelijke gebruikers deduceert de student requirements volgens een voorgeschreven methode. Deze requirements dienen na validatie door de opdrachtgever als basis voor het ontwerp.", "indicators": [], "examples": [], "competentie": "Analyseren"},
                2: {"title": "Adviseren", "description": "Student adviseert opdrachtgever na de analyse van diens vereisten en doelstellingen over de te implementeren requirements. Het advies is helder onderbouwd en gepresenteerd. Het is goed uit te leggen aan niet-ICT-ers. Het er uit voortvloeiende ontwerp is degelijk onderbouwd en helder gedocumenteerd volgens een voorgeschreven methode, goed uit te leggen aan een volgend ontwikkelteam.", "indicators": [], "examples": [], "competentie": "Adviseren"},
                3: {"title": "Ontwerpen", "description": "Student ontwerpt gebaseerd op de requirements en volgens voorgeschreven methoden een hybride systeem met een real-time embedded subsysteem en een frontend/backend/database subsysteem.", "indicators": [], "examples": [], "competentie": "Ontwerpen"},
                4: {"title": "Realiseren", "description": "Student realiseert vanuit het ontwerp een hybride systeem met een real-time embedded subsysteem en een frontend/backend/database subsysteem. Hij test daarbij de subsystemen zoveel mogelijk apart, alvorens het systeem als geheel te testen. De tests worden uitgevoerd volgens een vooraf beschreven testplan. Testresultaten worden helder gedocumenteerd, evenals de testcontext. De test moet daarmee desgewenst op een later moment gereproduceerd kunnen worden.", "indicators": [], "examples": [], "competentie": "Realiseren"},
                5: {"title": "Beheren", "description": "Student zet een professionele ontwikkelomgeving op. Hij debugt daarmee zijn software op een gestructureerde manier. Een uitdaging daarbij is dat de code van de diverse subsystemen verschillende programmeertalen gebruiken, en het totale systeem dus niet binnen een enkele debugger gedebugd kan worden. De student debugt tevens hardware door efficiënt gebruik te maken van daarvoor geëigende tooling.", "indicators": [], "examples": [], "competentie": "Beheren"},
                6: {"title": "Onderzoekend Vermogen", "description": "Student is in staat om bij zichzelf en/of binnen het projectteam vast te stellen welke kennis ontbreekt om het project adequaat af te ronden. Hij is in staat om de betreffende kennis met kritische houding op een doordachte wijze op te doen.", "indicators": [], "examples": [], "competentie": "Onderzoekend Vermogen"},
                7: {"title": "Organiserend Vermogen", "description": "Student kan zelfstandig een planning opstellen voor een (groeps)project  met het oog op implementatie van de oplossing, rekening houdend met beschikbare middelen, tijd, ethische en duurzaamheidskwesties en te verwachten risico's.", "indicators": [], "examples": [], "competentie": "Organiserend Vermogen"},
                8: {"title": "Interactief Vermogen", "description": "Student kan zich zowel mondeling als schriftelijk in begrijpelijk en correct Nederlands, gericht op het doel, uiten; daarnaast neemt student geregeld het initiatief voor een gesprek met betrokkenen om tijdens dit gesprek relevante input te geven en vragen adequaat te beantwoorden.", "indicators": [], "examples": [], "competentie": "Interactief Vermogen"},
                9: {"title": "Zelflerend Vermogen", "description": "Student kijkt terug op de afgelopen periode om het eigen gedrag ook in relatie tot andermans waarden en normen te analyseren en bepaalt of dat toereikend was. Student past zo nodig het eigen handelen aan, bijvoorbeeld naar aanleiding van feedback van anderen, doet dit periodiek en op systematische wijze, bijvoorbeeld op basis van bestaande reflectiemethoden.", "indicators": [], "examples": [], "competentie": "Zelflerend Vermogen"}
            },
            "4": {
                1: {
                    "title": "S4.1",
                    "description": "Student analyseert de vereisten en doelstellingen van de opdrachtgever betreffende een 'Digital Twin' van een bestaand embedded systeem. Op basis hiervan en rekening houdend met de mogelijke gebruikers deduceert de student requirements volgens een voorgeschreven methode. Deze requirements dienen na validatie door de opdrachtgever als basis voor het ontwerp.",
                    "competentie": "Analyseren"
                },
                2: {
                    "title": "S4.2",
                    "description": "Student adviseert de opdrachtgever, na analyse van de vereisten en doelstellingen, over de inzet van een digital twin. Het advies is helder onderbouwd en gepresenteerd, zodat het begrijpelijk is voor alle stakeholders/betrokkenen. Het voorgestelde ontwerp is goed gedocumenteerd en het advies volgt een voorgeschreven methode, zodat de implementatie efficiënt kan worden voortgezet.",
                    "competentie": "Adviseren"
                },
                3: {
                    "title": "S4.3",
                    "description": "Student ontwerpt gebaseerd op de requirements en volgens voorgeschreven methoden een 'Digital Twin', inclusief grafische representatie, van een bestaand embedded systeem. Dit ontwerp omvat ook een ontwerp voor teststrategieën.",
                    "competentie": "Ontwerpen"
                },
                4: {
                    "title": "S4.4",
                    "description": "Student realiseert vanuit het ontwerp een 'Digital Twin' van een bestaand embedded systeem, inclusief grafische representatie. Hierbij wordt gewerkt volgens een voorgeschreven methode waarin testen centraal staat, ten behoeve van het uitvoeren van tests op verschillende ontwikkelniveaus. Testresultaten, omstandigheden en afhankelijkheden worden helder gedocumenteerd, omwille van het reproduceren van de testresultaten.",
                    "competentie": "Realiseren"
                },
                5: {
                    "title": "S4.5",
                    "description": "Student zet een professionele ontwikkelomgeving op voor desktop development. Daarbij houdt hij rekening met de samenwerking tussen verschillende programmeertalen. De desktop debugging wordt op een gestructureerde manier uitgevoerd. De tests worden uitgevoerd volgens een vooraf beschreven testplan en moeten desgewenst op een later moment reproduceerbaar zijn. De student werkt volgens een voorgeschreven methodiek en maakt gebruik van geschikte tooling software debugging.",
                    "competentie": "Beheren"
                },
                6: {
                    "title": "S4.6",
                    "description": "De student kan een probleem vertalen naar een product door randvoorwaarden en requirements op te stellen in overleg met de opdrachtgever. Het project wordt gestructureerd opgezet, uitgevoerd en opgeleverd, met aandacht voor omgevingsfactoren, en maatschappelijke en ethische aspecten.",
                    "competentie": "Toekomstgericht organiseren"
                },
                7: {
                    "title": "S4.7",
                    "description": "De student onderhoudt actief de relatie met relevante samenwerkingspartners (denk aan teamleden, opdrachtgevers, eindgebruikers, maatschappelijke organisaties en/of andere stakeholders) door middel van het geven van weloverwogen presentaties die afgestemd zijn op de doelgroep.",
                    "competentie": "Doelgericht interacteren"
                },
                8: {
                    "title": "S4.8",
                    "description": "De student bereidt zich voor op studie- en loopbaankeuzes. De student evalueert hierbij persoonlijke ambities en kwaliteiten in relatie tot de gewenste positionering in het werkveld. De student kan deze effectief communiceren in bv sollicitatie brief of gesprek.",
                    "competentie": "Persoonlijk leiderschap"
                },
                9: {
                    "title": "S4.9",
                    "description": "De student kan een praktijkgericht probleem identificeren en de juiste oplossingsrichting kiezen door wensen van de opdrachtgever centraal te stellen. Gedurende het proces handelt de student onderzoekend, stelt kritische vragen en past verschillende (hbo-ICT) methoden toe om relevante informatie te verzamelen. Hierbij wordt de informatie op gestructureerde en grondige wijze geanalyseerd en worden daarmee keuzes onderbouwt, rekening houdend met maatschappelijke standaarden en ethische aspecten.",
                    "competentie": "Onderzoek probleem oplossen"
                }
            }
        }

        # Default: semester 4 leeruitkomsten (huidige)
        self.learning_outcomes = self.semester_learning_outcomes.get("4")
        
        # Load saved data and build the GUI
        self.load_data()
        
        # Set correct semester based on loaded student info
        if self.student_info and self.student_info.get('semester'):
            self.set_semester(self.student_info.get('semester'))
        else:
            self.set_semester("2")  # default
        
        self.setup_gui()

        # If no student info is present, run first time setup
        if not self.student_info:
            self.root.after(100, lambda: self.first_time_setup())

    def set_semester(self, semester):
        """Laad leeruitkomsten voor het gekozen semester"""
        semester_str = str(semester)
        if semester_str in self.semester_learning_outcomes:
            self.learning_outcomes = self.semester_learning_outcomes[semester_str]
            self.current_semester = semester_str
        else:
            # fallback: default
            self.learning_outcomes = self.semester_learning_outcomes.get("4", self.learning_outcomes)
            self.current_semester = "4"

    def show_settings(self):
        settings_win = tk.Toplevel(self.root)
        settings_win.title("Instellingen")
        settings_win.geometry("350x200")

        # Semester selectie
        tk.Label(settings_win, text="Kies semester:").pack(pady=(20,5))
        semester_var = tk.StringVar(value=getattr(self, "current_semester", self.student_info.get("semester", "4")))
        semester_box = ttk.Combobox(settings_win, textvariable=semester_var, values=["2", "3", "4"], state="readonly")
        semester_box.pack(pady=5)

        def update_semester():
            self.set_semester(semester_var.get())
            self.student_info["semester"] = semester_var.get()
            self.save_data()
            self.update_display()
            self.update_learning_outcomes_info()
            messagebox.showinfo("Instelling opgeslagen", f"Semester ingesteld op S{semester_var.get()}")

        tk.Button(settings_win, text="Opslaan", command=update_semester).pack(pady=20)

    def update_learning_outcomes_info(self):
        # Sluit bestaande leeruitkomsten-info dialog als die open is en open opnieuw
        # (of forceer refresh van de view als je die als widget hebt)
        pass

    def setup_gui(self):
        # Menubalk bovenin
        menubar = tk.Menu(self.root)

        # Help menu uitgebreid
        help_menu = tk.Menu(menubar, tearoff=0)
        help_menu.add_command(label="Studentgegevens wijzigen", command=self.edit_student_info)
        help_menu.add_command(label="Info over de app", command=self.show_app_info)
        help_menu.add_command(label="Data exporteren", command=self.export_data)
        help_menu.add_command(label="Data importeren", command=self.import_data)
        help_menu.add_separator()
        help_menu.add_command(label="Uitleg: Hoe werkt de app?", command=self.show_help_page)
        menubar.add_cascade(label="Help", menu=help_menu)

        # Feedback menu: link naar GitHub issues
        feedback_menu = tk.Menu(menubar, tearoff=0)
        feedback_menu.add_command(label="Probleem melden (GitHub)", command=self.open_github_issues)
        menubar.add_cascade(label="Feedback", menu=feedback_menu)

        # Directe knop Leeruitkomsten Info
        menubar.add_command(label="Leeruitkomsten Info", command=self.show_learning_outcomes_info)

        self.root.config(menu=menubar)

        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

        # Student info display
        info_frame = ttk.LabelFrame(main_frame, text="Student Informatie", padding="10")
        info_frame.grid(row=0, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 10))

        self.info_label = ttk.Label(info_frame, text="")
        self.info_label.grid(row=0, column=0, sticky=(tk.W))

        # Attention frame for feedback reminders
        self.attention_frame = ttk.LabelFrame(main_frame, text="⚠️ BELANGRIJK", padding="10")
        self.attention_frame.grid(row=1, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 10))

        self.attention_label = ttk.Label(self.attention_frame, text="", font=("Arial", 10, "bold"), foreground="red")
        self.attention_label.grid(row=0, column=0, sticky=(tk.W))

        # Buttons frame
        buttons_frame = ttk.Frame(main_frame)
        buttons_frame.grid(row=2, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 10))

        ttk.Button(buttons_frame, text="Portfolio Item Toevoegen",
                   command=self.add_portfolio_item, width=25).grid(row=0, column=0, padx=(0, 10))
        ttk.Button(buttons_frame, text="Portfolio Items Beheren",
                   command=self.manage_portfolio_items, width=25).grid(row=0, column=1, padx=(0, 10))
        ttk.Button(buttons_frame, text="Alle Feedback",
                   command=self.show_all_feedback, width=25).grid(row=0, column=2, padx=(10, 0))
        ttk.Button(buttons_frame, text="Feedback toevoegen",
                   command=self.quick_add_feedback, width=25).grid(row=0, column=3, padx=(10, 0))

        # Opvallende Document Inleveren knop helemaal rechts
        submit_btn = tk.Button(buttons_frame, text="Document Inleveren",
                              command=self.submit_document,
                              font=("Arial", 12, "bold"),
                              bg="#ff8800", fg="white", activebackground="#ffaa33",
                              width=30, relief=tk.RAISED, borderwidth=3)
        submit_btn.grid(row=0, column=4, padx=(20,0), sticky="e")

        # Portfolio items list
        list_frame = ttk.LabelFrame(main_frame, text="Portfolio Items", padding="10")
        list_frame.grid(row=3, column=0, columnspan=2, sticky=(tk.W, tk.E, tk.N, tk.S), pady=(0, 10))

        # Treeview for portfolio items
        columns = ("Titel", "Leeruitkomsten", "Type", "Datum", "Feedback")
        self.tree = ttk.Treeview(list_frame, columns=columns, show="headings", height=10)

        # Set column headings and widths
        column_widths = {"Titel": 200, "Leeruitkomsten": 150, "Type": 100, "Datum": 100, "Feedback": 80}
        for col in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=column_widths.get(col, 150))

        scrollbar = ttk.Scrollbar(list_frame, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)

        self.tree.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        scrollbar.grid(row=0, column=1, sticky=(tk.N, tk.S))

        # Configure weights for resizing
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(0, weight=1)
        main_frame.rowconfigure(3, weight=1)
        list_frame.columnconfigure(0, weight=1)
        list_frame.rowconfigure(0, weight=1)

        self.update_display()

    def update_display(self):
        """Update the display with current data"""
        # Update student info
        if self.student_info:
            semester = self.student_info.get('semester', '')
            info_text = f"Naam: {self.student_info.get('name', '')} | " \
                       f"Studentnummer: {self.student_info.get('student_number', '')} | " \
                       f"Semester: {semester} | " \
                       f"Peilmoment: {self.student_info.get('milestone', '')}"
            self.info_label.config(text=info_text)
            # Update window title
            if semester:
                self.root.title(f"PeilDocument Manager - S{semester}")

        # Update portfolio items list
        for item in self.tree.get_children():
            self.tree.delete(item)
        for item in self.portfolio_items:
            learning_outcomes_text = ", ".join([f"LU{lo}" for lo in item.get('learning_outcomes', [])])
            item_type = "Groep" if item.get('is_group_work', False) else "Persoonlijk"
            feedback_count = len(item.get('feedback', []))
            self.tree.insert("", "end", values=(
                item.get('title', 'Geen titel'),
                learning_outcomes_text,
                item_type,
                item.get('date_added', ''),
                f"({feedback_count})"
            ))
        
        # Update attention label with feedback status per learning outcome
        self.update_feedback_attention()

    def update_feedback_attention(self):
        """Update the attention label with total feedback needed"""
        if not self.portfolio_items:
            self.attention_label.config(text="Nog geen portfolio items toegevoegd.", foreground="red")
            return
        
        # Count total items that need feedback
        items_without_feedback = 0
        total_items = 0
        
        for item in self.portfolio_items:
            # Only count items that have learning outcomes assigned
            if item.get('learning_outcomes', []):
                total_items += 1
                if not item.get('feedback', []):
                    items_without_feedback += 1
        
        if total_items == 0:
            self.attention_label.config(text="Geen portfolio items met leeruitkomsten.", foreground="red")
            return
        
        # Show status
        if items_without_feedback == 0:
            self.attention_label.config(
                text="✓ Alle portfolio items hebben feedback!", 
                foreground="green"
            )
        else:
            self.attention_label.config(
                text=f"{items_without_feedback} portfolio item(s) hebben nog geen feedback nodig", 
                foreground="red"
            )

    def first_time_setup(self):
        """First time setup dialog"""
        dialog = tk.Toplevel(self.root)
        dialog.title("Eerste Installatie")
        dialog.geometry("450x400")
        dialog.transient(self.root)
        dialog.grab_set()
        dialog.resizable(False, False)  # Prevent resizing to maintain layout
        
        # Center the dialog
        dialog.geometry("+%d+%d" % (self.root.winfo_rootx() + 50, self.root.winfo_rooty() + 50))
        
        # Ensure dialog is on top
        dialog.lift()
        dialog.focus_force()
        
        # Ensure dialog is always on top
        dialog.lift()
        dialog.focus_force()
        
        frame = ttk.Frame(dialog, padding="15")
        frame.pack(fill=tk.BOTH, expand=True)
        
        ttk.Label(frame, text="Welkom bij de PeilDocument Manager!", 
                 font=("Arial", 12, "bold")).pack(pady=(0, 15))
        
        ttk.Label(frame, text="Vul eerst je basisgegevens in:").pack(anchor="w", pady=(0, 8))
        
        # Student name
        ttk.Label(frame, text="Naam student:").pack(anchor="w")
        name_entry = ttk.Entry(frame, width=40)
        name_entry.pack(pady=(2, 8), fill="x")
        
        # Student number
        ttk.Label(frame, text="Studentnummer:").pack(anchor="w")
        number_entry = ttk.Entry(frame, width=40)
        number_entry.pack(pady=(2, 8), fill="x")
        
        # Semester
        ttk.Label(frame, text="Semester (2-8):").pack(anchor="w")
        semester_var = tk.StringVar(value="4")
        semester_combo = ttk.Combobox(frame, textvariable=semester_var, 
                                    values=["2", "3", "4", "5", "6", "7", "8"], state="readonly", width=37)
        semester_combo.pack(pady=(2, 8), fill="x")
        
        # Milestone
        ttk.Label(frame, text="Peilmoment (1-4):").pack(anchor="w")
        milestone_var = tk.StringVar(value="1")
        milestone_combo = ttk.Combobox(frame, textvariable=milestone_var, 
                                     values=["1", "2", "3", "4"], state="readonly", width=37)
        milestone_combo.pack(pady=(2, 15), fill="x")
        
        def save_and_close():
            name = name_entry.get().strip()
            number = number_entry.get().strip()
            semester = semester_var.get()
            milestone = milestone_var.get()
            
            if not name or not number:
                messagebox.showerror("Fout", "Vul alle velden in!")
                return
            
            self.student_info = {
                "name": name,
                "student_number": number,
                "semester": semester,
                "milestone": milestone
            }
            self.set_semester(semester)  # Laad de juiste leeruitkomsten
            self.save_data()
            self.update_display()
            dialog.destroy()
        
        # Buttons frame for better layout
        button_frame = ttk.Frame(frame)
        button_frame.pack(pady=(15, 0), fill="x")
        
        ttk.Button(button_frame, text="OK", command=save_and_close).pack(side="right", padx=(5, 0))
        ttk.Button(button_frame, text="Annuleren", command=dialog.destroy).pack(side="right")

    def edit_student_info(self):
        """Edit student information"""
        dialog = tk.Toplevel(self.root)
        dialog.title("Student Gegevens Wijzigen")
        dialog.geometry("450x400")
        dialog.transient(self.root)
        dialog.grab_set()
        dialog.resizable(False, False)
        
        # Ensure dialog is on top
        dialog.lift()
        dialog.focus_force()
        
        frame = ttk.Frame(dialog, padding="15")
        frame.pack(fill=tk.BOTH, expand=True)
        
        # Student name
        ttk.Label(frame, text="Naam student:").pack(anchor="w")
        name_entry = ttk.Entry(frame, width=40)
        name_entry.insert(0, self.student_info.get("name", ""))
        name_entry.pack(pady=(2, 8), fill="x")
        
        # Student number
        ttk.Label(frame, text="Studentnummer:").pack(anchor="w")
        number_entry = ttk.Entry(frame, width=40)
        number_entry.insert(0, self.student_info.get("student_number", ""))
        number_entry.pack(pady=(2, 8), fill="x")
        
        # Semester
        ttk.Label(frame, text="Semester (2-8):").pack(anchor="w")
        semester_var = tk.StringVar(value=self.student_info.get("semester", "4"))
        semester_combo = ttk.Combobox(frame, textvariable=semester_var, 
                                    values=["2", "3", "4", "5", "6", "7", "8"], state="readonly", width=37)
        semester_combo.pack(pady=(2, 8), fill="x")
        
        # Milestone
        ttk.Label(frame, text="Peilmoment (1-4):").pack(anchor="w")
        milestone_var = tk.StringVar(value=self.student_info.get("milestone", "1"))
        milestone_combo = ttk.Combobox(frame, textvariable=milestone_var, 
                                     values=["1", "2", "3", "4"], state="readonly", width=37)
        milestone_combo.pack(pady=(2, 15), fill="x")
        
        def save_and_close():
            self.student_info = {
                "name": name_entry.get().strip(),
                "student_number": number_entry.get().strip(),
                "semester": semester_var.get(),
                "milestone": milestone_var.get()
            }
            self.set_semester(semester_var.get())  # Laad de juiste leeruitkomsten
            self.save_data()
            self.update_display()
            dialog.destroy()
        
        button_frame = ttk.Frame(frame)
        button_frame.pack(pady=(15, 0), fill="x")
        ttk.Button(button_frame, text="Opslaan", command=save_and_close).pack(side="right", padx=(5, 0))
        ttk.Button(button_frame, text="Annuleren", command=dialog.destroy).pack(side="right")

    def add_portfolio_item(self):
        """Add a new portfolio item"""
        dialog = PortfolioItemDialog(self.root, self.learning_outcomes)
        self.root.wait_window(dialog.dialog)
        
        if dialog.result:
            dialog.result['date_added'] = datetime.datetime.now().strftime("%Y-%m-%d")
            
            self.portfolio_items.append(dialog.result)
            self.save_data()
            self.update_display()

    def manage_portfolio_items(self):
        """Open portfolio items management window (improved two-pane view)"""
        dialog = tk.Toplevel(self.root)
        dialog.title("Portfolio Items Beheren")
        dialog.geometry("900x650")
        dialog.transient(self.root)
        dialog.grab_set()

        # Ensure dialog is on top
        dialog.lift()
        dialog.focus_force()

        main_frame = ttk.Frame(dialog, padding=10)
        main_frame.pack(fill=tk.BOTH, expand=True)

        # Top: search and add button
        top_frame = ttk.Frame(main_frame)
        top_frame.pack(fill="x", pady=(0, 8))
        ttk.Label(top_frame, text="Zoek:").pack(side="left", padx=(0, 6))
        search_var = tk.StringVar()
        search_entry = ttk.Entry(top_frame, textvariable=search_var, width=40)
        search_entry.pack(side="left", padx=(0, 6))
        ttk.Button(top_frame, text="Wis", command=lambda: (search_var.set(""), refresh_list())).pack(side="left", padx=(6, 6))
        ttk.Button(top_frame, text="Nieuw Portfolio Item", command=lambda: add_item()).pack(side="right")

        content_frame = ttk.Frame(main_frame)
        content_frame.pack(fill=tk.BOTH, expand=True)

        # Left pane: list of items
        left_frame = ttk.Frame(content_frame)
        left_frame.pack(side="left", fill=tk.BOTH, expand=False)
        left_frame.configure(width=320)

        listbox = tk.Listbox(left_frame, width=45, activestyle='none')
        list_scroll = ttk.Scrollbar(left_frame, orient=tk.VERTICAL, command=listbox.yview)
        listbox.configure(yscrollcommand=list_scroll.set)
        listbox.pack(side="left", fill=tk.BOTH, expand=True)
        list_scroll.pack(side="right", fill=tk.Y)

        # Right pane: details
        right_frame = ttk.LabelFrame(content_frame, text="Details", padding=8)
        right_frame.pack(side="left", fill=tk.BOTH, expand=True, padx=(8, 0))

        title_label = ttk.Label(right_frame, text="", font=(None, 12, "bold"), wraplength=480, justify="left")
        title_label.pack(anchor="w", pady=(0, 6))

        lu_label = ttk.Label(right_frame, text="Leeruitkomsten: ", font=(None, 10))
        lu_label.pack(anchor="w")

        type_label = ttk.Label(right_frame, text="Type: ", font=(None, 10))
        type_label.pack(anchor="w", pady=(4, 6))

        github_label = ttk.Label(right_frame, text="GitHub: ", foreground="blue", cursor="hand2")
        github_label.pack(anchor="w", pady=(0, 6))

        desc_label = ttk.Label(right_frame, text="Beschrijving:", font=(None, 10, "bold"))
        desc_label.pack(anchor="w")
        desc_text = tk.Text(right_frame, height=6, wrap=tk.WORD)
        desc_text.configure(state=tk.DISABLED)
        desc_scroll = ttk.Scrollbar(right_frame, orient=tk.VERTICAL, command=desc_text.yview)
        desc_text.configure(yscrollcommand=desc_scroll.set)
        desc_text.pack(fill="x", pady=(0, 8))
        desc_scroll.place(in_=desc_text, relx=1.0, rely=0, relheight=1.0, anchor="ne")

        feedback_label = ttk.Label(right_frame, text="Feedback (preview):", font=(None, 10, "bold"))
        feedback_label.pack(anchor="w")

        feedback_listbox = tk.Listbox(right_frame, height=6)
        feedback_scroll = ttk.Scrollbar(right_frame, orient=tk.VERTICAL, command=feedback_listbox.yview)
        feedback_listbox.configure(yscrollcommand=feedback_scroll.set)
        feedback_listbox.pack(fill="both", expand=True)
        feedback_scroll.place(in_=feedback_listbox, relx=1.0, rely=0, relheight=1.0, anchor="ne")

        # Bottom buttons
        btn_frame = ttk.Frame(dialog, padding=(8, 8))
        btn_frame.pack(fill="x")
        ttk.Button(btn_frame, text="Bewerken", command=lambda: edit_item()).pack(side="left", padx=(0, 6))
        ttk.Button(btn_frame, text="Verwijderen", command=lambda: delete_item()).pack(side="left", padx=(0, 6))
        ttk.Button(btn_frame, text="Sluiten", command=dialog.destroy).pack(side="right")

        # Helper functions
        def open_github(event=None):
            url = current_item.get('github_link', '') if current_item else ''
            if url:
                try:
                    webbrowser.open(url)
                except Exception:
                    messagebox.showinfo("Openen GitHub", f"Kan de link niet openen:\n{url}")

        def refresh_list():
            term = search_var.get().strip().lower()
            listbox.delete(0, tk.END)
            for i, item in enumerate(self.portfolio_items):
                title = item.get('title', 'Untitled')
                if not term or term in title.lower() or term in item.get('description', '').lower():
                    listbox.insert(tk.END, f"{i+1}. {title}")

        current_item = None

        def show_details(event=None):
            nonlocal current_item
            sel = listbox.curselection()
            if not sel:
                # clear details
                current_item = None
                title_label.config(text="")
                lu_label.config(text="Leeruitkomsten: ")
                type_label.config(text="Type: ")
                github_label.config(text="GitHub: ")
                desc_text.config(state=tk.NORMAL)
                desc_text.delete('1.0', tk.END)
                desc_text.config(state=tk.DISABLED)
                feedback_listbox.delete(0, tk.END)
                return

            # Determine actual index from displayed list entry
            displayed_index = sel[0]
            term = search_var.get().strip().lower()
            visible_indices = [i for i, item in enumerate(self.portfolio_items) if not term or term in item.get('title', '').lower() or term in item.get('description', '').lower()]
            if displayed_index >= len(visible_indices):
                return
            idx = visible_indices[displayed_index]
            current_item = self.portfolio_items[idx]

            title_label.config(text=current_item.get('title', ''))
            lu_text = ", ".join([f"LU{lo}" for lo in current_item.get('learning_outcomes', [])])
            lu_label.config(text=f"Leeruitkomsten: {lu_text}")
            type_label.config(text=("Groep" if current_item.get('is_group_work') else "Persoonlijk"))
            github_label.config(text=(current_item.get('github_link', '')))
            github_label.bind("<Button-1>", open_github)

            desc_text.config(state=tk.NORMAL)
            desc_text.delete('1.0', tk.END)
            desc_text.insert(tk.END, current_item.get('description', ''))
            desc_text.config(state=tk.DISABLED)

            feedback_listbox.delete(0, tk.END)
            for fb in current_item.get('feedback', []):
                lo_text = ''
                if fb.get('learning_outcomes'):
                    lo_text = f" ({', '.join([f'LU{n}' for n in fb.get('learning_outcomes', [])])})"
                snippet = fb.get('text', '').replace('\n', ' ')
                if len(snippet) > 60:
                    snippet = snippet[:60].rsplit(' ', 1)[0] + '...'
                feedback_listbox.insert(tk.END, f"{fb.get('from', 'Onbekend')}{lo_text}: {snippet}")

        def add_item():
            dialog_item = PortfolioItemDialog(dialog, self.learning_outcomes)
            dialog.wait_window(dialog_item.dialog)
            if dialog_item.result:
                dialog_item.result['date_added'] = datetime.datetime.now().strftime("%Y-%m-%d")
                self.portfolio_items.append(dialog_item.result)
                self.save_data()
                self.update_display()
                refresh_list()

        def edit_item():
            sel = listbox.curselection()
            if not sel:
                messagebox.showwarning("Selectie", "Selecteer eerst een item.")
                return
            displayed_index = sel[0]
            term = search_var.get().strip().lower()
            visible_indices = [i for i, item in enumerate(self.portfolio_items) if not term or term in item.get('title', '').lower() or term in item.get('description', '').lower()]
            idx = visible_indices[displayed_index]
            existing = self.portfolio_items[idx]

            edit_dialog = PortfolioItemDialog(dialog, self.learning_outcomes, existing)
            dialog.wait_window(edit_dialog.dialog)
            if edit_dialog.result:
                self.portfolio_items[idx] = edit_dialog.result
                self.save_data()
                self.update_display()
                refresh_list()

        def delete_item():
            sel = listbox.curselection()
            if not sel:
                messagebox.showwarning("Selectie", "Selecteer eerst een item.")
                return
            if not messagebox.askyesno("Bevestiging", "Weet je zeker dat je dit item wilt verwijderen?"):
                return
            displayed_index = sel[0]
            term = search_var.get().strip().lower()
            visible_indices = [i for i, item in enumerate(self.portfolio_items) if not term or term in item.get('title', '').lower() or term in item.get('description', '').lower()]
            idx = visible_indices[displayed_index]
            del self.portfolio_items[idx]
            self.save_data()
            self.update_display()
            refresh_list()

        # Bind events
        listbox.bind('<<ListboxSelect>>', show_details)
        search_entry.bind('<KeyRelease>', lambda e: refresh_list())

        # Initial population
        refresh_list()
        # If items exist, select first
        if listbox.size() > 0:
            listbox.selection_set(0)
            show_details()

    def submit_document(self):
        """Submit the document - collect reflection data and generate markdown/PDF"""
        dialog = SubmissionDialog(self.root, self.reflection_data)
        self.root.wait_window(dialog.dialog)
        
        if dialog.result:
            self.reflection_data = dialog.result
            self.save_data()
            
            # Generate markdown document
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
                messagebox.showerror("PDF Generatie", f"PDF generatie is mislukt: {str(e)}")
                # Clean up temp file
                if os.path.exists(temp_markdown_filename):
                    os.remove(temp_markdown_filename)
                return
            
            # Generate markdown file if requested
            if dialog.result.get('generate_markdown', False):
                final_markdown_filename = f"Verantwoordingsdocument_{self.student_info.get('name', 'Student')}_{timestamp}.md"
                os.rename(temp_markdown_filename, final_markdown_filename)
                generated_files.append(f"Markdown: {final_markdown_filename}")
            else:
                # Remove temp markdown file if not needed
                if os.path.exists(temp_markdown_filename):
                    os.remove(temp_markdown_filename)
            
            # Show success message
            files_text = "\n".join(generated_files)
            messagebox.showinfo("Succes", f"Document succesvol gegenereerd!\n\n{files_text}")

            # Vraag de gebruiker of we automatisch naar het volgende peilmoment moeten
            try:
                advance = messagebox.askyesno("Volgende peilmoment", "Wil je automatisch naar het volgende peilmoment gaan?")
                if advance:
                    # Milestones are stored as strings like '1'..'4'
                    current = int(self.student_info.get('milestone', '1') or 1)
                    if current < 4:
                        new = current + 1
                        self.student_info['milestone'] = str(new)
                        self.save_data()
                        self.update_display()
                        messagebox.showinfo("Peilmoment bijgewerkt", f"Peilmoment verhoogd naar {new}.")
                    else:
                        messagebox.showinfo("Peilmoment", "Het peilmoment is al 4; kan niet verder verhogen.")
            except Exception:
                # Niet-kritische prompt; negeren bij fouten
                pass

    def generate_markdown_document(self):
        """Generate the complete markdown document"""
        content = []
        
        # Header
        content.append("![logo](https://www.hu.nl/-/media/hu/afbeeldingen/algemeen/hu-logo.ashx) [](logo-id)\n")
        content.append("# Verantwoordingsdocument[](title-id) <!-- omit in toc -->\n")
        
        # Table of contents (simplified)
        semester = self.student_info.get('semester', '4')
        content.append("### Inhoud[](toc-id)\n")
        content.append(f"- [Portfolio Technische Informatica (TI) semester {semester} (S{semester})](#portfolio-technische-informatica-ti-semester-{semester}-s{semester})")
        content.append("- [Algemeen](#algemeen)")
        content.append("- [Leeruitkomsten](#leeruitkomsten)")
        
        # Add TOC entries for all learning outcomes
        for i in range(1, 10):
            content.append(f"  - [Leeruitkomst {i} {self.learning_outcomes[i]['title']}](#leeruitkomst-{i}-{self.learning_outcomes[i]['title'].lower()})")
        
        content.append("")
        content.append("---\n")
        content.append("**v1.0.0 [](version-id)** Gegenereerd door PeilDocument Manager[](author-id).\n")
        content.append("---\n")
        
        # Student info table
        semester = self.student_info.get('semester', '4')
        content.append(f"<h2 class='portfolio-header'>Portfolio Technische Informatica (TI) semester {semester} (S{semester})</h2>\n")
        content.append("Onderwerp | Graag invullen | Opmerking")
        content.append("--- | --- | ---")
        content.append(f"*Peilmoment* | `peilmoment {self.student_info.get('milestone', '')}` | ")
        content.append(f"*Naam student* | `{self.student_info.get('name', '')}` | ")
        content.append(f"*Studentnummer* | `{self.student_info.get('student_number', '')}` | ")
        content.append(f"*Semester* | `semester {semester}` | ")
        content.append(f"*Datum* | `{datetime.datetime.now().strftime('%d-%m-%Y')}` | dd-mm-jjjj\n")
        
        # General reflection
        content.append("## Algemeen\n")
        content.append(f"*Waar ik het meest trots op ben:*\n")
        content.append(f'<div class="reflection-box">{self.reflection_data.get("proud_of", "--")}</div>\n')
        content.append(f"*Waar ik de afgelopen periode moeite mee heb gehad en welke actie ik heb ondernomen:*\n")
        content.append(f'<div class="reflection-box">{self.reflection_data.get("struggled_with", "--")}</div>\n')
        content.append(f"*Wat ik nog graag wil leren en welke actie ik wil gaan ondernemen:*\n")
        content.append(f'<div class="reflection-box">{self.reflection_data.get("want_to_learn", "--")}</div>\n')
        content.append("---\n")
        
        # Learning outcomes
        content.append("## Leeruitkomsten\n")
        
        for lo_num in range(1, 10):
            lo = self.learning_outcomes[lo_num]
            content.append(f"### Leeruitkomst {lo_num} {lo['title']}\n")
            content.append(f"*{lo['description']}*\n")
            content.append("")  # Empty line between description and indicators
            content.append("**Indicatoren:**")
            content.append("")  # Empty line after "Indicatoren:"
            content.append('<ul class="indicators-list">')
            for indicator in lo['indicators']:
                content.append(f"<li>{indicator}</li>")
            content.append("</ul>")
            content.append("")  # Empty line before separator
            content.append("---\n")
            
            # Get portfolio items for this learning outcome
            personal_items = [item for item in self.portfolio_items 
                            if lo_num in item.get('learning_outcomes', []) and not item.get('is_group_work', False)]
            group_items = [item for item in self.portfolio_items 
                         if lo_num in item.get('learning_outcomes', []) and item.get('is_group_work', False)]
            
            # Check if there are any items for this learning outcome
            if personal_items or group_items:
                # Personal assignments
                if personal_items:
                    content.append(f"**Leeruitkomst {lo_num} Persoonlijke opdrachten:**\n")
                    content.append("| Portfolio-item     | Beschrijving                                           | Bewijslast               |")
                    content.append("|--------------------|--------------------------------------------------------|--------------------------|")
                    
                    for item in personal_items:
                        content.append(f"| {item.get('title', 'Portfolio-item')} | {item.get('description', 'Beschrijving niet beschikbaar')} | [link naar {item.get('github_link', 'repository')}]({item.get('github_link', 'http://')}) |")
                    
                    content.append("")
                    
                    # Add feedback if available for this specific learning outcome
                    for item in personal_items:
                        # Only show feedback that is specifically for this learning outcome
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
                
                # Group assignments
                if group_items:
                    content.append(f"**Leeruitkomst {lo_num} Groepsopdrachten:**\n")
                    content.append("| Portfolio-item     | Beschrijving                                           | Bewijslast               |")
                    content.append("|--------------------|--------------------------------------------------------|--------------------------|")
                    
                    for item in group_items:
                        content.append(f"| {item.get('title', 'Portfolio-item')} | {item.get('description', 'Beschrijving niet beschikbaar')} | [link naar {item.get('github_link', 'repository')}]({item.get('github_link', 'http://')}) |")
                    
                    content.append("")
                    
                    # Add feedback if available for this specific learning outcome
                    for item in group_items:
                        # Only show feedback that is specifically for this learning outcome
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
                # No portfolio items for this learning outcome
                content.append("<div class='no-portfolio-item'>Student heeft nog geen portfolio item ingeleverd voor deze leeruitkomst.</div>\n")
            
            content.append("---\n")
        
        return "\n".join(content)

    def generate_pdf(self, markdown_filename):
        """Generate PDF from markdown using weasyprint"""
        import weasyprint
        
        # Convert markdown to HTML
        with open(markdown_filename, 'r', encoding='utf-8') as f:
            markdown_content = f.read()
        
        html_content = markdown.markdown(markdown_content, extensions=['tables'])
        
        # Add basic CSS styling
        html_with_css = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="UTF-8">
            <style>
                body {{ font-family: Arial, sans-serif; margin: 40px; line-height: 1.6; word-wrap: break-word; }}
                h1, h2, h3 {{ color: #333; }}
                h2.portfolio-header {{ font-size: 1.3em; }}
                table {{ border-collapse: collapse; width: 100%; margin: 20px 0; table-layout: fixed; }}
                th, td {{ border: 1px solid #ddd; padding: 8px; text-align: left; word-wrap: break-word; overflow-wrap: break-word; hyphens: auto; }}
                th {{ background-color: #f2f2f2; }}
                code {{ background-color: #f4f4f4; padding: 2px 4px; border-radius: 3px; word-wrap: break-word; }}
                pre {{ background-color: #f4f4f4; padding: 10px; border-radius: 5px; overflow-x: auto; word-wrap: break-word; }}
                p {{ word-wrap: break-word; overflow-wrap: break-word; }}
                .no-portfolio-item {{ color: red; font-weight: bold; }}
                h3 + p em {{ font-style: italic; font-size: 0.9em; color: #666; word-wrap: break-word; }}
                p strong:contains("Indicatoren:") {{ font-weight: bold; }}
                .indicators-list {{ font-style: normal; font-size: 1em; color: #333; margin-top: 0.5em; }}
                .indicators-list li {{ margin: 0.2em 0; }}
                .feedback-section {{ margin: 10px 0; }}
                .feedback-item {{ margin-bottom: 15px; padding: 10px; background-color: #f9f9f9; border-left: 3px solid #ddd; word-wrap: break-word; overflow-wrap: break-word; }}
                .feedback-item strong {{ color: #555; }}
                .feedback-item p {{ margin: 5px 0 0 0; line-height: 1.4; word-wrap: break-word; overflow-wrap: break-word; }}
                .reflection-box {{ background-color: #f4f4f4; padding: 10px; margin: 10px 0 20px 0; border-radius: 3px; word-wrap: break-word; overflow-wrap: break-word; line-height: 1.6; }}
            </style>
        </head>
        <body>
        {html_content}
        </body>
        </html>
        """
        
        # Generate PDF
        pdf_filename = markdown_filename.replace('.md', '.pdf')
        weasyprint.HTML(string=html_with_css).write_pdf(pdf_filename)

    def setup_github(self):
        """Setup GitHub credentials"""
        messagebox.showinfo("GitHub Setup", "GitHub integratie komt in een volgende versie beschikbaar.")

    def show_learning_outcomes_info(self):
        """Show detailed information about learning outcomes in a cleaner two-pane layout.

        Left: searchable list of LUs
        Right: structured details (title, description, indicators, examples)
        """
        dialog = tk.Toplevel(self.root)
        dialog.title("Leeruitkomsten Informatie")
        dialog.geometry("900x600")
        dialog.transient(self.root)
        dialog.grab_set()

        # Ensure dialog is on top
        dialog.lift()
        dialog.focus_force()

        main_frame = ttk.Frame(dialog, padding=10)
        main_frame.pack(fill=tk.BOTH, expand=True)

        # Search box
        search_frame = ttk.Frame(main_frame)
        search_frame.pack(fill="x", pady=(0, 8))
        ttk.Label(search_frame, text="Zoek leeruitkomsten:").pack(side="left", padx=(0, 6))
        search_var = tk.StringVar()
        search_entry = ttk.Entry(search_frame, textvariable=search_var, width=50)
        search_entry.pack(side="left", fill="x", expand=True)
        ttk.Button(search_frame, text="Wis", command=lambda: (search_var.set(""), populate_list())).pack(side="left", padx=6)

        content_frame = ttk.Frame(main_frame)
        content_frame.pack(fill=tk.BOTH, expand=True)

        # Left: list of learning outcomes
        left_frame = ttk.LabelFrame(content_frame, text="Leeruitkomsten", padding=8)
        left_frame.pack(side="left", fill=tk.BOTH, expand=False, padx=(0, 8))
        left_frame.configure(width=300)

        lo_listbox = tk.Listbox(left_frame, width=40, activestyle='none')
        lo_scroll = ttk.Scrollbar(left_frame, orient=tk.VERTICAL, command=lo_listbox.yview)
        lo_listbox.configure(yscrollcommand=lo_scroll.set)
        lo_listbox.pack(side="left", fill=tk.BOTH, expand=True)
        lo_scroll.pack(side="right", fill=tk.Y)

        # Right: details pane
        right_frame = ttk.Frame(content_frame, padding=6)
        right_frame.pack(side="left", fill=tk.BOTH, expand=True)

        title_label = ttk.Label(right_frame, text="", font=(None, 13, "bold"), wraplength=520, justify="left")
        title_label.pack(anchor="w", pady=(0, 6))

        desc_label = ttk.Label(right_frame, text="Beschrijving:", font=(None, 10, "bold"))
        desc_label.pack(anchor="w")
        desc_text = tk.Text(right_frame, height=6, wrap=tk.WORD)
        desc_text.configure(state=tk.DISABLED)
        desc_scroll = ttk.Scrollbar(right_frame, orient=tk.VERTICAL, command=desc_text.yview)
        desc_text.configure(yscrollcommand=desc_scroll.set)
        desc_text.pack(fill="x", pady=(0, 8))
        desc_scroll.place(in_=desc_text, relx=1.0, rely=0, relheight=1.0, anchor="ne")

        indicators_label = ttk.Label(right_frame, text="Indicatoren:", font=(None, 10, "bold"))
        indicators_label.pack(anchor="w")
        indicators_list = tk.Listbox(right_frame, height=6)
        indicators_scroll = ttk.Scrollbar(right_frame, orient=tk.VERTICAL, command=indicators_list.yview)
        indicators_list.configure(yscrollcommand=indicators_scroll.set)
        indicators_list.pack(fill="x", pady=(0, 8))
        indicators_scroll.place(in_=indicators_list, relx=1.0, rely=0, relheight=1.0, anchor="ne")

        examples_label = ttk.Label(right_frame, text="Voorbeelden:", font=(None, 10, "bold"))
        examples_label.pack(anchor="w")
        examples_list = tk.Listbox(right_frame, height=6)
        examples_scroll = ttk.Scrollbar(right_frame, orient=tk.VERTICAL, command=examples_list.yview)
        examples_list.configure(yscrollcommand=examples_scroll.set)
        examples_list.pack(fill="both", expand=True)
        examples_scroll.place(in_=examples_list, relx=1.0, rely=0, relheight=1.0, anchor="ne")

        # Close button
        btn_frame = ttk.Frame(dialog, padding=(8, 8))
        btn_frame.pack(fill="x")
        ttk.Button(btn_frame, text="Sluiten", command=dialog.destroy).pack(side="right")

        # Populate and interactivity
        lo_items = []

        def build_lo_items():
            nonlocal lo_items
            lo_items = []
            for lo_num, lo_data in self.learning_outcomes.items():
                label = f"LU{lo_num}: {lo_data['title']}"
                combined = (label + "\n" + lo_data.get('description', '')).lower()
                lo_items.append((lo_num, label, combined))

        def populate_list():
            term = search_var.get().strip().lower()
            lo_listbox.delete(0, tk.END)
            for lo_num, label, combined in lo_items:
                if not term or term in combined:
                    lo_listbox.insert(tk.END, label)

        def show_lo_details(event=None):
            sel = lo_listbox.curselection()
            if not sel:
                return
            idx = sel[0]
            # Find the Nth displayed item by re-scanning with filter
            term = search_var.get().strip().lower()
            visible = [t for t in lo_items if (not term or term in t[2])]
            if idx >= len(visible):
                return
            lo_num = visible[idx][0]
            lo = self.learning_outcomes.get(lo_num, {})

            # Update right pane
            title_label.config(text=f"Leeruitkomst {lo_num}: {lo.get('title', '')}")

            desc_text.config(state=tk.NORMAL)
            desc_text.delete('1.0', tk.END)
            desc_text.insert(tk.END, lo.get('description', ''))
            desc_text.config(state=tk.DISABLED)

            indicators_list.delete(0, tk.END)
            for indicator in lo.get('indicators', []):
                indicators_list.insert(tk.END, f"• {indicator}")

            examples_list.delete(0, tk.END)
            for example in lo.get('examples', []):
                examples_list.insert(tk.END, f"• {example}")

        # Bind events
        lo_listbox.bind('<<ListboxSelect>>', show_lo_details)
        search_entry.bind('<KeyRelease>', lambda e: populate_list())

        # Prepare items and show first one
        build_lo_items()
        populate_list()
        # Select first if available
        if lo_listbox.size() > 0:
            lo_listbox.selection_set(0)
            show_lo_details()

    def show_all_feedback(self):
        """Show all feedback from all portfolio items in a scrollable dialog"""
        dialog = tk.Toplevel(self.root)
        dialog.title("Alle Feedback Overzicht")
        dialog.geometry("900x650")
        dialog.transient(self.root)
        dialog.grab_set()

        # Ensure dialog is on top
        dialog.lift()
        dialog.focus_force()

        # Top frame for search controls
        top_frame = ttk.Frame(dialog, padding=(10, 6))
        top_frame.pack(fill="x")

        ttk.Label(top_frame, text="Zoek:").pack(side="left", padx=(0, 6))
        search_var = tk.StringVar()
        search_entry = ttk.Entry(top_frame, textvariable=search_var, width=50)
        search_entry.pack(side="left", padx=(0, 6))

        ttk.Label(top_frame, text="Filter op:").pack(side="left", padx=(8, 6))
        filter_var = tk.StringVar(value="Alles")
        filter_combo = ttk.Combobox(top_frame, textvariable=filter_var, values=["Alles", "Auteur", "Tekst", "Leeruitkomst", "Item"], state="readonly", width=15)
        filter_combo.pack(side="left")

        ttk.Button(top_frame, text="Clear", command=lambda: (search_var.set(""), populate_list())).pack(side="right")

        # Create canvas/scrollbar to hold a variable amount of feedback
        canvas = tk.Canvas(dialog)
        scrollbar = ttk.Scrollbar(dialog, orient=tk.VERTICAL, command=canvas.yview)
        container_outer = ttk.Frame(canvas)

        container_outer.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )

        canvas.create_window((0, 0), window=container_outer, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        # Helper to clear a frame
        def clear_frame(frame):
            for child in frame.winfo_children():
                child.destroy()

        # Function to open a detail dialog for a specific feedback item
        def open_feedback_detail(item_index, fb_index):
            item = self.portfolio_items[item_index]
            fb = item.get('feedback', [])[fb_index]

            detail = tk.Toplevel(dialog)
            detail.title(f"Feedback - {item.get('title', 'Geen titel')}")
            detail.geometry("700x500")
            detail.transient(dialog)
            detail.grab_set()

            # Header
            header_text = f"Item: {item.get('title', 'Geen titel')}    |    Van: {fb.get('from', 'Onbekend')}    |    Datum: {fb.get('date', '')}"
            ttk.Label(detail, text=header_text, font=(None, 11, "bold"), wraplength=680).pack(fill="x", padx=10, pady=(10, 6))

            # LU tags
            lu_tags = fb.get('learning_outcomes', [])
            if lu_tags:
                ttk.Label(detail, text="Leeruitkomsten: " + ", ".join([f"LU{n}" for n in lu_tags]), foreground="#333").pack(anchor="w", padx=12)

            # Full feedback text
            text_frame = ttk.Frame(detail, padding=10)
            text_frame.pack(fill="both", expand=True)
            fb_text = tk.Text(text_frame, wrap=tk.WORD)
            fb_text.insert("1.0", fb.get('text', ''))
            fb_text.config(state=tk.DISABLED)
            fb_text.pack(fill="both", expand=True, side="left")
            fb_scroll = ttk.Scrollbar(text_frame, orient=tk.VERTICAL, command=fb_text.yview)
            fb_text.configure(yscrollcommand=fb_scroll.set)
            fb_scroll.pack(side="right", fill="y")

            # Buttons: Edit / Delete / Close
            btn_frame = ttk.Frame(detail, padding=10)
            btn_frame.pack(fill="x")

            def edit_this_feedback():
                # Open FeedbackDialog prefilled; portfolio item LOs used as available options
                dialog_fb = FeedbackDialog(detail, "Feedback Bewerken", existing_feedback=fb,
                                           learning_outcomes=self.learning_outcomes,
                                           portfolio_item_learning_outcomes=item.get('learning_outcomes', []))
                updated = dialog_fb.get_feedback()
                if updated:
                    # Update the feedback in the item
                    self.portfolio_items[item_index]['feedback'][fb_index] = updated
                    self.save_data()
                    populate_list()
                    detail.destroy()

            def delete_this_feedback():
                if messagebox.askyesno("Verwijderen", "Weet je zeker dat je deze feedback wilt verwijderen?"):
                    try:
                        del self.portfolio_items[item_index]['feedback'][fb_index]
                        self.save_data()
                    except Exception:
                        pass
                    populate_list()
                    detail.destroy()

            ttk.Button(btn_frame, text="Bewerken", command=edit_this_feedback).pack(side="left", padx=(0, 6))
            ttk.Button(btn_frame, text="Verwijderen", command=delete_this_feedback).pack(side="left", padx=(0, 6))
            ttk.Button(btn_frame, text="Sluiten", command=detail.destroy).pack(side="right")

        # Function to populate the container with filtered feedback
        def populate_list(*_args):
            search_term = search_var.get().strip().lower()
            filter_mode = filter_var.get()

            clear_frame(container_outer)

            any_feedback = False
            for item_index, item in enumerate(self.portfolio_items):
                feedback_list = item.get('feedback', [])
                if not feedback_list:
                    continue

                # For each item, check if any of its feedbacks match the filter
                item_matches = []
                for fb_index, fb in enumerate(feedback_list):
                    match = False
                    if not search_term:
                        match = True
                    else:
                        author = fb.get('from', '').lower()
                        text = fb.get('text', '').lower()
                        los = ", ".join([f"lu{n}" for n in fb.get('learning_outcomes', [])]).lower()
                        title = item.get('title', '').lower()

                        if filter_mode == "Alles":
                            match = search_term in author or search_term in text or search_term in los or search_term in title
                        elif filter_mode == "Auteur":
                            match = search_term in author
                        elif filter_mode == "Tekst":
                            match = search_term in text
                        elif filter_mode == "Leeruitkomst":
                            match = search_term in los
                        elif filter_mode == "Item":
                            match = search_term in title

                    if match:
                        item_matches.append((fb_index, fb))

                if not item_matches:
                    continue

                any_feedback = True

                # Item header
                header_frame = ttk.Frame(container_outer)
                header_frame.pack(fill="x", padx=10, pady=(8, 2), anchor="n")
                ttk.Label(header_frame, text=f"{item.get('title', 'Geen titel')} - {item.get('date_added', '')}", font=(None, 10, "bold")).pack(side="left")

                # Feedback entries for this item
                for fb_index, fb in item_matches:
                    fb_frame = tk.Frame(container_outer, bd=1, relief="solid", bg="#ffffff")
                    fb_frame.pack(fill="x", padx=18, pady=(6, 6))

                    fb_header = tk.Label(fb_frame, text=f"Van: {fb.get('from', 'Onbekend')}    Datum: {fb.get('date', '')}    " + (", ".join([f"LU{n}" for n in fb.get('learning_outcomes', [])]) if fb.get('learning_outcomes') else ""),
                                         font=(None, 10, "bold"), anchor="w", bg="#ffffff")
                    fb_header.pack(fill="x", padx=8, pady=(6, 0))

                    preview = fb.get('text', '').strip().replace("\n", " ")
                    if len(preview) > 250:
                        preview = preview[:250].rsplit(' ', 1)[0] + '...'

                    fb_preview = tk.Label(fb_frame, text=preview, wraplength=820, justify="left", bg="#ffffff", cursor="hand2")
                    fb_preview.pack(fill="x", padx=8, pady=(4, 8))

                    # Bind click to open full detail (capture indices in defaults)
                    fb_preview.bind("<Button-1>", lambda e, ii=item_index, fi=fb_index: open_feedback_detail(ii, fi))

            if not any_feedback:
                ttk.Label(container_outer, text="Er is nog geen feedback toegevoegd.", foreground="gray").pack(padx=20, pady=20)

        # Bind search entry to live updates
        search_entry.bind("<KeyRelease>", populate_list)
        filter_combo.bind("<<ComboboxSelected>>", populate_list)

        # Initial populate
        populate_list()

        # Close button
        btn_frame = ttk.Frame(dialog)
        btn_frame.pack(fill="x", pady=6)
        ttk.Button(btn_frame, text="Sluiten", command=dialog.destroy).pack(side="right", padx=8)

    def quick_add_feedback(self):
        """Quick guided flow to add feedback to an existing portfolio item"""
        if not self.portfolio_items:
            messagebox.showinfo("Geen items", "Er zijn nog geen portfolio items om feedback aan toe te voegen.")
            return

        dialog = tk.Toplevel(self.root)
        dialog.title("Feedback toevoegen - Snel")
        dialog.geometry("500x220")
        dialog.transient(self.root)
        dialog.grab_set()

        frame = ttk.Frame(dialog, padding=12)
        frame.pack(fill=tk.BOTH, expand=True)

        ttk.Label(frame, text="Selecteer portfolio item:", font=(None, 10, "bold")).pack(anchor="w")
        item_titles = [f"{i+1}. {itm.get('title', 'Untitled')}" for i, itm in enumerate(self.portfolio_items)]
        selected_var = tk.StringVar()
        combo = ttk.Combobox(frame, values=item_titles, textvariable=selected_var, state="readonly")
        combo.pack(fill="x", pady=(6, 10))
        combo.current(0)

        ttk.Label(frame, text="(Je kunt later het feedback-item bewerken in het portfolio item zelf)", foreground="gray").pack(anchor="w", pady=(0, 6))

        def open_feedback_editor():
            sel = combo.current()
            if sel < 0:
                messagebox.showwarning("Selectie", "Selecteer eerst een portfolio item.")
                return

            item = self.portfolio_items[sel]
            # Only allow selecting LOs that belong to the item
            available_los = item.get('learning_outcomes', [])

            fb_dialog = FeedbackDialog(dialog, "Feedback Toevoegen", learning_outcomes=self.learning_outcomes,
                                       portfolio_item_learning_outcomes=available_los)
            feedback = fb_dialog.get_feedback()

            if feedback:
                if 'feedback' not in item:
                    item['feedback'] = []
                item['feedback'].append(feedback)
                self.save_data()
                self.update_display()
                messagebox.showinfo("Opgeslagen", "Feedback succesvol toegevoegd.")
                dialog.destroy()

        btn_frame = ttk.Frame(frame)
        btn_frame.pack(fill="x", pady=(12, 0))
        ttk.Button(btn_frame, text="Toevoegen", command=open_feedback_editor).pack(side="right", padx=(6, 0))
        ttk.Button(btn_frame, text="Annuleren", command=dialog.destroy).pack(side="right")

    def show_feedback_info(self):
        """Open the project's GitHub issues page for feedback/suggestions."""
        url = "https://github.com/RickMageddon/PortfolioDocumentManager/issues"
        try:
            webbrowser.open(url)
            # Inform the user that the browser was opened
            messagebox.showinfo("Feedback", f"De issues-pagina wordt geopend in je browser:\n{url}")
        except Exception as e:
            # Fallback: show contact email if the browser couldn't be opened
            messagebox.showinfo("Feedback", 
                                "Kan de webbrowser niet automatisch openen.\n\n"
                                "Je kunt je feedback ook per e-mail sturen naar:\n"
                                "rick.vandervoort@student.hu.nl\n\n"
                                f"Fout: {str(e)}")

    def show_about(self):
        """Show about dialog"""
        dialog = tk.Toplevel(self.root)
        dialog.title("Over PeilDocument Manager")
        dialog.geometry("450x350")
        dialog.transient(self.root)
        dialog.grab_set()
        dialog.resizable(False, False)
        
        # Ensure dialog is on top
        dialog.lift()
        dialog.focus_force()
        
        frame = ttk.Frame(dialog, padding="20")
        frame.pack(fill=tk.BOTH, expand=True)
        
        # Title
        ttk.Label(frame, text="PeilDocument Manager", 
                 font=("Arial", 14, "bold")).pack(pady=(0, 10))
        
        ttk.Label(frame, text="Versie 2.0", 
                 font=("Arial", 10)).pack(pady=(0, 15))
        
        # Description
        ttk.Label(frame, text="Een tool voor het beheren van portfolio items\nvoor het verantwoordingsdocument.", 
                 font=("Arial", 10), justify="center").pack(pady=(0, 15))
        
        # Developer info
        ttk.Label(frame, text="Ontwikkeld door:", 
                 font=("Arial", 10, "bold")).pack(pady=(0, 5))
        ttk.Label(frame, text="Rick van der Voort", 
                 font=("Arial", 10)).pack()
        
        # Website link
        website_label = ttk.Label(frame, text="rickmageddon.com", 
                                 font=("Arial", 10, "underline"), 
                                 foreground="blue", cursor="hand2")
        website_label.pack(pady=(5, 15))
        website_label.bind("<Button-1>", lambda e: webbrowser.open("https://rickmageddon.com"))
        
        # Target audience
        ttk.Label(frame, text="Voor HU studenten", 
                 font=("Arial", 9), foreground="gray").pack(pady=(0, 20))
        
        # Close button
        ttk.Button(frame, text="Sluiten", command=dialog.destroy).pack()

    def export_data(self):
        """Export data to file"""
        filename = filedialog.asksaveasfilename(
            defaultextension=".json",
            filetypes=[("JSON files", "*.json"), ("All files", "*.*")]
        )
        if filename:
            try:
                data = {
                    "student_info": self.student_info,
                    "portfolio_items": self.portfolio_items,
                    "reflection_data": self.reflection_data
                }
                with open(filename, 'w', encoding='utf-8') as f:
                    json.dump(data, f, indent=2, ensure_ascii=False)
                messagebox.showinfo("Succes", f"Data geëxporteerd naar {filename}")
            except Exception as e:
                messagebox.showerror("Fout", f"Exporteren mislukt: {str(e)}")

    def import_data(self):
        """Import data from file"""
        filename = filedialog.askopenfilename(
            filetypes=[("JSON files", "*.json"), ("All files", "*.*")]
        )
        if filename:
            try:
                with open(filename, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                
                self.student_info = data.get("student_info", {})
                self.portfolio_items = data.get("portfolio_items", [])
                self.reflection_data = data.get("reflection_data", {})
                
                self.save_data()
                self.update_display()
                messagebox.showinfo("Succes", f"Data geïmporteerd van {filename}")
            except Exception as e:
                messagebox.showerror("Fout", f"Importeren mislukt: {str(e)}")

    def load_data(self):
        """Load data from JSON file"""
        if os.path.exists(self.data_file):
            try:
                with open(self.data_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                
                self.student_info = data.get("student_info", {})
                self.portfolio_items = data.get("portfolio_items", [])
                self.reflection_data = data.get("reflection_data", {})
            except Exception as e:
                messagebox.showerror("Fout", f"Laden van data mislukt: {str(e)}")

    def save_data(self):
        """Save data to JSON file"""
        try:
            data = {
                "student_info": self.student_info,
                "portfolio_items": self.portfolio_items,
                "reflection_data": self.reflection_data
            }
            with open(self.data_file, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
        except Exception as e:
            messagebox.showerror("Fout", f"Opslaan van data mislukt: {str(e)}")

    def run(self):
        """Start the application"""
        self.root.mainloop()

    def count_items_without_feedback(self):
        """Count portfolio items that have no feedback"""
        count = 0
        for item in self.portfolio_items:
            # Check if item has any feedback
            if not item.get('feedback') or len(item.get('feedback', [])) == 0:
                count += 1
        return count


class FeedbackDialog:
    def __init__(self, parent, title="Feedback Toevoegen", existing_feedback=None, learning_outcomes=None, portfolio_item_learning_outcomes=None):
        self.result = None
        self.learning_outcomes = learning_outcomes or {}
        self.portfolio_item_learning_outcomes = portfolio_item_learning_outcomes or []
        
        self.dialog = tk.Toplevel(parent)
        self.dialog.title(title)
        self.dialog.geometry("600x800")
        self.dialog.transient(parent)
        self.dialog.grab_set()
        self.dialog.resizable(True, True)  # Allow resizing
        
        # Center the dialog
        self.dialog.geometry("+%d+%d" % (parent.winfo_rootx() + 30, parent.winfo_rooty() + 30))
        
        # Ensure dialog is on top
        self.dialog.lift()
        self.dialog.focus_force()
        
        self.create_widgets(existing_feedback)
        
    def create_widgets(self, existing_feedback=None):
        # Create main canvas and scrollbar for scrollable content
        canvas = tk.Canvas(self.dialog)
        scrollbar = ttk.Scrollbar(self.dialog, orient="vertical", command=canvas.yview)
        scrollable_frame = ttk.Frame(canvas)
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        # Add mouse wheel scrolling
        def _on_mousewheel(event):
            canvas.yview_scroll(int(-1*(event.delta/120)), "units")

        # Bind the mousewheel only while the cursor is over the canvas.
        # Using bind_all leaves a global binding that can reference
        # destroyed widgets, which raises TclError when dialogs close.
        def _bind_mousewheel(event):
            canvas.bind_all("<MouseWheel>", _on_mousewheel)

        def _unbind_mousewheel(event):
            try:
                canvas.unbind_all("<MouseWheel>")
            except Exception:
                pass

        canvas.bind("<Enter>", _bind_mousewheel)
        canvas.bind("<Leave>", _unbind_mousewheel)
        
        # Pack canvas and scrollbar
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        main_frame = ttk.Frame(scrollable_frame, padding="20")
        main_frame.pack(fill="both", expand=True)
        
        # Van (who gave feedback)
        ttk.Label(main_frame, text="Feedback van:", font=("Arial", 11, "bold")).pack(anchor="w", pady=(0, 5))
        self.from_var = tk.StringVar()
        from_entry = ttk.Entry(main_frame, textvariable=self.from_var, font=("Arial", 10), width=50)
        from_entry.pack(fill="x", pady=(0, 20))
        
        # Learning outcomes selection for feedback
        ttk.Label(main_frame, text="Voor welke leeruitkomsten is deze feedback:", font=("Arial", 11, "bold")).pack(anchor="w", pady=(0, 5))
        ttk.Label(main_frame, text="(alleen leeruitkomsten van dit portfolio item worden getoond)", font=("Arial", 9, "italic")).pack(anchor="w", pady=(0, 10))
        
        # Create frame for learning outcomes checkboxes with better spacing
        lo_frame = ttk.LabelFrame(main_frame, text="Leeruitkomsten", padding="15")
        lo_frame.pack(fill="x", pady=(0, 20))
        
        self.feedback_lo_vars = {}
        
        # Only show learning outcomes that are part of this portfolio item
        for lo_num in self.portfolio_item_learning_outcomes:
            if lo_num in self.learning_outcomes:
                lo_data = self.learning_outcomes[lo_num]
                var = tk.BooleanVar()
                
                # Load existing selection if editing
                if existing_feedback and lo_num in existing_feedback.get('learning_outcomes', []):
                    var.set(True)
                
                self.feedback_lo_vars[lo_num] = var
                
                # Create checkbox with better spacing
                checkbox = ttk.Checkbutton(lo_frame, 
                                         text=f"LU{lo_num}: {lo_data['title']}", 
                                         variable=var)
                checkbox.pack(anchor="w", pady=5)
        
        # Feedback text
        ttk.Label(main_frame, text="Feedback tekst:", font=("Arial", 11, "bold")).pack(anchor="w", pady=(0, 5))
        text_frame = ttk.Frame(main_frame)
        text_frame.pack(fill="both", expand=True, pady=(0, 20))
        
        self.feedback_text = tk.Text(text_frame, height=12, font=("Arial", 10), wrap=tk.WORD)
        text_scrollbar = ttk.Scrollbar(text_frame, orient=tk.VERTICAL, command=self.feedback_text.yview)
        self.feedback_text.configure(yscrollcommand=text_scrollbar.set)
        
        self.feedback_text.pack(side=tk.LEFT, fill="both", expand=True)
        text_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Load existing data if editing
        if existing_feedback:
            self.from_var.set(existing_feedback.get('from', ''))
            self.feedback_text.insert('1.0', existing_feedback.get('text', ''))
        
        # Buttons frame with better spacing
        button_frame = ttk.Frame(main_frame)
        button_frame.pack(fill="x", pady=(20, 0))
        
        ttk.Button(button_frame, text="Opslaan", command=self.save_feedback).pack(side="right", padx=(10, 0))
        ttk.Button(button_frame, text="Annuleren", command=self.dialog.destroy).pack(side="right")
        
        # Focus on the first field
        from_entry.focus()
        
    def save_feedback(self):
        from_text = self.from_var.get().strip()
        feedback_text = self.feedback_text.get("1.0", tk.END).strip()
        
        # Get selected learning outcomes
        selected_los = [lo_num for lo_num, var in self.feedback_lo_vars.items() if var.get()]
        
        if not from_text or not feedback_text:
            messagebox.showwarning("Invoer", "Vul alle velden in.")
            return
            
        if not selected_los:
            messagebox.showwarning("Invoer", "Selecteer minimaal één leeruitkomst voor deze feedback.")
            return
        
        self.result = {
            'from': from_text,
            'text': feedback_text,
            'learning_outcomes': selected_los,
            'date': datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
        }
        
        self.dialog.destroy()
        
    def get_feedback(self):
        self.dialog.wait_window()
        return self.result

class PortfolioItemDialog:
    def __init__(self, parent, learning_outcomes, existing_item=None):
        self.result = None
        self.learning_outcomes = learning_outcomes
        
        self.dialog = tk.Toplevel(parent)
        self.dialog.title("Portfolio Item" + (" Bewerken" if existing_item else " Toevoegen"))
        self.dialog.geometry("650x900")
        self.dialog.transient(parent)
        self.dialog.grab_set()
        
        # Center the dialog
        self.dialog.geometry("+%d+%d" % (parent.winfo_rootx() + 50, parent.winfo_rooty() + 30))
        
        # Ensure dialog is on top
        self.dialog.lift()
        self.dialog.focus_force()
        
        self.setup_dialog(existing_item)

    def setup_dialog(self, existing_item):
        # Create main canvas and scrollbar for scrollable content
        canvas = tk.Canvas(self.dialog)
        scrollbar = ttk.Scrollbar(self.dialog, orient="vertical", command=canvas.yview)
        scrollable_frame = ttk.Frame(canvas)
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        # Add mouse wheel scrolling
        def _on_mousewheel(event):
            canvas.yview_scroll(int(-1*(event.delta/120)), "units")

        # Bind mousewheel only while the cursor is over the canvas to avoid
        # the callback referencing a destroyed canvas when the dialog closes.
        def _bind_mousewheel(event):
            canvas.bind_all("<MouseWheel>", _on_mousewheel)

        def _unbind_mousewheel(event):
            try:
                canvas.unbind_all("<MouseWheel>")
            except Exception:
                pass

        canvas.bind("<Enter>", _bind_mousewheel)
        canvas.bind("<Leave>", _unbind_mousewheel)
        
        # Pack canvas and scrollbar
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # Main content frame
        main_frame = ttk.Frame(scrollable_frame, padding="20")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Title field
        ttk.Label(main_frame, text="Titel:", font=("Arial", 10, "bold")).pack(anchor="w", pady=(0, 5))
        self.title_entry = ttk.Entry(main_frame, width=60)
        self.title_entry.pack(fill="x", pady=(0, 15))
        if existing_item:
            self.title_entry.insert(0, existing_item.get('title', ''))
        
        # Learning outcomes selection
        ttk.Label(main_frame, text="Selecteer leeruitkomsten:", font=("Arial", 10, "bold")).pack(anchor="w", pady=(0, 5))
        
        # Create frame for learning outcomes in 2 rows
        lo_frame = ttk.Frame(main_frame)
        lo_frame.pack(fill="x", pady=(0, 15))
        
        # Create two columns for checkboxes
        left_frame = ttk.Frame(lo_frame)
        left_frame.pack(side="left", fill="both", expand=True, padx=(0, 10))
        
        right_frame = ttk.Frame(lo_frame)
        right_frame.pack(side="left", fill="both", expand=True)
        
        self.lo_vars = {}
        learning_outcomes_list = list(self.learning_outcomes.items())
        
        # Split learning outcomes into two columns
        mid_point = len(learning_outcomes_list) // 2 + len(learning_outcomes_list) % 2
        
        # Left column (first half)
        for i, (lo_num, lo_data) in enumerate(learning_outcomes_list[:mid_point]):
            var = tk.BooleanVar()
            if existing_item and lo_num in existing_item.get('learning_outcomes', []):
                var.set(True)
            
            self.lo_vars[lo_num] = var
            
            # Create checkbox with tooltip
            checkbox = ttk.Checkbutton(left_frame, 
                                     text=f"LU{lo_num}: {lo_data['title']}", 
                                     variable=var)
            checkbox.pack(anchor="w", pady=2)
            
            # Add tooltip functionality
            self.create_tooltip(checkbox, lo_data['description'] + "\n\nVoorbeelden: " + ", ".join(lo_data['examples'][:3]))
        
        # Right column (second half)
        for i, (lo_num, lo_data) in enumerate(learning_outcomes_list[mid_point:]):
            var = tk.BooleanVar()
            if existing_item and lo_num in existing_item.get('learning_outcomes', []):
                var.set(True)
            
            self.lo_vars[lo_num] = var
            
            # Create checkbox with tooltip
            checkbox = ttk.Checkbutton(right_frame, 
                                     text=f"LU{lo_num}: {lo_data['title']}", 
                                     variable=var)
            checkbox.pack(anchor="w", pady=2)
            
            # Add tooltip functionality
            self.create_tooltip(checkbox, lo_data['description'] + "\n\nVoorbeelden: " + ", ".join(lo_data['examples'][:3]))
        
        # Assignment type selection
        ttk.Label(main_frame, text="Type opdracht:", font=("Arial", 10, "bold")).pack(anchor="w", pady=(10, 5))
        
        # Create frame for radio buttons
        self.type_frame = ttk.Frame(main_frame)
        self.type_frame.pack(anchor="w", pady=(0, 10))
        
        self.assignment_type_var = tk.StringVar()
        if existing_item:
            self.assignment_type_var.set("group" if existing_item.get('is_group_work', False) else "personal")
        else:
            self.assignment_type_var.set("personal")  # Default to personal
        
        ttk.Radiobutton(self.type_frame, text="Persoonlijk", variable=self.assignment_type_var, 
                       value="personal", command=self.toggle_group_options).pack(side="left", padx=(0, 20))
        ttk.Radiobutton(self.type_frame, text="Groepswerk", variable=self.assignment_type_var, 
                       value="group", command=self.toggle_group_options).pack(side="left")
        
        # Group members frame (directly under radio buttons) - create but don't pack yet
        self.group_frame = ttk.LabelFrame(main_frame, text="Groepsleden", padding="10")
        ttk.Label(self.group_frame, text="Voer elke groepslid op een nieuwe regel in:", font=("Arial", 9)).pack(anchor="w", pady=(0, 5))
        self.group_members_text = tk.Text(self.group_frame, height=3, width=50)
        self.group_members_text.pack(fill="x")
        if existing_item and existing_item.get('group_members'):
            self.group_members_text.insert(tk.END, "\n".join(existing_item.get('group_members', [])))
        
        # GitHub link
        ttk.Label(main_frame, text="GitHub link:", font=("Arial", 10, "bold")).pack(anchor="w", pady=(10, 5))
        self.github_entry = ttk.Entry(main_frame, width=60)
        self.github_entry.pack(fill="x", pady=(0, 10))
        if existing_item:
            self.github_entry.insert(0, existing_item.get('github_link', ''))
        
        # Description
        ttk.Label(main_frame, text="Korte uitleg van wat je hebt gedaan:", font=("Arial", 10, "bold")).pack(anchor="w", pady=(10, 5))
        self.description_text = tk.Text(main_frame, height=4, width=60)
        self.description_text.pack(fill="x", pady=(0, 10))
        if existing_item:
            self.description_text.insert(tk.END, existing_item.get('description', ''))
        
        # Feedback section
        ttk.Label(main_frame, text="Feedback:", font=("Arial", 10, "bold")).pack(anchor="w", pady=(10, 5))
        
        feedback_frame = ttk.Frame(main_frame)
        feedback_frame.pack(fill="x", pady=(0, 10))
        
        self.feedback_list = []
        self.feedback_listbox = tk.Listbox(feedback_frame, height=3)
        self.feedback_listbox.pack(fill="x", pady=(0, 5))
        
        # Load existing feedback
        if existing_item and existing_item.get('feedback'):
            for feedback in existing_item.get('feedback', []):
                self.feedback_list.append(feedback)
                # Show learning outcomes in the display if available
                lo_text = ""
                if feedback.get('learning_outcomes'):
                    lo_text = f" ({', '.join([f'LU{lo}' for lo in feedback.get('learning_outcomes', [])])})"
                self.feedback_listbox.insert(tk.END, f"{feedback.get('from', 'Onbekend')}{lo_text}: {feedback.get('text', '')[:40]}... ({feedback.get('date', 'Geen datum')})")
        
        feedback_buttons = ttk.Frame(feedback_frame)
        feedback_buttons.pack(fill="x")
        ttk.Button(feedback_buttons, text="Feedback Toevoegen", command=self.add_feedback).pack(side="left", padx=(0, 10))
        ttk.Button(feedback_buttons, text="Feedback Bewerken", command=self.edit_feedback).pack(side="left", padx=(0, 10))
        ttk.Button(feedback_buttons, text="Feedback Verwijderen", command=self.remove_feedback).pack(side="left")
        
        # Buttons
        button_frame = ttk.Frame(main_frame)
        button_frame.pack(fill="x", pady=(20, 0))
        
        ttk.Button(button_frame, text="Opslaan", command=self.save_item).pack(side="right", padx=(10, 0))
        ttk.Button(button_frame, text="Annuleren", command=self.dialog.destroy).pack(side="right")
        
        # Initial toggle
        self.toggle_group_options()

    def create_tooltip(self, widget, text):
        """Create a tooltip for a widget"""
        def on_enter(event):
            tooltip = tk.Toplevel()
            tooltip.wm_overrideredirect(True)
            tooltip.wm_geometry(f"+{event.x_root+10}+{event.y_root+10}")
            
            label = tk.Label(tooltip, text=text, background="lightyellow", 
                           relief="solid", borderwidth=1, wraplength=300, justify="left")
            label.pack()
            
            widget.tooltip = tooltip
        
        def on_leave(event):
            if hasattr(widget, 'tooltip'):
                widget.tooltip.destroy()
                del widget.tooltip
        
        widget.bind("<Enter>", on_enter)
        widget.bind("<Leave>", on_leave)

    def toggle_group_options(self):
        """Show/hide group options based on assignment type selection"""
        if self.assignment_type_var.get() == "group":
            # Pack after the type_frame
            self.group_frame.pack(fill="x", pady=(10, 15), after=self.type_frame)
        else:
            self.group_frame.pack_forget()

    def add_feedback(self):
        """Voeg feedback toe via dialoog"""
        # Get currently selected learning outcomes
        selected_los = [lo_num for lo_num, var in self.lo_vars.items() if var.get()]
        
        if not selected_los:
            messagebox.showwarning("Geen leeruitkomsten", "Selecteer eerst leeruitkomsten voor dit portfolio item voordat je feedback toevoegt.")
            return
        
        dialog = FeedbackDialog(self.dialog, "Feedback Toevoegen", 
                              learning_outcomes=self.learning_outcomes,
                              portfolio_item_learning_outcomes=selected_los)
        feedback = dialog.get_feedback()
        
        if feedback:
            self.feedback_list.append(feedback)
            # Show learning outcomes in the display
            lo_text = ", ".join([f"LU{lo}" for lo in feedback.get('learning_outcomes', [])])
            self.feedback_listbox.insert(tk.END, f"{feedback.get('from', 'Onbekend')} ({lo_text}): {feedback.get('text', '')[:40]}... ({feedback.get('date', 'Geen datum')})")

    def edit_feedback(self):
        """Bewerk geselecteerde feedback"""
        selection = self.feedback_listbox.curselection()
        if not selection:
            messagebox.showwarning("Selectie", "Selecteer eerst een feedback item.")
            return
        
        # Get currently selected learning outcomes
        selected_los = [lo_num for lo_num, var in self.lo_vars.items() if var.get()]
        
        if not selected_los:
            messagebox.showwarning("Geen leeruitkomsten", "Selecteer eerst leeruitkomsten voor dit portfolio item voordat je feedback bewerkt.")
            return
        
        index = selection[0]
        existing_feedback = self.feedback_list[index]
        
        # Open feedback dialoog met bestaande feedback
        dialog = FeedbackDialog(self.dialog, "Feedback Bewerken", existing_feedback,
                              learning_outcomes=self.learning_outcomes,
                              portfolio_item_learning_outcomes=selected_los)
        feedback = dialog.get_feedback()
        
        if feedback:
            self.feedback_list[index] = feedback
            # Update display
            self.feedback_listbox.delete(index)
            lo_text = ", ".join([f"LU{lo}" for lo in feedback.get('learning_outcomes', [])])
            self.feedback_listbox.insert(index, f"{feedback.get('from', 'Onbekend')} ({lo_text}): {feedback.get('text', '')[:40]}... ({feedback.get('date', 'Geen datum')})")
            self.feedback_listbox.selection_set(index)

    def remove_feedback(self):
        """Remove selected feedback"""
        selection = self.feedback_listbox.curselection()
        if not selection:
            messagebox.showwarning("Selectie", "Selecteer eerst een feedback item.")
            return
        
        index = selection[0]
        del self.feedback_list[index]
        self.feedback_listbox.delete(index)

    def save_item(self):
        """Save the portfolio item"""
        # Get selected learning outcomes
        selected_los = [lo_num for lo_num, var in self.lo_vars.items() if var.get()]
        
        if not selected_los:
            messagebox.showerror("Fout", "Selecteer minimaal één leeruitkomst!")
            return
        
        title = self.title_entry.get().strip()
        github_link = self.github_entry.get().strip()
        description = self.description_text.get("1.0", tk.END).strip()
        
        if not title or not github_link or not description:
            messagebox.showerror("Fout", "Vul alle verplichte velden in!")
            return
        
        # Build result
        self.result = {
            "title": title,
            "learning_outcomes": selected_los,
            "is_group_work": self.assignment_type_var.get() == "group",
            "github_link": github_link,
            "description": description,
            "feedback": self.feedback_list.copy()
        }
        
        if self.assignment_type_var.get() == "group":
            group_members_text = self.group_members_text.get("1.0", tk.END).strip()
            self.result["group_members"] = [member.strip() for member in group_members_text.split("\n") if member.strip()]
        
        self.dialog.destroy()


class SubmissionDialog:
    def __init__(self, parent, existing_reflection=None):
        self.result = None
        
        self.dialog = tk.Toplevel(parent)
        self.dialog.title("Document Inleveren")
        self.dialog.geometry("650x600")
        self.dialog.transient(parent)
        self.dialog.grab_set()
        self.dialog.resizable(False, False)
        
        # Center the dialog
        self.dialog.geometry("+%d+%d" % (parent.winfo_rootx() + 100, parent.winfo_rooty() + 50))
        
        # Ensure dialog is on top
        self.dialog.lift()
        self.dialog.focus_force()
        
        self.setup_dialog(existing_reflection)

    def setup_dialog(self, existing_reflection):
        main_frame = ttk.Frame(self.dialog, padding="25")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        ttk.Label(main_frame, text="Reflectie Vragen", font=("Arial", 14, "bold")).pack(anchor="w", pady=(0, 20))
        
        # Question 1
        ttk.Label(main_frame, text="Waar ik het meest trots op ben:", font=("Arial", 10, "bold")).pack(anchor="w", pady=(0, 5))
        self.proud_text = tk.Text(main_frame, height=4, width=65, wrap=tk.WORD)
        self.proud_text.pack(fill="x", pady=(0, 15))
        if existing_reflection:
            self.proud_text.insert(tk.END, existing_reflection.get('proud_of', ''))
        
        # Question 2
        ttk.Label(main_frame, text="Waar ik de afgelopen periode moeite mee heb gehad en welke actie ik heb ondernomen:", font=("Arial", 10, "bold")).pack(anchor="w", pady=(0, 5))
        self.struggled_text = tk.Text(main_frame, height=4, width=65, wrap=tk.WORD)
        self.struggled_text.pack(fill="x", pady=(0, 15))
        if existing_reflection:
            self.struggled_text.insert(tk.END, existing_reflection.get('struggled_with', ''))
        
        # Question 3
        ttk.Label(main_frame, text="Wat ik nog graag wil leren en welke actie ik wil gaan ondernemen:", font=("Arial", 10, "bold")).pack(anchor="w", pady=(0, 5))
        self.learn_text = tk.Text(main_frame, height=4, width=65, wrap=tk.WORD)
        self.learn_text.pack(fill="x", pady=(0, 20))
        if existing_reflection:
            self.learn_text.insert(tk.END, existing_reflection.get('want_to_learn', ''))
        
        # Completeness check
        self.complete_var = tk.BooleanVar()
        if existing_reflection:
            self.complete_var.set(existing_reflection.get('is_complete', False))
        
        self.complete_checkbox = ttk.Checkbutton(main_frame, 
                                               text="Ik bevestig dat mijn portfolio compleet is en klaar voor inlevering", 
                                               variable=self.complete_var,
                                               command=self.toggle_generate_button)
        self.complete_checkbox.pack(anchor="w", pady=(0, 15))
        
        # Markdown generation option
        self.generate_md_var = tk.BooleanVar(value=False)  # Default unchecked
        self.md_checkbox = ttk.Checkbutton(main_frame, 
                                         text="Ook markdown (.md) bestand genereren", 
                                         variable=self.generate_md_var)
        self.md_checkbox.pack(anchor="w", pady=(0, 25))
        
        # Buttons
        button_frame = ttk.Frame(main_frame)
        button_frame.pack(fill="x", pady=(10, 0))
        
        self.generate_button = ttk.Button(button_frame, text="Document Genereren", command=self.generate_document)
        self.generate_button.pack(side="right", padx=(10, 0))
        ttk.Button(button_frame, text="Annuleren", command=self.dialog.destroy).pack(side="right")
        
        # Initial state for generate button
        self.toggle_generate_button()

    def toggle_generate_button(self):
        """Enable/disable the generate button based on checkbox state"""
        if self.complete_var.get():
            self.generate_button.config(state="normal")
        else:
            self.generate_button.config(state="disabled")

    def generate_document(self):
        """Generate the document"""
        proud_of = self.proud_text.get("1.0", tk.END).strip()
        struggled_with = self.struggled_text.get("1.0", tk.END).strip()
        want_to_learn = self.learn_text.get("1.0", tk.END).strip()
        
        if not proud_of or not struggled_with or not want_to_learn:
            messagebox.showerror("Fout", "Vul alle reflectie vragen in!")
            return
        
        # No need to check checkbox here since button is disabled when unchecked
        self.result = {
            "proud_of": proud_of,
            "struggled_with": struggled_with,
            "want_to_learn": want_to_learn,
            "is_complete": True,
            "generate_markdown": self.generate_md_var.get(),
            "submission_date": datetime.datetime.now().isoformat()
        }
        
        self.dialog.destroy()


if __name__ == "__main__":
    app = PortfolioManager()
    app.root.mainloop()
