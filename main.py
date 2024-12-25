import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import json
import os


class ModernTheme:
    BG_COLOR = "#f0f2f5"
    FRAME_BG = "#ffffff"
    ACCENT = "#1a73e8"
    TEXT = "#202124"
    SUCCESS = "#34a853"
    ERROR = "#ea4335"
    WARNING = "#fbbc05"


class EmailGenerator:
    def __init__(self, root):
        self.root = root
        self.root.title("Email Generator")
        self.root.configure(bg=ModernTheme.BG_COLOR)
        self.hosts = ["gmail.com", "yahoo.com", "hotmail.com"]
        self.load_hosts()
        self.setup_styles()
        self.setup_ui()

    def setup_styles(self):
        style = ttk.Style()
        style.configure('Modern.TLabelframe', background=ModernTheme.FRAME_BG)
        style.configure('Modern.TLabelframe.Label',
                        background=ModernTheme.FRAME_BG,
                        foreground=ModernTheme.TEXT,
                        font=('Segoe UI', 10, 'bold'))

        style.configure('Modern.TButton',
                        background=ModernTheme.ACCENT,
                        foreground='white',
                        padding=10)

        style.configure('Status.TLabel',
                        background=ModernTheme.FRAME_BG,
                        font=('Segoe UI', 9))

        style.configure('Header.TLabel',
                        background=ModernTheme.FRAME_BG,
                        foreground=ModernTheme.TEXT,
                        font=('Segoe UI', 9, 'bold'))

    def setup_ui(self):
        padding = {'padx': 15, 'pady': 10}

        # Main container
        main_frame = ttk.Frame(self.root, style='Modern.TFrame')
        main_frame.grid(row=0, column=0, **padding)

        # File management frame
        file_frame = ttk.LabelFrame(main_frame, text=" File Operations ", style='Modern.TLabelframe')
        file_frame.grid(row=0, column=0, **padding, sticky="ew")

        upload_btn = ttk.Button(file_frame, text="📁 Upload Names", command=self.upload_file)
        upload_btn.grid(row=0, column=0, **padding)

        generate_btn = ttk.Button(file_frame, text="✉️ Generate Emails", command=self.generate_emails)
        generate_btn.grid(row=0, column=1, **padding)

        # Host management frame
        host_frame = ttk.LabelFrame(main_frame, text=" Host Management ", style='Modern.TLabelframe')
        host_frame.grid(row=1, column=0, **padding, sticky="ew")

        # Add host section
        add_frame = ttk.Frame(host_frame)
        add_frame.grid(row=0, column=0, **padding)

        ttk.Label(add_frame, text="New Host:", style='Header.TLabel').grid(row=0, column=0, padx=5)
        self.host_var = tk.StringVar()
        entry = ttk.Entry(add_frame, textvariable=self.host_var, width=30)
        entry.grid(row=0, column=1, padx=5)
        ttk.Button(add_frame, text="➕ Add", command=self.add_host).grid(row=0, column=2, padx=5)

        # Host selection section
        select_frame = ttk.Frame(host_frame)
        select_frame.grid(row=1, column=0, **padding)

        ttk.Label(select_frame, text="Select Host:", style='Header.TLabel').grid(row=0, column=0, padx=5)
        self.selected_host_var = tk.StringVar()
        self.host_dropdown = ttk.Combobox(select_frame, textvariable=self.selected_host_var, width=27)
        self.host_dropdown['values'] = self.hosts
        self.host_dropdown.grid(row=0, column=1, padx=5)

        # Edit section
        edit_frame = ttk.Frame(host_frame)
        edit_frame.grid(row=2, column=0, **padding)

        ttk.Label(edit_frame, text="Edit Host:", style='Header.TLabel').grid(row=0, column=0, padx=5)
        self.edit_host_var = tk.StringVar()
        self.edit_host_entry = ttk.Entry(edit_frame, textvariable=self.edit_host_var, width=30)
        self.edit_host_entry.grid(row=0, column=1, padx=5)

        # Action buttons
        button_frame = ttk.Frame(host_frame)
        button_frame.grid(row=3, column=0, **padding)

        ttk.Button(button_frame, text="🗑️ Delete", command=self.delete_host).grid(row=0, column=0, padx=5)
        ttk.Button(button_frame, text="✏️ Edit", command=self.edit_host).grid(row=0, column=1, padx=5)
        ttk.Button(button_frame, text="📋 Show All", command=self.show_hosts).grid(row=0, column=2, padx=5)

        # Status frame with modern look
        status_frame = ttk.LabelFrame(main_frame, text=" Status ", style='Modern.TLabelframe')
        status_frame.grid(row=4, column=0, **padding, sticky="ew")

        self.status_var = tk.StringVar(value="Ready to start...")
        self.status_label = ttk.Label(status_frame, textvariable=self.status_var,
                                      style='Status.TLabel', wraplength=400)
        self.status_label.grid(row=0, column=0, **padding)

    def update_status(self, message, status_type="info"):
        color_map = {
            "success": ModernTheme.SUCCESS,
            "error": ModernTheme.ERROR,
            "warning": ModernTheme.WARNING,
            "info": ModernTheme.TEXT
        }
        self.status_label.configure(foreground=color_map.get(status_type, ModernTheme.TEXT))
        self.status_var.set(message)

    # [Previous methods remain the same, just update status calls]
    def load_hosts(self):
        try:
            if os.path.exists('hosts.json'):
                with open('hosts.json', 'r') as f:
                    self.hosts = json.load(f)
        except Exception as e:
            self.hosts = ["gmail.com", "yahoo.com", "hotmail.com"]
            self.update_status("Failed to load hosts, using defaults", "warning")

    def save_hosts(self):
        try:
            with open('hosts.json', 'w') as f:
                json.dump(self.hosts, f)
        except Exception as e:
            self.update_status(f"Error saving hosts: {str(e)}", "error")

    def upload_file(self):
        self.filename = filedialog.askopenfilename(filetypes=[("Text Files", "*.txt")])
        if self.filename:
            self.update_status(f"File loaded: {os.path.basename(self.filename)}", "success")

    def generate_email_combinations(self, first_name, last_name, host):
        return [
            f"{first_name}.{last_name}@{host}",
            f"{last_name}.{first_name}@{host}",
            f"{first_name}{last_name}@{host}",
            f"{first_name[0]}{last_name}@{host}",
            f"{first_name}{last_name[0]}@{host}"
        ]

    def generate_emails(self):
        if not hasattr(self, 'filename'):
            self.update_status("Please upload a names file first", "warning")
            return

        try:
            with open(self.filename, 'r') as f:
                names = f.readlines()

            all_emails = []
            for name in names:
                if ':' not in name:
                    continue
                first_name, last_name = name.strip().split(':')
                for host in self.hosts:
                    all_emails.extend(self.generate_email_combinations(
                        first_name.lower(), last_name.lower(), host))

            save_path = filedialog.asksaveasfilename(
                defaultextension=".txt",
                filetypes=[("Text Files", "*.txt")]
            )

            if save_path:
                with open(save_path, 'w') as f:
                    f.write('\n'.join(all_emails))
                self.update_status(f"✅ Emails saved successfully to: {os.path.basename(save_path)}", "success")
        except Exception as e:
            self.update_status(f"❌ Error: {str(e)}", "error")

    def update_host_dropdown(self):
        self.host_dropdown['values'] = self.hosts

    def add_host(self):
        host = self.host_var.get().strip()
        if host and host not in self.hosts:
            self.hosts.append(host)
            self.save_hosts()
            self.update_host_dropdown()
            self.update_status(f"✅ Added host: {host}", "success")
            self.host_var.set("")
        else:
            self.update_status("❌ Invalid host or already exists", "error")

    def delete_host(self):
        host = self.selected_host_var.get()
        if host in self.hosts:
            self.hosts.remove(host)
            self.save_hosts()
            self.update_host_dropdown()
            self.update_status(f"✅ Deleted host: {host}", "success")
            self.selected_host_var.set("")
        else:
            self.update_status("⚠️ Please select a host to delete", "warning")

    def edit_host(self):
        old_host = self.selected_host_var.get()
        new_host = self.edit_host_var.get().strip()

        if old_host and new_host:
            if old_host in self.hosts:
                index = self.hosts.index(old_host)
                self.hosts[index] = new_host
                self.save_hosts()
                self.update_host_dropdown()
                self.update_status(f"✅ Host updated: {old_host} → {new_host}", "success")
                self.edit_host_var.set("")
            else:
                self.update_status("❌ Selected host not found", "error")
        else:
            self.update_status("⚠️ Please select a host and enter a new name", "warning")

    def show_hosts(self):
        if self.hosts:
            hosts_text = "\n".join([f"• {host}" for host in self.hosts])
            messagebox.showinfo("Current Hosts", hosts_text)
        else:
            messagebox.showwarning("No Hosts", "No email hosts are currently configured.")


if __name__ == "__main__":
    root = tk.Tk()
    app = EmailGenerator(root)
    root.mainloop()