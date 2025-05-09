from typing import Any
import httpx
from mcp.server.fastmcp import FastMCP
import datetime

# Initialize FastMCP server
mcp = FastMCP("weather")

# Constants
NWS_API_BASE = "https://api.weather.gov"
USER_AGENT = "weather-app/1.0"


# async def make_nws_request(url: str) -> dict[str, Any] | None:
#     """Make a request to the NWS API with proper error handling."""
#     headers = {
#         "User-Agent": USER_AGENT,
#         "Accept": "application/geo+json"
#     }
#     async with httpx.AsyncClient() as client:
#         try:
#             response = await client.get(url, headers=headers, timeout=30.0)
#             response.raise_for_status()
#             return response.json()
#         except Exception:
#             return None


# def format_alert(feature: dict) -> str:
#     """Format an alert feature into a readable string."""
#     props = feature["properties"]
#     return f"""
# Event: {props.get('event', 'Unknown')}
# Area: {props.get('areaDesc', 'Unknown')}
# Severity: {props.get('severity', 'Unknown')}
# Description: {props.get('description', 'No description available')}
# Instructions: {props.get('instruction', 'No specific instructions provided')}
# """


@mcp.tool()
async def send_message(message: str, receiver: str) -> str:
    """Send a message to a person with the Slack API.

    Args:
        message: The message to send.
        receiver: The person to send the message to.
    """

    print("Simulated message sending...")
    # url = f"{NWS_API_BASE}/alerts/active/area/{state}"
    return "Den er grei!"
    # data = await make_nws_request(url)


@mcp.tool()
async def read_message(receiver: str) -> str:
    """Reads the newest message from a receiver.

    Args:
        receiver: The person to read the message from.
    """

    return f"Den er grei, klokken er nå {datetime.datetime.now()}"

if __name__ == "__main__":
    # Initialize and run the server
    mcp.run(transport='stdio')
