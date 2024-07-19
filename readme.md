# Steam Game Save Backup

Welcome to the Steam Game Save Backup project! This tool helps you automate the process of backing up save files for your Steam games. It retrieves the save paths from PCGamingWiki, filters the paths, and backs up the save files to another directory. Finally, it generates a text file listing the backed-up games.

## Table of Contents

- [Features](#features)
- [Installation](#installation)
- [Usage](#usage)
- [File Structure](#file-structure)
- [Contributing](#contributing)
- [License](#license)

## Features

- Retrieve installed Steam games
- Get save paths from PCGamingWiki
- Filter paths with necessary IDs
- Backup save files to another directory
- Generate a text file listing the backed-up games
- Customizable for different Steam installation paths
- Supports both 32-bit and 64-bit systems

## Installation

1. Clone the repository:

   ```sh
   git clone https://github.com/yourusername/steam-game-save-backup.git
   cd steam-game-save-backup
   ```

2. Install the required dependencies:

   ```sh
   pip install -r requirements.txt
   ```

3. Fill the .env variables in the .env file:

    ```plaintext
    steam_user_id=
    ubisoft_user_id=
    steam_acc_id=
    custom_steam_path=
    custom_ubisoft_path=
    ```
    The other values should already be filled up.

## Usage

1. Ensure you have Python installed on your system.

2. Run the main script:

   ```sh
   python main.py
   ```

3. The script will execute the following steps:
   - Download save paths from PCGamingWiki
   - Scan the paths for necessary IDs
   - Backup the save files to a specified directory
   - Dump the names of the backed-up games into a text file

## File Structure

- `main.py`: The main script that orchestrates the execution of other scripts.
- `src/download_paths.py`: Script to download save paths.
- `src/scan_paths.py`: Script to scan paths for necessary IDs.
- `src/backup_paths.py`: Script to backup save files.
- `src/dump_game_names.py`: Script to dump the names of backed-up games.

## Contributing

We welcome contributions! Here's how you can help:

1. Fork the repository.
2. Create a new branch (`git checkout -b feature-branch`).
3. Make your changes.
4. Commit your changes (`git commit -am 'Add new feature'`).
5. Push to the branch (`git push origin feature-branch`).
6. Create a new Pull Request.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.