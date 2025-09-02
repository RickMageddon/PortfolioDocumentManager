"""
GitHub Integration Module for Portfolio Document Manager
Handles GitHub API connections, repository browsing, and file management.
"""

import requests
import json
import os
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass
import base64

@dataclass
class GitHubConfig:
    """GitHub configuration data class"""
    access_token: str = ""
    username: str = ""
    private_repo: str = ""
    shared_repo: str = ""
    
    @classmethod
    def load(cls) -> 'GitHubConfig':
        """Load GitHub configuration from file"""
        try:
            if os.path.exists('github_config.json'):
                with open('github_config.json', 'r') as f:
                    data = json.load(f)
                return cls(**data)
            else:
                return cls()
        except Exception as e:
            print(f"Error loading GitHub config: {e}")
            return cls()
    
    def save(self) -> bool:
        """Save GitHub configuration to file"""
        try:
            with open('github_config.json', 'w') as f:
                json.dump(self.__dict__, f, indent=2)
            return True
        except Exception as e:
            print(f"Error saving GitHub config: {e}")
            return False

class GitHubIntegration:
    """GitHub API integration class"""
    
    def __init__(self, access_token: str):
        self.access_token = access_token
        self.base_url = "https://api.github.com"
        self.headers = {
            "Authorization": f"token {access_token}",
            "Accept": "application/vnd.github.v3+json",
            "User-Agent": "Portfolio-Document-Manager"
        }
        self.username = None
    
    def test_connection(self) -> Tuple[bool, str]:
        """Test GitHub API connection and get user info"""
        try:
            response = requests.get(f"{self.base_url}/user", headers=self.headers, timeout=10)
            
            if response.status_code == 200:
                user_data = response.json()
                self.username = user_data.get('login', '')
                return True, f"Connected as {user_data.get('name', self.username)} (@{self.username})"
            elif response.status_code == 401:
                return False, "Invalid access token"
            else:
                return False, f"API Error: {response.status_code}"
                
        except requests.exceptions.RequestException as e:
            return False, f"Connection error: {str(e)}"
    
    def get_user_repositories(self) -> List[Dict]:
        """Get all repositories for the authenticated user"""
        try:
            repositories = []
            page = 1
            
            while True:
                response = requests.get(
                    f"{self.base_url}/user/repos",
                    headers=self.headers,
                    params={
                        'per_page': 100,
                        'page': page,
                        'sort': 'updated',
                        'direction': 'desc'
                    },
                    timeout=10
                )
                
                if response.status_code != 200:
                    break
                    
                page_repos = response.json()
                if not page_repos:
                    break
                    
                repositories.extend(page_repos)
                page += 1
                
                # GitHub API pagination limit
                if page > 10:  # Limit to first 1000 repos
                    break
            
            return repositories
            
        except Exception as e:
            print(f"Error fetching repositories: {e}")
            return []
    
    def get_organization_repositories(self, org_name: str) -> List[Dict]:
        """Get repositories for a specific organization"""
        try:
            repositories = []
            page = 1
            
            while True:
                response = requests.get(
                    f"{self.base_url}/orgs/{org_name}/repos",
                    headers=self.headers,
                    params={
                        'per_page': 100,
                        'page': page,
                        'sort': 'updated',
                        'direction': 'desc'
                    },
                    timeout=10
                )
                
                if response.status_code != 200:
                    break
                    
                page_repos = response.json()
                if not page_repos:
                    break
                    
                repositories.extend(page_repos)
                page += 1
                
                if page > 5:  # Limit org repos
                    break
            
            return repositories
            
        except Exception as e:
            print(f"Error fetching organization repositories: {e}")
            return []
    
    def get_repository_contents(self, repo_full_name: str, path: str = "") -> List[Dict]:
        """Get contents of a repository directory"""
        try:
            url = f"{self.base_url}/repos/{repo_full_name}/contents/{path}"
            response = requests.get(url, headers=self.headers, timeout=10)
            
            if response.status_code == 200:
                return response.json()
            else:
                return []
                
        except Exception as e:
            print(f"Error fetching repository contents: {e}")
            return []
    
    def get_file_content(self, repo_full_name: str, file_path: str) -> Optional[str]:
        """Get the content of a specific file"""
        try:
            url = f"{self.base_url}/repos/{repo_full_name}/contents/{file_path}"
            response = requests.get(url, headers=self.headers, timeout=10)
            
            if response.status_code == 200:
                file_data = response.json()
                if file_data.get('encoding') == 'base64':
                    content = base64.b64decode(file_data['content']).decode('utf-8')
                    return content
                    
        except Exception as e:
            print(f"Error fetching file content: {e}")
            
        return None
    
    def get_file_url(self, repo_full_name: str, file_path: str, branch: str = "main") -> str:
        """Get the GitHub URL for a specific file"""
        return f"https://github.com/{repo_full_name}/blob/{branch}/{file_path}"
    
    def get_commit_info(self, repo_full_name: str, file_path: str) -> Optional[Dict]:
        """Get latest commit information for a file"""
        try:
            url = f"{self.base_url}/repos/{repo_full_name}/commits"
            params = {'path': file_path, 'per_page': 1}
            response = requests.get(url, headers=self.headers, params=params, timeout=10)
            
            if response.status_code == 200:
                commits = response.json()
                if commits:
                    return commits[0]
                    
        except Exception as e:
            print(f"Error fetching commit info: {e}")
            
        return None
    
    def search_repositories(self, query: str, organization: str = None) -> List[Dict]:
        """Search for repositories"""
        try:
            search_query = query
            if organization:
                search_query += f" org:{organization}"
                
            response = requests.get(
                f"{self.base_url}/search/repositories",
                headers=self.headers,
                params={
                    'q': search_query,
                    'sort': 'updated',
                    'order': 'desc',
                    'per_page': 50
                },
                timeout=10
            )
            
            if response.status_code == 200:
                return response.json().get('items', [])
                
        except Exception as e:
            print(f"Error searching repositories: {e}")
            
        return []

def create_github_file_reference(repo_full_name: str, file_path: str, branch: str = "main") -> Dict:
    """Create a standardized GitHub file reference"""
    return {
        'type': 'github_file',
        'repository': repo_full_name,
        'file_path': file_path,
        'branch': branch,
        'url': f"https://github.com/{repo_full_name}/blob/{branch}/{file_path}",
        'raw_url': f"https://raw.githubusercontent.com/{repo_full_name}/{branch}/{file_path}"
    }

def parse_github_url(url: str) -> Optional[Dict]:
    """Parse a GitHub URL to extract repository and file information"""
    try:
        # Handle various GitHub URL formats
        if 'github.com' in url:
            # Remove protocol and domain
            path = url.split('github.com/')[-1]
            
            # Split path components
            parts = path.split('/')
            if len(parts) >= 2:
                owner = parts[0]
                repo = parts[1]
                repo_full_name = f"{owner}/{repo}"
                
                # Check if it's a file URL (contains 'blob' or 'tree')
                if len(parts) >= 4 and parts[2] in ['blob', 'tree']:
                    branch = parts[3]
                    file_path = '/'.join(parts[4:]) if len(parts) > 4 else ''
                    
                    return {
                        'repository': repo_full_name,
                        'branch': branch,
                        'file_path': file_path,
                        'url': url
                    }
                else:
                    return {
                        'repository': repo_full_name,
                        'branch': 'main',
                        'file_path': '',
                        'url': url
                    }
                    
    except Exception as e:
        print(f"Error parsing GitHub URL: {e}")
        
    return None
