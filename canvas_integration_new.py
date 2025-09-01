"""
Enhanced Canvas LMS Integration Module
Provides comprehensive Canvas API functionality for the Portfolio Document Manager
with OAuth support and course management
"""
import requests
import json
from datetime import datetime, timedelta
from typing import List, Dict, Optional
import os
import webbrowser
import urllib.parse
import threading
from http.server import HTTPServer, BaseHTTPRequestHandler
import time


class OAuthCallbackHandler(BaseHTTPRequestHandler):
    """Handles OAuth callback from Canvas"""
    
    def do_GET(self):
        """Handle GET request from Canvas OAuth"""
        if self.path.startswith('/oauth/callback'):
            # Parse the authorization code from the URL
            query_components = urllib.parse.parse_qs(urllib.parse.urlparse(self.path).query)
            if 'code' in query_components:
                self.server.auth_code = query_components['code'][0]
                
                # Send success page
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                
                success_page = '''
                <html>
                <head><title>Canvas Login Successful</title></head>
                <body style="font-family: Arial, sans-serif; text-align: center; margin-top: 50px;">
                    <h1 style="color: green;">✓ Login Successful!</h1>
                    <p>You have successfully logged in to Canvas.</p>
                    <p>You can now close this window and return to the Portfolio Manager.</p>
                    <script>
                        setTimeout(function() {
                            window.close();
                        }, 3000);
                    </script>
                </body>
                </html>
                '''
                self.wfile.write(success_page.encode())
            else:
                # Error occurred
                self.send_response(400)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                
                error_page = '''
                <html>
                <head><title>Canvas Login Error</title></head>
                <body style="font-family: Arial, sans-serif; text-align: center; margin-top: 50px;">
                    <h1 style="color: red;">✗ Login Failed</h1>
                    <p>There was an error during the login process.</p>
                    <p>Please try again.</p>
                </body>
                </html>
                '''
                self.wfile.write(error_page.encode())
        else:
            self.send_response(404)
            self.end_headers()
    
    def log_message(self, format, *args):
        """Suppress log messages"""
        pass


