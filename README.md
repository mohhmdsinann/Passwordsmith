# Passwordsmith — Interactive Wordlist Generator

![Passwordsmith Banner](ascii/Passwordsmith.txt)

## Overview

**Passwordsmith** is a command-line interactive wordlist generator designed for security professionals, ethical hackers, and penetration testers. It creates highly customizable password lists based on user-provided details such as names, years, cities, hobbies, phone endings, and more.

**Features:**

- CLI-based tool, works in **Kali Linux** and **Termux**.
- Generates **all possible combinations** of provided data (first name, last name, nicknames, birth year, city, social usernames, pets, phone endings, hobbies/extra words, symbols).
- Ensures **password length between 8 and 32 characters**.
- Includes **symbols** in patterns (customizable, max 25 symbols).
- **Colorized prompts** for better readability.
- **Disclaimer and warnings** before usage (must confirm to proceed).
- Export wordlists to **TXT files** automatically.
- Optional **default common password list** included (`common_passwords_1000.txt`).
- Aligned and neatly spaced CLI input for professional appearance.
- Handles **required fields**, ensuring crucial inputs are not skipped.

---

## **Important Note**

Before using Passwordsmith:

- You **must type `PROCEED` in capital letters** when prompted to confirm the disclaimer.  
  - Example:  
    ```
    Type 'PROCEED' to continue: PROCEED
    ```

- Any other input will **not allow the script to run**.

---

## **Installation**

Clone the repository:

```bash
git clone <YOUR_GITHUB_REPO_URL>
cd Passwordsmith
