import requests
from urllib.parse import urljoin
from colorama import Fore, Style, init
from concurrent.futures import ThreadPoolExecutor, as_completed
import threading

#CODER = @crypted_tut 
init(autoreset=True)

#CODER = @crypted_tut
lock = threading.Lock()
#CODER = @crypted_tut
def print_ascii_art():
    art = r"""
--   _____ _   ___     __                                      
--  | ____| \ | \ \   / /  ___  ___ __ _ _ __  _ __   ___ _ __ 
--  |  _| |  \| |\ \ / /  / __|/ __/ _` | '_ \| '_ \ / _ \ '__|
--  | |___| |\  | \ V /   \__ \ (_| (_| | | | | | | |  __/ |   
--  |_____|_| \_|  \_/    |___/\___\__,_|_| |_|_| |_|\___|_|

--         BY @crypted_tut | CHANNEL : @skull_crack                                                           
    """
    print(Fore.CYAN + art)
#CODER = @crypted_tut
def scan_website(website, paths):
    """
    Scans a single website for .env and .env.example files.

    :param website: The website URL.
    :param paths: List of file paths to check.
    :return: List of found file URLs with valid content.
    """
    found_files = []
    try:
        for path in paths:
            file_url = urljoin(website, path)

            
            response = requests.get(file_url, timeout=10)
            if response.status_code == 200:
                found_files.append(file_url)
                print(Fore.GREEN + f"[+] Found: {file_url}")

                
                with lock:
                    with open("LARAVEL.txt", "a") as output_file:
                        output_file.write(file_url + "\n")

    except requests.RequestException as e:
        print(Fore.RED + f"[-] Error scanning {website}: {e}")

    return found_files
#CODER = @crypted_tut
def scan_env_files(websites_file, thread_count):
    """
    Scans a list of websites for .env and .env.example files using multithreading.

    :param websites_file: Path to the file containing a list of websites.
    :param thread_count: Number of threads to use for scanning.
    """
    try:
        print_ascii_art()
        print(Fore.YELLOW + "[INFO] Starting scan for .env files...")

     #CODER = @crypted_tut   
        with open(websites_file, 'r') as file:
            websites = [line.strip() for line in file if line.strip()]

        total_websites = len(websites)

        
        paths = [".env", ".env.example"]

        
        with open("LARAVEL.txt", "w") as output_file:
            output_file.write("")

        
        with ThreadPoolExecutor(max_workers=thread_count) as executor:
            future_to_website = {executor.submit(scan_website, website, paths): website for website in websites}

            for idx, future in enumerate(as_completed(future_to_website), start=1):
                try:
                    future.result()
                except Exception as e:
                    print(Fore.RED + f"[-] Error processing a website: {e}")

                progress = (idx / total_websites) * 100
                print(Fore.CYAN + f"[INFO] Progress: {idx}/{total_websites} ({progress:.2f}%)")

        print(Fore.GREEN + f"\n[INFO] Scan completed. Results saved to LARAVEL.txt")

    except Exception as e:
        print(Fore.RED + f"[ERROR] An error occurred: {e}")
#CODER = @crypted_tut
#CODER = @crypted_tut
if __name__ == "__main__":
    websites_file = input("{!} Enter the path to the websites file: ").strip()
    thread_count = int(input("{!} Enter the number of threads to use: ").strip())
    scan_env_files(websites_file, thread_count)
#CODER = @crypted_tut
