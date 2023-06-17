import nbformat as nbf
import base64
import os
import sys
import re
from mimetypes import guess_extension

def encode_image(image_path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode()

def convert_images_in_notebook(notebook_path):
    # Read the notebook
    with open(notebook_path, 'r', encoding='utf-8') as f:
        notebook = nbf.read(f, as_version=4)

    # Iterate through all cells
    for cell in notebook.cells:
        if cell.cell_type == "markdown":
            # Replace markdown image links with Base64 strings
            lines = cell.source.split('\n')
            for i, line in enumerate(lines):
                # Markdown images
                markdown_image = re.search(r'!\[.*\]\((.*)\)', line)
                # HTML images
                html_image = re.search(r'<img src="(.*)"', line)

                if markdown_image:
                    image_path = markdown_image.group(1).strip()
                elif html_image:
                    image_path = html_image.group(1).strip()
                else:
                    continue

                # Skip if the image path is already in base64 format
                if not image_path.startswith("data:image"):
                    # Convert image to base64
                    if image_path.startswith("attachment:"):
                        attachment_key = image_path[len("attachment:"):]
                        # print(cell.attachments[attachment_key])
                        # 1/0
                        # mime, encoded_image = cell.attachments[attachment_key]['image/png']
                        # ext = guess_extension(mime)
                        encoded_image = cell.attachments[attachment_key]['image/png']
                        ext = 'png'
                    else:
                        if not os.path.isabs(image_path):
                            # If relative path, make it absolute based on notebook directory
                            image_path = os.path.join(os.path.dirname(notebook_path), image_path)
                        encoded_image = encode_image(image_path)
                        ext = os.path.splitext(image_path)[-1].replace(".", "")
                    
                    # Replace image link in line
                    if markdown_image:
                        lines[i] = re.sub(r'!\[.*\]\(.*\)', f'![Image](data:image/{ext};base64,{encoded_image})', line)
                    elif html_image:
                        lines[i] = re.sub(r'<img src=".*"', f'<img src="data:image/{ext};base64,{encoded_image}"', line)

            # Update cell source
            cell.source = '\n'.join(lines)

    # Write the updated notebook
    output_path = os.path.splitext(notebook_path)[0] + '_base64_converted.ipynb'
    with open(output_path, 'w', encoding='utf-8') as f:
        nbf.write(notebook, f)

if __name__ == '__main__':
    if len(sys.argv) != 2:
        print("Usage: python convert_images_to_base64.py <path_to_notebook>")
    else:
        convert_images_in_notebook(sys.argv[1])
