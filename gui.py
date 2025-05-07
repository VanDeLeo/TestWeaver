import customtkinter as ctk
import tkinter as tk
from tkinter import ttk
import psutil
import os
from analyze_script import analyze_script
import sequence_handler

class TestWeaverGUI(ctk.CTk):
    def __init__(self):
        super().__init__()
        
        self.title("TestWeaver")
        self.geometry("900x600")
        self.minsize(800, 600)

        self.create_menu()
        self.create_widgets()
        self.configure_grid()

        #print(analyze_script("./SequenceScripts/GetDate.py"))

    def create_menu(self):
        self.menu_bar = tk.Menu(self)

        file_menu = tk.Menu(self.menu_bar, tearoff=0)
        file_menu.add_command(label="New", command=self.new_testplan)
        file_menu.add_command(label="Edit", command=self.testplan_editor)
        file_menu.add_command(label="Open", command=self.select_file)
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=self.quit)
        self.menu_bar.add_cascade(label="File", menu=file_menu)

        options_menu = tk.Menu(self.menu_bar, tearoff=0)
        options_menu.add_command(label="CPU Affinity", command=self.cores_affinity)
        options_menu.add_command(label="CPU Priority", command=self.cpu_priority)
        self.menu_bar.add_cascade(label="Settings", menu=options_menu)

        self.config(menu=self.menu_bar)

    def configure_grid(self):
        self.grid_rowconfigure(1, weight=0)   # RUN button
        self.grid_rowconfigure(3, weight=1)   # Terminals
        self.grid_rowconfigure(4, weight=1)   # Report

        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)

    def create_widgets(self):
        self.run_button = ctk.CTkButton(self, text="RUN", width=100, height=40, command=self.run_test)
        self.run_button.grid(row=1, column=0, sticky="w", padx=20, pady=(20, 10), columnspan=2)

        self.left_title = ctk.CTkLabel(self, text="Test info", font=ctk.CTkFont(size=16))
        self.left_title.grid(row=3, column=0, sticky="nw", padx=20, pady=(0, 5))

        self.right_title = ctk.CTkLabel(self, text="Status", font=ctk.CTkFont(size=16))
        self.right_title.grid(row=3, column=1, sticky="nw", padx=20, pady=(0, 5))

        self.left_textbox = ctk.CTkTextbox(self)
        self.left_textbox.grid(row=3, column=0, sticky="nsew", padx=20, pady=(30, 10))

        self.right_textbox = ctk.CTkTextbox(self)
        self.right_textbox.grid(row=3, column=1, sticky="nsew", padx=20, pady=(30, 10))

        self.report_title = ctk.CTkLabel(self, text="Report", font=ctk.CTkFont(size=16))
        self.report_title.grid(row=4, column=0, sticky="w", padx=20, pady=(10, 0), columnspan=2)

        self.tree_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.tree_frame.grid(row=4, column=0, columnspan=2, sticky="nsew", padx=20, pady=(40, 20))

        self.tree_frame.grid_rowconfigure(0, weight=1)
        self.tree_frame.grid_columnconfigure(0, weight=1)

        self.report_tree = ttk.Treeview(
            self.tree_frame, 
            columns=("Column1", "Column2", "Column3", "Column4", "Column5", "Column6"), 
            show="headings"
        )
        self.report_tree.grid(row=0, column=0, sticky="nsew")

        self.report_tree.heading("Column1", text="ID")
        self.report_tree.heading("Column2", text="Test Step")
        self.report_tree.heading("Column3", text="Low limit")
        self.report_tree.heading("Column4", text="Result")
        self.report_tree.heading("Column5", text="High limit")
        self.report_tree.heading("Column6", text="Time")
        self.tree_scrollbar = tk.Scrollbar(self.tree_frame, orient="vertical", command=self.report_tree.yview)
        self.tree_scrollbar.grid(row=0, column=1, sticky="ns")
        self.report_tree.configure(yscrollcommand=self.tree_scrollbar.set)

    def run_test(self):
        self.left_textbox.insert("end", "Running test sequence...\n")
        self.right_textbox.insert("end", "Initializing environment...\n")

        self.report_tree.insert("", "end", values=("Test 1", "PASS"))
        self.report_tree.insert("", "end", values=("Test 2", "FAIL"))

    def select_file(self):
        file_path = tk.filedialog.askopenfilename(title="Select sequence file", filetypes=[("JSON files", ".json")])

        if file_path:
            self.right_textbox.insert("end", f"Selected file: {file_path}\n")

    def cores_affinity(self):
        affinityOptions = tk.Toplevel(self)
        affinityOptions.title("Cores Affinity")

        cpuCount = os.cpu_count()
        actualAffinity = psutil.Process(os.getpid()).cpu_affinity()

        #Calculate window size based on CPU count
        rows = (cpuCount // 5) + (1 if cpuCount % 5 != 0 else 0)  # max 5 rows
        window_height = 100 + (rows * 40)  # height + 40px per row
        window_width = 300 + (cpuCount // 5) * 100  # width + 100px per column
        affinityOptions.geometry(f"{window_width}x{window_height}")

        title_label = ctk.CTkLabel(affinityOptions, text="Select CPU affinity:")
        title_label.grid(row=0, column=0, padx=20, pady=(20, 10))

        self.cpu_all = ctk.CTkCheckBox(affinityOptions, text="All CPUs", command=lambda: self.select_all_cpus(cpuCount))
        self.cpu_all.grid(row=1, column=0, padx=20, pady=(10, 5))


        self.cpu_checkbuttons = []

        row = 0
        column = 0

        for index, cpu_option in enumerate(range(cpuCount)):
            row = 2 + (index % 5)  # Cada 5 elementos, reinicia la fila
            column = index // 5    # Incrementa la columna cada 5 elementos
            cpu_checkbutton = ctk.CTkCheckBox(affinityOptions, text=f"CPU {cpu_option}")
            cpu_checkbutton.grid(row=row, column=column, padx=20, pady=(10, 5))
            if cpu_option in actualAffinity:
                cpu_checkbutton.select()
            self.cpu_checkbuttons.append(cpu_checkbutton)  # Almacenar el checkbox en la lista
        
        saveButton = ctk.CTkButton(affinityOptions, text="Save", command=lambda: self.save_affinity())
        saveButton.grid(row=row + 1, column=column, padx=20, pady=(10, 5))

    def select_all_cpus(self):
        # Check if the "All CPUs" checkbox is selected
        if self.cpu_all.get():
            # Select all CPU checkboxes
            for cpu_checkbutton in self.cpu_checkbuttons:
                cpu_checkbutton.select()
        else:
            # Deselect all CPU checkboxes
            for cpu_checkbutton in self.cpu_checkbuttons:
                cpu_checkbutton.deselect()

    def save_affinity(self):
        selected_cpus = [index for index, cpu_checkbutton in enumerate(self.cpu_checkbuttons) if cpu_checkbutton.get()]
        if selected_cpus:
            psutil.Process(os.getpid()).cpu_affinity(selected_cpus)
            self.right_textbox.insert("end", f"Affinity set to CPUs: {selected_cpus}\n")
        else:
            self.right_textbox.insert("end", "No CPUs selected. Affinity not changed.\n")

    def cpu_priority(self):
        priorityOptions = tk.Toplevel(self)
        priorityOptions.title("CPU Priority")

        title_label = ctk.CTkLabel(priorityOptions, text="Select CPU priority:")
        title_label.grid(row=0, column=0, padx=20, pady=(20, 10))

        actualPriority = psutil.Process(os.getpid()).nice()

        if actualPriority == psutil.IDLE_PRIORITY_CLASS:
            actualPriority = "Idle"
        elif actualPriority == psutil.BELOW_NORMAL_PRIORITY_CLASS:
            actualPriority = "Below Normal"
        elif actualPriority == psutil.NORMAL_PRIORITY_CLASS:
            actualPriority = "Normal"
        elif actualPriority == psutil.ABOVE_NORMAL_PRIORITY_CLASS:
            actualPriority = "Above Normal"
        elif actualPriority == psutil.HIGH_PRIORITY_CLASS:
            actualPriority = "High"
        elif actualPriority == psutil.REALTIME_PRIORITY_CLASS:
            actualPriority = "Real Time"
        else:
            actualPriority = "Unknown Priority"
        
        print(actualPriority)

        prioritySelection = ctk.CTkOptionMenu(
            priorityOptions, 
            values=["Idle", "Below Normal", "Normal", "Above Normal", "High", "Real Time"]
        )
        prioritySelection.grid(row=1, column=0, padx=20, pady=(10, 5))

        prioritySelection.set(actualPriority)

        saveButton = ctk.CTkButton(priorityOptions, text="Save", command=lambda: self.set_priority(prioritySelection.get()))
        saveButton.grid(row=2, column=0, padx=20, pady=(10, 5))

    def set_priority(self, priority):
        print(priority)
        if priority != "Unknown Priority":
            if priority == "Idle":
                psutil.Process(os.seetpid())
            elif priority == "Below Normal":
                psutil.Process(os.getpid()).nice(psutil.BELOW_NORMAL_PRIORITY_CLASS)
            elif priority == "Normal":
                psutil.Process(os.getpid()).nice(psutil.NORMAL_PRIORITY_CLASS)
            elif priority == "Above Normal":
                psutil.Process(os.getpid()).nice(psutil.ABOVE_NORMAL_PRIORITY_CLASS)
            elif priority == "High":
                psutil.Process(os.getpid()).nice(psutil.HIGH_PRIORITY_CLASS)
            elif priority == "Real Time":
                psutil.Process(os.getpid()).nice(psutil.REALTIME_PRIORITY_CLASS)
                print("Real Time priority set")
            pass
        else: pass

    def new_testplan(self):
        filePath = tk.filedialog.asksaveasfilename(
            title="Create new testplan",
            defaultextension=".json",
            filetypes=[("JSON files", ".json")],
            initialdir=os.getcwd()
        )

        if filePath:
            try:
                with open(filePath,"w") as file:
                    file.write("{}")
                    self.testplan_editor()
            except Exception as e:
                print(f"Error creating file: {e}")
        else:
            print("File creation cancelled.")

    def testplan_editor(self):
        # Crear la ventana del editor de test plans
        testplanEditor = tk.Toplevel(self)
        testplanEditor.title("Test Plan Editor")
        testplanEditor.geometry("1450x650")
        testplanEditor.resizable(False, False)  # Deshabilitar redimensionamiento

        # Crear el menú
        menu_bar = tk.Menu(testplanEditor)

        # Menú File
        file_menu = tk.Menu(menu_bar, tearoff=0)
        file_menu.add_command(label="Save", command=lambda: self.save_testplan(test_tree,variables_tree))
        menu_bar.add_cascade(label="File", menu=file_menu)

        # Configurar el menú en la ventana
        testplanEditor.config(menu=menu_bar)

        # Configurar el grid principal
        testplanEditor.grid_rowconfigure(0, weight=1)
        testplanEditor.grid_columnconfigure(0, weight=0)
        testplanEditor.grid_columnconfigure(1, weight=0)
        testplanEditor.grid_columnconfigure(2, weight=1)

        left_Frame = ctk.CTkFrame(testplanEditor, fg_color="transparent")
        left_Frame.grid(row=0, column=0, sticky="nsew", padx=5, pady=(20, 0))

        tree_title_Frame = ctk.CTkFrame(left_Frame, fg_color="transparent")
        tree_title_Frame.pack(side="top", fill="x", padx=20, pady=(0, 5))

        tree_tile = ctk.CTkLabel(tree_title_Frame, text="Test Sequence", font=ctk.CTkFont(size=16))
        tree_tile.grid(row=0, column=0, padx=5, pady=5, sticky="w")

        # Treeview para mostrar la secuencia de tests
        tree_frame = ctk.CTkFrame(left_Frame, fg_color="transparent")
        tree_frame.pack(side="top", fill="both", expand=True, padx=20, pady=(0, 20))

        tree_frame.grid_rowconfigure(0, weight=1)
        tree_frame.grid_columnconfigure(0, weight=1)

        test_tree = ttk.Treeview(
            tree_frame,
            columns=("Test Name", "Script"),
            show="headings"
        )
        test_tree.grid(row=0, column=0, sticky="nsew")

        # Configurar encabezados del Treeview
        test_tree.heading("Test Name", text="Test Name")
        test_tree.heading("Script", text="Script")

        # Scrollbar para el Treeview
        tree_scrollbar = tk.Scrollbar(tree_frame, orient="vertical", command=test_tree.yview)
        tree_scrollbar.grid(row=0, column=1, sticky="ns")
        test_tree.configure(yscrollcommand=tree_scrollbar.set)

        center_Frame = ctk.CTkFrame(testplanEditor, fg_color="transparent")
        center_Frame.grid(row=0, column=1, sticky="nsew", padx=5, pady=(20, 0))

        up_center_Frame = ctk.CTkFrame(center_Frame, fg_color="transparent")
        up_center_Frame.pack(side="top", fill="x", padx=20, pady=(0, 5))

        test_options_label = ctk.CTkLabel(up_center_Frame, text="Test Options", font=ctk.CTkFont(size=16))
        test_options_label.pack(side="top", padx=5, pady=5, anchor="w")

        # Frame para los inputs y outputs dinámicos
        dynamic_frame_container_1 = ctk.CTkFrame(up_center_Frame, fg_color="white")
        dynamic_frame_container_1.pack(side="top", fill="both", expand=True, padx=20, pady=(0, 20))

        # Canvas para manejar el scroll del primer frame
        canvas_1 = tk.Canvas(dynamic_frame_container_1)
        canvas_1.grid(row=0, column=0, sticky="nsew")

        scrollbar_1 = tk.Scrollbar(dynamic_frame_container_1, orient="vertical", command=canvas_1.yview)
        scrollbar_1.grid(row=0, column=1, sticky="ns")
        canvas_1.configure(yscrollcommand=scrollbar_1.set)

        # Frame interno para los elementos dinámicos del primer frame
        dynamic_frame_1 = ctk.CTkFrame(canvas_1, fg_color="transparent")
        canvas_1.create_window((0, 0), window=dynamic_frame_1, anchor="nw")

        # Configurar el tamaño dinámico del primer frame
        dynamic_frame_1.bind("<Configure>", lambda e: canvas_1.configure(scrollregion=canvas_1.bbox("all")))

        # Función para actualizar el frame dinámico
        def update_dynamic_frame(details):

            # Limpiar el frame dinámico
            for widget in dynamic_frame_1.winfo_children():
                widget.destroy()

            row = 0
            # Agregar inputs
            titleInputs = ctk.CTkLabel(dynamic_frame_1, text="Inputs", font=ctk.CTkFont(size=16))
            titleInputs.grid(row=row, column=0, padx=5, pady=5, sticky="w")

            if details.get("inputs"):
                
                row = 1
                for key, value in details["inputs"].items():
                    entry = ctk.CTkEntry(dynamic_frame_1, width=200)
                    entry.insert(0, key)
                    entry.configure(state="readonly")
                    entry.grid(row=row, column=0, padx=5, pady=5, sticky="w")

                    entry.bind("<FocusIn>", lambda event, key=key: on_option_select("inputs",key))

                    combobox = ctk.CTkComboBox(dynamic_frame_1, values=self.get_variables(variables_tree))
                    combobox.grid(row=row, column=1, padx=5, pady=5, sticky="w")

                    row += 1

            # Agregar outputs
            titleOutputs = ctk.CTkLabel(dynamic_frame_1, text="Outputs", font=ctk.CTkFont(size=16))
            titleOutputs.grid(row=row, column=0, padx=5, pady=5, sticky="w")
            row += 1
            if details.get("outputs"):    
                for key, value in details["outputs"].items():
                    entry = ctk.CTkEntry(dynamic_frame_1, width=200)
                    entry.insert(0, key)
                    entry.configure(state="readonly")
                    entry.grid(row=row, column=0, padx=5, pady=5, sticky="w")

                    entry.bind("<FocusIn>", lambda event, key=key: on_option_select("outputs",key))

                    combobox = ctk.CTkComboBox(dynamic_frame_1, values=self.get_variables(variables_tree))
                    combobox.grid(row=row, column=1, padx=5, pady=5, sticky="w")

                    row += 1

        

        def on_test_select(event):
            selected_item = test_tree.selection()
            if selected_item:
                script_name = test_tree.item(selected_item, "values")[1]
                self.details = analyze_script(script_name)
                update_dynamic_frame(self.details)

        test_tree.bind("<<TreeviewSelect>>", on_test_select)
               
        option_description_Frame = ctk.CTkFrame(center_Frame, fg_color="white")
        option_description_Frame.pack(side="top", fill="x", padx=20, pady=(0, 20))

        option_title = ctk.CTkLabel(option_description_Frame, text="Description", font=ctk.CTkFont(size=16))
        option_title.pack(side="top", padx=5, pady=5, anchor="w")

        option_textbox = ctk.CTkTextbox(option_description_Frame, width=400, height=100)
        option_textbox.pack(side="top", fill="both", expand=True, padx=5, pady=(0, 20))

        def on_option_select(kind,key):
            option_textbox.configure(state="normal")
            option_textbox.delete("1.0", "end")
            option_textbox.insert("end", self.details[kind][key])
            option_textbox.configure(state="disabled")
            
        
        add_delete_Frame = ctk.CTkFrame(center_Frame, fg_color="white")
        add_delete_Frame.pack(side="top", fill="x", padx=20, pady=(0, 20))

        add_delete_Title = ctk.CTkLabel(add_delete_Frame, text="Add/Delete Test in Sequence", font=ctk.CTkFont(size=16))
        add_delete_Title.pack(side="top", padx=5, pady=5, anchor="w")

        # Botones debajo del primer frame dinámico
        button_row_frame_1 = ctk.CTkFrame(add_delete_Frame, fg_color="white")
        button_row_frame_1.pack(side="top", fill="x", padx=20, pady=(0, 20))

        add_button_1 = ctk.CTkButton(button_row_frame_1, text="Add", command=lambda: self.add_test(test_tree), width=100)
        add_button_1.grid(row=0, column=0, padx=5)

        delete_button_1 = ctk.CTkButton(button_row_frame_1, text="Delete", command=lambda: self.delete_test(test_tree, dynamic_frame_1, option_textbox), width=100)
        delete_button_1.grid(row=0, column=1, padx=5)

        right_Frame = ctk.CTkFrame(testplanEditor, fg_color="transparent")
        right_Frame.grid(row=0, column=2, sticky="nsew", padx=5, pady=(20, 0))

        variables_Frame = ctk.CTkFrame(right_Frame, fg_color="transparent")
        variables_Frame.pack(side="top", fill="x", padx=20, pady=(0, 5))

        variables_title = ctk.CTkLabel(variables_Frame, text="Variables", font=ctk.CTkFont(size=16))
        variables_title.pack(side="top", padx=5, pady=5, anchor="w")

        variables_tree_Frame = ctk.CTkFrame(variables_Frame)
        variables_tree_Frame.pack(side="top", fill="both", expand=True, padx=20, pady=(0, 20))

        variables_tree = ttk.Treeview(
            variables_tree_Frame,
            columns=("Variable", "Last Value"),
            show="headings"
        )
        variables_tree.grid(row=0, column=0, sticky="nsew")

        # Configurar encabezados del Treeview
        variables_tree.heading("Variable", text="Variable")
        variables_tree.heading("Last Value", text="Last Value")

        # Scrollbar para el Treeview
        tree_variables_scrollbar = tk.Scrollbar(variables_tree_Frame, orient="vertical", command=variables_tree.yview)
        tree_variables_scrollbar.grid(row=0, column=1, sticky="ns")
        variables_tree.configure(yscrollcommand=tree_variables_scrollbar.set)

        # Botones debajo del segundo frame dinámico
        button_row_frame_2 = ctk.CTkFrame(variables_Frame, fg_color="transparent")
        button_row_frame_2.pack(side="top", padx=5, pady=5, anchor="w")

        add_button_2 = ctk.CTkButton(button_row_frame_2, text="Add", command=lambda: self.new_variable(variables_tree), width=100)
        add_button_2.grid(row=0, column=0, padx=5)

        delete_button_2 = ctk.CTkButton(button_row_frame_2, text="Delete", command=lambda: print("Delete clicked for Frame 2"), width=100)
        delete_button_2.grid(row=0, column=1, padx=5)

    def add_test(self, test_tree):
        # Crear una ventana emergente para agregar un nuevo test
        add_test_window = tk.Toplevel(self)
        add_test_window.title("Add New Test")
        add_test_window.geometry("500x250")  # Aumentar el tamaño de la ventana
        add_test_window.resizable(False, False)  # Deshabilitar redimensionamiento

        # Etiqueta y entrada para el nombre del test
        test_name_label = ctk.CTkLabel(add_test_window, text="Test Name:")
        test_name_label.grid(row=0, column=0, padx=10, pady=10, sticky="e")

        test_name_entry = ctk.CTkEntry(add_test_window, width=300)
        test_name_entry.grid(row=0, column=1, padx=10, pady=10, sticky="w", columnspan=2)

        # Etiqueta y entrada para la ubicación del script
        script_label = ctk.CTkLabel(add_test_window, text="Script Path:")
        script_label.grid(row=1, column=0, padx=10, pady=10, sticky="e")

        script_path_entry = ctk.CTkEntry(add_test_window, width=300)
        script_path_entry.grid(row=1, column=1, padx=10, pady=10, sticky="w")

        # Botón para abrir el explorador de archivos
        def select_script():
            script_path = tk.filedialog.askopenfilename(
                title="Select Script",
                filetypes=[("Python Files", "*.py"), ("All Files", "*.*")]
            )
            if script_path:
                script_path_entry.delete(0, "end")
                script_path_entry.insert(0, script_path)

        browse_button = ctk.CTkButton(add_test_window, text="Browse", command=select_script, width=80)
        browse_button.grid(row=1, column=2, padx=10, pady=10)

        # Botón para guardar el test
        def save_test():
            test_name = test_name_entry.get()
            script_path = script_path_entry.get()

            if not test_name or not script_path:
                tk.messagebox.showerror("Error", "Both Test Name and Script Path are required.")
                return

            # Agregar el test al Treeview
            test_tree.insert("", "end", values=(test_name, script_path))
            add_test_window.destroy()

        save_button = ctk.CTkButton(add_test_window, text="Save", command=save_test, width=100)
        save_button.grid(row=2, column=1, padx=10, pady=20, sticky="e")

        # Botón para cancelar
        cancel_button = ctk.CTkButton(add_test_window, text="Cancel", command=add_test_window.destroy, width=100)
        cancel_button.grid(row=2, column=2, padx=10, pady=20, sticky="w")

    def delete_test(self, test_tree, options_frame, textbox):
        selected_item = test_tree.selection()
        if selected_item:
            test_tree.delete(selected_item)
            for widget in options_frame.winfo_children(): widget.destroy()
            textbox.configure(state="normal")
            textbox.delete("1.0", "end")
            textbox.configure(state="disabled")
        else:
            tk.messagebox.showwarning("Warning", "No test selected to delete.")

    def new_variable(self, variables_tree):
        form_window = tk.Toplevel(self)
        form_window.title("New Variable")
        form_window.geometry("400x200")
        form_window.resizable(False, False)

        # Etiqueta para el campo de entrada
        label = ctk.CTkLabel(form_window, text="Name")
        label.grid(row=0, column=0, padx=20, pady=20, sticky="e")

        # Campo de entrada
        entry = ctk.CTkEntry(form_window, width=250)
        entry.grid(row=0, column=1, padx=20, pady=20, sticky="w")

        #Botón para guardar el valor
        def save_value():
            value = entry.get()
            if self.insert_variable:
                self.insert_variable(variables_tree,value)  # Llamar al callback con el valor ingresado
            form_window.destroy()

        save_button = ctk.CTkButton(form_window, text="Save", command=save_value, width=100)
        save_button.grid(row=1, column=0, padx=20, pady=20, sticky="e")

        # Botón para cancelar
        cancel_button = ctk.CTkButton(form_window, text="Cancel", command=form_window.destroy, width=100)
        cancel_button.grid(row=1, column=1, padx=20, pady=20, sticky="w")


    def insert_variable(self, variables_tree, variable):
        variables_tree.insert("", "end", values=(variable))

    def get_variables(self, variables_tree):
        variables = []
        for item in variables_tree.get_children():
            variable = variables_tree.item(item, "values")[0]
            variables.append(variable)

        print(variables)
        return variables
    
    def save_testplan(self, test_tree, variables_tree):
        tests = []
        for item in test_tree.get_children():
            test_name = test_tree.item(item, "values")[0]
            script_path = test_tree.item(item, "values")[1]
            tests.append({"name": test_name, "script": script_path})
        
        sequence_handler.save(tests)
        
