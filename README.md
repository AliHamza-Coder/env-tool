<div align="center">
  <img src="https://img.shields.io/github/license/AliHamza-Coder/env-tool?color=blue&style=for-the-badge" alt="License" />
  <img src="https://img.shields.io/github/languages/code-size/AliHamza-Coder/env-tool?color=green&style=for-the-badge" alt="Code Size" />
  <img src="https://img.shields.io/github/last-commit/AliHamza-Coder/env-tool?color=orange&style=for-the-badge" alt="Last Commit" />
  <img src="https://img.shields.io/badge/platform-Windows%20%7C%20Linux%20%7C%20macOS-blue?style=for-the-badge" alt="Platform" />
  <img src="https://img.shields.io/badge/version-1.4.0-blue?style=for-the-badge" alt="Version" />
</div>

<br />

<div align="center">
  <h1 align="center">🐍 Env Tool</h1>
  <p align="center">
    <strong>The Professional Python Virtual Environment Manager</strong>
    <br />
    <em>One Command to rule your environments. Zero manual setup. Pure Python magic.</em>
  </p>
</div>

---

## 🚀 One-Command Installation

Run the following command in your terminal to install **Env Tool** instantly:

### **Windows (PowerShell)**

```powershell
iwr https://raw.githubusercontent.com/AliHamza-Coder/env-tool/main/install.ps1 | iex
```

### **Linux / macOS (Bash)**

```bash
curl -sSL https://raw.githubusercontent.com/AliHamza-Coder/env-tool/main/install.sh | bash
```

---

## 🌟 Why Env Tool?

Env Tool automates the tedious parts of Python development. Whether you're on Windows, Linux, or macOS, the experience is identical and lightning fast.

| Feature             |   Env Tool   |         Manual Method         |
| ------------------- | :----------: | :---------------------------: |
| venv Creation       |   ✅ `env`   |    ❌ `python -m venv ...`    |
| Direct Execution    | ✅ `env run` | ❌ `source ... && python ...` |
| Auto-activation     |    ✅ Yes    |       ❌ Path specific        |
| Pip & Tools Upgrade |   ✅ Auto    |           ❌ Manual           |
| Smart Notifications |    ✅ Yes    |     ❌ Outdated packages      |
| Cross-Platform      |    ✅ Yes    |    ❌ OS specific scripts     |

---

### 🌍 Global Environment Management

Save space by sharing virtual environments across multiple projects.

| Command            | Action                                                         | Example                |
| :----------------- | :------------------------------------------------------------- | :--------------------- |
| **`env g list`**   | **Storefront**: View all centrally stored global environments. | `env g list`           |
| **`env g create`** | **Birth**: Create a new venv in the central master store.      | `env g create web-dev` |
| **`env g use`**    | **Link**: Connect your current project to a global venv.       | `env g use web-dev`    |
| **`env g clean`**  | **Purge**: Delete specific or all global environments.         | `env g clean --all`    |

### 🛠️ Core Commands

| Command          | Description                                                                      | Usage                   |
| ---------------- | -------------------------------------------------------------------------------- | ----------------------- |
| `env`            | **Magic Setup**: Creates venv, upgrades pip, and alerts for dependencies.        | `env`                   |
| `env a`          | **Activate**: Get the activation command for your current shell.                 | `env a`                 |
| `env d`          | **Deactivate**: Get the deactivation command.                                    | `env d`                 |
| `env run`        | **Execute**: Run code inside venv (supports **Shell & .env**).                   | `env run --shell "..."` |
| `env init`       | **Project Bootstrap**: Automatically creates `src/`, `tests/`, and `.gitignore`. | `env init`              |
| `env clean`      | **Deep Reset**: Safely delete `myenv` and all `__pycache__` folders.             | `env clean`             |
| `env list`       | **Inspect**: List packages or view a **Hierarchy Tree**.                         | `env list --tree`       |
| `env freeze`     | **Dependency Lock**: Quickly export all packages to `requirements.txt`.          | `env freeze`            |
| `env update`     | **Power Sync**: Synchronize and upgrade all packages at once.                    | `env update`            |
| `env completion` | **Setup**: Enable Tab-Completion for your terminal.                              | `env completion`        |
| `env help`       | **Guidance**: Pro-grade command reference.                                       | `env help`              |
| `env net`        | **Connection**: Check if your device is Online or Offline.                       | `env net`               |
| `env version`    | **Smart Info**: Check version & get update notifications.                        | `env version`           |
| `env upgrade`    | **Auto-Update**: Keep Env Tool itself on the cutting edge.                       | `env upgrade`           |
| `env uninstall`  | **Safe Removal**: Securely remove Env Tool from your system.                     | `env uninstall`         |

