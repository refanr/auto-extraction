from bs4 import BeautifulSoup
from pathlib import Path
import re

# Path to your folder containing HTML files
html_folder = "Icelandic_Law/allt"
txt_folder = "Icelandic_Law/allt_txt"

def clean_text(text):
    """Cleans extracted text by removing unwanted patterns."""
    text = re.sub(r"\d+\)\s*", "", text)  # Remove footnotes like "1)\n"
    text = re.sub(r"(\d+)\s*/\s*\n*\s*(\d+)", r"\1/\2", text)  # Fix broken fractions (e.g., "2\n/\n3" -> "2/3")
    return text

def extract_text_from_html(file_path):
    """Extracts and cleans text from an HTML file, starting from '1. gr.'"""
    with open(file_path, "r", encoding="iso-8859-1") as f:
        soup = BeautifulSoup(f, "html.parser")
        raw_text = soup.get_text(separator="\n", strip=True)

        # Find where "1. gr." first appears and extract from there
        start_index = raw_text.find("1. gr.")
        if start_index != -1:
            raw_text = raw_text[start_index:]

        return clean_text(raw_text)

# Process all HTML files in the folder
html_files = Path(html_folder).glob("*.html")
texts = {file.name: extract_text_from_html(file) for file in html_files}

# Save cleaned text to .txt files
for filename, text in texts.items():
    output_file = Path(txt_folder) / f"{filename}.txt"
    with open(output_file, "w", encoding="utf-8") as f:
        f.write(text)

print("Text extraction complete. Cleaned and saved to .txt files.")
