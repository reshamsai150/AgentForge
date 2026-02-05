from .weather import get_weather
from .github import search_repositories

TOOL_REGISTRY = {
    "weather": get_weather,
    "github_search": search_repositories
}

def get_tool(name: str):
    return TOOL_REGISTRY.get(name)
