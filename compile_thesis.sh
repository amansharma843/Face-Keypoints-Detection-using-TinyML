#!/bin/bash
# Compile thesis and presentation to PDF

echo "📚 Compiling Thesis Documents"
echo "=============================="

cd "$(dirname "$0")"

# Compile thesis
echo ""
echo "1️⃣ Compiling thesis.tex..."
pdflatex -interaction=nonstopmode thesis.tex > /dev/null 2>&1
biber thesis > /dev/null 2>&1
pdflatex -interaction=nonstopmode thesis.tex > /dev/null 2>&1
pdflatex -interaction=nonstopmode thesis.tex > /dev/null 2>&1

if [ -f "thesis.pdf" ]; then
    echo "   ✅ thesis.pdf created!"
    pages=$(pdfinfo thesis.pdf 2>/dev/null | grep Pages | awk '{print $2}')
    echo "   Pages: $pages"
else
    echo "   ❌ Failed to compile thesis.pdf"
fi

# Compile presentation
echo ""
echo "2️⃣ Compiling presentation.tex..."
pdflatex -interaction=nonstopmode presentation.tex > /dev/null 2>&1
pdflatex -interaction=nonstopmode presentation.tex > /dev/null 2>&1

if [ -f "presentation.pdf" ]; then
    echo "   ✅ presentation.pdf created!"
    slides=$(pdfinfo presentation.pdf 2>/dev/null | grep Pages | awk '{print $2}')
    echo "   Slides: $slides"
else
    echo "   ❌ Failed to compile presentation.pdf"
fi

# Clean up auxiliary files
echo ""
echo "3️⃣ Cleaning up..."
rm -f *.aux *.log *.out *.toc *.bbl *.blg *.bcf *.run.xml *.nav *.snm
echo "   ✅ Cleaned auxiliary files"

echo ""
echo "=============================="
echo "✅ Compilation complete!"
echo ""
echo "Generated files:"
ls -lh *.pdf 2>/dev/null | awk '{print "   " $9 " (" $5 ")"}'

echo ""
echo "📧 Ready to send to professor:"
echo "   - thesis.pdf"
echo "   - presentation.pdf"  
echo "   - THESIS_SUMMARY.md"



