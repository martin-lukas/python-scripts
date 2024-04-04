# Python scripts

To add a Python script on a path as an executable:

1. Add a shebang on top: `#!/usr/bin/env python3.12`
2. Make the file executable: `chmod +x script.py`
3. Create a folder for local scripts, e.g. `~/.bin`
4. Add it to the path in `~/.zprofile`: `export PATH="$PATH:$HOME/.bin"`
5. Create a symbolic link to the script: `ln -s /abs/path/to/script ~/.bin/executable_name`
