<p align="center">
   <img src="data/logo.png" alt="Description of image" width="500" style="border-radius: 20%">
</p>

# BlueClawAI

---

## Before you begin (required)

Install and verify these **before** you clone the project or run any install script.

### 1. Python

- Install a recent **Python 3** from [python.org](https://www.python.org/downloads/) or your OS package manager.
- Confirm it works:

```bash
python3 --version
```

The included macOS install scripts call **`python3.14`**. If your system uses another command (for example `python3` or `python3.12`), edit the install script and replace `python3.14` with the interpreter you use, or install Python 3.14 to match.

### 2. Ollama

- Install **Ollama** from [https://ollama.com](https://ollama.com).
- Start the Ollama service (on macOS, the Ollama app does this; on Linux you may run `ollama serve` in a terminal).
- Pull the models the app expects (defaults in the server use these names):

```bash
ollama pull llama3.1
ollama pull qwen2.5:3b
```

---

## Install from GitHub (clone + bash)

### 1. Clone the repository

```bash
git clone https://github.com/daoduylam2008/BlueClawAI.git
cd BlueClawAI
```

*(If you prefer a ZIP, download it from the repository’s **Code → Download ZIP** page and extract it, then `cd` into the extracted folder.)*

### 2. Run the install script (macOS)

From the **root of the cloned project**, run the server install script so `blueclawai`, `app.py`, and the `server` package are copied under `~/.blueclawai` and your shell `PATH` is updated:

```bash
bash "server_instal (mac).sh"
```

```bash
source ~/.zprofile   # zsh (default on recent macOS)
# and/or
source ~/.bash_profile
```

**What this does:** installs Python dependencies from `server/requirements.txt`, creates `~/.blueclawai`, copies `blueclawai`, `app.py`, and `server/` there, and appends `~/.blueclawai` to your `PATH`.

> **Note:** There is also `client_install (mac).bash`, which only copies the CLI launcher and `app.py` (no `server/` tree). Use **`server_instal (mac).sh`** if you want the full local server and the `start_server` workflow.

---

## Using BlueClawAI with `blueclawai`

The `blueclawai` command is a small CLI. After installation, ensure **Ollama is running** and you have pulled the models (see above).

### Where to run commands

The server and TUI expect to find `server/` and `app.py` next to each other. After the full install, that layout lives under **`~/.blueclawai`**. Open a terminal and:

```bash
cd ~/.blueclawai
```

Use that directory whenever you run `blueclawai` in the steps below.

### Show help

```bash
blueclawai --help
```

### Start the API server (port 8080)

In **one** terminal (from `~/.blueclawai`):

```bash
blueclawai start_server
```

Leave this running. It serves the LLM backend used by the terminal UI and by `request`.

### Open the terminal chat UI

In **another** terminal (from `~/.blueclawai`):

```bash
blueclawai run
```

This launches the Textual-based interface. Type a message and submit to chat with the model (the UI talks to `http://127.0.0.1:8080`).

### Send a single question from the shell

With the server already running:

```bash
blueclaw

# To run with a query to server
blueclaw request <query>
```

---

## OpenWeather API key (weather tool)

The agent can call OpenWeatherMap when users ask about weather. That requires a free API key.
 
## API Keys
 
### OpenWeather API Key
 
BlueClaw uses the OpenWeather API for weather-related features. You'll need a free API key to enable this.
 
1. Go to [https://home.openweathermap.org/users/sign_up](https://home.openweathermap.org/users/sign_up) and create a free account.
2. After signing in, navigate to **API Keys** at [https://home.openweathermap.org/api_keys](https://home.openweathermap.org/api_keys).
3. Copy your default key or generate a new one.
4. In the root of the project, create a `.env` file if it doesn't already exist:
 
```bash
touch .env
```
 
5. Open the `.env` file and add your API key:
 
```env
OPENWEATHER_API_KEY=your_api_key_here
```
 
6. Save the file. The server will automatically load it on startup.
 
> **Note:** Never commit your `.env` file to version control. Make sure `.env` is listed in your `.gitignore`.
 
> **Note:** Newly created API keys may take up to a few hours to activate.
 
---
## Setting Up Ollama & Llama 3.1
 
BlueClaw uses [Ollama](https://ollama.com) to run the Llama 3.1 language model locally.
 
### 1. Download and Install Ollama
 
Go to [https://ollama.com/download](https://ollama.com/download) and download the installer for your OS:
 
| OS | Instructions |
|----|-------------|
| macOS | Download the `.dmg`, open it, and drag Ollama to your Applications folder |
| Windows | Download and run the `.exe` installer |
| Linux | Run the install script in your terminal: |
 
```bash
# Linux only
curl -fsSL https://ollama.com/install.sh | sh
```
 
Verify the installation:
 
```bash
ollama --version
```
 
### 2. Pull the Llama 3.1 Model
 
Once Ollama is installed, download the Llama 3.1 model:
 
```bash
ollama pull llama3.1
```
 
> This will download several gigabytes of model weights. Make sure you have a stable internet connection and enough disk space (~5 GB).
 
### 3. Verify the Model is Available
 
```bash
ollama list
```
 
You should see `llama3.1` listed. Ollama must be running in the background before you start the BlueClaw server.
 
### 4. Start Ollama (if not already running)
 
```bash
ollama serve
```
 
---

## Troubleshooting

| Issue | What to check |
|--------|----------------|
| `blueclawai: command not found` | Reload `~/.zprofile` / `~/.bash_profile` or open a new terminal; confirm `~/.blueclawai` is on `PATH`. |
| Connection errors in the UI or `request` | Run `blueclawai start_server` from `~/.blueclawai` and ensure nothing else uses port **8080**. |
| Model errors from Ollama | Ollama is running; you ran `ollama pull` for the model names in `server/llm.py`. |
| `python3.14` not found | Install Python 3.14 or edit the install script and `parser.py` to use your `python3` command. |

---

## Author

**Dao Duy Lam** — [@daoduylam2008](https://github.com/daoduylam2008)
