# AzmiCertBot
## Telegram Bot for Generating PDF Certificates

### 1. **Overview**

This Python script creates a Telegram bot that interacts with users, collects their details (Name and ID Number), and generates a PDF certificate based on a predefined template. The user inputs their data in a specific format, which is overlaid onto a PDF file. The completed PDF file is then sent back to the user through Telegram.

### 2. **Code Breakdown and How It Works**

#### **Imports:**
```python
import logging
import webbrowser
from telegram import Update, InputFile
from telegram.ext import Application, CommandHandler, MessageHandler, filters, CallbackContext
import fitz  # PyMuPDF
```
- **logging**: Used to log errors and system info.
- **webbrowser**: Opens a web page (GitHub in this case).
- **telegram, telegram.ext**: Libraries to interface with the Telegram API for bot creation.
- **fitz**: PyMuPDF library used for working with PDF files to add text to the NID template.

#### **Logging Setup:**
```python
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)
```
- Configures the logging module to log the bot’s activities, including errors.

#### **Start Command:**
```python
async def start(update: Update, context: CallbackContext):
    await update.message.reply_text("Welcome! Please send me your details in the format: \nName, ID Number")
```
- The `/start` command triggers this function and sends a welcome message. The bot awaits user input in the format `Name, ID Number`.

#### **Create Certificate (NID) Card:**
```python
def create_cert_card(data, output_filename):
    template_path = 'cert_template.pdf'  # Path to your NID template
    template = fitz.open(template_path)
    
    page = template[0]
    
    # Color setup
    color_blue = (48/255, 169/255, 222/255)
    color_black = (0, 0, 0)

    # Insert text onto the PDF
    page.insert_text((200, 220), f"{data['name']}", fontsize=26, fontname="helv", color=color_blue)
    page.insert_text((240, 240), f"ID Number: {data['id_number']}", fontsize=12, fontname="helv", color=color_black)

    # Save the PDF
    template.save(output_filename)
    template.close()
```
- **create_cert_card** function:
  - Loads the certificate template (`cert_template.pdf`) using `fitz`.
  - Inserts the `name` and `ID number` at predefined coordinates with specific font sizes and colors.
  - Saves the modified PDF with a new name (`generated_cert.pdf`).

#### **Process User Data:**
```python
async def process_data(update: Update, context: CallbackContext):
    user_data = update.message.text.split(',')
    if len(user_data) == 2:
        data = {
            'name': user_data[0].strip(),
            'id_number': user_data[1].strip(),
        }
        output_pdf = 'generated_cert.pdf'
        create_cert_card(data, output_pdf)
        
        with open(output_pdf, 'rb') as f:
            await update.message.reply_document(document=InputFile(f), filename=output_pdf)
    else:
        await update.message.reply_text("Invalid format. Please use: Name, ID Number")
```
- Processes the user’s input and splits the string into two parts: name and ID number.
- If the format is correct, the bot calls `create_cert_card()` to generate the certificate, then sends the PDF back to the user.

#### **Error Handling:**
```python
async def error(update: Update, context: CallbackContext):
    logger.warning('Update "%s" caused error "%s"', update, context.error)
```
- Handles any errors encountered during execution.

#### **Open GitHub Command:**
```python
async def open_github(update: Update, context: CallbackContext):
    github_url = "https://github.com/azizulabedinazmi"
    webbrowser.open(github_url)
    await update.message.reply_text(f"Opening GitHub: {github_url}")
```
- The `/github` command opens the user’s GitHub profile in a web browser.

#### **Main Function:**
```python
def main():
    application = Application.builder().token("Your_Token").build()
    
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("github", open_github))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, process_data))
    
    application.add_error_handler(error)
    
    application.run_polling()
```
- Initializes the bot with your unique bot token and sets up various handlers for commands and messages.
- The bot uses polling to continuously check for new messages.

### 3. **Installation and Setup Guide**

#### **Step 1: Install Dependencies**

