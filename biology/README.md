# Biology worksheet diagrams (sections 3.3–3.10)

Exam-style line diagrams: thin black outlines, flat colour only, white background, clear labels.

- `svg/` holds the vector source of each diagram. It scales cleanly and is the best choice for a PDF.
- `png/` holds 2× raster copies of the same diagrams.

To change a diagram, edit `build_diagrams.py`, then run:

    python3 build_diagrams.py && ./render_png.sh

`render_png.sh` uses headless Chromium and Pillow.
