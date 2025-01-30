import google.generativeai as genai
from config.settings import GEMINI_API_KEY
import re
from telegram.constants import ParseMode

# Configure API key for Gemini
genai.configure(api_key=GEMINI_API_KEY)

text_model = genai.GenerativeModel('gemini-1.5-flash')   
vision_model = genai.GenerativeModel('gemini-1.5-flash')

def clean_text_for_telegram(text):
    """Remove or escape problematic characters for Telegram messages."""
    if not text:
        return "⚠️ No response generated."
    
    # Remove or replace problematic characters
    text = text.replace('*', '').replace('_', '')  # Remove Markdown formatting
    text = text.replace('`', "'")  # Replace code blocks
    text = text.replace('\n\n\n', '\n\n')  # Clean up multiple newlines
    
    # Truncate if too long (Telegram has a 4096 character limit)
    if len(text) > 4000:
        text = text[:4000] + "...(truncated)"
        
    return text.strip()

def get_gemini_response(prompt):
    """Generates text response from the Gemini model."""
    try:
        response = text_model.generate_content(prompt)
        return clean_text_for_telegram(response.text)
    except Exception as e:
        print(f"Error in get_gemini_response: {str(e)}")
        return f"⚠️ Error generating response: {str(e)}"

def analyze_image(img):
    """Processes an image using Gemini and returns a cleaned response."""
    try:
        response = vision_model.generate_content(["Describe this image in detail.", img])
        text = response.text if hasattr(response, "text") else "⚠️ No response generated."
        return clean_text_for_telegram(text)
    except Exception as e:
        print(f"Error in analyze_image: {str(e)}")
        return f"⚠️ Error analyzing image: {str(e)}"

def summarize_search_results(results):
    """Summarize search results using Gemini."""
    try:
        response = text_model.generate_content(f"Summarize these search results: {results}")
        return clean_text_for_telegram(response.text)
    except Exception as e:
        print(f"Error in summarize_search_results: {str(e)}")
        return f"⚠️ Error summarizing results: {str(e)}"