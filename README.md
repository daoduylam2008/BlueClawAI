<p align="center">
   <img src="data/logo.png" alt="Description of image" width="500" style="border-radius: 20%">
</p>

# BlueClaw

**Local Host Artificial Intelligence** — A locally hosted AI assistant that runs entirely on your own machine, with a Python backend powered by Ollama models and a web-based client interface.

## Overview

BlueClaw lets you run and interact with AI language models locally, without sending data to external APIs. It uses a Python FastAPI server to handle requests

## Features

- **100% Local** — All AI inference runs on your own hardware, keeping your data private
- **Web Client** — Browser-based chat interface served by the local Python server

## Tech Stack

| Layer | Technology |
|-------|-----------|
| Backend / AI Server | Python, FastAPI |
| Web Frontend | Running on your terminal |

## Project Structure

```
BlueClaw/
├── server/             # Python FastAPI backend — serves the AI model and API
├── client/             # Web frontend — browser-based chat interface
└── __pycache__/
```

## Prerequisites

- Python 3.x
- pip
- A compatible GPU (recommended for faster inference) or CPU

## Download & Installation

### Option 1: Clone with Git

```bash
git clone https://github.com/daoduylam2008/BlueClaw.git
cd BlueClaw
```

### Option 2: Download ZIP

1. Go to the [repository page](https://github.com/daoduylam2008/BlueClaw).
2. Click the green **Code** button.
3. Select **Download ZIP**.
4. Extract the ZIP to a folder of your choice.

## Installation

Install the required Python dependencies:

```bash
pip install -r requirements.txt
```


## Setting Up Your PATH

Before running the app, make sure Python and pip are accessible from your terminal.

### Check if Python is already in your PATH

```bash
python --version
# or
python3 --version
```

If you see a version number, you're good to go. If you get a "command not found" error, follow the steps below for your OS.

### Windows

1. Find your Python installation path (typically something like `C:\Users\YourName\AppData\Local\Programs\Python\Python3xx\`).
2. Open **Start** → search for **"Environment Variables"** → click **"Edit the system environment variables"**.
3. Under **System Variables**, select **Path** → click **Edit**.
4. Click **New** and add both:
   ```
   C:\Users\YourName\AppData\Local\Programs\Python\Python3xx\
   C:\Users\YourName\AppData\Local\Programs\Python\Python3xx\Scripts\
   ```
5. Click **OK** and restart your terminal.

### macOS

Add Python to your PATH by editing the appropriate shell config file(s). On macOS you may need to update more than one depending on your shell:

| Shell | Login shell file | Interactive shell file |
|-------|-----------------|----------------------|
| Zsh (default on macOS Catalina+) | `~/.zprofile` | `~/.zshrc` |
| Bash | `~/.bash_profile` | `~/.bashrc` |

Edit the relevant file(s):

```bash
# For Zsh
nano ~/.zprofile

# For Bash
nano ~/.bash_profile
```
Add this line at the bottom (Edit the path to direct to the bin folder):
```bash
export PATH=$PATH":$HOME/bin"
```
Add this line at the bottom (adjust the path to match your Python version):

```bash
export PATH="/usr/local/bin/python3:$PATH"
```

Save and reload:

```bash
source ~/.zprofile    # or source ~/.bash_profile
```

### Linux

Edit `~/.bashrc` (or `~/.zshrc` if using Zsh):

```bash
nano ~/.bashrc

# Add at the bottom:
export PATH="/usr/local/bin/python3:$PATH"

# Save and reload:
source ~/.bashrc
```

### Make BlueClaw Runnable as a Command

Move `blueclaw.py` to a directory on your PATH and make it executable so you can run it directly from any terminal location:

```bash
# Create bn directory in the user path
mkdir ~/bin

# Move to client folder
cd client/

# Copy the blueclaw.py to ~/bin/
cp blueclaw ~/bin/blueclaw
```

Now you can run it from anywhere:

```bash
blueclaw

# To run with a query to server
blueclaw request <query>
```

> **Note:** On macOS, if `/usr/local/bin` requires elevated permissions, prefix the `mv` command with `sudo`:
> ```bash
> sudo mv blueclaw.py /usr/local/bin/blueclaw
> ```

### Verify pip is also available

```bash
pip --version
# or
pip3 --version
```

If pip is missing, install it with:

```bash
python -m ensurepip --upgrade
```

---

## Running the App

### Start the Server

```bash
cd server
fastapi dev main.py
```

Then open your browser and navigate to:

```
http://localhost:8000
```

## Notes

- For best performance, a CUDA-compatible GPU is recommended. CPU inference is supported but will be slower.

## Author

- **Dao Duy Lam** — [@daoduylam2008](https://github.com/daoduylam2008)
