import os
import subprocess
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def execute_script(script_name):
    """
    This function executes a script using subprocess.run.

    Parameters:
    script_name (str): The name of the script to be executed.

    Returns:
    bool: True if the script executed successfully, False otherwise.
    """
    result = subprocess.run(['python', script_name], capture_output=True, text=True)
    term_size = os.get_terminal_size()
    line = '='*term_size.columns
    if result.returncode != 0:
        print(f'\n{line}')
        logging.error(f"Error executing {script_name}:\n {result.stderr.strip()}")
        return False
    else:
        print(f'\n{line}')
        logging.info(f"Output of {script_name}:\n {result.stdout.strip()}")
        return True

def main():
    scripts = ['src/download_paths.py', 'src/scan_paths.py', 'src/backup_paths.py', 'src/dump_game_names.py']
    success_count = 0
    failure_count = 0

    for script in scripts:
        if execute_script(script):
            success_count += 1
        else:
            failure_count += 1

    logging.info(f"Successful operations: {success_count}/{len(scripts)}")
    logging.info(f"Failed operations: {failure_count}/{len(scripts)}")

if __name__ == "__main__":
    main()