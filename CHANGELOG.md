# Changelog

All notable changes to this project are documented here. The format is based on
[Keep a Changelog](https://keepachangelog.com/en/1.1.0/), and this project
adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.2.0] — 2026-06-30

### Fixed
- **Theme no longer hard-fails without `orcidlink`.** `orcidlink` is now loaded
  defensively (`\IfFileExists`), with a no-op `\orcidlink` fallback, so
  `\usetheme{Clean}` works on TeX installs that lack the package — including
  decks that never render an ORCID id.
- **Title slide is now chrome-free.** `\maketitle` renders the title page as a
  `[plain, noframenumbering]` frame: no footer/slide number on the title, and the
  first *content* slide is numbered `1 / N` instead of `2 / N` (matches the Typst
  reference).
- **Example blocks stay on-palette.** `\begin{exampleblock}` previously rendered
  in Beamer's default green; `example text` / block-title colours are now mapped
  to the theme palette (standard = primary, alert = secondary).
- **Author grid alignment.** The final partial row of the author grid is padded
  to a full set of columns, so 5/8/11-author decks no longer drift the last cell
  toward the slide centre.
- **`\institute` no longer silently dropped** when `\cleanauthor` is used: a
  document-level `\institute{...}` now renders beneath the author grid.
- **Level-3 itemize marker** is the primary arrow (matching level 2, as in the
  Typst theme) instead of a dot.
- **Author names** on the title page use Roboto Regular (400) so they sit heavier
  than the light body, matching the reference.

### Changed
- Package version bumped to `v0.2` (`\ProvidesPackage` date `2026/06/30`).
- CI: added an explicit least-privilege `permissions: contents: read` block and a
  `concurrency` group that cancels superseded in-flight runs.

### Added
- Upstream MIT attribution: `reference/LICENSE-upstream` reproduces the
  kazuyanagimoto and Grant McDermott copyright/permission notices, with a
  "License & attribution" section in the README.
- A **Blocks** demo frame exercising `block` / `alertblock` / `exampleblock`.
- This `CHANGELOG.md`.

## [0.1.0]

Initial release: the Clean Beamer theme (`beamerthemeClean.sty`) plus a `demo.tex`
exercising left-aligned frame titles, primary-accent list markers, `x / y` footer,
automatic section slides, a title-page author grid with ORCID badges,
`biblatex-chicago` citations, figure examples, and a GitHub Actions build that
compiles the demo and uploads `demo.pdf`.

[0.2.0]: https://github.com/andrerecio/clean-beamer/releases/tag/v0.2
[0.1.0]: https://github.com/andrerecio/clean-beamer/releases/tag/v0.1