- Ensure you have Python 3.8+ installed.
- Install the required Python packages:
  ```bash
  pip install python-telegram-bot==20.0a4
  pip install pymupdf
  ```
  - `python-telegram-bot`: Provides the Telegram bot API functionality.
  - `PyMuPDF (fitz)`: Handles PDF manipulation.

#### **Step 2: Create the Telegram Bot**

1. Open Telegram and search for **BotFather**.
2. Type `/start` and then `/newbot`.
3. Follow the prompts to name your bot.
4. BotFather will provide you with a unique bot token. Copy it and replace `Your_Token` in the script with your actual token.

#### **Step 3: Prepare the Certificate Template**

- Create or design a PDF certificate template (`cert_template.pdf`) with placeholders for the name and ID.
- Place the file in the same directory as your script.

#### **Step 4: Adjust Coordinates**

- The `page.insert_text` function requires precise coordinates to place the text in the correct spots on the PDF. Adjust `(200, 220)` and `(240, 240)` in `create_cert_card()` to match the locations on your template where you want the `name` and `ID` to appear.

#### **Step 5: Run the Script**

Run the Python script:
```bash
python telegram_cert_bot.py
```

#### **Step 6: Test the Bot**

- Open your bot in Telegram and start interacting by sending the `/start` command.
- Provide the requested details (Name, ID Number) to receive the generated certificate in PDF format.

### 4. **Create a Virtual Machine (VM) on Azure** 

