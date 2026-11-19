# mcp_server.py
import httpx
from mcp.server.mcpserver import MCPServer

mcp = MCPServer("Iris Classifier", log_level="WARNING")


@mcp.tool()
def classify_iris(sepal_length: float, sepal_width: float, petal_length: float, petal_width: float) -> str:
    """Classify an iris flower from its four measurements, in centimeters.
    Returns the predicted species: setosa, versicolor, or virginica.
    """
    response = httpx.post(
        "http://127.0.0.1:8000/predict",
        json={
            "sepal_length": sepal_length,
            "sepal_width": sepal_width,
            "petal_length": petal_length,
            "petal_width": petal_width,
        },
    )
    return f"Predicted species: {response.json()['species']}"


@mcp.tool()
def iris_probabilities(sepal_length: float, sepal_width: float, petal_length: float, petal_width: float) -> str:
    """Get how confident the model is for each iris species, as a probability from 0 to 1
    for setosa, versicolor and virginica, from the four measurements in centimeters.
    Use this instead of classify_iris when the user wants to know how sure the model is,
    or whether the flower is a borderline case, rather than just the single best guess.
    """
    response = httpx.post(
        "http://127.0.0.1:8000/probabilities",
        json={
            "sepal_length": sepal_length,
            "sepal_width": sepal_width,
            "petal_length": petal_length,
            "petal_width": petal_width,
        },
    )
    return f"Probabilities: {response.json()}"


if __name__ == "__main__":
    mcp.run()
