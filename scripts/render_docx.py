#!/usr/bin/env python3
"""Convert a practical Markdown subset to DOCX. Mermaid fences remain text."""
import argparse, re
from pathlib import Path
from docx import Document
from docx.shared import Inches, Pt
from docx.oxml import OxmlElement
from docx.oxml.ns import qn

def style_run(run, name="Microsoft YaHei", size=10.5, bold=None):
    run.font.name = name
    run._element.get_or_add_rPr().rFonts.set(qn("w:eastAsia"), name)
    run.font.size = Pt(size)
    if bold is not None:
        run.bold = bold

def add_inline(p, text):
    for token in re.split(r"(\*\*.*?\*\*|`.*?`)", text):
        if not token:
            continue
        if token.startswith("**") and token.endswith("**"):
            r = p.add_run(token[2:-2]); style_run(r, bold=True)
        elif token.startswith("`") and token.endswith("`"):
            r = p.add_run(token[1:-1]); style_run(r, "Consolas", 9)
        else:
            r = p.add_run(token); style_run(r)

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("input")
    ap.add_argument("-o", "--output")
    args = ap.parse_args()
    src = Path(args.input)
    out = Path(args.output) if args.output else src.with_suffix(".docx")
    lines = src.read_text(encoding="utf-8").splitlines()
    doc = Document()
    sec = doc.sections[0]
    sec.top_margin = Inches(.7); sec.bottom_margin = Inches(.7)
    sec.left_margin = Inches(.8); sec.right_margin = Inches(.8)
    for n in ["Normal", "Title", "Heading 1", "Heading 2", "Heading 3"]:
        st = doc.styles[n]
        st.font.name = "Microsoft YaHei"
        st._element.rPr.rFonts.set(qn("w:eastAsia"), "Microsoft YaHei")
    doc.styles["Normal"].font.size = Pt(10.5)
    i = 0; in_code = False; code = []
    while i < len(lines):
        line = lines[i]
        if line.strip().startswith("```"):
            if in_code:
                p = doc.add_paragraph()
                r = p.add_run("\n".join(code)); style_run(r, "Consolas", 8.5)
                code = []; in_code = False
            else:
                in_code = True
            i += 1; continue
        if in_code:
            code.append(line); i += 1; continue
        if not line.strip():
            i += 1; continue
        if line.startswith("|") and i + 1 < len(lines) and re.match(r"^\s*\|?[\s:\-|]+\|?\s*$", lines[i+1]):
            rows = []
            while i < len(lines) and lines[i].startswith("|"):
                row = [x.strip() for x in lines[i].strip("|").split("|")]
                if not all(re.fullmatch(r"[\s:\-]+", x or "-") for x in row):
                    rows.append(row)
                i += 1
            if rows:
                cols = max(map(len, rows))
                table = doc.add_table(rows=0, cols=cols); table.style = "Table Grid"
                for ri, row in enumerate(rows):
                    cells = table.add_row().cells
                    for ci in range(cols):
                        cells[ci].text = row[ci] if ci < len(row) else ""
                        if ri == 0:
                            sh = OxmlElement("w:shd"); sh.set(qn("w:fill"), "E8EEF5")
                            cells[ci]._tc.get_or_add_tcPr().append(sh)
                        for p in cells[ci].paragraphs:
                            for r in p.runs:
                                style_run(r, size=9, bold=(ri == 0))
            continue
        h = re.match(r"^(#{1,6})\s+(.*)", line)
        if h:
            p = doc.add_heading(level=min(len(h.group(1)), 3))
            add_inline(p, h.group(2)); i += 1; continue
        if re.match(r"^\s*[-*]\s+", line):
            p = doc.add_paragraph(style="List Bullet")
            add_inline(p, re.sub(r"^\s*[-*]\s+", "", line)); i += 1; continue
        if re.match(r"^\s*\d+[.)]\s+", line):
            p = doc.add_paragraph(style="List Number")
            add_inline(p, re.sub(r"^\s*\d+[.)]\s+", "", line)); i += 1; continue
        p = doc.add_paragraph(); add_inline(p, line); i += 1
    if in_code and code:
        p = doc.add_paragraph()
        r = p.add_run("\n".join(code)); style_run(r, "Consolas", 8.5)
    doc.save(out)
    print(out)

if __name__ == "__main__":
    main()
