import imgkit
import os
import re

WKHTML_PATH = r"C:\Program Files\wkhtmltopdf\bin\wkhtmltoimage.exe"
config = imgkit.config(wkhtmltoimage=WKHTML_PATH)

html_file = r"E:\sem6\AI-A-coding-v2\2303A51206_8.2.html"
output_dir = r"E:\sem6\AI-A-coding-v2\screenshots"
os.makedirs(output_dir, exist_ok=True)

with open(html_file, "r", encoding="utf-8") as f:
    full_html = f.read()

# Extract the <head> section for styles
head_match = re.search(r"(<head.*?</head>)", full_html, re.DOTALL)
head_section = head_match.group(1) if head_match else "<head></head>"

# Split notebook into task sections by <hr> tags or markdown "---" rendered as <hr>
# Each task starts with a markdown heading "## Task N"
# We'll find cell groups between Task headings

# Find all cell divs
cells = re.findall(r'(<div class="cell[^"]*".*?</div>\s*</div>\s*</div>)', full_html, re.DOTALL)

# Strategy: search for task boundaries in the HTML
# Split by <hr> which separates tasks
sections = re.split(r'<hr\s*/?>', full_html)

# Task sections are the ones containing "Task 1", "Task 2", etc.
task_sections = []
for i, section in enumerate(sections):
    for task_num in range(1, 6):
        if f"Task {task_num}" in section and ("test" in section.lower() or "def " in section.lower()):
            task_sections.append((task_num, section))
            break

# If splitting by <hr> didn't work well, just take the full HTML as one image
if len(task_sections) < 5:
    # Fallback: generate one full screenshot
    print("Generating full notebook screenshot...")
    options = {
        'format': 'png',
        'width': '1200',
        'quality': '100',
        'encoding': 'UTF-8',
        'enable-local-file-access': '',
    }
    imgkit.from_file(html_file, os.path.join(output_dir, "full_notebook.png"),
                     options=options, config=config)
    print(f"Saved: {os.path.join(output_dir, 'full_notebook.png')}")
else:
    for task_num, section in task_sections:
        task_html = f"""<!DOCTYPE html>
<html>
{head_section}
<body style="background:#fff; padding:20px;">
{section}
</body>
</html>"""
        
        output_path = os.path.join(output_dir, f"task{task_num}_imgkit.png")
        options = {
            'format': 'png',
            'width': '1200',
            'quality': '100',
            'encoding': 'UTF-8',
            'enable-local-file-access': '',
        }
        imgkit.from_string(task_html, output_path, options=options, config=config)
        print(f"Saved: {output_path}")

print("\nAll imgkit screenshots generated!")
