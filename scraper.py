from bs4 import BeautifulSoup
import httpx


class Scraper:
    def fetch_html(self, url):
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
            "Accept-Language": "en-US,en;q=0.5",
            "Upgrade-Insecure-Requests": "1",
            "Sec-Fetch-Dest": "document",
            "Sec-Fetch-Mode": "navigate",
            "Sec-Fetch-Site": "none",
            "Sec-Fetch-User": "?1",
        }
        with httpx.Client(http2=True, headers=headers, follow_redirects=True) as client:
            try:
                response = client.get(url, timeout=20.0)
                response.raise_for_status()
                return response.text
            except Exception as e:
                print(f"Bypass failed: {e}")
                return

    def fetch_headings(self, parsed_doc):
        headings = []
        table = parsed_doc.table

        for heading in table.thead.find_all("th"):
            txt = str(heading.contents[0]).strip()
            headings.append(txt)

        headings.pop(0)
        return headings

    def fetch_data(self, parsed_doc):
        table = parsed_doc.table
        contents = []
        ignore_vals = ["Leading In", "Won In", "Trailing In", ":"]
        for values in table.tbody.find_all("tr"):
            real_vals = []

            for v in values.find_all("td"):
                if v.table:
                    continue
                else:
                    value = v.contents
                    if value and value[0] not in ignore_vals:
                        real_vals.append(value[0])
            contents.append(real_vals)

        clean_contents = [x for x in contents if x and len(x) > 4]
        data = []
        for c in clean_contents:
            del c[4:7]
            del c[6:9]
            data.append(dict(zip(self.headings, c)))
        return data

    def print_data(self):
        for i in self.data:
            print(i)

    def __init__(self, url="") -> None:
        self.url = url
        html_doc = self.fetch_html(url)
        self.parsed = BeautifulSoup(html_doc, "html.parser")
        self.headings = self.fetch_headings(self.parsed)
        self.data = self.fetch_data(self.parsed)
