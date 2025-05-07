METADATA = {
    "inputs": {
        "file_path": "str - Path to the output text file",
        "content": "str - Content to write to the file"
    },
    "outputs": {
        "status": "str - Status message indicating success or failure"
    }
}

def main(inputs):
    """
    Main function to write content to a text file.

    Args:
        inputs (dict): A dictionary containing the input variables.
            - file_path (str): The path to the output text file.
            - content (str): The content to write to the file.

    Returns:
        dict: A dictionary containing the output variables.
            - status (str): Status message indicating success or failure.
    """
    file_path = inputs.get("file_path")
    content = inputs.get("content")

    if not file_path or not content:
        raise ValueError("Missing required inputs: 'file_path' and 'content'")

    try:
        with open(file_path, "w") as file:
            file.write(content)
        return {"status": "File written successfully"}
    except Exception as e:
        return {"status": f"Error writing file: {str(e)}"}