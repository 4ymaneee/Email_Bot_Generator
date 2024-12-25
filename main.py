import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import json
import os


class ModernTheme:
    BG_COLOR = "#6EACDA"
    FRAME_BG = "#6EACDA"
    PRIMARY = "#000000"
    SECONDARY = "#000000"
    SUCCESS = "#6ab04c"
    WARNING = "#f9ca24"
    ERROR = "#eb4d4b"
    INFO = "#30336b"
    TEXT_PRIMARY = "#000000"
    TEXT_SECONDARY = "#000000"
    TEXT_LIGHT = "#000000"


class EmailGenerator:
    def __init__(self, root):
        self.root = root
        self.root.title("✉️ Modern Email Generator")
        self.root.geometry("420x640")
        self.root.resizable(False, False)
        self.root.configure(bg=ModernTheme.BG_COLOR)
        self.hosts = ["gmail.com", "yahoo.com", "hotmail.com"]
        self.load_hosts()
        self.setup_styles()
        self.setup_ui()

    def setup_styles(self):
        style = ttk.Style()

        style.configure('Modern.TFrame', background=ModernTheme.BG_COLOR)
        style.configure('Card.TFrame', background=ModernTheme.FRAME_BG,
                        relief='raised', borderwidth=1)

        style.configure('Modern.TLabelframe',
                        background=ModernTheme.FRAME_BG,
                        relief='solid',
                        borderwidth=1)
        style.configure('Modern.TLabelframe.Label',
                        background=ModernTheme.FRAME_BG,
                        foreground=ModernTheme.PRIMARY,
                        font=('Segoe UI', 11, 'bold'))

        style.configure('Primary.TButton',
                        background=ModernTheme.PRIMARY,
                        foreground=ModernTheme.TEXT_LIGHT,
                        font=('Segoe UI', 10),
                        padding=10)
        style.configure('Secondary.TButton',
                        background=ModernTheme.SECONDARY,
                        font=('Segoe UI', 9),
                        padding=8)

        style.configure('Header.TLabel',
                        background=ModernTheme.FRAME_BG,
                        foreground=ModernTheme.TEXT_PRIMARY,
                        font=('Segoe UI', 10, 'bold'))
        style.configure('Info.TLabel',
                        background=ModernTheme.FRAME_BG,
                        foreground=ModernTheme.TEXT_SECONDARY,
                        font=('Segoe UI', 9))

        style.configure('Modern.TEntry',
                        fieldbackground=ModernTheme.BG_COLOR,
                        padding=5)

    def setup_ui(self):
        main_frame = ttk.Frame(self.root, style='Modern.TFrame')
        main_frame.pack(expand=True, fill='both', padx=20, pady=20)

        # Title section
        title_frame = ttk.Frame(main_frame, style='Card.TFrame')
        title_frame.pack(fill='x', pady=(0, 20), ipady=10)

        title_label = ttk.Label(title_frame,
                                text="Email Generator Pro",
                                font=('Segoe UI', 16, 'bold'),
                                foreground=ModernTheme.PRIMARY,
                                background=ModernTheme.FRAME_BG)
        title_label.pack()

        subtitle_label = ttk.Label(title_frame,
                                   text="Generate professional email combinations easily",
                                   font=('Segoe UI', 9),
                                   foreground=ModernTheme.TEXT_SECONDARY,
                                   background=ModernTheme.FRAME_BG)
        subtitle_label.pack()

        # File section
        file_frame = ttk.LabelFrame(main_frame, text=" 📁 File Operations ", style='Modern.TLabelframe')
        file_frame.pack(fill='x', pady=(0, 20), ipady=10)

        file_info = ttk.Label(file_frame,
                              text="Upload a text file with names in format: first_name:last_name",
                              style='Info.TLabel')
        file_info.pack(pady=(5, 0))

        button_frame = ttk.Frame(file_frame, style='Modern.TFrame')
        button_frame.pack(pady=10)

        ttk.Button(button_frame, text="Upload Names File",
                   style='Primary.TButton', command=self.upload_file).pack(side='left', padx=5)
        ttk.Button(button_frame, text="Generate Emails",
                   style='Primary.TButton', command=self.generate_emails).pack(side='left', padx=5)

        # Host Management section
        host_frame = ttk.LabelFrame(main_frame, text=" 🔧 Host Management ", style='Modern.TLabelframe')
        host_frame.pack(fill='x', pady=(0, 20), ipady=10)

        # Add host section
        add_frame = ttk.Frame(host_frame, style='Modern.TFrame')
        add_frame.pack(fill='x', padx=15, pady=10)

        ttk.Label(add_frame, text="Add New Host:",
                  style='Header.TLabel').pack(side='left', padx=(0, 10))

        self.host_var = tk.StringVar()
        ttk.Entry(add_frame, textvariable=self.host_var,
                  style='Modern.TEntry', width=30).pack(side='left', padx=(0, 10))

        ttk.Button(add_frame, text="Add Host",
                   style='Secondary.TButton', command=self.add_host).pack(side='left')

        # Host selection section
        select_frame = ttk.Frame(host_frame, style='Modern.TFrame')
        select_frame.pack(fill='x', padx=15, pady=10)

        ttk.Label(select_frame, text="Select Host:",
                  style='Header.TLabel').pack(side='left', padx=(0, 10))

        self.selected_host_var = tk.StringVar()
        self.host_dropdown = ttk.Combobox(select_frame, textvariable=self.selected_host_var,
                                          width=27, state='readonly')
        self.host_dropdown['values'] = self.hosts
        self.host_dropdown.pack(side='left')

        # Edit section
        edit_frame = ttk.Frame(host_frame, style='Modern.TFrame')
        edit_frame.pack(fill='x', padx=15, pady=10)

        ttk.Label(edit_frame, text="New Host Name:",
                  style='Header.TLabel').pack(side='left', padx=(0, 10))

        self.edit_host_var = tk.StringVar()
        ttk.Entry(edit_frame, textvariable=self.edit_host_var,
                  style='Modern.TEntry', width=30).pack(side='left')

        # Action buttons
        button_frame = ttk.Frame(host_frame, style='Modern.TFrame')
        button_frame.pack(pady=10)

        buttons = [
            ("🗑️ Delete Host", self.delete_host),
            ("✏️ Edit Host", self.edit_host),
            ("📋 Show All Hosts", self.show_hosts)
        ]

        for text, command in buttons:
            ttk.Button(button_frame, text=text,
                       style='Secondary.TButton',
                       command=command).pack(side='left', padx=5)

        # Status section
        status_frame = ttk.LabelFrame(main_frame, text=" 📊 Status ", style='Modern.TLabelframe')
        status_frame.pack(fill='x', pady=(0, 20), ipady=10)

        self.status_var = tk.StringVar(value="Ready to start...")
        self.status_label = ttk.Label(status_frame, textvariable=self.status_var,
                                      style='Info.TLabel', wraplength=500)
        self.status_label.pack(pady=10)

    def update_status(self, message, status_type="info"):
        color_map = {
            "success": ModernTheme.SUCCESS,
            "error": ModernTheme.ERROR,
            "warning": ModernTheme.WARNING,
            "info": ModernTheme.TEXT_SECONDARY
        }
        self.status_label.configure(foreground=color_map.get(status_type, ModernTheme.TEXT_SECONDARY))
        self.status_var.set(message)

    def load_hosts(self):
        try:
            if os.path.exists('hosts.json'):
                with open('hosts.json', 'r') as f:
                    self.hosts = json.load(f)
        except Exception as e:
            self.hosts = ["gmail.com", "yahoo.com", "hotmail.com"]
            self.update_status("⚠️ Failed to load hosts, using defaults", "warning")

    def save_hosts(self):
        try:
            with open('hosts.json', 'w') as f:
                json.dump(self.hosts, f)
        except Exception as e:
            self.update_status(f"❌ Error saving hosts: {str(e)}", "error")

    def upload_file(self):
        self.filename = filedialog.askopenfilename(
            title="Select Names File",
            filetypes=[("Text Files", "*.txt")]
        )
        if self.filename:
            self.update_status(f"✅ File loaded: {os.path.basename(self.filename)}", "success")

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
            self.update_status("⚠️ Please upload a names file first", "warning")
            return

        try:
            with open(self.filename, 'r') as f:
                names = f.readlines()

            if not names:
                self.update_status("⚠️ The file is empty", "warning")
                return

            all_emails = []
            invalid_lines = []

            for line_num, name in enumerate(names, 1):
                name = name.strip()
                if ':' not in name:
                    invalid_lines.append(str(line_num))
                    continue

                first_name, last_name = name.split(':')
                if not first_name or not last_name:
                    invalid_lines.append(str(line_num))
                    continue

                for host in self.hosts:
                    all_emails.extend(self.generate_email_combinations(
                        first_name.lower(), last_name.lower(), host))

            if invalid_lines:
                self.update_status(
                    f"⚠️ Warning: Invalid format in lines: {', '.join(invalid_lines)}",
                    "warning"
                )

            if all_emails:
                save_path = filedialog.asksaveasfilename(
                    title="Save Generated Emails",
                    defaultextension=".txt",
                    filetypes=[("Text Files", "*.txt")]
                )

                if save_path:
                    with open(save_path, 'w') as f:
                        f.write('\n'.join(all_emails))
                    self.update_status(
                        f"✅ Generated {len(all_emails)} emails and saved to: {os.path.basename(save_path)}",
                        "success"
                    )
            else:
                self.update_status("❌ No valid names found to generate emails", "error")

        except Exception as e:
            self.update_status(f"❌ Error: {str(e)}", "error")

    def update_host_dropdown(self):
        self.host_dropdown['values'] = self.hosts
        if self.hosts:
            self.host_dropdown.set(self.hosts[0])

    def add_host(self):
        host = self.host_var.get().strip()
        if not host:
            self.update_status("⚠️ Please enter a host name", "warning")
            return

        if host in self.hosts:
            self.update_status("❌ This host already exists", "error")
            return

        if '@' in host or ' ' in host:
            self.update_status("❌ Invalid host format", "error")
            return

        self.hosts.append(host)
        self.save_hosts()
        self.update_host_dropdown()
        self.update_status(f"✅ Added host: {host}", "success")
        self.host_var.set("")

    def delete_host(self):
        host = self.selected_host_var.get()
        if not host:
            self.update_status("⚠️ Please select a host to delete", "warning")
            return

        if len(self.hosts) <= 1:
            self.update_status("❌ Cannot delete the last host", "error")
            return

        self.hosts.remove(host)
        self.save_hosts()
        self.update_host_dropdown()
        self.update_status(f"✅ Deleted host: {host}", "success")

    def edit_host(self):
        old_host = self.selected_host_var.get()
        new_host = self.edit_host_var.get().strip()

        if not old_host:
            self.update_status("⚠️ Please select a host to edit", "warning")
            return

        if not new_host:
            self.update_status("⚠️ Please enter a new host name", "warning")
            return

        if '@' in new_host or ' ' in new_host:
            self.update_status("❌ Invalid host format", "error")
            return

        if new_host in self.hosts:
            self.update_status("❌ This host already exists", "error")
            return

        index = self.hosts.index(old_host)
        self.hosts[index] = new_host
        self.save_hosts()
        self.update_host_dropdown()
        self.update_status(f"✅ Host updated: {old_host} → {new_host}", "success")
        self.edit_host_var.set("")

    def show_hosts(self):
        if not self.hosts:
            messagebox.showwarning("No Hosts", "No email hosts are currently configured.")
            return

        hosts_text = "\n".join([f"• {host}" for host in self.hosts])
        messagebox.showinfo(
            "Current Hosts",
            f"Available email hosts:\n\n{hosts_text}"
        )


if __name__ == "__main__":
    root = tk.Tk()
    app = EmailGenerator(root)
    root.mainloop()