---

## 📂 Path Configuration Guide

**Env Tool** is smart about how it finds your environments.

### 1. Smart Detection (New!)

When you run `env`, it automatically looks for existing environments in your project. It prioritizes them in this order:

1.  **Linked**: Via `.envlink` file.
2.  **Standards**: Any folder named `.venv`, `venv`, `env`, or `myenv`.
3.  **Creation**: If none found, it creates `myenv`.

---

## ⚡ Power Features (v1.4.0)

### 1. Dependency Tree

Visualize your project structure instantly:

```bash
env list --tree
```

### 2. Shell Execution & Scaling

Need to use pipes (`|`) or redirects (`>`)? Use the `--shell` flag:

```bash
env run --shell "python app.py | grep 'Error' > log.txt"
```

### 3. Environment Variables

Env Tool automatically loads your **`.env`** file before running any command via `env run`. No extra config needed.

### 4. Custom Python Runtime

Want to use a specific Python version for your venv?

```bash
env --python 3.10
```

### 5. Tab Completion

Tired of typing? Set up completion:

```bash
env completion
```

---

### Understanding Environment Paths

Here is how the paths look in different scenarios:

### 1. Local Environment (The Default)

When you run `env`, it creates a folder named `myenv` inside your project.

- **Project Path**: `C:\Projects\Alpha\`
- **Venv Path**: `C:\Projects\Alpha\myenv\`
- **Best for**: Single-use projects or projects with very specific dependencies.

### 2. Global Environment (The Power User Way)

When you use a global environment, your project folder stays clean.

- **Global Store**: `C:\Users\Hamza\.envtool\envs\shared-env\`
- **Your Project**: `D:\Work\Beta\`
- **The Connection**: A hidden `.envlink` file inside `D:\Work\Beta\` tells the tool: _"Use the venv at C:\Users\Hamza\.envtool\envs\shared-env"_.
- **Best for**: Saving disk space on your laptop or working across different drives (C:, D:, USB).

> [!TIP]
> **Switching is Easy**: If you already have a local `myenv` but want to switch to global, just run `env g use <name>`. The tool will prioritize the link!

---

## 🛠️ Advanced Features

### 1. Smart Update Notifications

Env Tool keeps itself and your project on the cutting edge. It automatically pings GitHub for updates and alerts you if a newer version is available.

### 2. Offline Ready

Env Tool is designed for developers on the move. Most features (venv creation, project init, clean, run) work perfectly offline. Network tasks like version checks are gracefully handled.

### 3. Live Progress Monitoring

Powered by **Rich**, Env Tool provides beautiful terminal spinners and status indicators, so you always know exactly what's happening backstage.

### 4. Dependency Controls

No more accidental installations. Env Tool detects your `requirements.txt` and **asks for your confirmation** before installing anything.

---

## 🖥️ Usage Guide

### 1. Zero-Config Setup

Just navigate to any directory and type:

```bash
env
```

It handles the venv creation and pip upgrade. If a `requirements.txt` is found, it will ask if you want to install them.

### 2. Quick Activation

Need to activate your shell?

```bash
env a
```

### 3. No-Activation Workflow

Forget `source myenv/bin/activate`. Just run your code directly:

```bash
env run python main.py
```

### 4. Reset & Refresh

Need to clear your local environment files?

```bash
env clean
```

---

## 🤝 Contributing

We love builders!

1. **Fork** the repository.
2. **Create** your feature branch.
3. **Commit** your magic.
4. **Push** and open a **Pull Request**.

## 📄 License

Distributed under the **MIT License**. See `LICENSE` for more information.

<div align="center">
  <br />
  <strong>⭐ If Env Tool saves you time, consider giving it a Star! ⭐</strong>
  <br />
  <p>Created with ❤️ by <a href="https://github.com/AliHamza-Coder">Ali Hamza</a></p>
</div>
