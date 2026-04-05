# Lit2Lab

Lit2Lab is an AI research copilot that turns paper abstracts into concise summaries, key variables, follow-up experiments, and reviewer-style critiques.

## Demo

[Watch the demo video](https://www.youtube.com/watch?v=-aJP174spK0)

## What it does

Given a paper abstract or excerpt, Lit2Lab generates:

- a clear summary of the main question, method, and finding
- the key variables or concepts in the study
- a proposed next experiment
- a reviewer-style critique

The goal is to help researchers move faster from reading literature to planning the next step.

## Features

- Paste a paper abstract or excerpt
- Generate structured research insights
- Load example papers for quick demos
- Get a suggested follow-up experiment
- Get a short reviewer-style critique

## Tech stack

- Jac
- Python
- Claude
- Anthropic API

## Project structure

- `main.jac` - main app frontend and backend interface
- `anthropic_helper.py` - Claude API helper and response parsing
- `jac.toml` - Jac project configuration
- `components/` - UI components
- `assets/` - static assets

## How to run

1. Clone the repository
2. Set your Anthropic API key in your environment
3. Start the Jac dev server

```bash
export ANTHROPIC_API_KEY="your_api_key_here"
jac start main.jac

Then open:

`http://localhost:8000/`

## Example workflow

1. Paste a scientific paper abstract
2. Click **Generate Research Insight**
3. Read the summary, key variables, next experiment, and critique

## Why we built it

Reading papers is only the first step. Researchers still have to manually figure out what matters most and what experiment should come next. Lit2Lab is designed to shorten that gap.

## Future work

- better domain-specific suggestions
- support for organizing multiple paper analyses
- improved export and sharing options

## License

MIT
