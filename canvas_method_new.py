    def show_canvas_integration_view(self, e=None):
        """Show enhanced Canvas LMS integration view with course selection and assignment tracking"""
        print("DEBUG: Canvas integration view method called")
        self.current_view = "canvas_integration"
        
        # Container for dynamic content updates
        self.canvas_content_container = ft.Container()
        
        # Main content structure
        content = ft.Column([
            ft.Row([self.show_back_button()], alignment=ft.MainAxisAlignment.START),
            ft.Text(self.get_text("canvas_integration"), size=24, weight=ft.FontWeight.BOLD),
            self.canvas_content_container
        ], spacing=10, scroll=ft.ScrollMode.AUTO)
        
        self.main_content.content = content
        self.page.update()
        
        # Load content based on configuration status
        self._load_canvas_view_content()
    
    def _load_canvas_view_content(self):
        """Load the appropriate Canvas view content based on configuration status"""
        if not CANVAS_AVAILABLE:
            self._show_canvas_unavailable()
        elif not self.canvas_config.get('access_token'):
            self._show_canvas_login_setup()
        else:
            self._show_canvas_dashboard()
    
    def _show_canvas_unavailable(self):
        """Show Canvas unavailable message"""
        content = ft.Card(
            content=ft.Container(
                content=ft.Column([
                    ft.Icon(ft.Icons.ERROR, size=64, color=ft.Colors.RED),
                    ft.Text("Canvas Integration Unavailable", size=18, weight=ft.FontWeight.BOLD),
                    ft.Text("The requests library is required for Canvas integration.", size=14),
                    ft.Text("Please install it using: pip install requests", size=12, color=ft.Colors.GREY_600)
                ], spacing=10, horizontal_alignment=ft.CrossAxisAlignment.CENTER),
                padding=40
            )
        )
        
        self.canvas_content_container.content = content
        self.page.update()
    
    def _show_canvas_login_setup(self):
        """Show Canvas login setup interface"""
        # Canvas URL field (pre-filled with HU Canvas)
        canvas_url_field = ft.TextField(
            label=self.get_text("canvas_url_label"),
            value=self.canvas_config.get('canvas_url', 'https://canvas.hu.nl'),
            hint_text=self.get_text("canvas_url_hint"),
            width=400,
            disabled=True  # HU Canvas URL is fixed
        )
        
        # Access token field
        canvas_token_field = ft.TextField(
            label=self.get_text("canvas_token_label"),
            value=self.canvas_config.get('access_token', ''),
            hint_text=self.get_text("canvas_token_hint"),
            password=True,
            width=400
        )
        
        def save_canvas_settings(e):
            if canvas_token_field.value.strip():
                self.canvas_config = {
                    'canvas_url': canvas_url_field.value.strip(),
                    'access_token': canvas_token_field.value.strip(),
                    'selected_course_id': None
                }
                CanvasConfig.save(self.canvas_config)
                self.setup_canvas_integration()
                
                # Test connection and proceed
                if self.canvas_integration and self.canvas_integration.test_connection():
                    self.show_snackbar(self.get_text("canvas_settings_saved"))
                    self._load_canvas_view_content()  # Reload view
                else:
                    self.show_error_dialog(self.get_text("canvas_settings"), self.get_text("canvas_connection_failed"))
            else:
                self.show_error_dialog(self.get_text("canvas_settings"), "Please enter your Canvas access token")
        
        def open_canvas_settings():
            webbrowser.open('https://canvas.hu.nl/profile/settings')
        
        content = ft.Column([
            # Login instructions card
            ft.Card(
                content=ft.Container(
                    content=ft.Column([
                        ft.Text(self.get_text("canvas_login_instructions"), size=18, weight=ft.FontWeight.BOLD),
                        ft.Divider(),
                        ft.Text(self.get_text("canvas_how_to_token"), size=14, weight=ft.FontWeight.BOLD),
                        ft.Text(self.get_text("canvas_token_step1"), size=12),
                        ft.Text(self.get_text("canvas_token_step2"), size=12),
                        ft.Text(self.get_text("canvas_token_step3"), size=12),
                        ft.Text(self.get_text("canvas_token_step4"), size=12),
                        ft.ElevatedButton(
                            text="Open Canvas Settings",
                            icon=ft.Icons.OPEN_IN_NEW,
                            on_click=lambda e: open_canvas_settings(),
                            style=ft.ButtonStyle(bgcolor=ft.Colors.BLUE_600, color=ft.Colors.WHITE)
                        )
                    ], spacing=10),
                    padding=20
                ),
                margin=ft.margin.only(bottom=20)
            ),
            
            # Settings form card
            ft.Card(
                content=ft.Container(
                    content=ft.Column([
                        ft.Text(self.get_text("canvas_settings"), size=18, weight=ft.FontWeight.BOLD),
                        canvas_url_field,
                        canvas_token_field,
                        ft.ElevatedButton(
                            text=self.get_text("canvas_save_settings"),
                            icon=ft.Icons.SAVE,
                            on_click=save_canvas_settings,
                            style=ft.ButtonStyle(bgcolor=ft.Colors.GREEN_600, color=ft.Colors.WHITE)
                        )
                    ], spacing=15),
                    padding=20
                )
            )
        ], spacing=10)
        
        self.canvas_content_container.content = content
        self.page.update()
    
    def _show_canvas_dashboard(self):
        """Show the main Canvas dashboard with course selection and assignments"""
        if not self.canvas_integration:
            self.setup_canvas_integration()
        
        if not self.canvas_integration:
            self._show_canvas_login_setup()
            return
        
        # Get user info and courses
        user_info = self.canvas_integration.get_user_info()
        courses = self.canvas_integration.get_courses()
        
        # Course selection dropdown
        course_dropdown = ft.Dropdown(
            label=self.get_text("canvas_select_course"),
            width=400,
            value=str(self.canvas_config.get('selected_course_id', '')) if self.canvas_config.get('selected_course_id') else None
        )
        
        if courses:
            course_dropdown.options = [
                ft.dropdown.Option(key=str(course['id']), text=course['name'])
                for course in courses
            ]
        else:
            course_dropdown.options = [ft.dropdown.Option(key="", text=self.get_text("canvas_no_courses"))]
        
        def on_course_selected(e):
            if e.control.value and e.control.value != "":
                course_id = int(e.control.value)
                self.canvas_integration.select_course(course_id)
                self.canvas_config['selected_course_id'] = course_id
                CanvasConfig.save(self.canvas_config)
                self.show_snackbar(self.get_text("canvas_course_selection_saved"))
                # Refresh the assignments view
                self._update_assignments_view()
        
        course_dropdown.on_change = on_course_selected
        
        # Assignments container
        self.assignments_container = ft.Container()
        
        # User info and controls
        user_name = user_info.get('name', 'Unknown User') if user_info else 'Unknown User'
        selected_course_name = self.canvas_integration.get_selected_course_name() if hasattr(self.canvas_integration, 'get_selected_course_name') else "No course selected"
        
        content = ft.Column([
            # User info card
            ft.Card(
                content=ft.Container(
                    content=ft.Column([
                        ft.Text(f"👤 {user_name}", size=16, weight=ft.FontWeight.BOLD),
                        ft.Text(f"{self.get_text('canvas_selected_course')} {selected_course_name}", size=14),
                        ft.Divider(),
                        course_dropdown,
                        ft.Row([
                            ft.ElevatedButton(
                                text=self.get_text("canvas_refresh_assignments"),
                                icon=ft.Icons.REFRESH,
                                on_click=lambda e: self._update_assignments_view(),
                                style=ft.ButtonStyle(bgcolor=ft.Colors.BLUE_600, color=ft.Colors.WHITE)
                            ),
                            ft.ElevatedButton(
                                text="Settings",
                                icon=ft.Icons.SETTINGS,
                                on_click=lambda e: self._show_canvas_login_setup(),
                                style=ft.ButtonStyle(bgcolor=ft.Colors.GREY_600, color=ft.Colors.WHITE)
                            )
                        ], spacing=10)
                    ], spacing=15),
                    padding=20
                )
            ),
            
            # Assignments section
            self.assignments_container
        ], spacing=10)
        
        self.canvas_content_container.content = content
        self.page.update()
        
        # Load assignments if course is selected
        if self.canvas_config.get('selected_course_id'):
            self._update_assignments_view()
    
    def _update_assignments_view(self):
        """Update the assignments view with current data"""
        if not self.canvas_integration or not self.canvas_config.get('selected_course_id'):
            self.assignments_container.content = ft.Card(
                content=ft.Container(
                    content=ft.Text(
                        self.get_text("canvas_no_assignments_selected"),
                        size=14,
                        text_align=ft.TextAlign.CENTER
                    ),
                    padding=20
                )
            )
            self.page.update()
            return
        
        # Get upcoming assignments
        assignments = self.canvas_integration.get_upcoming_assignments()
        
        if not assignments:
            self.assignments_container.content = ft.Card(
                content=ft.Container(
                    content=ft.Column([
                        ft.Icon(ft.Icons.ASSIGNMENT_TURNED_IN, size=48, color=ft.Colors.GREEN),
                        ft.Text(self.get_text("canvas_no_upcoming"), size=16, text_align=ft.TextAlign.CENTER)
                    ], horizontal_alignment=ft.CrossAxisAlignment.CENTER),
                    padding=30
                )
            )
            self.page.update()
            return
        
        # Create assignment cards
        assignment_cards = []
        
        for assignment in assignments:
            due_date = assignment['due_date_formatted']
            days_until_due = assignment['days_until_due']
            
            # Determine urgency color and text
            if days_until_due < 0:
                urgency_color = ft.Colors.RED
                urgency_text = self.get_text("canvas_assignment_overdue")
            elif days_until_due == 0:
                urgency_color = ft.Colors.ORANGE
                urgency_text = self.get_text("canvas_assignment_due_today")
            elif days_until_due <= 3:
                urgency_color = ft.Colors.ORANGE_300
                urgency_text = self.get_text("canvas_assignment_due_in").format(days_until_due)
            else:
                urgency_color = ft.Colors.GREEN
                urgency_text = self.get_text("canvas_assignment_due_in").format(days_until_due)
            
            # Submission status
            submission_status = self.get_text("canvas_assignment_submitted") if assignment['is_submitted'] else self.get_text("canvas_assignment_not_submitted")
            status_color = ft.Colors.GREEN if assignment['is_submitted'] else ft.Colors.GREY_600
            
            def create_assignment_actions(assignment_data):
                buttons = []
                
                # View assignment button
                buttons.append(
                    ft.ElevatedButton(
                        text=self.get_text("canvas_view_assignment"),
                        icon=ft.Icons.OPEN_IN_NEW,
                        on_click=lambda e, url=assignment_data['html_url']: webbrowser.open(url) if url else None,
                        style=ft.ButtonStyle(bgcolor=ft.Colors.BLUE_600, color=ft.Colors.WHITE)
                    )
                )
                
                # Mark as completed button (if submitted)
                if assignment_data['is_submitted']:
                    buttons.append(
                        ft.ElevatedButton(
                            text=self.get_text("canvas_mark_completed"),
                            icon=ft.Icons.CHECK_CIRCLE,
                            on_click=lambda e, aid=assignment_data['id']: self._mark_assignment_completed(aid),
                            style=ft.ButtonStyle(bgcolor=ft.Colors.GREEN_600, color=ft.Colors.WHITE)
                        )
                    )
                
                return ft.Row(buttons, spacing=10)
            
            assignment_card = ft.Card(
                content=ft.Container(
                    content=ft.Column([
                        ft.Row([
                            ft.Text(assignment['name'], size=16, weight=ft.FontWeight.BOLD, expand=True),
                            ft.Container(
                                content=ft.Text(urgency_text, size=12, color=ft.Colors.WHITE),
                                bgcolor=urgency_color,
                                padding=ft.padding.symmetric(horizontal=8, vertical=4),
                                border_radius=10
                            )
                        ]),
                        ft.Text(f"{self.get_text('canvas_due_date')} {due_date}", size=12, color=ft.Colors.GREY_600),
                        ft.Text(f"{self.get_text('canvas_points')} {assignment['points_possible'] or 'N/A'}", size=12, color=ft.Colors.GREY_600),
                        ft.Text(submission_status, size=12, color=status_color, weight=ft.FontWeight.BOLD),
                        create_assignment_actions(assignment)
                    ], spacing=8),
                    padding=15
                ),
                margin=ft.margin.only(bottom=10)
            )
            
            assignment_cards.append(assignment_card)
        
        self.assignments_container.content = ft.Card(
            content=ft.Container(
                content=ft.Column([
                    ft.Text(
                        f"{self.get_text('canvas_assignments_dashboard')} ({len(assignments)})",
                        size=18,
                        weight=ft.FontWeight.BOLD
                    ),
                    ft.Divider(),
                    ft.Column(assignment_cards, scroll=ft.ScrollMode.AUTO)
                ], spacing=10),
                padding=20
            )
        )
        
        self.page.update()
    
    def _mark_assignment_completed(self, assignment_id):
        """Mark an assignment as completed and remove from view"""
        if self.canvas_integration:
            self.canvas_integration.mark_assignment_completed(assignment_id)
            self.show_snackbar("Assignment marked as completed!")
            self._update_assignments_view()  # Refresh the view
    
    def _add_assignments_to_dashboard(self):
        """Add Canvas assignments to the main dashboard"""
        if not self.canvas_integration or not self.canvas_config.get('selected_course_id'):
            return None
        
        assignments = self.canvas_integration.get_upcoming_assignments()
        
        if not assignments:
            return None
        
        # Create a compact assignments widget for the dashboard
        assignment_items = []
        for assignment in assignments[:3]:  # Show max 3 on dashboard
            days_until_due = assignment['days_until_due']
            
            if days_until_due <= 1:
                urgency_icon = ft.Icons.WARNING
                urgency_color = ft.Colors.RED
            elif days_until_due <= 3:
                urgency_icon = ft.Icons.SCHEDULE
                urgency_color = ft.Colors.ORANGE
            else:
                urgency_icon = ft.Icons.ASSIGNMENT
                urgency_color = ft.Colors.BLUE
            
            assignment_items.append(
                ft.ListTile(
                    leading=ft.Icon(urgency_icon, color=urgency_color),
                    title=ft.Text(assignment['name'], size=12),
                    subtitle=ft.Text(f"Due: {assignment['due_date_formatted']}", size=10),
                    on_click=lambda e, url=assignment['html_url']: webbrowser.open(url) if url else None
                )
            )
        
        return ft.Card(
            content=ft.Container(
                content=ft.Column([
                    ft.Text("📚 Upcoming Canvas Assignments", size=14, weight=ft.FontWeight.BOLD),
                    ft.Column(assignment_items),
                    ft.TextButton(
                        text="View All Assignments",
                        on_click=lambda e: self.show_canvas_integration_view()
                    )
                ], spacing=5),
                padding=15
            ),
            margin=ft.margin.only(bottom=10)
        )
