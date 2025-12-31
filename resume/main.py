import tkinter as tk
from tkinter import messagebox, filedialog
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from textwrap import wrap
import os

profile_photo_path = None
template_index = 0   # 🔥 auto-switch template

# ================= UTIL =================

def wrap_text(text, width):
    lines = []
    for line in text.split("\n"):
        lines.extend(wrap(line.strip(), width))
    return lines

# ================= PHOTO =================

def upload_photo():
    global profile_photo_path
    profile_photo_path = filedialog.askopenfilename(
        filetypes=[("Image Files", "*.png;*.jpg;*.jpeg")]
    )

# ================= TEMPLATE 1 =================
# Sidebar layout

def template_sidebar(c, data):
    width, height = A4
    sidebar = width * 0.3
    x = sidebar + 20
    y = height - 60

    # Sidebar
    c.setFillColor(colors.HexColor("#2C3E50"))
    c.rect(0, 0, sidebar, height, fill=1)

    if profile_photo_path:
        try:
            c.drawImage(profile_photo_path, 40, height - 120, 80, 80, mask="auto")
        except:
            pass

    c.setFillColor(colors.white)
    sy = height - 160

    def side(title, content):
        nonlocal sy
        if not content: return
        c.setFont("Helvetica-Bold", 11)
        c.drawString(30, sy, title)
        sy -= 15
        c.setFont("Helvetica", 9)
        for l in wrap_text(content, 28):
            c.drawString(35, sy, "- " + l)
            sy -= 12
        sy -= 10

    side("SKILLS", data["skills"])
    side("LANGUAGES", data["languages"])
    side("CERTIFICATES", data["certificates"])

    c.setFillColor(colors.black)
    c.setFont("Helvetica-Bold", 18)
    c.drawString(x, y, data["name"])
    y -= 22
    c.setFont("Helvetica", 11)
    c.setFillColor(colors.grey)
    c.drawString(x, y, f'{data["email"]} | {data["phone"]}')
    y -= 30

    def section(title, content):
        nonlocal y
        if not content: return
        c.setFont("Helvetica-Bold", 12)
        c.setFillColor(colors.HexColor("#2C3E50"))
        c.drawString(x, y, title)
        y -= 15
        c.setFont("Helvetica", 10)
        c.setFillColor(colors.black)
        for l in wrap_text(content, 80):
            c.drawString(x + 10, y, l)
            y -= 12
        y -= 10

    section("PROFILE", data["summary"])
    section("EXPERIENCE", data["experience"])
    section("EDUCATION", data["education"])

# ================= TEMPLATE 2 =================
# Clean top-header layout

def template_top_header(c, data):
    width, height = A4
    y = height - 70

    c.setFillColor(colors.HexColor("#34495E"))
    c.rect(0, height - 130, width, 130, fill=1)

    c.setFillColor(colors.white)
    c.setFont("Helvetica-Bold", 22)
    c.drawCentredString(width / 2, y, data["name"])
    y -= 30
    c.setFont("Helvetica", 11)
    c.drawCentredString(width / 2, y, f'{data["email"]} | {data["phone"]}')

    y = height - 170

    def section(title, content):
        nonlocal y
        if not content: return
        c.setFont("Helvetica-Bold", 13)
        c.setFillColor(colors.HexColor("#2C3E50"))
        c.drawString(50, y, title)
        y -= 15
        c.setFont("Helvetica", 10)
        c.setFillColor(colors.black)
        for l in wrap_text(content, 95):
            c.drawString(60, y, "- " + l)
            y -= 12
        y -= 12

    section("SUMMARY", data["summary"])
    section("SKILLS", data["skills"])
    section("EXPERIENCE", data["experience"])
    section("EDUCATION", data["education"])

# ================= GENERATE =================

templates = [template_sidebar, template_top_header]

def generate_pdf_resume():
    global template_index

    data = {
        "name": entry_name.get().strip(),
        "email": entry_email.get().strip(),
        "phone": entry_phone.get().strip(),
        "summary": text_summary.get("1.0", tk.END).strip(),
        "education": text_education.get("1.0", tk.END).strip(),
        "skills": text_skills.get("1.0", tk.END).strip(),
        "experience": text_experience.get("1.0", tk.END).strip(),
        "languages": text_languages.get("1.0", tk.END).strip(),
        "certificates": text_certificates.get("1.0", tk.END).strip(),
    }

    if not data["name"] or not data["email"] or not data["phone"]:
        messagebox.showerror("Error", "Name, Email & Phone required")
        return

    safe = data["name"].replace(" ", "_")
    file_name = f"{safe}_Resume_{template_index+1}.pdf"

    c = canvas.Canvas(file_name, pagesize=A4)
    templates[template_index](c, data)
    c.save()

    template_index = (template_index + 1) % len(templates)

    messagebox.showinfo("Success", f"Resume created:\n{file_name}")

# ================= GUI =================

root = tk.Tk()
root.title("Smart Resume Builder")
root.geometry("760x700")

def field(lbl, widget, row):
    tk.Label(root, text=lbl).grid(row=row, column=0, sticky="e", padx=5)
    widget.grid(row=row, column=1, padx=10, pady=5)

entry_name = tk.Entry(root, width=55)
entry_email = tk.Entry(root, width=55)
entry_phone = tk.Entry(root, width=55)
text_summary = tk.Text(root, height=3, width=55)
text_education = tk.Text(root, height=4, width=55)
text_skills = tk.Text(root, height=4, width=55)
text_experience = tk.Text(root, height=6, width=55)
text_languages = tk.Text(root, height=2, width=55)
text_certificates = tk.Text(root, height=2, width=55)

widgets = [
    ("Full Name", entry_name),
    ("Email", entry_email),
    ("Phone", entry_phone),
    ("Summary", text_summary),
    ("Education", text_education),
    ("Skills", text_skills),
    ("Experience", text_experience),
    ("Languages", text_languages),
    ("Certificates", text_certificates),
]

for i, (l, w) in enumerate(widgets):
    field(l, w, i)

tk.Button(root, text="Upload Photo", command=upload_photo).grid(row=10, column=0, pady=10)
tk.Button(root, text="Generate PDF Resume", command=generate_pdf_resume).grid(row=10, column=1)

root.mainloop()
