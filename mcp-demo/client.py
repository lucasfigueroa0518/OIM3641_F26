# client.py: plays the part of an AI app (the "host")
import asyncio
import sys

from mcp import Client, StdioServerParameters

# Start mcp_server.py and talk to it, the way Claude Desktop or Cursor would
server = StdioServerParameters(command=sys.executable, args=["mcp_server.py"])


async def main():
    async with Client(server) as client:
        # 1. Discovery: ask the server what tools it has
        result = await client.list_tools()
        for tool in result.tools:
            print("Tool:", tool.name)
            print("Description:", tool.description)
            print("Inputs:", tool.input_schema["properties"])
            print()

        # 2. Use a tool, as an AI app would after reading the descriptions
        answer = await client.call_tool(
            "iris_probabilities",
            {"sepal_length": 6.0, "sepal_width": 2.7, "petal_length": 5.1, "petal_width": 1.6},
        )
        print(answer.content[0].text)


asyncio.run(main())
