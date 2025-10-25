# Thesis Documents

## 📄 Files

- `thesis.tex` - Complete thesis document (LaTeX)
- `presentation.tex` - Presentation slides (LaTeX Beamer)
- `references.bib` - Bibliography
- `THESIS_SUMMARY.md` - Quick summary for professor

## 🔨 How to Compile

### Compile Thesis (PDF):

```bash
cd /Users/amansharma/Desktop/Thesis/thesis

# Compile with biber for references
pdflatex thesis.tex
biber thesis
pdflatex thesis.tex
pdflatex thesis.tex

# Output: thesis.pdf
```

### Compile Presentation:

```bash
pdflatex presentation.tex
pdflatex presentation.tex

# Output: presentation.pdf
```

### Or use online: Overleaf

1. Go to https://www.overleaf.com
2. Create new project
3. Upload `thesis.tex`, `references.bib`
4. Click "Recompile"
5. Download PDF

## 📊 Current Status

### Completed Sections:
- ✅ Abstract (complete)
- ✅ Introduction (complete)
- ✅ Background and Related Work (outline complete)
- ✅ System Design (complete)
- ✅ Implementation (complete)
- ✅ Experimental Setup (complete)
- ✅ Initial Results (complete)
- ✅ Conclusion (complete)

### Marked "TO BE ADDED":
- Detailed literature review tables
- Baseline comparison experiments
- Public dataset evaluation (LFW, WFLW)
- Robustness analysis details
- Additional plots and figures
- Actual MAX78000 deployment (if time permits)

## 📏 Current Page Count

**Estimated: ~40-50 pages** (with TO BE ADDED sections filled: 80-100 pages)

## 📧 Sending to Professor

Email this:
- `thesis.pdf` (compiled from thesis.tex)
- `presentation.pdf` (compiled from presentation.tex)
- Mention sections marked "TO BE ADDED"
- Highlight completed work (system implementation, initial results)



