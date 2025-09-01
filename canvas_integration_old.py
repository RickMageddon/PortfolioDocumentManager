"""
Canvas LMS Integration Module
Provides Canvas API functionality for the Portfolio Document Manager
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
    def __init__(self, canvas_url: str, access_token: str):
        """
        Initialize Canvas integration
        
        Args:
            canvas_url: Your Canvas instance URL (e.g., "https://canvas.university.edu")
            access_token: Canvas API access token
        """
        self.canvas_url = canvas_url.rstrip('/')
        self.access_token = access_token
        self.headers = {
            'Authorization': f'Bearer {access_token}',
            'Content-Type': 'application/json'
        }
        self.user_id = None
        
    def test_connection(self) -> bool:
        """Test if the Canvas connection is working"""
        try:
            response = requests.get(
                f"{self.canvas_url}/api/v1/users/self",
                headers=self.headers,
                timeout=10
            )
            response.raise_for_status()
            user_data = response.json()
            self.user_id = user_data.get('id')
            return True
        except Exception as e:
            print(f"Canvas connection test failed: {e}")
            return False
    
    def get_user_profile(self) -> Optional[Dict]:
        """Get current user profile"""
        try:
            response = requests.get(
                f"{self.canvas_url}/api/v1/users/self/profile",
                headers=self.headers,
                timeout=10
            )
            response.raise_for_status()
            return response.json()
        except Exception as e:
            print(f"Error getting user profile: {e}")
            return None
    
    def get_courses(self) -> List[Dict]:
        """Get all active courses for the current user"""
        try:
            response = requests.get(
                f"{self.canvas_url}/api/v1/courses",
                headers=self.headers,
                params={
                    'enrollment_state': 'active',
                    'state[]': 'available',
                    'include[]': ['term']
                },
                timeout=10
            )
            response.raise_for_status()
            return response.json()
        except Exception as e:
            print(f"Error getting courses: {e}")
            return []
    
    def get_assignments(self, course_id: int, include_future: bool = True) -> List[Dict]:
        """Get assignments for a specific course"""
        try:
            params = {
                'include[]': ['submission', 'rubric_assessment'],
                'per_page': 100
            }
            
            if not include_future:
                params['bucket'] = 'past'
            
            response = requests.get(
                f"{self.canvas_url}/api/v1/courses/{course_id}/assignments",
                headers=self.headers,
                params=params,
                timeout=10
            )
            response.raise_for_status()
            return response.json()
        except Exception as e:
            print(f"Error getting assignments for course {course_id}: {e}")
            return []
    
    def get_submission(self, course_id: int, assignment_id: int, user_id: int = None) -> Optional[Dict]:
        """Get submission details for a specific assignment"""
        try:
            if user_id is None:
                user_id = self.user_id or 'self'
            
            response = requests.get(
                f"{self.canvas_url}/api/v1/courses/{course_id}/assignments/{assignment_id}/submissions/{user_id}",
                headers=self.headers,
                params={
                    'include[]': ['submission_comments', 'rubric_assessment', 'submission_history']
                },
                timeout=10
            )
            response.raise_for_status()
            return response.json()
        except Exception as e:
            print(f"Error getting submission: {e}")
            return None
    
    def get_upcoming_assignments(self, days_ahead: int = 14) -> List[Dict]:
        """
        Get upcoming assignments across all courses
        
        Args:
            days_ahead: Number of days to look ahead for assignments
        """
        upcoming = []
        courses = self.get_courses()
        cutoff_date = datetime.now() + timedelta(days=days_ahead)
        
        for course in courses:
            assignments = self.get_assignments(course['id'], include_future=True)
            
            for assignment in assignments:
                due_at = assignment.get('due_at')
                if due_at:
                    try:
                        due_date = datetime.fromisoformat(due_at.replace('Z', '+00:00'))
                        # Convert to local time (naive datetime for comparison)
                        due_date = due_date.replace(tzinfo=None)
                        
                        if due_date > datetime.now() and due_date <= cutoff_date:
                            upcoming.append({
                                'course_name': course['name'],
                                'course_id': course['id'],
                                'assignment_name': assignment['name'],
                                'assignment_id': assignment['id'],
                                'due_at': due_date,
                                'due_at_string': due_at,
                                'points_possible': assignment.get('points_possible'),
                                'assignment_url': assignment.get('html_url'),
                                'description': assignment.get('description', ''),
                                'submission_types': assignment.get('submission_types', [])
                            })
                    except (ValueError, TypeError):
                        # Skip assignments with invalid dates
                        continue
        
        # Sort by due date
        upcoming.sort(key=lambda x: x['due_at'])
        return upcoming
    
    def check_pending_feedback(self) -> List[Dict]:
        """
        Check for submitted assignments that don't have feedback yet
        
        Returns:
            List of assignments awaiting feedback
        """
        pending_feedback = []
        courses = self.get_courses()
        
        for course in courses:
            assignments = self.get_assignments(course['id'], include_future=False)
            
            for assignment in assignments:
                submission = self.get_submission(course['id'], assignment['id'])
                
                if submission and submission.get('workflow_state') == 'submitted':
                    # Check if feedback is missing
                    has_grade = submission.get('grade') is not None and submission.get('grade') != ''
                    has_comments = len(submission.get('submission_comments', [])) > 0
                    has_rubric_feedback = bool(submission.get('rubric_assessment'))
                    
                    # Consider it pending if no feedback at all
                    if not (has_grade or has_comments or has_rubric_feedback):
                        submitted_at = submission.get('submitted_at')
                        submitted_date = None
                        if submitted_at:
                            try:
                                submitted_date = datetime.fromisoformat(submitted_at.replace('Z', '+00:00'))
                                submitted_date = submitted_date.replace(tzinfo=None)
                            except (ValueError, TypeError):
                                pass
                        
                        pending_feedback.append({
                            'course_name': course['name'],
                            'course_id': course['id'],
                            'assignment_name': assignment['name'],
                            'assignment_id': assignment['id'],
                            'submitted_at': submitted_date,
                            'submitted_at_string': submitted_at,
                            'assignment_url': assignment.get('html_url'),
                            'points_possible': assignment.get('points_possible')
                        })
        
        # Sort by submission date (most recent first)
        pending_feedback.sort(key=lambda x: x['submitted_at'] or datetime.min, reverse=True)
        return pending_feedback
    
    def get_assignment_feedback(self, course_id: int, assignment_id: int) -> Dict:
        """Get detailed feedback for a specific assignment"""
        try:
            submission = self.get_submission(course_id, assignment_id)
            if not submission:
                return {}
            
            feedback = {
                'grade': submission.get('grade'),
                'score': submission.get('score'),
                'comments': [],
                'rubric_feedback': {},
                'workflow_state': submission.get('workflow_state')
            }
            
            # Process comments
            for comment in submission.get('submission_comments', []):
                feedback['comments'].append({
                    'author': comment.get('author_name', 'Unknown'),
                    'comment': comment.get('comment', ''),
                    'created_at': comment.get('created_at')
                })
            
            # Process rubric assessment
            rubric_assessment = submission.get('rubric_assessment')
            if rubric_assessment:
                for criterion_id, assessment in rubric_assessment.items():
                    feedback['rubric_feedback'][criterion_id] = {
                        'points': assessment.get('points'),
                        'comments': assessment.get('comments', '')
                    }
            
            return feedback
            
        except Exception as e:
            print(f"Error getting assignment feedback: {e}")
            return {}


class CanvasConfig:
    """Manages Canvas configuration storage"""
    
    CONFIG_FILE = "canvas_config.json"
    
    @classmethod
    def load(cls) -> Dict:
        """Load Canvas configuration from file"""
        try:
            if os.path.exists(cls.CONFIG_FILE):
                with open(cls.CONFIG_FILE, 'r', encoding='utf-8') as f:
                    return json.load(f)
        except Exception as e:
            print(f"Error loading Canvas config: {e}")
        return {}
    
    @classmethod
    def save(cls, config: Dict):
        """Save Canvas configuration to file"""
        try:
            with open(cls.CONFIG_FILE, 'w', encoding='utf-8') as f:
                json.dump(config, f, indent=2, ensure_ascii=False)
        except Exception as e:
            print(f"Error saving Canvas config: {e}")
    
    @classmethod
    def is_configured(cls) -> bool:
        """Check if Canvas is properly configured"""
        config = cls.load()
        return bool(config.get('canvas_url') and config.get('access_token'))
