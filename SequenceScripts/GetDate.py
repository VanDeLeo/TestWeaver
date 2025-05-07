import datetime

# Metadatos opcionales para describir las entradas y salidas
METADATA = {
    "inputs": {
        "format": "str - Date format (e.g., 'YYYYMMDD', 'MMDDYYYY', 'DDMMYYYY')"
    },
    "outputs": {
        "date": "str - Formatted date"
    }
}

def main(inputs):
    """
    Main function to get the current date in a specified format.

    Args:
        inputs (dict): A dictionary containing the input variables.
            - format (str): The date format ('YYYYMMDD', 'MMDDYYYY', 'DDMMYYYY').

    Returns:
        dict: A dictionary containing the output variables.
            - date (str): The formatted date.
    """
    format = inputs.get("format")
    if not format:
        raise ValueError("Missing required input: 'format'")

    if format == "YYYYMMDD":
        date = datetime.datetime.now().strftime("%Y%m%d")
    elif format == "MMDDYYYY":
        date = datetime.datetime.now().strftime("%m%d%Y")
    elif format == "DDMMYYYY":
        date = datetime.datetime.now().strftime("%d%m%Y")
    else:
        raise ValueError("Invalid format. Use 'YYYYMMDD', 'MMDDYYYY', or 'DDMMYYYY'.")

    return {"date": date}
    