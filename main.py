import customtkinter as ctk
from tkinter import filedialog, messagebox
import json
import os


class ModernEmailGenerator:
    def __init__(self, root):
        self.root = root
        self.root.title("📨 Modern Email Generator Pro")
        self.root.geometry("400x650")
        self.root.resizable(False, False)

        # Set theme
        ctk.set_appearance_mode("System")  # Modes: System, Light, Dark
        ctk.set_default_color_theme("blue")

        self.hosts = ["gmail.com", "yahoo.com", "hotmail.com"]
        self.load_hosts()

        # UI Setup
        self.setup_ui()

    def setup_ui(self):
        # Main Frame
        self.main_frame = ctk.CTkFrame(self.root, corner_radius=15)
        self.main_frame.pack(padx=20, pady=20, fill="both", expand=True)

        # Title Section
        self.title_label = ctk.CTkLabel(self.main_frame, text="Email Generator Pro",
                                        font=("Segoe UI", 24, "bold"))
        self.title_label.pack(pady=10)

        self.subtitle_label = ctk.CTkLabel(self.main_frame,
                                           text="Generate professional email combinations easily",
                                           font=("Segoe UI", 14))
        self.subtitle_label.pack(pady=5)

        # File Operations
        self.file_frame = ctk.CTkFrame(self.main_frame, corner_radius=10)
        self.file_frame.pack(pady=20, fill="x")

        self.file_label = ctk.CTkLabel(self.file_frame,
                                       text="Upload a text file with names (first_name:last_name)",
                                       font=("Segoe UI", 12))
        self.file_label.pack(pady=10)

        self.upload_button = ctk.CTkButton(self.file_frame, text="Upload Names File",
                                           command=self.upload_file, width=200)
        self.upload_button.pack(pady=5)

        self.generate_button = ctk.CTkButton(self.file_frame, text="Generate Emails",
                                             command=self.generate_emails, width=200)
        self.generate_button.pack(pady=5)

        # Host Management
        self.host_frame = ctk.CTkFrame(self.main_frame, corner_radius=10)
        self.host_frame.pack(pady=20, fill="x")

        self.host_label = ctk.CTkLabel(self.host_frame, text="Manage Hosts", font=("Segoe UI", 14, "bold"))
        self.host_label.pack(pady=10)

        self.host_entry = ctk.CTkEntry(self.host_frame, placeholder_text="Add New Host")
        self.host_entry.pack(pady=5)

        self.add_host_button = ctk.CTkButton(self.host_frame, text="Add Host",
                                             command=self.add_host, width=150)
        self.add_host_button.pack(pady=5)

        self.hosts_dropdown = ctk.CTkOptionMenu(self.host_frame, values=self.hosts)
        self.hosts_dropdown.pack(pady=5)

        self.delete_host_button = ctk.CTkButton(self.host_frame, text="Delete Selected Host",
                                                command=self.delete_host, width=200)
        self.delete_host_button.pack(pady=5)

        # Status Section
        self.status_frame = ctk.CTkFrame(self.main_frame, corner_radius=10)
        self.status_frame.pack(pady=20, fill="x")

        self.status_label = ctk.CTkLabel(self.status_frame, text="Ready to start...",
                                         font=("Segoe UI", 12))
        self.status_label.pack(pady=10)

    def update_status(self, message, status_type="info"):
        color_map = {
            "success": "green",
            "error": "red",
            "warning": "orange",
            "info": "blue"
        }
        self.status_label.configure(text=message, text_color=color_map.get(status_type, "blue"))

    def load_hosts(self):
        try:
            if os.path.exists('hosts.json'):
                with open('hosts.json', 'r') as f:
                    self.hosts = json.load(f)
        except Exception:
            self.hosts = ["gmail.com", "yahoo.com", "hotmail.com"]
            self.update_status("Failed to load hosts. Using defaults.", "warning")

    def save_hosts(self):
        try:
            with open('hosts.json', 'w') as f:
                json.dump(self.hosts, f)
        except Exception as e:
            self.update_status(f"Error saving hosts: {str(e)}", "error")

    def upload_file(self):
        self.filename = filedialog.askopenfilename(
            title="Select Names File",
            filetypes=[("Text Files", "*.txt")]
        )
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
            self.update_status("Please upload a names file first.", "warning")
            return

        try:
            with open(self.filename, 'r') as f:
                names = f.readlines()

            if not names:
                self.update_status("The file is empty.", "warning")
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
                self.update_status(f"Warning: Invalid format in lines: {', '.join(invalid_lines)}", "warning")

            output_file = "generated_emails.txt"
            with open(output_file, 'w') as f:
                f.write("\n".join(all_emails))

            self.update_status(f"Generated {len(all_emails)} emails. Saved to {output_file}.", "success")

        except Exception as e:
            self.update_status(f"Error: {str(e)}", "error")

    def add_host(self):
        new_host = self.host_entry.get().strip()
        if not new_host:
            self.update_status("Please enter a host name.", "warning")
            return

        if new_host in self.hosts:
            self.update_status("This host already exists.", "error")
            return

        self.hosts.append(new_host)
        self.save_hosts()
        self.hosts_dropdown.configure(values=self.hosts)
        self.update_status(f"Added host: {new_host}", "success")
        self.host_entry.delete(0, ctk.END)

    def delete_host(self):
        selected_host = self.hosts_dropdown.get()
        if selected_host not in self.hosts:
            self.update_status("Please select a valid host to delete.", "warning")
            return

        self.hosts.remove(selected_host)
        self.save_hosts()
        self.hosts_dropdown.configure(values=self.hosts)
        self.update_status(f"Deleted host: {selected_host}", "success")


def main():
    root = ctk.CTk()
    app = ModernEmailGenerator(root)
    root.mainloop()


if __name__ == "__main__":
    main()
