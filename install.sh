#!/usr/bin/env bash
# =============================================================================
# BlueClawAI Installer
# Usage: curl -fsSL https://raw.githubusercontent.com/daoduylam2008/BlueClawAI/main/install.sh | bash
# =============================================================================

set -e  # Exit immediately if any command fails

# ─── Config ──────────────────────────────────────────────────────────────────
REPO="daoduylam2008/BlueClawAI"
VERSION="v1.2.0"
INSTALL_DIR="$HOME/.blueclawai"
BIN_DIR="$INSTALL_DIR/bin"
TMP_DIR=$(mktemp -d)

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
BOLD='\033[1m'
NC='\033[0m' # No Color

# ─── Helper functions ─────────────────────────────────────────────────────────
info()    { echo -e "${BLUE}[INFO]${NC}  $1"; }
success() { echo -e "${GREEN}[OK]${NC}    $1"; }
warn()    { echo -e "${YELLOW}[WARN]${NC}  $1"; }
error()   { echo -e "${RED}[ERROR]${NC} $1"; exit 1; }
step()    { echo -e "\n${BOLD}── $1${NC}"; }

cleanup() {
  rm -rf "$TMP_DIR"
}
trap cleanup EXIT  # Always clean up temp files on exit

# ─── Step 1: Detect OS and Architecture ──────────────────────────────────────
detect_platform() {
  step "Detecting your platform"

  OS=$(uname -s)
  ARCH=$(uname -m)

  case "$OS" in
    Darwin)
      OS_NAME="macos"
      ;;
    Linux)
      OS_NAME="linux"
      ;;
    *)
      error "Unsupported OS: $OS. BlueClawAI currently supports macOS and Linux."
      ;;
  esac

  case "$ARCH" in
    arm64|aarch64)
      ARCH_NAME="arm64"
      ;;
    *)
      error "Unsupported architecture: $ARCH"
      ;;
  esac

  PLATFORM="${OS_NAME}-${ARCH_NAME}"
  TARBALL="blueclawai-${PLATFORM}.tar.gz"
  DOWNLOAD_URL="https://github.com/${REPO}/releases/download/${VERSION}/${TARBALL}"

  success "Detected: $OS_NAME ($ARCH_NAME)"
}

# ─── Step 2: Check Ollama is installed ───────────────────────────────────────
check_ollama() {
  step "Checking Ollama"

  if ! command -v ollama &>/dev/null; then
    echo ""
    warn "Ollama is not installed."
    echo ""
    echo "  BlueClawAI requires Ollama to run AI models locally."
    echo "  Please install it first:"
    echo ""
    echo "    macOS/Linux: https://ollama.com/download"
    echo "    Or run:      curl -fsSL https://ollama.com/install.sh | sh"
    echo ""
    read -r -p "  Press Enter after installing Ollama, or Ctrl+C to cancel... "

    # Re-check after user confirms
    if ! command -v ollama &>/dev/null; then
      error "Ollama still not found. Please install it and re-run this installer."
    fi
  fi

  success "Ollama found: $(ollama --version 2>/dev/null || echo 'installed')"
}

# ─── Step 3: Check if already installed (upgrade path) ───────────────────────
check_existing() {
  step "Checking for existing installation"

  if [ -d "$INSTALL_DIR" ]; then
    warn "BlueClawAI is already installed at $INSTALL_DIR"
    read -r -p "  Upgrade/reinstall? [y/N] " confirm
    case "$confirm" in
      [yY][eE][sS]|[yY])
        info "Removing old installation..."
        rm -rf "$INSTALL_DIR"
        success "Old installation removed"
        ;;
      *)
        echo "  Installation cancelled."
        exit 0
        ;;
    esac
  else
    info "No existing installation found — fresh install"
  fi
}

# ─── Step 4: Download binaries ────────────────────────────────────────────────
download_binaries() {
  step "Downloading BlueClawAI $VERSION"
  info "Platform: $PLATFORM"
  info "Source:   $DOWNLOAD_URL"
  echo ""

  # Check the release actually exists for this platform
  HTTP_STATUS=$(curl -fsSL -o /dev/null -w "%{http_code}" -I "$DOWNLOAD_URL" 2>/dev/null || echo "000")

  if [ "$HTTP_STATUS" = "000" ] || [ "$HTTP_STATUS" = "404" ]; then
    echo ""
    error "No binary found for $PLATFORM at $VERSION.
    
    This platform may not have a release yet.
    Please check: https://github.com/$REPO/releases
    
    Or install manually from source:
    https://github.com/$REPO#install-from-github-clone--bash"
  fi

  # Download with progress
  curl -fsSL --progress-bar "$DOWNLOAD_URL" -o "$TMP_DIR/$TARBALL"
  success "Downloaded $TARBALL"

  # Extract
  tar -xzf "$TMP_DIR/$TARBALL" -C "$TMP_DIR/"
  EXTRACTED_DIR="$TMP_DIR/blueclawai-${PLATFORM}"

  if [ ! -d "$EXTRACTED_DIR" ]; then
    error "Extraction failed — expected folder: $EXTRACTED_DIR"
  fi

  success "Extracted successfully"
}

