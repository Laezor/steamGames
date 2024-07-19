import os, shutil
from dotenv import load_dotenv
from global_funcs import read_paths_from_file, read_appids_from_file
load_dotenv()

def backup_save_files(game_id, save_paths, backup_dir):
    """
    This function accepts a game id, a set of save paths, and a backup directory as parameters.
    It goes through the save locations, finds the path in the backup folder, and makes the folder if it is not there. Next, it duplicates the storage location to the destination folder within the backup directory while displaying a notification.
    
    Input parameters:
    
    game_id (str): The identification number for the game.
    
    save_paths (list): A collection of save paths.
    
    backup_dir (string): The directory where backups are stored. 
    """
    for save_path in save_paths:
        resolved_path = os.path.join(backup_dir, save_path)
        
        if not os.path.exists(backup_dir):
            os.makedirs(resolved_path)
        file_name = f"{game_id}"
        target_dir = os.path.join(backup_dir, file_name)
        shutil.copytree(save_path, target_dir)
        print(f"copied to {target_dir}")

def main():
    save_paths = read_paths_from_file('steam_paths_final.json')
    appids = read_appids_from_file('steam_paths_final.json')
    for game_id, save_path in zip(appids, save_paths):
        backup_save_files(game_id, [save_path], os.environ.get("backup_dir"))


if __name__ == '__main__':
    main()