1. **Login to Azure Portal**  
   Go to the [Azure Portal](https://portal.azure.com/) and log in to your account.

2. **Create a New Virtual Machine**
   - Navigate to the "Virtual Machines" service.
   - Click on "Create" and select "Virtual Machine."
   - Fill in the required fields:
     - **Resource group**: Create a new one or select an existing one.
     - **Name**: Name your VM (e.g., `telegram-bot-vm`).
     - **Region**: Choose the region closest to you.
     - **Image**: Choose a Linux distribution (Ubuntu 20.04 LTS is recommended).
     - **Size**: For this project, a small instance (Standard B1s or B1ms) is sufficient.
     - **Authentication**: Choose SSH public key for secure access. Generate a key pair if you don’t have one.
   
3. **Networking**
   - Configure the networking settings, allowing HTTP and SSH traffic. You can leave the default settings.

4. **Review + Create**
   - Review the settings and click on "Create."
   - Once the VM is created, you’ll receive an IP address for accessing it via SSH.

---

#### **Access Your VM via SSH**

Once the VM is created, SSH into the VM from your local machine.

1. Open a terminal (or use an SSH client on Windows like PuTTY) and run:
   ```bash
   ssh your_username@your_vm_ip_address
   ```
   Replace `your_username` with the username you set during VM creation and `your_vm_ip_address` with the public IP address of your VM.

2. Accept the SSH fingerprint and log in to the VM.

---

#### **Install Python and Required Packages**

Now that you're inside your Azure VM, you need to install Python, `python-telegram-bot`, and `PyMuPDF`.

1. **Update Package List**  
   Ensure your VM is up-to-date:
   ```bash
   sudo apt update
   ```

2. **Install Python and Pip**  
   Install Python and its package manager, `pip`:
   ```bash
   sudo apt install python3 python3-pip
   ```

3. **Install Required Python Packages**  
   Install the `python-telegram-bot` and `PyMuPDF` (fitz) packages:
   ```bash
   pip3 install python-telegram-bot==20.0a4
   pip3 install pymupdf
   ```

---

#### **Upload Your Bot Files to the VM**

Use `scp` (secure copy protocol) or a file transfer tool like `rsync` to upload your bot files, including the PDF template and Python script, to the VM.

1. **From Your Local Machine**:
   ```bash
   scp /path/to/your/telegram_cert_bot.py your_username@your_vm_ip_address:/home/your_username/
   scp /path/to/cert_template.pdf your_username@your_vm_ip_address:/home/your_username/
   ```

   Replace `/path/to/your/telegram_cert_bot.py` and `/path/to/cert_template.pdf` with the actual paths to your bot script and PDF template. Ensure these are uploaded to your home directory on the VM.

2. **Check the Files**:  
   Once the files are uploaded, navigate to the directory in your VM to confirm:
   ```bash
   cd /home/your_username/
   ls
   ```

---

#### **Edit Your Bot Script on the VM**

If you haven't already replaced the bot token in your script with the actual token from BotFather, you can do so on the VM.

1. **Edit the Python Script**:
   ```bash
   nano telegram_cert_bot.py
   ```
   - Replace the line `application = Application.builder().token("Your_Token").build()` with your actual Telegram bot token.
   - Press `CTRL + X`, then `Y`, and hit `Enter` to save and exit.

---

#### **Test the Bot Locally on the VM**

Before setting up the bot as a service, it's a good idea to test it by running it manually.

1. Run the Python script to start the bot:
   ```bash
   python3 telegram_cert_bot.py
   ```

2. **Interacting with the Bot**:
   - Open Telegram on your phone or desktop.
   - Start a conversation with your bot by searching for its username.
   - Type `/start` and provide the necessary details (Name, ID number) to test if the bot responds correctly and generates the PDF.

If everything works, you’re ready to make the bot run continuously on your VM.

---

#### **Configure the Bot to Run Continuously with systemd**

To ensure the bot runs in the background even after you log out, you'll create a systemd service.

1. **Create a systemd Service File**:  
   Use the following command to create the service file:
   ```bash
   sudo nano /etc/systemd/system/telegram-bot.service
   ```

2. **Define the Service**:  
   Add the following content to the service file:
   ```bash
   [Unit]
   Description=Telegram Bot Service
   After=network.target

   [Service]
   User=your_username
   WorkingDirectory=/home/your_username/
   ExecStart=/usr/bin/python3 /home/your_username/telegram_cert_bot.py
   Restart=always

   [Install]
   WantedBy=multi-user.target
   ```

   Replace `your_username` with your actual VM username.

3. **Save and Exit**:  
   Press `CTRL + X`, then `Y`, and hit `Enter`.

4. **Reload systemd**:  
   To load the new service into systemd, run:
   ```bash
   sudo systemctl daemon-reload
   ```

5. **Start and Enable the Service**:  
   Start the bot service and enable it to run on boot:
   ```bash
   sudo systemctl start telegram-bot
   sudo systemctl enable telegram-bot
   ```

6. **Check the Status of the Service**:  
   To confirm the bot is running, check the status of the service:
   ```bash
   sudo systemctl status telegram-bot
   ```

   You should see that the service is running. If there are any errors, they will be displayed here.

---

#### **Monitor Logs and Maintain the Bot**

To monitor the bot’s logs, you can use the `journalctl` command. This will display the logs generated by the service:
```bash
sudo journalctl -u telegram-bot -f
```
- Use this command if you need to troubleshoot any issues.

---

#### **Updating the Bot**

If you need to update your bot's code or add new features:
1. Edit the `telegram_cert_bot.py` on the VM using a text editor like `nano`.
2. After making changes, restart the service to apply the updates:
   ```bash
   sudo systemctl restart telegram-bot
   ```

---

#### **Final Notes**

- **Security**: Make sure to properly secure your VM by disabling unused ports and services. Consider using **firewall rules** to restrict access to only the necessary services (SSH and HTTP).
- **Backup**: Regularly back up your bot files and ensure the VM’s snapshot is updated, so you can restore the VM in case of issues.

---

### 5. **Important Notes**

- **Replace YOUR_TOKEN**: Make sure to replace `'Your_Token'` with the bot token you received from BotFather.
- **PDF Template**: Ensure the `cert_template.pdf` file is designed properly and located in the same directory as your script.
- **Text Coordinates**: Adjust the `(200, 220)` and `(240, 240)` coordinates in `create_cert_card()` to match the correct locations on your PDF template.

