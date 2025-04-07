# instruction.py (updated)
from flask import Flask, render_template, request, redirect, url_for

instruction = Flask(__name__)

# Step data with potential problems/solutions
os_steps = {
    "windows": [
        {
            "title": "Download Python Installer",
            "desc": "Visit https://www.python.org/downloads/windows/ and download Windows installer",
            "problems": [
                {"issue": "32-bit vs 64-bit confusion",
                 "solution": "Check system type: Win + Pause/Break > System > System type"},
                {"issue": "Download fails/slow",
                 "solution": "Use mirror: https://npm.taobao.org/mirrors/python/"},
                {"issue": "Certificate errors",
                 "solution": "Disable VPN/proxy or try http:// version"}
            ]
        },
        {
            "title": "Run Installer",
            "desc": "Double-click installer > CHECK 'Add Python to PATH' > Install Now",
            "problems": [
                {"issue": "Installation blocked by Windows Defender",
                 "solution": "Temporarily disable real-time protection"},
                {"issue": "Admin privileges required",
                 "solution": "Right-click > Run as Administrator"},
                {"issue": "Existing Python installation detected",
                 "solution": "1. Uninstall previous version first\n2. Or choose 'Customize installation'"}
            ]
        },
        {
            "title": "Advanced Options",
            "desc": "For custom setup: Select 'Customize installation' >",
            "problems": [
                {"issue": "Optional features selection",
                 "solution": "Recommend checking:\n- pip\n- py launcher\n- for all users"},
                {"issue": "Install location errors",
                 "solution": "Use default path (C:\\Python312)\nAvoid spaces in path"},
                {"issue": "Disk space warning",
                 "solution": "Python 3.12 requires ~100MB free space"}
            ]
        },
        {
            "title": "PATH Configuration",
            "desc": "Ensure Python added to system PATH",
            "problems": [
                {"issue": "'python' not recognized in CMD",
                 "solution": "Manual PATH setup:\n1. Win + S > 'Environment Variables'\n2. Edit Path > Add Python install path"},
                {"issue": "Multiple Python versions conflict",
                 "solution": "Use py launcher: py -3.12"}
            ]
        },
        {
            "title": "Verify Installation",
            "desc": "Open Command Prompt and run:",
            "problems": [
                {"issue": "Python version check fails",
                 "solution": "1. python --version\n2. py --version\n3. where python"},
                {"issue": "DLL load failed errors",
                 "solution": "Install latest Windows updates\nInstall VC++ Redistributable"}
            ]
        },
        {
            "title": "Pip Configuration",
            "desc": "Verify package manager: pip --version",
            "problems": [
                {"issue": "Pip not recognized",
                 "solution": "Re-run installer with 'Install pip' option"},
                {"issue": "SSL certificate errors",
                 "solution": "Update certifi: python -m pip install --upgrade certifi"},
                {"issue": "Proxy configuration",
                 "solution": "Set environment variables:\nHTTP_PROXY=http://proxy:port\nHTTPS_PROXY=https://proxy:port"}
            ]
        },
        {
            "title": "Post-Installation Checks",
            "desc": "Test basic functionality",
            "problems": [
                {"issue": "Import errors",
                 "solution": "Check PYTHONPATH environment variable"},
                {"issue": "Virtual environment issues",
                 "solution": "python -m venv myenv\nmyenv\\Scripts\\activate"},
                {"issue": "IDE detection problems",
                 "solution": "Restart VS Code/PyCharm\nSelect correct interpreter"}
            ]
        }
    ],
    # Keep existing macOS/Linux config

    "macos": [
    {
        "title": "System Preparation",
        "desc": "Update macOS to latest version (Ventura or newer recommended)",
        "problems": [
            {"issue": "Unsupported older macOS version",
             "solution": "Use legacy Python builds: https://www.python.org/downloads/macos/"},
            {"issue": "Disk space limitations",
             "solution": "Requires 150MB free space for Python + dependencies"}
        ]
    },
    {
        "title": "Xcode Tools Installation",
        "desc": "Full Xcode (App Store) or Command Line Tools only",
        "problems": [
            {"issue": "xcode-select: error",
             "solution": "Remove broken install: sudo rm -rf /Library/Developer/CommandLineTools"},
            {"issue": "Apple Developer Account required",
             "solution": "Use standalone CLT package: https://developer.apple.com/download/all/"}
        ]
    },
    {
        "title": "Homebrew Installation (Apple Silicon)",
        "desc": "M1/M2 Specific Path Configuration:",
        "problems": [
            {"issue": "/opt/homebrew permissions",
             "solution": "sudo chown -R $(whoami) /opt/homebrew"},
            {"issue": "Rosetta 2 compatibility",
             "solution": "arch -x86_64 /bin/bash -c \"$(curl -fsSL...)\""}
        ]
    },
    {
        "title": "Python Version Management",
        "desc": "Using pyenv for multiple versions:",
        "problems": [
            {"issue": "DYLD_LIBRARY_PATH conflicts",
             "solution": "Disable SIP or use pyenv's shims"},
            {"issue": "M1 native vs x86 builds",
             "solution": "PYTHON_CONFIGURE_OPTS=\"--enable-universalsdk\" pyenv install 3.12.1"}
        ]
    },
    {
        "title": "GUI Framework Support",
        "desc": "Installing Tkinter and GUI toolkits:",
        "problems": [
            {"issue": "tkinter module missing",
             "solution": "brew install python-tk@3.12"},
            {"issue": "Quartz/CoreGraphics dependencies",
             "solution": "Install XQuartz: https://www.xquartz.org/"}
        ]
    },
    {
        "title": "Enterprise Deployment",
        "desc": "MDM-based silent installation:",
        "problems": [
            {"issue": "System-wide installation",
             "solution": "sudo installer -pkg python-3.12.1-macos11.pkg -target /"},
            {"issue": "Corporate proxy configuration",
             "solution": "Create .curlrc and .wgetrc with proxy settings"}
        ]
    },
    {
        "title": "Advanced Diagnostics",
        "desc": "Troubleshooting script:",
        "problems": [
            {"issue": "Verify installation integrity",
             "solution": "python3 -m test --list-tests && python3 -m venv testenv"},
            {"issue": "SSL/TLS configuration",
             "solution": "/Applications/Python*/Update\\ Shell\\ Profile.command"}
        ]
    }
],
    "linux": [
    {
        "title": "Update Package Manager",
        "desc": "Debian/Ubuntu: sudo apt update && sudo apt upgrade -y\nFedora: sudo dnf update -y",
        "problems": [
            {"issue": "Permission denied",
             "solution": "Use sudo or become root: su -"},
            {"issue": "Broken package dependencies",
             "solution": "Run: sudo apt --fix-broken install\nor sudo dnf clean all"}
        ]
    },
    {
        "title": "Install Python System Package",
        "desc": "Debian/Ubuntu: sudo apt install python3 python3-pip -y\nFedora: sudo dnf install python3 python3-pip -y",
        "problems": [
            {"issue": "Outdated repository version",
             "solution": "Ubuntu: sudo add-apt-repository ppa:deadsnakes/ppa\nFedora: sudo dnf install python3.12"},
            {"issue": "Missing GPG keys",
             "solution": "Ubuntu: sudo apt-key adv --keyserver keyserver.ubuntu.com --recv-keys [key]\nFedora: sudo rpm --import /etc/pki/rpm-gpg/RPM-GPG-KEY-fedora-*"}
        ]
    },
    {
        "title": "Verify Installation",
        "desc": "Check versions:\npython3 --version\npip3 --version",
        "problems": [
            {"issue": "'python3' not found",
             "solution": "Create symlink: sudo ln -s /usr/bin/python3.12 /usr/bin/python3"},
            {"issue": "pip installation failed",
             "solution": "Manual install: curl https://bootstrap.pypa.io/get-pip.py | python3"}
        ]
    },
    {
        "title": "Virtual Environment Setup",
        "desc": "Create and activate:\npython3 -m venv ~/venv\nsource ~/venv/bin/activate",
        "problems": [
            {"issue": "venv module missing",
             "solution": "Install python3-venv: sudo apt install python3.12-venv"},
            {"issue": "Permission denied in venv",
             "solution": "chmod -R 755 ~/venv"}
        ]
    },
    {
        "title": "Development Tools",
        "desc": "Install build essentials:\nUbuntu: sudo apt install build-essential python3-dev -y\nFedora: sudo dnf groupinstall 'Development Tools' -y",
        "problems": [
            {"issue": "Missing header files",
             "solution": "Install python3.12-dev/ python3-devel"},
            {"issue": "SSL module build failures",
             "solution": "Install libssl-dev: sudo apt install libssl-dev"}
        ]
    },
    {
        "title": "Alternative Installation (pyenv)",
        "desc": "Install multiple versions:\ncurl https://pyenv.run | bash",
        "problems": [
            {"issue": "Build dependencies missing",
             "solution": "Ubuntu: sudo apt install make build-essential libssl-dev zlib1g-dev [...]\nFedora: sudo dnf install @development zlib-devel bzip2 bzip2-devel [...]"},
            {"issue": "pyenv command not found",
             "solution": "Add to shell config:\nexport PATH=\"$HOME/.pyenv/bin:$PATH\"\neval \"$(pyenv init -)\""}
        ]
    },
    {
        "title": "Post-Install Checks",
        "desc": "Test critical functionality:",
        "problems": [
            {"issue": "Tkinter not working",
             "solution": "Install tk-dev: sudo apt install python3-tk"},
            {"issue": "SSL module failure",
             "solution": "Recompile Python with openssl 1.1.1+ support"}
        ]
    },
    {
        "title": "System Configuration",
        "desc": "Set default Python version:",
        "problems": [
            {"issue": "Alternatives conflict",
             "solution": "sudo update-alternatives --install /usr/bin/python python /usr/bin/python3.12 1"},
            {"issue": "Shell not recognizing changes",
             "solution": "source ~/.bashrc or restart shell"}
        ]
    }
]
}


@instruction.route("/")
def home():
    return render_template("index.html")

@instruction.route("/guide/<os_name>")
def os_guide(os_name):
    if os_name not in os_steps:
        return render_template("error.html", message="OS not supported")
    return render_template("guide.html", os_name=os_name.capitalize(), steps=os_steps[os_name])

@instruction.route("/complete")
def complete():
    return render_template("complete.html")

if __name__ == "__main__":
    instruction.run(debug=True)