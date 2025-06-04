import fitz  # PyMuPDF
from pathlib import Path
import tkinter as tk
from tkinter import filedialog, messagebox

def add_file_path_link_to_pdf(pdf_path):
    pdf_path = Path(pdf_path).resolve()
    file_uri = f'file:///{pdf_path.as_posix()}'

    # Open the PDF
    doc = fitz.open(str(pdf_path))
    page = doc[0]  # First page

    # Define position of the text and link rectangle
    text = "📂 Open File Location"
    x, y = 72, 72  # 1 inch from top-left
    font_size = 12

    # Draw the text
    page.insert_text((x, y), text, fontsize=font_size, color=(0, 0, 1))

    # Create a clickable link (URI annotation)
    link_rect = fitz.Rect(x, y, x + 150, y + 15)
    page.insert_link({
        "kind": fitz.LINK_URI,
        "from": link_rect,
        "uri": file_uri
    })

    # Save to new PDF
    output_path = pdf_path.with_stem(f"{pdf_path.stem}_with_link")
    doc.save(str(output_path))
    doc.close()

    return output_path

def select_pdf():
    file_path = filedialog.askopenfilename(
        title="Select PDF File",
        filetypes=[("PDF files", "*.pdf")]
    )
    if file_path:
        file_label.config(text=file_path)
        try:
            result_path = add_file_path_link_to_pdf(file_path)
            messagebox.showinfo("Success", f"Modified PDF saved at:\n{result_path}")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to process PDF:\n{e}")

# --- GUI Setup ---
root = tk.Tk()
root.title("PDF Link Adder")
root.geometry("500x200")
root.resizable(False, False)

tk.Label(root, text="Add 'Open File Location' link to front page of a PDF", font=("Arial", 12)).pack(pady=10)

tk.Button(root, text="Select PDF File", command=select_pdf, font=("Arial", 11)).pack(pady=10)

file_label = tk.Label(root, text="No file selected", fg="gray", wraplength=400, font=("Arial", 10))
file_label.pack(pady=5)

root.mainloop()
