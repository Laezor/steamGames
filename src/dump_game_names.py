import os
import httpx
import asyncio
from global_funcs import read_appids_from_file
from dotenv import load_dotenv

load_dotenv()

async def fetch_game_name(client, appid):
    req_url = f"https://store.steampowered.com/api/appdetails/?appids={appid}"
    response = await client.get(req_url)
    if response.status_code != 200:
        print(f"Error: {response.status_code} {response.reason}")
        return None
    return response.json()[appid]['data']['name']

async def request_steam(appids):
    """
    This function takes a list of appids as input and returns a list of game names.
    It iterates over each appid, sends a request to the Steam API to get the game details,
    and extracts the game name from the response. If the request fails, it prints an error message.
    
    Parameters:
    appids (list): A list of appids to request game names for.
    
    Returns:
    list: A list of game names corresponding to the input appids.
    """
    game_names = []
    async with httpx.AsyncClient() as client:
        tasks = [fetch_game_name(client, appid) for appid in appids]
        game_names = await asyncio.gather(*tasks)
    return [name for name in game_names if name is not None]

def dump_to_txt(appids, names, filename="output.txt"):
    """
    This function takes a list of appids, a list of game names, and an optional filename as input.
    It opens a file in write mode with the specified filename and encoding.
    It then iterates over each appid and its corresponding game name, printing a message and writing the appid and game name to the file.
    
    Parameters:
    appids (list): A list of appids to dump.
    names (list): A list of game names corresponding to the input appids.
    filename (str, optional): The name of the file to write the output to. Defaults to "output.txt".
    """
    with open(f'{os.environ.get("backup_dir")}/{filename}', 'w', encoding="utf-8") as f:
        for appid, name in zip(appids, names):
            print(f"Dumping {appid}={name}")
            f.write(f"{appid}={name},\n")

def main():
    appids = read_appids_from_file("steam_paths_final.json")
    names = asyncio.run(request_steam(appids))
    dump_to_txt(appids, names)

if __name__ == '__main__':
    main()