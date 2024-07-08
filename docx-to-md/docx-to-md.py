import sys
from docx import Document

def paragraph_to_markdown(paragraph):
    """Convert a DOCX paragraph to Markdown based on its style."""
    text = paragraph.text
    style = paragraph.style.name
    
    # Convert headings based on style name
    if style.startswith('Heading'):
        level = len(style.split()) - 1  # Assuming style names like "Heading 1", "Heading 2", etc.
        markdown = '#' * level + ' ' + text
    elif any(run.font.name == 'Courier New' for run in paragraph.runs):  # Assuming code blocks use Courier New font
        markdown = '```\n' + text + '\n```'
    else:
        markdown = text
    
    return markdown

def docx_to_markdown(docx_path, md_path):
    document = Document(docx_path)
    md_content = []

    for paragraph in document.paragraphs:
        md_content.append(paragraph_to_markdown(paragraph))

    with open(md_path, 'w', encoding='utf-8') as md_file:
        md_file.write('\n\n'.join(md_content))

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python script.py <input_docx_path> <output_md_path>")
        sys.exit(1)

    docx_path = sys.argv[1]
    md_path = sys.argv[2]

    docx_to_markdown(docx_path, md_path)