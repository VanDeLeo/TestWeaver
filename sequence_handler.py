from tkinter import filedialog
import json
import os

def load():
    pass

def save(test_sequence):

    if test_sequence is not None:
        # Abrir un diálogo para guardar el archivo
        file_path = filedialog.asksaveasfilename(
            title="Save Testplan",
            defaultextension=".json",
            filetypes=[("JSON files", "*.json")]
        )

        if file_path:
            # Extraer el nombre del archivo sin la extensión
            testplan_name = os.path.splitext(os.path.basename(file_path))[0]

            # Crear el formato JSON deseado
            formatted_data = {
                "TestplanName": testplan_name,
                "Date": "",  # Puedes agregar la fecha actual aquí si es necesario
                "TestSequence": {}
            }

            # Convertir la lista en el formato requerido
            for index, test in enumerate(test_sequence, start=1):
                formatted_data["TestSequence"][str(index)] = {
                    "TestName": test.get("name", ""),
                    "Script": test.get("script", "")
                }

            # Guardar el archivo JSON
            with open(file_path, 'w') as file:
                json.dump(formatted_data, file, indent=4)
            print(f"Test sequence saved to {file_path}")
        else:
            print("Save operation cancelled.")

