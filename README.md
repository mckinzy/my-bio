# my-bio

A polished personal biography website designed as a single-page profile for `Mckinzy`.

This repository contains a complete static portfolio site with:
- a responsive `index.html` landing page,
- custom visual styling in `styles.css`,
- a prompt template for generating expanded biography content,
- a simple Python script to output prompt content into a generated file,
- and a small local server helper script for previewing the site.

## Project purpose

The site is built to present a high-detail, thoughtful professional profile. It is structured to communicate identity, journey, work, values, and contact information in an elegant one-page experience.

## Files and structure

- `index.html`
  - Main static web page.
  - Contains the site structure: hero section, about, journey, work, values, contact, and navigation.
  - Uses a modern, minimal layout with semantic HTML.

- `styles.css`
  - Page styling for typography, spacing, cards, navigation, buttons, and responsive layout.
  - Uses a dark theme with accent colors and smooth controls.

- `prompts/profile_prompt_loop.md`
  - Prompt template for an autoprompting workflow.
  - Defines a writing mission, narrative structure, and output expectations.
  - Intended for iterative profile copy generation.

- `scripts/auto_prompt_loop.py`
  - Python helper script.
  - Reads `prompts/profile_prompt_loop.md` and writes its contents to `generated/profile_loop_output.md`.
  - Ensures the generated directory exists before writing.

- `scripts/serve.sh`
  - Bash helper script.
  - Starts a local HTTP server on port `8000` from the repository root.
  - Useful for previewing the static site in a browser.

- `generated/profile_loop_output.md`
  - Output file created by `scripts/auto_prompt_loop.py`.
  - Stores the prompt content from `prompts/profile_prompt_loop.md`.

## Setup and requirements

This project is static and requires no build tools to render the site.

Recommended environment:
- Linux, macOS, or Windows
- Python 3 installed
- A modern browser for previewing the site

## Usage

1. Preview the site locally:

   ```bash
   ./scripts/serve.sh
   ```

2. Open your browser and visit:

   ```text
   http://localhost:8000
   ```

3. Regenerate the prompt output file if needed:

   ```bash
   python3 scripts/auto_prompt_loop.py
   ```

   This writes the prompt content into `generated/profile_loop_output.md`.

4. Edit the profile copy or site design by modifying:
   - `index.html` for the page content,
   - `styles.css` for styling and layout,
   - `prompts/profile_prompt_loop.md` for prompt structure and messaging.

## Development notes

- `index.html` is intentionally simple and self-contained, so the page can be served from any static host.
- The `scripts` folder contains utilities rather than production code.
- The generated folder is used for output artifacts and can be regenerated at any time.

## Notes

- The current site content is written in a confident, reflective brand voice tailored for a professional biography.
- The prompt loop is intended to help expand the profile content into a more detailed storytelling format.
- If you want to extend the site, consider adding sections such as "Accomplishments", "Skills", or "Featured Work".

---

If you need help customizing the profile content or adding new sections, I can update the HTML, CSS, and README accordingly.