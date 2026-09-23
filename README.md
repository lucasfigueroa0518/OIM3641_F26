# Lucas Figueroa's OIM3641 F26 Repo

This repository is for Lucas to manage classwork and assignments for OIM3641. It is a fork of the course repo ([mjmacarty/OIM3641_F26](https://github.com/mjmacarty/OIM3641_F26)). The instructor repo is set as the `upstream` remote so you can pull class updates into this fork.

## Skills

- SQL
- JSON
- UI and UX design
- Agentic orchestration and feedback loops

## How this repo is organized

Work lives on the `main` branch. There is no separate production/feature/dev branch workflow—assignments and demos are committed directly as the course progresses.

| Location | Contents |
| --- | --- |
| Repo root | Numbered course files (`01-` … `06-`): Python scripts, Jupyter notebooks, and small demos (LLM calls, LlamaIndex, Streamlit, and related exercises) |
| `data/` | Data files used by assignments (for example, `desolation_row.txt`) |
| Standalone scripts | `loan_pmt.py`, `OOP Python Course.py`, and similar one-off exercises alongside the numbered modules |

Git remotes:

- **origin** — [lucasfigueroa0518/OIM3641_F26](https://github.com/lucasfigueroa0518/OIM3641_F26) (your fork)
- **upstream** — [mjmacarty/OIM3641_F26](https://github.com/mjmacarty/OIM3641_F26) (course repo; use when pulling instructor updates)

## Clone and run locally

```bash
git clone https://github.com/lucasfigueroa0518/OIM3641_F26.git
cd OIM3641_F26
python -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate
```

Install packages as needed for the script or notebook you are running (for example `python-dotenv`, `google-genai`, `streamlit`, `pandas`). Some demos expect a `.env` file with API keys—see each file for details.

## Links

- [LinkedIn](https://www.linkedin.com/in/lucas-figueroa-705382243/)
- [Portfolio](https://www.heliosgroup.ai/)
