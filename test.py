import asyncio
from mcp.server import Server
import mcp.types as types
from mcp.server.models import InitializationOptions
from mcp.server import NotificationOptions
from server import (
        NavigateToolHandler,
        ClickTextToolHandler,
        FillToolHandler,
        ClickToolHandler
    )

async def test_login():
    # Initialize the tools
    tool_handlers = {
        "playwright_navigate": NavigateToolHandler(),
        "playwright_click_text": ClickTextToolHandler(),
        "playwright_fill": FillToolHandler(),
        "playwright_click": ClickToolHandler(),
    }

    # Navigate to the website
    await tool_handlers["playwright_navigate"].handle("playwright_navigate", {
        "url": "http://eaapp.somee.com/"
    })

    # Click on the login link
    await tool_handlers["playwright_click_text"].handle("playwright_click_text", {
        "text": "Login"
    })

    # Fill in username
    await tool_handlers["playwright_fill"].handle("playwright_fill", {
        "selector": "#UserName",
        "value": "admin"
    })

    # Fill in password
    await tool_handlers["playwright_fill"].handle("playwright_fill", {
        "selector": "#Password",
        "value": "password"
    })

    # Click login button
    await tool_handlers["playwright_click"].handle("playwright_click", {
        "selector": "input[value='Log in']"
    })

if __name__ == "__main__":
    asyncio.run(test_login())
