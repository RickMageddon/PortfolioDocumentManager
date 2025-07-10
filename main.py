#!/usr/bin/env python3
"""
Portfolio Document Program
Een programma voor het beheren van portfolio items voor het TI S4 verantwoordingsdocument.
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
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Portfolio Document Manager - TI")
        self.root.geometry("1000x700")
        
        # Data storage
        self.data_file = "portfolio_data.json"
        self.student_info = {}
        self.portfolio_items = []
        self.reflection_data = {}
        
        # Learning outcomes definitions with examples
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
        
        # Load existing data
        self.load_data()
        
        # Initialize GUI
        self.setup_gui()
        
        # Check if first time setup is needed
        if not self.student_info:
            self.first_time_setup()

    def setup_gui(self):
        """Setup the main GUI interface"""
        # Create menu bar
        menubar = tk.Menu(self.root)
        self.root.config(menu=menubar)
        
        # Options menu
        options_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Opties", menu=options_menu)
        options_menu.add_command(label="Student gegevens wijzigen", command=self.edit_student_info)
        options_menu.add_command(label="GitHub inloggegevens", command=self.setup_github)
        options_menu.add_separator()
        options_menu.add_command(label="Data exporteren", command=self.export_data)
        options_menu.add_command(label="Data importeren", command=self.import_data)
        
        # Help menu
        help_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Help", menu=help_menu)
        help_menu.add_command(label="Feedback", command=self.show_feedback_info)
        help_menu.add_command(label="Over", command=self.show_about)
        
        # Leeruitkomsten info as separate menu item
        menubar.add_command(label="Leeruitkomsten Info", command=self.show_learning_outcomes_info)
        
        # Main frame
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
        
        ttk.Button(buttons_frame, text="Nieuw Portfolio Item Toevoegen", 
                  command=self.add_portfolio_item, width=25).grid(row=0, column=0, padx=(0, 10))
        ttk.Button(buttons_frame, text="Portfolio Items Beheren", 
                  command=self.manage_portfolio_items, width=25).grid(row=0, column=1, padx=(0, 10))
        ttk.Button(buttons_frame, text="Document Inleveren", 
                  command=self.submit_document, width=25).grid(row=0, column=2)
        
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
                self.root.title(f"Portfolio Document Manager - TI S{semester}")
        
        # Update attention message for feedback
        items_without_feedback = self.count_items_without_feedback()
        if items_without_feedback > 0:
            if items_without_feedback == 1:
                attention_text = f"Je hebt nog {items_without_feedback} portfolio item zonder feedback!"
            else:
                attention_text = f"Je hebt nog {items_without_feedback} portfolio items zonder feedback!"
            self.attention_label.config(text=attention_text, foreground="red")
            self.attention_frame.grid()  # Show the frame
        else:
            if self.portfolio_items:  # Only show if there are items
                self.attention_label.config(text="✅ Alle portfolio items hebben feedback!", foreground="green")
                self.attention_frame.grid()  # Show the frame
            else:
                self.attention_frame.grid_remove()  # Hide if no items
        
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
        
        ttk.Label(frame, text="Welkom bij de Portfolio Document Manager!", 
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
        """Open portfolio items management window"""
        if not self.portfolio_items:
            messagebox.showinfo("Info", "Er zijn nog geen portfolio items toegevoegd.")
            return
        
        dialog = tk.Toplevel(self.root)
        dialog.title("Portfolio Items Beheren")
        dialog.geometry("800x600")
        dialog.transient(self.root)
        dialog.grab_set()
        
        # Ensure dialog is on top
        dialog.lift()
        dialog.focus_force()
        
        frame = ttk.Frame(dialog, padding="10")
        frame.pack(fill=tk.BOTH, expand=True)
        
        # List of items
        listbox = tk.Listbox(frame, height=15)
        for i, item in enumerate(self.portfolio_items):
            listbox.insert(tk.END, f"{i+1}. {item.get('title', 'Untitled')}")
        listbox.pack(fill=tk.BOTH, expand=True, pady=(0, 10))
        
        # Buttons
        button_frame = ttk.Frame(frame)
        button_frame.pack(fill="x")
        
        def edit_item():
            selection = listbox.curselection()
            if not selection:
                messagebox.showwarning("Selectie", "Selecteer eerst een item.")
                return
            
            index = selection[0]
            item = self.portfolio_items[index]
            
            edit_dialog = PortfolioItemDialog(dialog, self.learning_outcomes, item)
            dialog.wait_window(edit_dialog.dialog)
            
            if edit_dialog.result:
                self.portfolio_items[index] = edit_dialog.result
                self.save_data()
                self.update_display()
                # Update listbox
                listbox.delete(index)
                listbox.insert(index, f"{index+1}. {edit_dialog.result.get('title', 'Untitled')}")
        
        def delete_item():
            selection = listbox.curselection()
            if not selection:
                messagebox.showwarning("Selectie", "Selecteer eerst een item.")
                return
            
            if messagebox.askyesno("Bevestiging", "Weet je zeker dat je dit item wilt verwijderen?"):
                index = selection[0]
                del self.portfolio_items[index]
                self.save_data()
                self.update_display()
                listbox.delete(index)
        
        ttk.Button(button_frame, text="Bewerken", command=edit_item).pack(side="left", padx=(0, 10))
        ttk.Button(button_frame, text="Verwijderen", command=delete_item).pack(side="left", padx=(0, 10))
        ttk.Button(button_frame, text="Sluiten", command=dialog.destroy).pack(side="right")

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
        content.append("**v1.0.0 [](version-id)** Gegenereerd door Portfolio Document Manager[](author-id).\n")
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
        content.append(f"    {self.reflection_data.get('proud_of', '--')}\n")
        content.append(f"*Waar ik de afgelopen periode moeite mee heb gehad en welke actie ik heb ondernomen:*\n")
        content.append(f"    {self.reflection_data.get('struggled_with', '--')}\n")
        content.append(f"*Wat ik nog graag wil leren en welke actie ik wil gaan ondernemen:*\n")
        content.append(f"    {self.reflection_data.get('want_to_learn', '--')}\n")
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
                p strong:contains("Indicatoren:") {{ font-weight: bold; }}
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
        
        # Generate PDF
        pdf_filename = markdown_filename.replace('.md', '.pdf')
        weasyprint.HTML(string=html_with_css).write_pdf(pdf_filename)

    def setup_github(self):
        """Setup GitHub credentials"""
        messagebox.showinfo("GitHub Setup", "GitHub integratie komt in een volgende versie beschikbaar.")

    def show_learning_outcomes_info(self):
        """Show detailed information about learning outcomes"""
        dialog = tk.Toplevel(self.root)
        dialog.title("Leeruitkomsten Informatie")
        dialog.geometry("800x600")
        dialog.transient(self.root)
        dialog.grab_set()
        
        # Ensure dialog is on top
        dialog.lift()
        dialog.focus_force()
        
        frame = ttk.Frame(dialog, padding="10")
        frame.pack(fill=tk.BOTH, expand=True)
        
        # Create notebook for tabs
        notebook = ttk.Notebook(frame)
        notebook.pack(fill=tk.BOTH, expand=True)
        
        for lo_num, lo_data in self.learning_outcomes.items():
            # Create tab for each learning outcome
            tab_frame = ttk.Frame(notebook)
            notebook.add(tab_frame, text=f"LU{lo_num}: {lo_data['title']}")
            
            # Scrollable text widget
            text_frame = ttk.Frame(tab_frame)
            text_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
            
            text_widget = tk.Text(text_frame, wrap=tk.WORD, height=20)
            scrollbar = ttk.Scrollbar(text_frame, orient=tk.VERTICAL, command=text_widget.yview)
            text_widget.configure(yscrollcommand=scrollbar.set)
            
            # Add content
            content = f"Leeruitkomst {lo_num}: {lo_data['title']}\n\n"
            content += f"Beschrijving:\n{lo_data['description']}\n\n"
            content += "Indicatoren:\n"
            for indicator in lo_data['indicators']:
                content += f"• {indicator}\n"
            content += "\nVoorbeelden van opdrachten:\n"
            for example in lo_data['examples']:
                content += f"• {example}\n"
            
            text_widget.insert(tk.END, content)
            text_widget.config(state=tk.DISABLED)
            
            text_widget.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
            scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

    def show_feedback_info(self):
        """Show feedback information dialog"""
        messagebox.showinfo("Feedback", 
                          "Heb je feedback, suggesties of vragen over deze applicatie?\n\n"
                          "Stuur een e-mail naar:\n"
                          "rick.vandervoort@student.hu.nl\n\n"
                          "Bedankt voor je input!")

    def show_about(self):
        """Show about dialog"""
        dialog = tk.Toplevel(self.root)
        dialog.title("Over Portfolio Document Manager")
        dialog.geometry("450x300")
        dialog.transient(self.root)
        dialog.grab_set()
        dialog.resizable(False, False)
        
        # Ensure dialog is on top
        dialog.lift()
        dialog.focus_force()
        
        frame = ttk.Frame(dialog, padding="20")
        frame.pack(fill=tk.BOTH, expand=True)
        
        # Title
        ttk.Label(frame, text="Portfolio Document Manager", 
                 font=("Arial", 14, "bold")).pack(pady=(0, 10))
        
        ttk.Label(frame, text="Versie 1.0.4", 
                 font=("Arial", 10)).pack(pady=(0, 15))
        
        # Description
        ttk.Label(frame, text="Een tool voor het beheren van portfolio items\nvoor het TI verantwoordingsdocument.", 
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
        ttk.Label(frame, text="Voor HU Technische Informatica studenten", 
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
        canvas.bind_all("<MouseWheel>", _on_mousewheel)
        
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
        canvas.bind_all("<MouseWheel>", _on_mousewheel)
        
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
    app.run()
