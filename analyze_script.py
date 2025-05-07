import ast
import importlib.util
import os

def analyze_script(script_path):
    analysis_result = {
        "inputs": None,
        "outputs": None,
        "errors": None
    }

    try:
        # Verificar si el archivo existe
        if not os.path.exists(script_path):
            analysis_result["errors"] = f"Script '{script_path}' not found."
            return analysis_result

        # Analizar el script para obtener metadatos y estructura
        with open(script_path, "r") as file:
            tree = ast.parse(file.read())

        # Extraer inputs y outputs desde METADATA
        for node in ast.walk(tree):
            if isinstance(node, ast.Assign) and isinstance(node.targets[0], ast.Name) and node.targets[0].id == "METADATA":
                metadata = ast.literal_eval(node.value)
                analysis_result["inputs"] = metadata.get("inputs")
                analysis_result["outputs"] = metadata.get("outputs")

        # Cargar dinámicamente el script y ejecutar la función main
        spec = importlib.util.spec_from_file_location("module.name", script_path)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)

        if not hasattr(module, "main"):
            analysis_result["errors"] = "Script does not have a 'main' function."
            return analysis_result

    except Exception as e:
        analysis_result["errors"] = str(e)

    return analysis_result