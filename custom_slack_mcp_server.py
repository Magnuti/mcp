from mcp.server.fastmcp import FastMCP
import datetime

# Initialize FastMCP server
mcp = FastMCP("weather")


@mcp.tool()
async def send_message(message: str, receiver: str) -> str:
    """Send a message to a person with the Slack API.

    Args:
        message: The message to send.
        receiver: The person to send the message to.
    """

    print("Simulated message sending...")
    return


@mcp.tool()
async def read_message(receiver: str) -> str:
    """Reads the newest message from a receiver.

    Args:
        receiver: The person to read the message from.
    """

    one_hour_later = datetime.datetime.now() + datetime.timedelta(hours=1, minutes=30)
    formatted_time = one_hour_later.strftime("%H:%M")
    return f"Den er grei, men du må være her innen {formatted_time}!"

if __name__ == "__main__":
    # Initialize and run the server
    mcp.run(transport='stdio')
