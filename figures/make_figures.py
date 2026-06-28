#!/usr/bin/env python3
"""Generate the example figure assets used by demo.tex.

Pure Python standard library only (zlib + struct) — no matplotlib / PIL — so it
runs anywhere without extra installs. Produces:

  example-plot.png    a minimalist raster line plot in the Clean theme colours
  example-diagram.pdf a tiny vector PDF diagram (three theme-coloured boxes)

These exist purely to prove that \\includegraphics handles both a .png (raster)
and a .pdf (vector) figure in the CI build. Regenerate with:

    python3 figures/make_figures.py
"""

import os
import struct
import zlib

HERE = os.path.dirname(os.path.abspath(__file__))

# Theme colours (RGB) -------------------------------------------------------
JET = (0x13, 0x15, 0x16)
PRIMARY = (0x10, 0x78, 0x95)
SECONDARY = (0x9A, 0x25, 0x15)
WHITE = (0xFF, 0xFF, 0xFF)


# ---------------------------------------------------------------------------
# PNG: a small line plot drawn by hand into an RGB pixel buffer
# ---------------------------------------------------------------------------
def make_png(path, width=640, height=400):
    # white canvas
    px = bytearray(WHITE * (width * height))

    def put(x, y, rgb):
        if 0 <= x < width and 0 <= y < height:
            i = (y * width + x) * 3
            px[i:i + 3] = bytes(rgb)

    def disk(cx, cy, r, rgb):
        for dy in range(-r, r + 1):
            for dx in range(-r, r + 1):
                if dx * dx + dy * dy <= r * r:
                    put(cx + dx, cy + dy, rgb)

    def line(x0, y0, x1, y1, rgb, w=1):
        # Bresenham, thickened by stamping a small disk at each step
        dx, dy = abs(x1 - x0), abs(y1 - y0)
        sx = 1 if x0 < x1 else -1
        sy = 1 if y0 < y1 else -1
        err = dx - dy
        while True:
            disk(x0, y0, w, rgb)
            if x0 == x1 and y0 == y1:
                break
            e2 = 2 * err
            if e2 > -dy:
                err -= dy
                x0 += sx
            if e2 < dx:
                err += dx
                y0 += sy

    # plot frame (axes) with a margin
    ml, mr, mt, mb = 60, 20, 30, 50
    x0, x1 = ml, width - mr
    y0, y1 = mt, height - mb
    line(x0, y1, x1, y1, JET, 1)   # x axis
    line(x0, y0, x0, y1, JET, 1)   # y axis

    # data: a gentle upward curve, mapped into the plot area
    data = [0.10, 0.18, 0.15, 0.30, 0.42, 0.38, 0.55, 0.68, 0.72, 0.85]
    n = len(data)
    pts = []
    for k, v in enumerate(data):
        x = x0 + round((x1 - x0) * k / (n - 1))
        y = y1 - round((y1 - y0) * v)
        pts.append((x, y))

    for (xa, ya), (xb, yb) in zip(pts, pts[1:]):
        line(xa, ya, xb, yb, PRIMARY, 2)
    for (x, y) in pts:
        disk(x, y, 4, PRIMARY)

    _write_png(path, width, height, px)


def _write_png(path, width, height, px):
    # add the per-row filter byte (0 = none)
    raw = bytearray()
    stride = width * 3
    for y in range(height):
        raw.append(0)
        raw.extend(px[y * stride:(y + 1) * stride])

    def chunk(tag, data):
        out = struct.pack(">I", len(data)) + tag + data
        out += struct.pack(">I", zlib.crc32(tag + data) & 0xFFFFFFFF)
        return out

    sig = b"\x89PNG\r\n\x1a\n"
    ihdr = struct.pack(">IIBBBBB", width, height, 8, 2, 0, 0, 0)  # 8-bit RGB
    idat = zlib.compress(bytes(raw), 9)
    with open(path, "wb") as f:
        f.write(sig)
        f.write(chunk(b"IHDR", ihdr))
        f.write(chunk(b"IDAT", idat))
        f.write(chunk(b"IEND", b""))


# ---------------------------------------------------------------------------
# PDF: a minimal one-page vector diagram (three filled, labelled boxes)
# ---------------------------------------------------------------------------
def make_pdf(path, width=300, height=150):
    def rgb(c):
        return " ".join(f"{v / 255:.3f}" for v in c)

    boxes = [
        (20, 55, PRIMARY, "Clean"),
        (120, 55, SECONDARY, "Beamer"),
        (220, 55, JET, "Theme"),
    ]
    bw, bh = 60, 40

    ops = []
    for (x, y, color, label) in boxes:
        ops.append(f"{rgb(color)} rg")
        ops.append(f"{x} {y} {bw} {bh} re f")
        ops.append("1 1 1 rg")              # white label text
        ops.append("BT /F1 11 Tf")
        ops.append(f"{x + 8} {y + 15} Td ({label}) Tj ET")
    # connecting arrows between boxes
    ops.append("0.2 0.2 0.2 RG 1 w")
    ops.append(f"{20 + bw} {55 + bh // 2} m {120} {55 + bh // 2} l S")
    ops.append(f"{120 + bw} {55 + bh // 2} m {220} {55 + bh // 2} l S")
    stream = "\n".join(ops).encode("latin-1")

    objs = []
    objs.append(b"<< /Type /Catalog /Pages 2 0 R >>")
    objs.append(b"<< /Type /Pages /Kids [3 0 R] /Count 1 >>")
    objs.append(
        f"<< /Type /Page /Parent 2 0 R /MediaBox [0 0 {width} {height}] "
        f"/Resources << /Font << /F1 5 0 R >> >> /Contents 4 0 R >>".encode()
    )
    objs.append(
        b"<< /Length " + str(len(stream)).encode() + b" >>\nstream\n"
        + stream + b"\nendstream"
    )
    objs.append(b"<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica >>")

    out = bytearray(b"%PDF-1.4\n")
    offsets = []
    for i, body in enumerate(objs, start=1):
        offsets.append(len(out))
        out += f"{i} 0 obj\n".encode() + body + b"\nendobj\n"

    xref_pos = len(out)
    out += f"xref\n0 {len(objs) + 1}\n".encode()
    out += b"0000000000 65535 f \n"
    for off in offsets:
        out += f"{off:010d} 00000 n \n".encode()
    out += (
        f"trailer\n<< /Size {len(objs) + 1} /Root 1 0 R >>\n"
        f"startxref\n{xref_pos}\n%%EOF\n"
    ).encode()

    with open(path, "wb") as f:
        f.write(out)


if __name__ == "__main__":
    make_png(os.path.join(HERE, "example-plot.png"))
    make_pdf(os.path.join(HERE, "example-diagram.pdf"))
    print("wrote example-plot.png and example-diagram.pdf")
