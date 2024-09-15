import os
import subprocess
import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import webbrowser
from PIL import Image, ImageTk

class CompilerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Python to EXE Compiler")
        self.root.geometry("800x350")
        self.root.configure(bg='#f0f0f0')

        self.py_file = ""
        self.icon_file = ""
        self.output_folder = ""
        self.include_icon = tk.BooleanVar()
        self.use_custom_output = tk.BooleanVar()
        self.force_top = tk.BooleanVar(value=True)
        self.show_logo = tk.BooleanVar(value=True)

        self.create_widgets()
        self.create_menu()
        self.load_image()
        self.apply_settings()

    def create_widgets(self):
        style = ttk.Style()
        style.configure('TLabel', background='#f0f0f0', font=('Arial', 10))
        style.configure('TButton', padding=6, relief='flat', background='#000000', foreground='black', font=('Arial', 10))
        style.map('TButton', background=[('pressed', '#333333'), ('active', '#444444')])
        style.configure('TEntry', padding=5, relief='flat')

        ttk.Label(self.root, text="Python File:").grid(row=0, column=0, padx=15, pady=10, sticky='w')
        self.py_file_entry = ttk.Entry(self.root, width=70)
        self.py_file_entry.grid(row=0, column=1, padx=15, pady=10)
        ttk.Button(self.root, text="Browse", command=self.select_py_file).grid(row=0, column=2, padx=15, pady=10)

        ttk.Label(self.root, text="Include Icon:").grid(row=1, column=0, padx=15, pady=10, sticky='w')
        ttk.Checkbutton(self.root, variable=self.include_icon, command=self.toggle_icon_entry).grid(row=1, column=1, padx=15, pady=10, sticky='w')

        self.icon_file_label = ttk.Label(self.root, text="Icon File:")
        self.icon_file_entry = ttk.Entry(self.root, width=70)
        self.icon_file_button = ttk.Button(self.root, text="Browse", command=self.select_icon_file)

        self.icon_file_label.grid(row=2, column=0, padx=15, pady=10, sticky='w')
        self.icon_file_entry.grid(row=2, column=1, padx=15, pady=10)
        self.icon_file_button.grid(row=2, column=2, padx=15, pady=10)

        ttk.Label(self.root, text="Use Custom Output Folder:").grid(row=3, column=0, padx=15, pady=10, sticky='w')
        ttk.Checkbutton(self.root, variable=self.use_custom_output, command=self.toggle_output_entry).grid(row=3, column=1, padx=15, pady=10, sticky='w')

        self.output_folder_label = ttk.Label(self.root, text="Output Folder:")
        self.output_folder_entry = ttk.Entry(self.root, width=70)
        self.output_folder_button = ttk.Button(self.root, text="Browse", command=self.select_output_folder)

        self.output_folder_label.grid(row=4, column=0, padx=15, pady=10, sticky='w')
        self.output_folder_entry.grid(row=4, column=1, padx=15, pady=10)
        self.output_folder_button.grid(row=4, column=2, padx=15, pady=10)

        ttk.Button(self.root, text="Compile", command=self.compile_to_exe).grid(row=5, column=1, padx=15, pady=20)

        self.toggle_icon_entry()
        self.toggle_output_entry()

    def create_menu(self):
        menu_bar = tk.Menu(self.root)
        self.root.config(menu=menu_bar)

        help_menu = tk.Menu(menu_bar, tearoff=0)
        menu_bar.add_cascade(label="Help", menu=help_menu)
        help_menu.add_command(label="Help", command=self.show_help)

        credits_menu = tk.Menu(menu_bar, tearoff=0)
        menu_bar.add_cascade(label="Credits", menu=credits_menu)
        credits_menu.add_command(label="Credits", command=self.show_credits)

        settings_menu = tk.Menu(menu_bar, tearoff=0)
        menu_bar.add_cascade(label="Settings", menu=settings_menu)
        settings_menu.add_command(label="Settings", command=self.show_settings)

    def get_initial_dir(self):
        return os.path.dirname(os.path.abspath(__file__))

    def select_py_file(self):
        try:
            file_path = filedialog.askopenfilename(
                filetypes=[("Python Files", "*.py")],
                initialdir=self.get_initial_dir(),
                title="Select Python File"
            )
            if file_path:
                self.py_file = file_path
                self.py_file_entry.delete(0, tk.END)
                self.py_file_entry.insert(0, file_path)
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred while selecting the Python file: {e}")

    def select_icon_file(self):
        try:
            file_path = filedialog.askopenfilename(
                filetypes=[("Icon Files", "*.ico")],
                initialdir=self.get_initial_dir(),
                title="Select Icon File"
            )
            if file_path:
                self.icon_file = file_path
                self.icon_file_entry.delete(0, tk.END)
                self.icon_file_entry.insert(0, file_path)
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred while selecting the Icon file: {e}")

    def select_output_folder(self):
        try:
            folder_path = filedialog.askdirectory(
                initialdir=self.get_initial_dir(),
                title="Select Output Folder"
            )
            if folder_path:
                self.output_folder = folder_path
                self.output_folder_entry.delete(0, tk.END)
                self.output_folder_entry.insert(0, folder_path)
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred while selecting the Output folder: {e}")

    def toggle_icon_entry(self):
        if self.include_icon.get():
            self.icon_file_label.grid()
            self.icon_file_entry.grid()
            self.icon_file_button.grid()
        else:
            self.icon_file_label.grid_remove()
            self.icon_file_entry.grid_remove()
            self.icon_file_button.grid_remove()

    def toggle_output_entry(self):
        if self.use_custom_output.get():
            self.output_folder_label.grid()
            self.output_folder_entry.grid()
            self.output_folder_button.grid()
        else:
            self.output_folder_label.grid_remove()
            self.output_folder_entry.grid_remove()
            self.output_folder_button.grid_remove()
            self.output_folder = ""

    def compile_to_exe(self):
        if not self.py_file:
            messagebox.showerror("Error", "Please select a Python file.")
            return

        command = ['pyinstaller', '--onefile']
        
        if self.include_icon.get() and self.icon_file:
            command.extend(['--icon', self.icon_file])
        
        command.append(self.py_file)

        if self.use_custom_output.get() and self.output_folder:
            command.extend(['--distpath', self.output_folder])
        else:
            command.extend(['--distpath', os.path.dirname(self.py_file)])

        try:
            subprocess.run(command, check=True)
            self.cleanup_files()
            messagebox.showinfo("Success", "Compilation complete! Check the output folder.")
        except subprocess.CalledProcessError as e:
            messagebox.showerror("Error", f"Error occurred during compilation: {e}")
        except Exception as e:
            messagebox.showerror("Error", f"An unexpected error occurred: {e}")

    def cleanup_files(self):
        try:
            build_path = os.path.join(os.path.dirname(self.py_file), 'build')
            spec_file = os.path.join(os.path.dirname(self.py_file), f'{os.path.basename(self.py_file).replace(".py", ".spec")}')
            
            if os.path.exists(build_path):
                subprocess.run(['rmdir', '/S', '/Q', build_path], shell=True)
            
            if os.path.exists(spec_file):
                os.remove(spec_file)

            for folder in ['__pycache__', 'dist']:
                folder_path = os.path.join(os.path.dirname(self.py_file), folder)
                if os.path.exists(folder_path):
                    subprocess.run(['rmdir', '/S', '/Q', folder_path], shell=True)
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred during cleanup: {e}")

    def show_help(self):
        help_text = (
            "Q: How do I add an icon?\n"
            "A: Get a .ico file (ex. icon.ico) and select the 'Include Icon:' box.\n\n"
            "Q: How do I use a custom output folder?\n"
            "A: Select the box, then select your output folder for the exe.\n\n"
            "Q: Does this only work for Python?\n"
            "A: Yes, this is a Python compiler."
        )
        messagebox.showinfo("Help", help_text)

    def show_credits(self):
        credits_window = tk.Toplevel(self.root)
        credits_window.title("Credits")
        credits_window.geometry("300x150")

        link_label = ttk.Label(credits_window, text="https://github.com/o5e1", foreground="blue", cursor="hand2")
        link_label.pack(padx=10, pady=10)
        link_label.bind("<Button-1>", lambda e: webbrowser.open("https://github.com/o5e1"))

    def show_settings(self):
        settings_window = tk.Toplevel(self.root)
        settings_window.title("Settings")
        settings_window.geometry("300x150")

        force_top_checkbutton = ttk.Checkbutton(
            settings_window, 
            text="Force Top",
            variable=self.force_top,
            command=self.toggle_force_top
        )
        force_top_checkbutton.pack(padx=10, pady=10)

        show_logo_checkbutton = ttk.Checkbutton(
            settings_window, 
            text="Show Logo",
            variable=self.show_logo,
            command=self.toggle_logo
        )
        show_logo_checkbutton.pack(padx=10, pady=10)

    def toggle_force_top(self):
        if self.force_top.get():
            self.root.wm_attributes("-topmost", 1)
        else:
            self.root.wm_attributes("-topmost", 0)

    def toggle_logo(self):
        if self.show_logo.get():
            self.load_image()
        else:
            if hasattr(self, 'img_label'):
                self.img_label.grid_remove()

    def load_image(self):
        try:
            img_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'files', 'picture.png')
            img = Image.open(img_path)
            img = img.resize((100, 100), Image.LANCZOS)
            self.img_tk = ImageTk.PhotoImage(img)
            if hasattr(self, 'img_label'):
                self.img_label.grid_remove()
            self.img_label = tk.Label(self.root, image=self.img_tk, bg='#f0f0f0')
            self.img_label.image = self.img_tk
            self.img_label.place(x=750, y=330, anchor='se')
        except Exception as e:
            print(f"Error loading image: {e}")

    def apply_settings(self):
        self.toggle_force_top()
        self.toggle_logo()

if __name__ == "__main__":
    root = tk.Tk()
    app = CompilerApp(root)
    root.mainloop()
