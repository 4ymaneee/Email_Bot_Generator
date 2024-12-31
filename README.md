# 📨 Modern Email Generator Pro

**Modern Email Generator Pro** is a Python-based desktop application that enables users to easily generate professional email combinations from a list of names. This tool supports multiple email domains, allows file uploads for name processing, and offers a sleek, modern interface powered by **CustomTkinter**. It also supports multiple languages (English and French), making it both versatile and user-friendly.

<div align="center">
<img src="img.png" alt="Modern Email Generator Pro" width="300" />
</div>

## Features

- **Generate Professional Email Combinations**: Automatically create multiple email combinations from first and last names in various formats:
  - first.last@domain.com
  - last.first@domain.com
  - firstlast@domain.com
  - first@domain.com
  - firstl@domain.com

- **Customizable Hosts**: Add and remove custom email domains (e.g., gmail.com, yahoo.com, hotmail.com) directly from the UI.

- **File Upload Support**: Upload a .txt file containing names formatted as first_name:last_name, and the app will generate emails automatically.

- **Multi-language Support**: Available in **English** and **French**, with an easy-to-switch language dropdown.

- **Persistent Host Management**: Custom hosts are stored in a hosts.json file, ensuring that your preferences are saved between sessions.

- **Organized Output**: Generated email combinations are saved in a folder called Emails Generated. Each new file is numbered sequentially (e.g., Emails_Combination_1.txt).

- **Real-time Status Updates**: Displays status messages for actions like file uploads, email generation, and error handling.

## Installation

### Prerequisites

Ensure that you have **Python 3.x** installed. The application also requires the customtkinter library.

### Install Dependencies

Install the required Python dependencies by running:

bash
pip install customtkinter
