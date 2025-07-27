import os
import json
import pdfplumber
import fitz  # PyMuPDF

def extract_outline(file_path):
    outline = []
    title = ""
    with pdfplumber.open(file_path) as pdf:
        font_stats = {}
        for page_num, page in enumerate(pdf.pages):
            for char in page.chars:
                text = char['text'].strip()
                if not text.isalpha() or len(text) < 2:
                    continue
                font_size = round(char['size'])
                font_stats.setdefault(font_size, []).append(text)

        title_font = sorted(font_stats.items(), key=lambda x: -len(x[1]))[0][0]
        title = " ".join(font_stats[title_font][:10])

    doc = fitz.open(file_path)
    for page_num, page in enumerate(doc):
        blocks = page.get_text("dict")["blocks"]
        for block in blocks:
            for line in block.get("lines", []):
                spans = line.get("spans", [])
                for span in spans:
                    text = span["text"].strip()
                    if not text or len(text.split()) > 20:
                        continue
                    font_size = int(span["size"])
                    level = None
                    if font_size >= title_font:
                        level = "H1"
                    elif font_size >= title_font - 2:
                        level = "H2"
                    elif font_size >= title_font - 4:
                        level = "H3"
                    if level:
                        outline.append({
                            "level": level,
                            "text": text,
                            "page": page_num + 1
                        })

    return {
        "title": title,
        "outline": outline
    }

def main():
    input_dir = "/app/input"
    output_dir = "/app/output"

    for filename in os.listdir(input_dir):
        if filename.endswith(".pdf"):
            input_path = os.path.join(input_dir, filename)
            output_path = os.path.join(output_dir, filename.replace(".pdf", ".json"))
            data = extract_outline(input_path)
            with open(output_path, "w") as f:
                json.dump(data, f, indent=2)

if __name__ == "__main__":
    main()
