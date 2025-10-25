# Adding Images to Presentation

## 📸 Your Demo Screenshot

I've created a **short, concise presentation** in `presentation_short.tex` (only 11 slides!)

---

## How to Add Your Demo Image:

### Step 1: Save Your Screenshot

Save the demo screenshot as:
```
/Users/amansharma/Desktop/Thesis/thesis/demo_screenshot.png
```

The image shows:
- Your face with facial keypoints (green/colored dots)
- System interface
- Perfect for showing the working system!

### Step 2: Presentation Already References It!

The presentation slide says:
```latex
\includegraphics[width=0.85\textwidth]{demo_screenshot.png}
```

Just save your screenshot with that filename in the `thesis/` folder!

---

## 📊 New Presentation Structure (SHORT!)

**Total: Only 11 slides** (was 20+ before)

1. Title
2. Problem (1 slide)
3. What is HDC? (1 slide)
4. System Pipeline (1 slide)
5. **Live Demo Screenshot** (1 slide) ← YOUR IMAGE HERE
6. Training (1 slide)
7. Continual Learning (1 slide)
8. Results (1 slide)
9. Multi-Face (1 slide - optional)
10. Contributions (1 slide)
11. Conclusion (1 slide)
12. Thank you

**Much more concise and focused!**

---

## 🎨 To Add More Images:

If you have other screenshots, add them like this:

```latex
\begin{frame}{Your Title}
\begin{center}
\includegraphics[width=0.8\textwidth]{your_image.png}
\end{center}
\end{frame}
```

Just save images in the `thesis/` folder with the same name!

---

## 🚀 Quick Start:

1. **Save screenshot as:** `thesis/demo_screenshot.png`
2. **Compile:** Use Overleaf or run:
   ```bash
   cd thesis
   pdflatex presentation_short.tex
   ```
3. **Done!** You have a concise presentation with your demo image!

---

## 💡 Recommended Images to Include:

From your work, take screenshots of:
1. ✅ **Demo with keypoints** (you already have this!)
2. Multi-face detection (if you tested with multiple people)
3. System statistics output
4. Enrollment progress bar

All optional - the presentation works with just the one image you have!



