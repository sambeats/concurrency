import threading
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
from queue import Queue

class WebCrawler:
    def __init__(self, base_url, max_threads=5):
        self.base_url = base_url
        self.visited = set()
        self.lock = threading.Lock()
        self.queue = Queue()
        self.queue.put(base_url)
        self.max_threads = max_threads

    def crawl(self):
        threads = []
        for _ in range(self.max_threads):
            t = threading.Thread(target=self.worker)
            t.start()
            threads.append(t)
        for t in threads:
            t.join()

    def worker(self):
        while not self.queue.empty():
            url = self.queue.get()
            try:
                self.fetch(url)
            finally:
                self.queue.task_done()

    def fetch(self, url):
        with self.lock:
            if url in self.visited:
                return
            self.visited.add(url)
            print(f"Crawling: {url}")

        try:
            response = requests.get(url, timeout=5)
            if "text/html" not in response.headers.get("Content-Type", ""):
                return
            soup = BeautifulSoup(response.text, "html.parser")
            for link in soup.find_all("a", href=True):
                full_url = urljoin(url, link["href"])
                if self.is_valid_url(full_url):
                    with self.lock:
                        if full_url not in self.visited:
                            self.queue.put(full_url)
        except requests.RequestException:
            pass

    def is_valid_url(self, url):
        parsed = urlparse(url)
        return parsed.scheme in {"http", "https"} and parsed.netloc == urlparse(self.base_url).netloc

if __name__ == "__main__":
    seed_url = "https://example.com"
    crawler = WebCrawler(seed_url, max_threads=5)
    crawler.crawl()
