<div align="center">
  <img src="https://img.shields.io/github/license/AliHamza-Coder/env-tool?color=blue&style=for-the-badge" alt="License" />
  <img src="https://img.shields.io/github/languages/code-size/AliHamza-Coder/env-tool?color=green&style=for-the-badge" alt="Code Size" />
  <img src="https://img.shields.io/github/last-commit/AliHamza-Coder/env-tool?color=orange&style=for-the-badge" alt="Last Commit" />
  <img src="https://img.shields.io/badge/platform-Windows%20%7C%20Linux%20%7C%20macOS-blue?style=for-the-badge" alt="Platform" />
  <img src="https://img.shields.io/badge/version-1.3.0-blue?style=for-the-badge" alt="Version" />
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

## 🎯 Commands

| Command         | Description                                                                      | Usage                   |
| --------------- | -------------------------------------------------------------------------------- | ----------------------- |
| `env`           | **Magic Setup**: Creates venv, upgrades pip, and alerts for dependencies.        | `env`                   |
| `env a`         | **Activate**: Get the activation command for your current shell.                 | `env a`                 |
| `env d`         | **Deactivate**: Get the deactivation command.                                    | `env d`                 |
| `env run`       | **Direct Execute**: Run any command inside the venv without activating.          | `env run python app.py` |
| `env init`      | **Project Bootstrap**: Automatically creates `src/`, `tests/`, and `.gitignore`. | `env init`              |
| `env clean`     | **Deep Reset**: Safely delete `myenv` and all `__pycache__` folders.             | `env clean`             |
| `env freeze`    | **Dependency Lock**: Quickly export all packages to `requirements.txt`.          | `env freeze`            |
| `env update`    | **Power Sync**: Synchronize and upgrade all packages at once.                    | `env update`            |
| `env version`   | **Smart Info**: Check version & get update notifications.                        | `env version`           |
| `env upgrade`   | **Auto-Update**: Keep Env Tool itself on the cutting edge.                       | `env upgrade`           |
| `env uninstall` | **Clean Removal**: Completely remove Env Tool from your system.                  | `env uninstall`         |

---

## 🛠️ Advanced Features

### 1. Smart Update Notifications

Env Tool keeps itself and your project on the cutting edge. It automatically pings GitHub for updates and alerts you if a newer version is available, even with robust offline handling.

### 2. Live Progress Monitoring

Powered by **Rich**, Env Tool provides beautiful terminal spinners and status indicators, so you always know exactly what's happening backstage.

### 3. Dependency Controls

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
