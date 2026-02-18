<div align="center">
  <img src="https://img.shields.io/github/license/AliHamza-Coder/env-tool?color=blue&style=for-the-badge" alt="License" />
  <img src="https://img.shields.io/github/languages/code-size/AliHamza-Coder/env-tool?color=green&style=for-the-badge" alt="Code Size" />
  <img src="https://img.shields.io/github/last-commit/AliHamza-Coder/env-tool?color=orange&style=for-the-badge" alt="Last Commit" />
  <img src="https://img.shields.io/badge/platform-Windows%20%7C%20Linux%20%7C%20macOS-blue?style=for-the-badge" alt="Platform" />
  <img src="https://img.shields.io/badge/version-1.2.0-blue?style=for-the-badge" alt="Version" />
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

Env Tool automates the tedious parts of Python development. Whether you're on Windows, Linux, or macOS, the experience is identical.

| Feature         |    Env Tool     |      Manual Method      |
| --------------- | :-------------: | :---------------------: |
| venv Creation   |    ✅ `env`     | ❌ `python -m venv ...` |
| Auto-activation |     ✅ Yes      |    ❌ Path specific     |
| Pip Upgrade     |     ✅ Auto     |        ❌ Manual        |
| Dependency Sync | ✅ `env update` |      ❌ Many steps      |
| Cross-Platform  |     ✅ Yes      |     ❌ Script heavy     |

---

## 🎯 Commands

| Command           | Description                                                             | Usage             |
| ----------------- | ----------------------------------------------------------------------- | ----------------- |
| `env`             | **Magic Setup**: Creates venv, upgrades pip, and installs dependencies. | `env`             |
| `env freeze`      | **Dependency Lock**: Quickly export all packages to `requirements.txt`. | `env freeze`      |
| `env update`      | **Power Sync**: Synchronize and upgrade all packages at once.           | `env update`      |
| `env version`     | **System Info**: Get detailed version info for Env Tool and Python.     | `env version`     |
| `env self-update` | **Auto-Upgrade**: Keep Env Tool itself on the cutting edge.             | `env self-update` |

---

## 🖥️ Usage Guide

### 1. New Project Setup

Navigate to your project folder and simply type:

```bash
env
```

Env Tool will automatically detect your project, create `myenv`, upgrade your tools, and get you ready for code in seconds.

### 2. Freeze Dependencies

Done installing packages? Lock them down:

```bash
env freeze
```

### 3. Update Environment

Want the latest versions of your requirements?

```bash
env update
```

---

## 🛠️ Technical Specifications

- **Powered by Click**: Professional CLI interface with rich error handling.
- **Venv Standard**: Built on the native `venv` library for maximum stability.
- **Native Performance**: Light-weight and lightning fast.
- **Scalable**: Handles everything from tiny scripts to massive mono-repos.

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
