import httpx
import os
from typing import Dict, Any, List

def search_repositories(query: str, limit: int = 5) -> Dict[str, Any]:
    """
    Search for GitHub repositories by query.
    Returns a list of repository details.
    """
    token = os.getenv("GITHUB_TOKEN")
    headers = {}
    if token:
        headers["Authorization"] = f"token {token}"
    
    url = f"https://api.github.com/search/repositories?q={query}&per_page={limit}"
    
    try:
        response = httpx.get(url, headers=headers, timeout=10.0)
        response.raise_for_status()
        data = response.json()
        
        items = data.get("items", [])
        repos = []
        for item in items:
            repos.append({
                "full_name": item.get("full_name"),
                "description": item.get("description"),
                "stars": item.get("stargazers_count"),
                "url": item.get("html_url"),
                "language": item.get("language")
            })
            
        return {
            "query": query,
            "count": len(repos),
            "repositories": repos,
            "success": True
        }
    except Exception as e:
        return {
            "success": False,
            "error": str(e)
        }
