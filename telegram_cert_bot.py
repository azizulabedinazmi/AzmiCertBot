import logging
import webbrowser
from telegram import Update, InputFile # type: ignore
from telegram.ext import Application, CommandHandler, MessageHandler, filters, CallbackContext # type: ignore
import fitz  # type: ignore # PyMuPDF

# Set up logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

# Asynchronous function to handle the /start command
async def start(update: Update, context: CallbackContext):
    await update.message.reply_text("Welcome! Please send me your details in the format: \nName, ID Number")

# Function to overlay text onto a PDF template
def create_cert_card(data, output_filename):
    # Load the template
    template_path = 'cert_template.pdf'  # Path to your NID template
    template = fitz.open(template_path)
    
    # Access the first page of the PDF template
    page = template[0]
    
    # Convert RGB color values to 0-1 range
    color_blue = (48/255, 169/255, 222/255)
    color_black = (0, 0, 0)

    # Insert text with a standard font
    page.insert_text((200, 220), f"{data['name']}", fontsize=26, fontname="helv", color=color_blue)
    page.insert_text((240, 240), f"ID Number: {data['id_number']}", fontsize=12, fontname="helv", color=color_black)

    # Save the modified PDF
    template.save(output_filename)
    template.close()

# Asynchronous function to process user data and generate NID card
async def process_data(update: Update, context: CallbackContext):
    user_data = update.message.text.split(',')
    if len(user_data) == 2:
        data = {
            'name': user_data[0].strip(),
            'id_number': user_data[1].strip(),
        }
        output_pdf = 'generated_cert.pdf'
        
        # Create the NID card
        create_cert_card(data, output_pdf)
        
        # Send the PDF to the user
        with open(output_pdf, 'rb') as f:
            await update.message.reply_document(document=InputFile(f), filename=output_pdf)
    else:
        await update.message.reply_text("Invalid format. Please use: Name, ID Number")

# Asynchronous function to handle errors
async def error(update: Update, context: CallbackContext):
    logger.warning('Update "%s" caused error "%s"', update, context.error)

# Asynchronous function to handle the /github command
async def open_github(update: Update, context: CallbackContext):
    github_url = "https://github.com/azizulabedinazmi"
    webbrowser.open(github_url)
    await update.message.reply_text(f"Opening GitHub: {github_url}")

# Main function to set up the bot
def main():
    # Replace 'YOUR_TOKEN' with your actual bot token
    application = Application.builder().token("Your_Token").build()
    
    # Command handler for /start
    application.add_handler(CommandHandler("start", start))
    
    # Command handler for /github
    application.add_handler(CommandHandler("github", open_github))
    
    # Message handler for user input
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, process_data))

    # Error handler
    application.add_error_handler(error)

    # Start the Bot
    application.run_polling()

if __name__ == '__main__':
    main()
