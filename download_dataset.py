import aiohttp
import asyncio
from bs4 import BeautifulSoup
import urllib.parse
import os
from tqdm.asyncio import tqdm
import aiofiles
from typing import List, Tuple

# Maximum number of concurrent connections
MAX_CONCURRENT_REQUESTS = 15
CHUNK_SIZE = 8192  # 8KB chunks for streaming

async def get_urls_and_sizes(session, url) -> List[Tuple[str, int]]:
    """Returns list of tuples containing (url, size)"""
    results = []
    async with session.get(url) as response:
        html = await response.text()
        soup = BeautifulSoup(html, 'html.parser')
        
        for link in soup.find_all('a'):
            href = link.get('href')
            if href and not href.startswith(('?', '/', 'http', '..')):
                full_url = urllib.parse.urljoin(url, href)
                if full_url.endswith('/'):
                    # Recursively get URLs and sizes from subdirectory
                    sub_results = await get_urls_and_sizes(session, full_url)
                    results.extend(sub_results)
                else:
                    # Get file size with HEAD request
                    try:
                        async with session.head(full_url) as head_response:
                            size = int(head_response.headers.get('content-length', 0))
                            results.append((full_url, size))
                    except Exception as e:
                        print(f"\nError getting size for {full_url}: {str(e)}")
                        results.append((full_url, 0))
    return results

async def download_file(session, url, size, output_dir, main_progress):
    try:
        # Create relative path structure
        relative_path = url.replace("https://physionet.org/files/afdb/1.0.0/", "")
        filepath = os.path.join(output_dir, relative_path)
        filename = os.path.basename(filepath)
        
        # Create directory if it doesn't exist
        os.makedirs(os.path.dirname(filepath), exist_ok=True)
        
        async with session.get(url, timeout=None) as response:
            if response.status == 200:
                async with aiofiles.open(filepath, 'wb') as f:
                    # Create progress bar for this file
                    with tqdm(
                        total=size,
                        unit='B',
                        unit_scale=True,
                        unit_divisor=1024,
                        desc=filename,
                        leave=False
                    ) as pbar:
                        async for chunk in response.content.iter_chunked(CHUNK_SIZE):
                            await f.write(chunk)
                            bytes_downloaded = len(chunk)
                            pbar.update(bytes_downloaded)
                            main_progress.update(bytes_downloaded)
                
                return True
            return False
    except Exception as e:
        print(f"\nError downloading {url}: {str(e)}")
        return False

async def main():
    # Create output directory if it doesn't exist
    output_dir = "mit-bih-raw"
    os.makedirs(output_dir, exist_ok=True)
    
    # Create TCP connector with connection limit
    connector = aiohttp.TCPConnector(limit=MAX_CONCURRENT_REQUESTS)
    
    base_url = "https://physionet.org/files/afdb/1.0.0/"
    
    # Get all download URLs and their sizes in one pass
    print("Scanning directories and calculating sizes...")
    async with aiohttp.ClientSession() as session:
        url_size_pairs = await get_urls_and_sizes(session, base_url)
    
    total_size = sum(size for _, size in url_size_pairs)
    print(f"Found {len(url_size_pairs)} files to download ({total_size / (1024*1024):.1f} MB total)")
    print(f"Downloading with maximum {MAX_CONCURRENT_REQUESTS} concurrent connections")
    
    # Create main progress bar for overall progress
    with tqdm(
        total=total_size,
        desc="Overall progress",
        unit='B',
        unit_scale=True,
        unit_divisor=1024
    ) as main_progress:
        # Now download all files in parallel with progress bar
        async with aiohttp.ClientSession(connector=connector) as session:
            tasks = [download_file(session, url, size, output_dir, main_progress) 
                    for url, size in url_size_pairs]
            results = await asyncio.gather(*tasks)
            
            # Print summary
            successful = sum(1 for r in results if r)
            failed = sum(1 for r in results if not r)
    
    print(f"\nDownload complete: {successful} successful, {failed} failed")

if __name__ == "__main__":
    asyncio.run(main())