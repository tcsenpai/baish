# 🐚 Baish

**Natural Language to Bash Commands using Ollama**

Baish is a simple, elegant terminal application that converts natural language instructions into bash/linux commands using a local Ollama instance. Say goodbye to googling command syntax!

![Demo](https://img.shields.io/badge/Python-3.8+-blue.svg)
![License](https://img.shields.io/badge/License-MIT-green.svg)

## ✨ Features

- 🎨 **Beautiful Terminal UI** - Rich, colorful interface with panels and prompts
- 🔗 **Ollama Integration** - Works with any Ollama model locally
- ⚡ **Dual Modes** - Interactive mode or single command execution
- 🛡️ **Safety First** - Built-in checks for potentially dangerous commands
- 🚀 **Real-time Execution** - Live command output streaming
- 📝 **Help System** - Built-in help with `-h` and `/help` commands

## 🚀 Quick Start

### Prerequisites

1. **Python 3.8+** with `uv` package manager
2. **Ollama** installed and running locally
3. A model downloaded in Ollama (e.g., `ollama pull llama3.2`)

### Installation

#### Option 1: From PyPI (Recommended)
```bash
pip install baish_assistant
```

#### Option 2: From Source
```bash
git clone https://github.com/tcsenpai/baish.git
cd baish
uv pip install -e .
```

#### Option 3: Direct Execution
```bash
git clone https://github.com/tcsenpai/baish.git
cd baish
uv pip install rich click python-dotenv requests
python main.py "show my ip address"
```

### Configuration

Create a `.env` file in your project directory:

```env
OLLAMA_URL=http://localhost:11434
OLLAMA_MODEL=llama3.2:latest
```

## 📖 Usage

### Command Line Interface

```bash
# Single command mode
baish "show my ip address"
baish "list files in current directory"
baish "check disk usage"

# Interactive mode
baish -i

# Show help
baish -h

# Direct execution (without installation)
python main.py "find python files"
uv run python main.py -i
```

### Interactive Mode

```bash
$ baish -i
┌─────────────────────────────────────────┐
│ 🐚 Baish - Natural Language to Bash    │
└─────────────────────────────────────────┘

What would you like to do? > show my ip address

🤔 Thinking...

┌─── Generated Command ───┐
│ ip addr show            │
└─────────────────────────┘

Execute this command? [Y/n]: y

────────────────────────────────────────────
1: lo: <LOOPBACK,UP,LOWER_UP> mtu 65536...
2: eth0: <BROADCAST,MULTICAST,UP,LOWER_UP>...
────────────────────────────────────────────
✓ Command completed successfully
```

## 🎯 Examples

| Natural Language | Generated Command |
|------------------|-------------------|
| "show my ip address" | `ip addr show` |
| "list files in current directory" | `ls -la` |
| "check disk usage" | `df -h` |
| "find python files" | `find . -name "*.py"` |
| "stop nginx service" | `sudo systemctl stop nginx` |
| "show running processes" | `ps aux` |
| "check memory usage" | `free -h` |
| "show network connections" | `netstat -tuln` |

## 🛡️ Safety Features

Baish includes built-in safety checks for potentially dangerous commands:

- **Pattern Detection**: Identifies risky commands like `rm -rf /`, `format`, `shutdown`, `curl | sh`
- **User Confirmation**: Always prompts before executing any command
- **Command Preview**: Shows exactly what will be executed in a highlighted panel
- **Graceful Cancellation**: Easy to cancel dangerous operations
- **Debug Mode**: Optional detailed logging for troubleshooting

**Dangerous patterns detected:**
- File system destruction (`rm -rf /`, `format`, `mkfs`)
- System control (`shutdown`, `reboot`, `init`)
- Privilege escalation risks (`chmod 777`, `chown root`)
- Remote execution (`curl | sh`, `wget | sh`)
- Fork bombs and system overload

## ⚙️ Configuration Options

### Environment Variables

- `OLLAMA_URL` - Ollama server URL (default: `http://localhost:11434`)
- `OLLAMA_MODEL` - Model to use (default: `llama3.2:latest`)
- `BASH_DEBUG` - Enable debug logging (optional)

### Advanced Configuration

```env
# Use remote Ollama instance
OLLAMA_URL=http://192.168.1.100:11434

# Use a specific model variant
OLLAMA_MODEL=codellama:7b-instruct

# Enable debug output
BASH_DEBUG=1
```

### Model Recommendations

- **Fast & Efficient**: `llama3.2:latest`, `qwen2.5:7b`, `phi3:mini`
- **More Capable**: `llama3.1:8b`, `codellama:7b`, `qwen2.5:14b`
- **Lightweight**: `tinyllama:latest`, `phi3:mini`
- **Code-Focused**: `codellama:7b`, `deepseek-coder:6.7b`

**Note**: Ensure your chosen model is installed in Ollama:
```bash
ollama pull llama3.2:latest
```

## 🏗️ Development

### Setup Development Environment

```bash
git clone https://github.com/tcsenpai/baish.git
cd baish

# Copy and configure environment
cp .env.example .env
# Edit .env with your Ollama settings

# Install dependencies
uv pip install -e ".[dev]"

# Run tests
pytest

# Format code
black .
ruff check .
```

### Project Structure

```
baish/
├── baish/
│   ├── __init__.py
│   └── main.py          # Package entry point
├── main.py              # Direct execution entry point
├── pyproject.toml       # Project configuration
├── .env                 # Configuration file
└── README.md           # This file
```

### Running Tests

```bash
pytest
```

### Code Formatting

```bash
black .
ruff check .
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- [Ollama](https://ollama.ai/) for the excellent local LLM platform
- [Rich](https://github.com/Textualize/rich) for the beautiful terminal UI
- [Click](https://click.palletsprojects.com/) for the CLI framework

## 📞 Support

- 🐛 **Bug Reports**: [GitHub Issues](https://github.com/tcsenpai/baish/issues)
- 💡 **Feature Requests**: [GitHub Discussions](https://github.com/tcsenpai/baish/discussions)
- 📧 **Email**: [tcsenpai@discus.sh]

---

**Made with ❤️ by [tcsenpai](https://github.com/tcsenpai)**
