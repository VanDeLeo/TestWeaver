import customtkinter as ctk
import tkinter as tk
from tkinter import ttk
import psutil
import os

class TestWeaverGUI(ctk.CTk):
    def __init__(self):
        super().__init__()
        
        self.title("TestWeaver")
        self.geometry("900x600")
        self.minsize(800, 600)

        self.create_menu()
        self.create_widgets()
        self.configure_grid()

    def create_menu(self):
        self.menu_bar = tk.Menu(self)

        file_menu = tk.Menu(self.menu_bar, tearoff=0)
        file_menu.add_command(label="Open", command=self.select_file)
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=self.quit)
        self.menu_bar.add_cascade(label="File", menu=file_menu)

        options_menu = tk.Menu(self.menu_bar, tearoff=0)
        options_menu.add_command(label="Performance", command=self.cores_affinity)
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