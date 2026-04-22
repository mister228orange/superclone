# 🔮 Superclone

[![PyPI version](https://badge.fury.io/py/superclone.svg)](https://badge.fury.io/py/superclone)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

**Superclone** clones any Git repository and automatically generates an `AI_doc.md` summary using a local LLM via [Ollama](https://ollama.com/). It’s like `git clone` with an AI-powered tour guide.

---

## ✨ Features

- 🚀 **Shallow clone** (`--depth 1`) for speed  
- 🤖 **LLM‑generated documentation** – Understand a repo at a glance  
- 🔧 **Configurable** via CLI flags or environment variables  
- 📁 **Respects `.gitignore`** – adds `AI_doc.md` automatically  
- ⚡ **Pre‑flight checks** – ensures Ollama is ready before cloning  
- 📦 **Simple installation** – one command with `uv` or `pipx`

---

## 📋 Prerequisites

- [Git](https://git-scm.com/) installed and in your `PATH`
- [Ollama](https://ollama.com/) running locally (`ollama serve`)
- A compatible model pulled (e.g., `ollama pull llama3`)

---

## 📦 Installation

### Using `uv` (recommended)

```bash
uv tool install superclone
```


### Or use direct github way

```bash
uv tool install git+https://github.com/mister228orange/superclone.git
```