class CanvasIntegration:
    def __init__(self, canvas_url: str = "https://canvas.hu.nl", access_token: str = None):
        """
        Initialize Canvas integration
        
        Args:
            canvas_url: Your Canvas instance URL (defaults to HU Canvas)
            access_token: Canvas API access token (optional for OAuth flow)
        """
        self.canvas_url = canvas_url.rstrip('/')
        self.access_token = access_token
        self.session = requests.Session()
        self.selected_course_id = None
        self.courses = []
        self.assignments = []
        self.user_id = None
        
        if self.access_token:
            self.session.headers.update({
                'Authorization': f'Bearer {self.access_token}',
                'Content-Type': 'application/json'
            })
    
    def login_with_token_instructions(self):
        """
        Provide instructions for manual token generation for HU Canvas
        """
        instructions = {
            'title': 'Canvas HU Login Instructions',
            'steps': [
                '1. Go to: https://canvas.hu.nl/profile/settings',
                '2. Scroll down to "Approved Integrations"',
                '3. Click "+ New Access Token"',
                '4. Enter purpose: "Portfolio Manager"',
                '5. Click "Generate Token"',
                '6. Copy the generated token',
                '7. Paste it in the Portfolio Manager'
            ],
            'url': 'https://canvas.hu.nl/profile/settings'
        }
        return instructions
    
    def set_access_token(self, token: str):
        """Set the access token and update session headers"""
        self.access_token = token
        self.session.headers.update({
            'Authorization': f'Bearer {self.access_token}',
            'Content-Type': 'application/json'
        })
    
    def test_connection(self) -> bool:
        """
        Test Canvas API connection
        
        Returns:
            True if connection successful, False otherwise
        """
        if not self.access_token:
            return False
        
        try:
            url = f"{self.canvas_url}/api/v1/users/self"
            response = self.session.get(url)
            return response.status_code == 200
        except Exception as e:
            print(f"Connection test failed: {e}")
            return False
    
    def get_user_info(self) -> Dict:
        """
        Get current user information
        
        Returns:
            User information dictionary
        """
        if not self.access_token:
            return {}
        
        try:
            url = f"{self.canvas_url}/api/v1/users/self"
            response = self.session.get(url)
            if response.status_code == 200:
                user_info = response.json()
                self.user_id = user_info['id']
                return user_info
            else:
                print(f"Failed to get user info: {response.status_code}")
                return {}
        except Exception as e:
            print(f"Error getting user info: {e}")
            return {}
    
    def get_courses(self) -> List[Dict]:
        """
        Get list of user's active courses
        
        Returns:
            List of course dictionaries
        """
        if not self.access_token:
            return []
        
        try:
            url = f"{self.canvas_url}/api/v1/courses"
            params = {
                'enrollment_state': 'active',
                'enrollment_type': 'student',
                'per_page': 100,
                'include[]': ['term']
            }
            
            response = self.session.get(url, params=params)
            if response.status_code == 200:
                courses = response.json()
                # Filter out concluded courses and sort by name
                active_courses = [c for c in courses if c.get('workflow_state') == 'available']
                active_courses.sort(key=lambda x: x.get('name', ''))
                self.courses = active_courses
                return active_courses
            else:
                print(f"Failed to fetch courses: {response.status_code}")
                return []
        except Exception as e:
            print(f"Error fetching courses: {e}")
            return []
    
    def select_course(self, course_id: int):
        """
        Select a course for assignment tracking
        
        Args:
            course_id: The Canvas course ID
        """
        self.selected_course_id = course_id
    
    def get_selected_course_name(self) -> str:
        """Get the name of the currently selected course"""
        if not self.selected_course_id or not self.courses:
            return "No course selected"
        
        for course in self.courses:
            if course['id'] == self.selected_course_id:
                return course['name']
        
        return "Unknown course"
    
    def get_upcoming_assignments(self, course_id: int = None, days_ahead: int = 30) -> List[Dict]:
        """
        Get upcoming assignments for a course
        
        Args:
            course_id: Course ID (uses selected course if None)
            days_ahead: Number of days to look ahead for assignments
            
        Returns:
            List of upcoming assignment dictionaries with enhanced info
        """
        if not self.access_token:
            return []
        
        course_id = course_id or self.selected_course_id
        if not course_id:
            return []
        
        try:
            url = f"{self.canvas_url}/api/v1/courses/{course_id}/assignments"
            params = {
                'per_page': 100,
                'order_by': 'due_at',
                'include[]': ['submission']
            }
            
            response = self.session.get(url, params=params)
            if response.status_code == 200:
                assignments = response.json()
                
                # Filter for upcoming assignments
                now = datetime.now()
                future_cutoff = now + timedelta(days=days_ahead)
                upcoming_assignments = []
                
                for assignment in assignments:
                    if assignment.get('due_at'):
                        try:
                            # Parse Canvas date format
                            due_date_str = assignment['due_at'].replace('Z', '+00:00')
                            due_date = datetime.fromisoformat(due_date_str).replace(tzinfo=None)
                            
                            # Check if assignment is upcoming and not submitted
                            if now <= due_date <= future_cutoff:
                                # Check submission status
                                submission = assignment.get('submission')
                                is_submitted = submission and submission.get('submitted_at') is not None
                                
                                # Enhanced assignment info
                                enhanced_assignment = {
                                    'id': assignment['id'],
                                    'name': assignment['name'],
                                    'due_at': assignment['due_at'],
                                    'due_date_formatted': due_date.strftime('%Y-%m-%d %H:%M'),
                                    'due_date_obj': due_date,
                                    'description': assignment.get('description', ''),
                                    'points_possible': assignment.get('points_possible'),
                                    'html_url': assignment.get('html_url'),
                                    'is_submitted': is_submitted,
                                    'submission_id': submission.get('id') if submission else None,
                                    'days_until_due': (due_date - now).days,
                                    'course_id': course_id
                                }
                                
                                upcoming_assignments.append(enhanced_assignment)
                        except (ValueError, TypeError) as e:
                            print(f"Error parsing date for assignment {assignment.get('name', 'Unknown')}: {e}")
                            continue
                
                # Sort by due date
                upcoming_assignments.sort(key=lambda x: x['due_date_obj'])
                self.assignments = upcoming_assignments
                return upcoming_assignments
            else:
                print(f"Failed to fetch assignments: {response.status_code}")
                return []
        except Exception as e:
            print(f"Error fetching assignments: {e}")
            return []
    
    def get_assignment_submission_status(self, course_id: int, assignment_id: int) -> Dict:
        """
        Get detailed submission status for an assignment
        
        Args:
            course_id: Course ID
            assignment_id: Assignment ID
            
        Returns:
            Dictionary with submission status and feedback info
        """
        if not self.access_token or not self.user_id:
            return {'error': 'Not authenticated'}
        
        try:
            url = f"{self.canvas_url}/api/v1/courses/{course_id}/assignments/{assignment_id}/submissions/{self.user_id}"
            params = {
                'include[]': ['submission_comments', 'rubric_assessment', 'submission_history']
            }
            
            response = self.session.get(url, params=params)
            if response.status_code == 200:
                submission = response.json()
                
                # Analyze submission status
                is_submitted = submission.get('submitted_at') is not None
                has_grade = submission.get('grade') is not None
                has_comments = bool(submission.get('submission_comments', []))
                has_rubric_feedback = bool(submission.get('rubric_assessment'))
                
                status = {
                    'is_submitted': is_submitted,
                    'submitted_at': submission.get('submitted_at'),
                    'grade': submission.get('grade'),
                    'score': submission.get('score'),
                    'has_feedback': has_grade or has_comments or has_rubric_feedback,
                    'has_grade': has_grade,
                    'has_comments': has_comments,
                    'has_rubric_feedback': has_rubric_feedback,
                    'workflow_state': submission.get('workflow_state'),
                    'submission_comments': submission.get('submission_comments', []),
                    'needs_feedback_request': is_submitted and not (has_grade or has_comments or has_rubric_feedback)
                }
                
                return status
            else:
                return {'error': f'Failed to get submission status: {response.status_code}'}
        except Exception as e:
            return {'error': f'Error getting submission status: {e}'}
    
    def mark_assignment_completed(self, assignment_id: int):
        """
        Mark an assignment as completed (remove from todo list)
        This is a local operation - the actual submission happens in Canvas
        
        Args:
            assignment_id: Assignment ID to mark as completed
        """
        self.assignments = [a for a in self.assignments if a['id'] != assignment_id]
    
    def get_pending_feedback(self, course_id: int = None) -> List[Dict]:
        """
        Get assignments that are submitted but pending feedback
        
        Args:
            course_id: Course ID (uses selected course if None)
            
        Returns:
            List of assignments awaiting feedback
        """
        if not self.access_token:
            return []
        
        course_id = course_id or self.selected_course_id
        if not course_id:
            return []
        
        try:
            # Get all assignments for the course
            url = f"{self.canvas_url}/api/v1/courses/{course_id}/assignments"
            params = {
                'per_page': 100,
                'include[]': ['submission']
            }
            
            response = self.session.get(url, params=params)
            if response.status_code == 200:
                assignments = response.json()
                pending_feedback = []
                
                for assignment in assignments:
                    submission = assignment.get('submission')
                    if submission and submission.get('submitted_at'):
                        # Check if has feedback
                        has_grade = submission.get('grade') is not None
                        has_comments = bool(submission.get('submission_comments', []))
                        
                        if not (has_grade or has_comments):
                            # This assignment is submitted but has no feedback
                            pending_feedback.append({
                                'id': assignment['id'],
                                'name': assignment['name'],
                                'submitted_at': submission['submitted_at'],
                                'course_id': course_id
                            })
                
                return pending_feedback
            else:
                print(f"Failed to fetch assignments for feedback check: {response.status_code}")
                return []
        except Exception as e:
            print(f"Error checking pending feedback: {e}")
            return []


class CanvasConfig:
    """Configuration management for Canvas integration"""
    
    CONFIG_FILE = "canvas_config.json"
    
    @classmethod
    def load(cls) -> Dict:
        """Load Canvas configuration from file"""
        try:
            if os.path.exists(cls.CONFIG_FILE):
                with open(cls.CONFIG_FILE, 'r') as f:
                    return json.load(f)
        except Exception as e:
            print(f"Error loading Canvas config: {e}")
        
        return {
            'canvas_url': 'https://canvas.hu.nl',
            'access_token': '',
            'selected_course_id': None,
            'user_id': None
        }
    
    @classmethod
    def save(cls, config: Dict):
        """Save Canvas configuration to file"""
        try:
            with open(cls.CONFIG_FILE, 'w') as f:
                json.dump(config, f, indent=2)
        except Exception as e:
            print(f"Error saving Canvas config: {e}")
    
    @classmethod
    def clear(cls):
        """Clear Canvas configuration"""
        try:
            if os.path.exists(cls.CONFIG_FILE):
                os.remove(cls.CONFIG_FILE)
        except Exception as e:
            print(f"Error clearing Canvas config: {e}")
