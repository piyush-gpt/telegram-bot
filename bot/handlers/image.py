from telegram import Update
from telegram.ext import MessageHandler, filters, CallbackContext
from bot.services.gemini import analyze_image
from bot.models.user import save_file_metadata
import os  
import io
import asyncio
from concurrent.futures import ThreadPoolExecutor
import fitz
from PIL import Image
async def handle_image(update: Update, context: CallbackContext) -> None:
    """Handle and analyze images using Gemini Vision."""
    file_path = None
    image = None
    
    try:
        chat_id = update.effective_chat.id
        photo = update.message.photo[-1]  # Get the largest photo
        
        # Create downloads directory if it doesn't exist
        downloads_dir = os.path.join(os.getcwd(), "downloads")
        os.makedirs(downloads_dir, exist_ok=True)
        
        # Download the image
        file = await context.bot.get_file(photo.file_id)
        file_path = os.path.join(downloads_dir, f"{photo.file_id}.jpg")
        
        # Download file using download_to_drive
        await file.download_to_drive(custom_path=file_path)
        
        # Open and analyze image using context manager
        with Image.open(file_path) as image:
            # Analyze image with Gemini Vision
            response = analyze_image(image)
            analysis = response
            
            # Save file metadata
            save_file_metadata(chat_id, photo.file_id, analysis,"image")
            
            await update.message.reply_text(f"Image Analysis:\n{analysis}",parse_mode=None)
            
    except Exception as e:
        print(f"Error processing image: {str(e)}")
        await update.message.reply_text("Sorry, I couldn't process this image. Please try again.")
    
    finally:
        # Cleanup in finally block to ensure it runs
        if image and hasattr(image, 'close'):
            image.close()
        
        # Add a small delay before trying to remove the file
        await asyncio.sleep(0.5)
        
        try:
            if file_path and os.path.exists(file_path):
                os.remove(file_path)
        except Exception as e:
            print(f"Error removing file: {str(e)}")


async def analyze_document_page(page_num, page, executor):
    """Analyze a single page asynchronously using a thread pool."""
    loop = asyncio.get_event_loop()
    # Run the page processing in a separate thread to avoid blocking the event loop
    return await loop.run_in_executor(executor, process_page, page_num, page)

def process_page(page_num, page):
    """Converts the PDF page to an image and analyzes it."""
    pix = page.get_pixmap()
    img_data = pix.tobytes("png")  # Consider 'jpeg' if needed
    image = Image.open(io.BytesIO(img_data))
    # Call analyze_image function (ensure it's synchronous)
    return analyze_image(image)

# Function to split text into chunks
def split_text(text, max_length=4000):
    """Split text into chunks of max_length (default 4000 characters)."""
    chunks = []
    while len(text) > max_length:
        split_pos = text.rfind("\n", 0, max_length)
        if split_pos == -1:
            split_pos = max_length
        chunks.append(text[:split_pos])
        text = text[split_pos:].lstrip()
    chunks.append(text)
    return chunks

async def handle_document(update: Update, context: CallbackContext) -> None:
    """Handle and analyze PDF documents using Gemini Vision."""
    file_path = None
    # Inside handle_document function
    await update.message.reply_text("Processing PDF... This may take a moment.")
    
    try:
        chat_id = update.effective_chat.id
        document = update.message.document
        if document.file_size > 10_000_000:  # 10MB limit
            await update.message.reply_text("PDF file is too large. Please send a smaller file.")
            return
        
        # Check if it's a PDF
        if not document.mime_type == "application/pdf":
            await update.message.reply_text("Please send a PDF document.")
            return
        
        # Create downloads directory if it doesn't exist
        downloads_dir = os.path.join(os.getcwd(), "downloads")
        os.makedirs(downloads_dir, exist_ok=True)
        
        # Download the PDF
        file = await context.bot.get_file(document.file_id)
        file_path = os.path.join(downloads_dir, f"{document.file_id}.pdf")
        
        # Download file
        await file.download_to_drive(custom_path=file_path)
        
        # Open the PDF and prepare for processing
        pdf_document = fitz.open(file_path)
        analyses = []
        
        # Use a ThreadPoolExecutor to run page processing in parallel
        with ThreadPoolExecutor() as executor:
            tasks = [
                analyze_document_page(page_num, pdf_document.load_page(page_num), executor)
                for page_num in range(min(pdf_document.page_count, 5))  # Limit to first 5 pages
            ]
            
            # Process all pages concurrently
            responses = await asyncio.gather(*tasks)
        
        # Combine analyses into a single string
        full_analysis = "\n".join([f"Page {page_num + 1}:\n{response}\n" for page_num, response in enumerate(responses)])
        
        pdf_document.close()
        
        # Save metadata (consider doing this async if possible)
        save_file_metadata(
            chat_id,
            document.file_id,
            full_analysis,
            "pdf"
        )
        
        # Split analysis into chunks if it's too long
        analysis_chunks = split_text(full_analysis)
        
        # Send each chunk as a separate message
        for chunk in analysis_chunks:
            await update.message.reply_text(chunk)
            await asyncio.sleep(1)  # Optional: Throttle responses to avoid rate limits
        
    except Exception as e:
        print(f"Error processing PDF: {str(e)}")
        await update.message.reply_text("Sorry, I couldn't process this PDF. Please try again.")
    
    finally:
        # Cleanup
        await asyncio.sleep(0.5)
        try:
            if file_path and os.path.exists(file_path):
                os.remove(file_path)
        except Exception as e:
            print(f"Error removing file: {str(e)}")


image_handler = MessageHandler(filters.PHOTO, handle_image)
doc_handler = MessageHandler(filters.Document.PDF, handle_document)