<p align="center">
   <img src="data/logo.png" alt="Description of image" width="500" style="border-radius: 20%">
</>

# BlueClawAI

A local AI terminal assistant powered by Ollama — runs entirely on your own machine.

-----

## Step 1 — Install Ollama

BlueClawAI requires [Ollama](https://ollama.com) to run AI models locally.

Go to <https://ollama.com/download> and install it for your OS:

|OS   |Instructions                                                             |
|-----|-------------------------------------------------------------------------|
|macOS|Download the `.dmg`, open it, and drag Ollama to your Applications folder|
|Linux|Run in your terminal: `curl -fsSL https://ollama.com/install.sh | sh`    |

Verify the install:

```bash
ollama --version
```

> Models will be pulled **automatically** during the BlueClawAI installation — you don’t need to pull them manually.

-----

## Step 2 — Install BlueClawAI

### macOS & Linux

Run this single command in your terminal:

```bash
curl -fsSL https://raw.githubusercontent.com/daoduylam2008/BlueClawAI/main/install.sh | bash
```

This will install everything and add `blueclawai` to your PATH automatically.

Once done, reload your shell:

```bash
source ~/.zprofile        # macOS Zsh (default)
source ~/.zshrc           # macOS Zsh (interactive)
source ~/.bash_profile    # macOS Bash
source ~/.bashrc          # Linux Bash
```

Then verify the install:

```bash
blueclawai --help
```

> You can also download the latest release directly from the [Releases page](https://github.com/daoduylam2008/BlueClawAI/releases).

-----

## Step 3 — Set Up Your OpenWeather API Key

BlueClawAI can look up weather information using the OpenWeather API. A free API key is required.

1. Sign up at <https://home.openweathermap.org/users/sign_up>
1. After signing in, go to <https://home.openweathermap.org/api_keys> and copy your key
1. Navigate to the BlueClawAI install directory:

```bash
cd ~/.blueclawai
```

1. Create a `.env` file:

```bash
touch .env
```

1. Open `.env` and add your key:

```env
OPENWEATHER_API_KEY=your_api_key_here
```

1. Save the file. The server loads it automatically on startup.

> **Note:** Never share or commit your `.env` file — it’s already listed in `.gitignore`.
> **Note:** Newly created API keys can take up to a few hours to activate.

-----

## Step 4 — Run BlueClawAI

### Terminal 1 — Start the server

```bash
blueclawai start_server
```

Keep this running. It powers the AI backend on port **8080**. This can run on one machine and be shared across multiple client computers on the same network.

### Terminal 2 — Open the chat UI

```bash
cd ~/.blueclawai
blueclawai run
```

Type a message and press Enter to chat with the AI.

-----

## Troubleshooting

|Problem                        |Solution                                                                         |
|-------------------------------|---------------------------------------------------------------------------------|
|`blueclawai: command not found`|Run `source ~/.zprofile` or `source ~/.bash_profile`, then open a new terminal   |
|Connection error in chat UI    |Make sure `blueclawai start_server` is running and port 8080 is free             |
|Ollama model errors            |Make sure Ollama is running (`ollama serve` on Linux)                            |
|API key not working            |Wait a few hours after creating a new key — OpenWeather takes time to activate it|

-----

## Author

**Dao Duy Lam** — [@daoduylam2008](https://github.com/daoduylam2008)