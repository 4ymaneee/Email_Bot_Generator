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

        # Language dictionary
        self.languages = {
            "en": {
                "title": "Email Generator Pro",
                "subtitle": "Generate professional email combinations easily",
                "file_label": "Upload a text file with names (first_name:last_name)",
                "upload_button": "Upload Names File",
                "generate_button": "Generate Emails",
                "host_label": "Manage Hosts",
                "add_host_button": "Add Host",
                "delete_host_button": "Delete Selected Host",
                "status_label": "Ready to start...",
                "invalid_file": "Please upload a names file first.",
                "empty_file": "The file is empty.",
                "invalid_format": "Warning: Invalid format in lines: ",
                "generated_emails": "Generated {0} emails. Saved to {1}.",
                "error_saving": "Error saving hosts: {0}",
                "file_loaded": "File loaded: {0}",
                "please_enter_host": "Please enter a host name.",
                "host_exists": "This host already exists.",
                "added_host": "Added host: {0}",
                "deleted_host": "Deleted host: {0}",
            },
            "fr": {
                "title": "Générateur d'email moderne",
                "subtitle": "Générez facilement des combinaisons d'emails professionnels",
                "file_label": "Téléchargez un fichier texte avec les noms (prénom:nom)",
                "upload_button": "Télécharger le fichier des noms",
                "generate_button": "Générer les emails",
                "host_label": "Gérer les hôtes",
                "add_host_button": "Ajouter un hôte",
                "delete_host_button": "Supprimer l'hôte sélectionné",
                "status_label": "Prêt à commencer...",
                "invalid_file": "Veuillez d'abord télécharger un fichier de noms.",
                "empty_file": "Le fichier est vide.",
                "invalid_format": "Avertissement : Format invalide dans les lignes : ",
                "generated_emails": "Généré {0} emails. Sauvegardé dans {1}.",
                "error_saving": "Erreur lors de la sauvegarde des hôtes : {0}",
                "file_loaded": "Fichier chargé : {0}",
                "please_enter_host": "Veuillez entrer un nom d'hôte.",
                "host_exists": "Cet hôte existe déjà.",
                "added_host": "Hôte ajouté : {0}",
                "deleted_host": "Hôte supprimé : {0}",
            }
        }
        self.current_language = "en"

        # UI Setup
        self.setup_ui()

    def setup_ui(self):
        # Clear previous UI elements
        for widget in self.root.winfo_children():
            widget.destroy()

        # Main Frame
        self.main_frame = ctk.CTkFrame(self.root, corner_radius=15)
        self.main_frame.pack(padx=20, pady=20, fill="both", expand=True)

        # Title Section
        self.title_label = ctk.CTkLabel(self.main_frame, text=self.translate("title"), font=("Segoe UI", 24, "bold"))
        self.title_label.pack(pady=10)

        self.subtitle_label = ctk.CTkLabel(self.main_frame, text=self.translate("subtitle"), font=("Segoe UI", 14))
        self.subtitle_label.pack(pady=5)

        # File Operations
        self.file_frame = ctk.CTkFrame(self.main_frame, corner_radius=10)
        self.file_frame.pack(pady=20, fill="x")

        self.file_label = ctk.CTkLabel(self.file_frame, text=self.translate("file_label"), font=("Segoe UI", 12))
        self.file_label.pack(pady=10)

        self.upload_button = ctk.CTkButton(self.file_frame, text=self.translate("upload_button"),
                                           command=self.upload_file, width=200)
        self.upload_button.pack(pady=5)

        self.generate_button = ctk.CTkButton(self.file_frame, text=self.translate("generate_button"),
                                             command=self.generate_emails, width=200)
        self.generate_button.pack(pady=5)

        # Host Management
        self.host_frame = ctk.CTkFrame(self.main_frame, corner_radius=10)
        self.host_frame.pack(pady=20, fill="x")

        self.host_label = ctk.CTkLabel(self.host_frame, text=self.translate("host_label"),
                                       font=("Segoe UI", 14, "bold"))
        self.host_label.pack(pady=10)

        self.host_entry = ctk.CTkEntry(self.host_frame, placeholder_text="Add New Host")
        self.host_entry.pack(pady=5)

        self.add_host_button = ctk.CTkButton(self.host_frame, text=self.translate("add_host_button"),
                                             command=self.add_host, width=150)
        self.add_host_button.pack(pady=5)

        self.hosts_dropdown = ctk.CTkOptionMenu(self.host_frame, values=self.hosts)
        self.hosts_dropdown.pack(pady=5)

        self.delete_host_button = ctk.CTkButton(self.host_frame, text=self.translate("delete_host_button"),
                                                command=self.delete_host, width=200)
        self.delete_host_button.pack(pady=5)

        # Status Section
        self.status_frame = ctk.CTkFrame(self.main_frame, corner_radius=10)
        self.status_frame.pack(pady=20, fill="x")

        self.status_label = ctk.CTkLabel(self.status_frame, text=self.translate("status_label"), font=("Segoe UI", 12))
        self.status_label.pack(pady=10)

        # Language Selection Dropdown at the bottom
        self.language_button = ctk.CTkButton(self.root, text="Choose Language", command=self.toggle_language_dropdown,
                                             width=120)
        self.language_button.place(relx=0.5, rely=0.95, anchor="center")

        # Language Selection Dropdown (hidden initially)
        self.language_dropdown = ctk.CTkOptionMenu(self.root, values=["en", "fr"], command=self.change_language)
        self.language_dropdown.place(relx=0.5, rely=0.9, anchor="center")
        self.language_dropdown.pack_forget()  # Initially hidden

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
            self.update_status(self.translate("error_saving").format("Failed to load hosts. Using defaults."),
                               "warning")

    def save_hosts(self):
        try:
            with open('hosts.json', 'w') as f:
                json.dump(self.hosts, f)
        except Exception as e:
            self.update_status(self.translate("error_saving").format(str(e)), "error")

    def upload_file(self):
        self.filename = filedialog.askopenfilename(
            title=self.translate("file_label"),
            filetypes=[("Text Files", "*.txt")]
        )
        if self.filename:
            self.update_status(self.translate("file_loaded").format(os.path.basename(self.filename)), "success")

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
            self.update_status(self.translate("invalid_file"), "warning")
            return

        try:
            with open(self.filename, 'r') as f:
                names = f.readlines()

            if not names:
                self.update_status(self.translate("empty_file"), "warning")
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
                self.update_status(self.translate("invalid_format") + ", ".join(invalid_lines), "warning")

            output_file = "generated_emails.txt"
            with open(output_file, 'w') as f:
                f.write("\n".join(all_emails))

            self.update_status(self.translate("generated_emails").format(len(all_emails), output_file), "success")

        except Exception as e:
            self.update_status(f"Error: {str(e)}", "error")

    def add_host(self):
        new_host = self.host_entry.get().strip()
        if not new_host:
            self.update_status(self.translate("please_enter_host"), "warning")
            return

        if new_host in self.hosts:
            self.update_status(self.translate("host_exists"), "error")
            return

        self.hosts.append(new_host)
        self.save_hosts()
        self.hosts_dropdown.configure(values=self.hosts)
        self.update_status(self.translate("added_host").format(new_host), "success")
        self.host_entry.delete(0, ctk.END)

    def delete_host(self):
        selected_host = self.hosts_dropdown.get()
        if selected_host not in self.hosts:
            self.update_status(self.translate("invalid_file"), "warning")
            return

        self.hosts.remove(selected_host)
        self.save_hosts()
        self.hosts_dropdown.configure(values=self.hosts)
        self.update_status(self.translate("deleted_host").format(selected_host), "success")

    def translate(self, key):
        return self.languages[self.current_language].get(key, key)

    def toggle_language_dropdown(self):
        if self.language_dropdown.winfo_ismapped():
            self.language_dropdown.pack_forget()
        else:
            self.language_dropdown.pack(pady=10)

    def change_language(self, value):
        self.current_language = value
        self.setup_ui()  # Reinitialize the UI with the new language


def main():
    root = ctk.CTk()
    app = ModernEmailGenerator(root)
    root.mainloop()


if __name__ == "__main__":
    main()
