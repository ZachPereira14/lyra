import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import os
from lyra.core import process_dfs
from lyra.plot import plot_lightcurve

class LyraGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Lyra Plot Generator")

        # Variables
        self.file_entries = []  # To store file entry widgets dynamically
        self.label_entries = []  # To store label entry widgets dynamically
        self.data_set_counter = 0  # Counter for data set numbering

        # Default values for plot parameters
        self.figsize_var = tk.StringVar(value="(10, 6)")
        self.invert_yaxis_var = tk.BooleanVar(value=True)
        self.ylabel_var = tk.StringVar(value="Magnitude (V)")
        self.xlabel_var = tk.StringVar(value="Phase")
        self.title_var = tk.StringVar(value="Partial Lightcurve")
        self.xlim_var = tk.StringVar(value="(0.0, 1.0)")
        self.grid_var = tk.BooleanVar(value=True)
        self.error_bars_var = tk.BooleanVar(value=False)

        self.period_var = tk.DoubleVar()
        self.clean_var = tk.BooleanVar(value=False)

        self.label_header_added = False  # Flag to track if label header has been added

        # Create widgets
        label_files = ttk.Label(self.root, text="Files (comma-separated):")
        self.entry_files = ttk.Entry(self.root, width=50)
        self.entry_files.bind("<Return>", self.add_from_entry)  # Bind Return key press
        button_browse = ttk.Button(self.root, text="Browse", command=self.browse_files)

        label_period = ttk.Label(self.root, text="Period:")
        entry_period = ttk.Entry(self.root, textvariable=self.period_var)

        check_clean = ttk.Checkbutton(self.root, text="Clean data", variable=self.clean_var)

        label_title = ttk.Label(self.root, text="Title:")
        entry_title = ttk.Entry(self.root, textvariable=self.title_var)

        label_figsize = ttk.Label(self.root, text="Figsize:")
        entry_figsize = ttk.Entry(self.root, textvariable=self.figsize_var)

        check_invert_yaxis = ttk.Checkbutton(self.root, text="Invert Y-axis", variable=self.invert_yaxis_var)

        label_ylabel = ttk.Label(self.root, text="Y-label:")
        entry_ylabel = ttk.Entry(self.root, textvariable=self.ylabel_var)

        label_xlabel = ttk.Label(self.root, text="X-label:")
        entry_xlabel = ttk.Entry(self.root, textvariable=self.xlabel_var)

        label_xlim = ttk.Label(self.root, text="X-lim:")
        entry_xlim = ttk.Entry(self.root, textvariable=self.xlim_var)

        check_grid = ttk.Checkbutton(self.root, text="Grid", variable=self.grid_var)

        check_error_bars = ttk.Checkbutton(self.root, text="Error Bars", variable=self.error_bars_var)

        button_plot = ttk.Button(self.root, text="Plot", command=self.plot)

        # Layout widgets using grid
        label_files.grid(row=0, column=0, padx=5, pady=5, sticky="w")
        self.entry_files.grid(row=0, column=1, padx=5, pady=5, sticky="ew")
        button_browse.grid(row=0, column=2, padx=5, pady=5, sticky="e")

        label_period.grid(row=1, column=0, padx=5, pady=5, sticky="w")
        entry_period.grid(row=1, column=1, padx=5, pady=5, sticky="ew")

        check_clean.grid(row=2, column=1, padx=5, pady=5, sticky="w")

        label_title.grid(row=3, column=0, padx=5, pady=5, sticky="w")
        entry_title.grid(row=3, column=1, padx=5, pady=5, sticky="ew")

        label_figsize.grid(row=0, column=3, padx=5, pady=5, sticky="w")
        entry_figsize.grid(row=0, column=4, padx=5, pady=5, sticky="ew")

        check_invert_yaxis.grid(row=1, column=4, padx=5, pady=5, sticky="w")

        label_ylabel.grid(row=2, column=3, padx=5, pady=5, sticky="w")
        entry_ylabel.grid(row=2, column=4, padx=5, pady=5, sticky="ew")

        label_xlabel.grid(row=3, column=3, padx=5, pady=5, sticky="w")
        entry_xlabel.grid(row=3, column=4, padx=5, pady=5, sticky="ew")

        label_xlim.grid(row=4, column=3, padx=5, pady=5, sticky="w")
        entry_xlim.grid(row=4, column=4, padx=5, pady=5, sticky="ew")

        check_grid.grid(row=5, column=4, padx=5, pady=5, sticky="w")

        check_error_bars.grid(row=6, column=4, padx=5, pady=5, sticky="w")

        button_plot.grid(row=7, column=4, padx=5, pady=10, sticky="se")  # Place button in bottom right corner

        # Resize behavior
        self.root.columnconfigure(1, weight=1)

    def browse_files(self):
            file_paths = filedialog.askopenfilenames(
                filetypes=[
                    ("All files", "*.*"),
                    ("CSV files", "*.csv"),
                    ("Excel files", "*.xlsx;*.xls"),
                    ("Table files", "*.tbl")
                ]
            )
            if file_paths:
                for file_path in file_paths:
                    self.add_file_entry(file_path)

    def add_file_entry(self, file_path):
        self.data_set_counter += 1

        # Add label header if it's the first data set
        if not self.label_header_added:
            label_header = ttk.Label(self.root, text="Data Label")
            label_header.grid(row=8, column=3, padx=5, pady=2, sticky="n")  # Centered with reduced pady
            self.label_header_added = True

        # Add label for data set
        label_data_set = ttk.Label(self.root, text=f"Data Set {self.data_set_counter}:")
        label_data_set.grid(row=len(self.file_entries) + 9, column=3, padx=5, pady=5, sticky="w")

        file_entry = ttk.Entry(self.root, width=50)
        file_entry.insert(tk.END, file_path)
        file_entry.grid(row=len(self.file_entries) + 9, column=4, padx=5, pady=5, sticky="ew")  # Adjust the starting row
        self.file_entries.append(file_entry)

        label_entry = ttk.Entry(self.root, width=20)
        label_entry.grid(row=len(self.label_entries) + 9, column=5, padx=5, pady=5, sticky="ew")  # Adjust the starting row
        self.label_entries.append(label_entry)

    def add_from_entry(self, event):
        # Function to add entries when Enter is pressed in the entry_files field
        file_paths = self.entry_files.get()
        if file_paths:
            files = file_paths.split(",")
            for file_path in files:
                file_path = file_path.strip()
                if not os.path.isfile(file_path):
                    messagebox.showerror("Error", f"Invalid file path: {file_path}")
                    return

                self.add_file_entry(file_path)

            self.entry_files.delete(0, tk.END)  # Clear the entry after adding

            # Add an empty set of entries below for further input
            self.add_file_entry("")

    def plot(self):
        period = self.period_var.get()
        if period == 0:
            messagebox.showerror("Error", "Period cannot be zero.")
            return

        dataframes = []
        for idx, file_entry in enumerate(self.file_entries):
            file_path = file_entry.get().strip()
            label_entry = self.label_entries[idx].get().strip()
            if file_path:
                dataframes.append((file_path, label_entry))

        clean = self.clean_var.get()
        title = self.title_var.get()

        figsize = eval(self.figsize_var.get())
        invert_yaxis = self.invert_yaxis_var.get()
        ylabel = self.ylabel_var.get()
        xlabel = self.xlabel_var.get()
        xlim = eval(self.xlim_var.get())
        grid = self.grid_var.get()
        error_bars = self.error_bars_var.get()

        if dataframes:
            processed_data = process_dfs(dataframes, period, clean=clean)
            plot_lightcurve(processed_data, figsize=figsize, invert_yaxis=invert_yaxis,
                            ylabel=ylabel, xlabel=xlabel, title=title,
                            xlim=xlim, grid=grid, error_bars=error_bars)

if __name__ == "__main__":
    root = tk.Tk()
    app = LyraGUI(root)
    root.mainloop()