# ─── Step 5: Install files ────────────────────────────────────────────────────
install_files() {
  step "Installing BlueClawAI to $INSTALL_DIR"

  # Create directories
  mkdir -p "$BIN_DIR"
  mkdir -p "$INSTALL_DIR/data"

  # Copy binaries
  if [ -f "$EXTRACTED_DIR/blueclawai" ]; then
    cp "$EXTRACTED_DIR/blueclawai" "$BIN_DIR/blueclawai"
    chmod +x "$BIN_DIR/blueclawai"
    success "Installed: blueclawai (CLI)"
  else
    error "blueclawai binary not found in release package"
  fi

  if [ -f "$EXTRACTED_DIR/app" ]; then
    cp "$EXTRACTED_DIR/app" "$BIN_DIR/app"
    chmod +x "$BIN_DIR/app"
    success "Installed: app"
  else
    warn "app binary not found — 'app' command may not work"
  fi

  # Copy data folder if it exists in the package
  if [ -d "$EXTRACTED_DIR/server" ]; then
    cp -r "$EXTRACTED_DIR/server/." "$BIN_DIR/server/"
    success "Installed: server files"
  fi
}

# ─── Step 6: Add to PATH ──────────────────────────────────────────────────────
setup_path() {
  step "Setting up PATH"

  PATH_LINE="export PATH=\"\$PATH:$BIN_DIR\""
  PATH_ADDED=false

  # Determine which shell profiles to update
  PROFILES=()

  # zsh (default on macOS Catalina+)
  if [ -f "$HOME/.zprofile" ] || [ "$SHELL" = "/bin/zsh" ]; then
    PROFILES+=("$HOME/.zprofile")
  fi

  # bash
  if [ -f "$HOME/.bash_profile" ] || [ "$SHELL" = "/bin/bash" ]; then
    PROFILES+=("$HOME/.bash_profile")
  fi

  # Fallback — always write at least one
  if [ ${#PROFILES[@]} -eq 0 ]; then
    PROFILES+=("$HOME/.profile")
  fi

  for PROFILE in "${PROFILES[@]}"; do
    # Only add if not already there
    if ! grep -q "$BIN_DIR" "$PROFILE" 2>/dev/null; then
      echo "" >> "$PROFILE"
      echo "# BlueClawAI" >> "$PROFILE"
      echo "$PATH_LINE" >> "$PROFILE"
      success "Added to PATH in $PROFILE"
      PATH_ADDED=true
    else
      info "PATH already set in $PROFILE"
    fi
  done

  # Also export for the current session so it works immediately
  export PATH="$PATH:$BIN_DIR"
}

# ─── Step 7: Pull Ollama models ───────────────────────────────────────────────
pull_models() {
  step "Pulling Ollama models"
  echo ""
  warn "This downloads AI model files (~5-8 GB total). It may take a while."
  echo ""
  read -r -p "  Pull models now? [Y/n] " confirm
  confirm=${confirm:-Y}  # Default to Y if user just presses Enter

  case "$confirm" in
    [nN][oO]|[nN])
      warn "Skipping model pull. Run these manually before using BlueClawAI:"
      echo ""
      echo "    ollama pull llama3.1"
      echo "    ollama pull qwen2.5:3b"
      echo ""
      ;;
    *)
      info "Pulling llama3.1 (~4.7 GB)..."
      ollama pull llama3.1 || warn "Failed to pull llama3.1 — run 'ollama pull llama3.1' manually"

      info "Pulling qwen2.5:3b (~2 GB)..."
      ollama pull qwen2.5:3b || warn "Failed to pull qwen2.5:3b — run 'ollama pull qwen2.5:3b' manually"

      success "Models ready"
      ;;
  esac
}

# ─── Step 8: Verify installation ──────────────────────────────────────────────
verify_install() {
  step "Verifying installation"

  if [ -x "$BIN_DIR/blueclawai" ]; then
    success "Binary is executable"
  else
    error "Binary not found or not executable at $BIN_DIR/blueclawai"
  fi

  # Test the binary runs
  if "$BIN_DIR/blueclawai" --help &>/dev/null; then
    success "blueclawai --help works"
  else
    warn "blueclawai --help returned an error — the binary may need further setup"
  fi
}

# ─── Step 9: Print success message ───────────────────────────────────────────
print_success() {
  echo ""
  echo -e "${GREEN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
  echo -e "${GREEN}  ✅  BlueClawAI installed successfully!${NC}"
  echo -e "${GREEN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
  echo ""
  echo -e "  ${BOLD}Next steps:${NC}"
  echo ""
  echo "  1. Restart your terminal (or run the command below)"
  echo "     source ~/.zprofile   # zsh"
  echo "     source ~/.bash_profile  # bash"
  echo ""
  echo "  2. Make sure Ollama is running"
  echo "     ollama serve   # if not already running"
  echo ""
  echo "  3. Open TWO terminal windows:"
  echo ""
  echo -e "     ${BOLD}Terminal 1 — Start the AI server:${NC}"
  echo "     blueclawai start_server"
  echo ""
  echo -e "     ${BOLD}Terminal 2 — Open the chat UI:${NC}"
  echo "     blueclawai run"
  echo ""
  echo "  ──────────────────────────────────────────────────"
  echo ""
  echo -e "  ${BOLD}Optional:${NC} Add your OpenWeather API key for weather features:"
  echo "  nano $INSTALL_DIR/.env"
  echo ""
  echo -e "  ${BOLD}Uninstall anytime:${NC}"
  echo "  rm -rf $INSTALL_DIR"
  echo ""
  echo -e "  ${BOLD}GitHub:${NC} https://github.com/$REPO"
  echo ""
}

# ─── Main ─────────────────────────────────────────────────────────────────────
main() {
  detect_platform
  check_ollama
  check_existing
  download_binaries
  install_files
  setup_path
  pull_models
  verify_install
  print_success
}

main