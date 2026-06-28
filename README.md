# clean-beamer

A minimalist Beamer theme — a LaTeX port of the Typst
[`touying-quarto-clean`](https://typst.app/universe/package/touying-quarto-clean/)
slide theme.

## Use

Put `beamerthemeClean.sty` next to your `.tex` file and:

```latex
\documentclass[aspectratio=169]{beamer}
\usepackage[sfdefault, light]{roboto}
\usepackage[scaled]{FiraMono}
\usetheme{Clean}
```

See `demo.tex` for a full example.

## Building

This repo does not assume any local LaTeX install. Every push is compiled by
GitHub Actions, which uploads the resulting `demo.pdf` as a build artifact
(Actions → latest run → Artifacts → `demo-pdf`).

To build locally anyway: `latexmk -pdf demo.tex`.
