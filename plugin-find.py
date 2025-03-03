"""
BSD 3-Clause License

Copyright (c) 2024, Ali Okan Yuksel
All rights reserved.

Redistribution and use in source and binary forms, with or without
modification, are permitted provided that the following conditions are met:

1. Redistributions of source code must retain the above copyright notice,
   this list of conditions, and the following disclaimer.
2. Redistributions in binary form must reproduce the above copyright notice,
   this list of conditions, and the following disclaimer in the documentation
   and/or other materials provided with the distribution.
3. Neither the name of the copyright holder nor the names of its contributors
   may be used to endorse or promote products derived from this software
   without specific prior written permission.

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE
LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR
CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF
SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS
INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN
CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE)
ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
POSSIBILITY OF SUCH DAMAGE.
"""


import requests
from bs4 import BeautifulSoup
import json
import argparse

class TenablePluginScraper:
    """
    A class to fetch and parse Tenable plugin search results.
    """

    def __init__(self, search_query):
        self.search_query = search_query
        self.url = f"https://www.tenable.com/plugins/search?q={search_query}"
        self.headers = {
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8",
        }

    def fetch_plugins(self):
        """
        Sends an HTTP request to fetch Tenable plugin search results.
        """
        response = requests.get(self.url, headers=self.headers)

        if response.status_code == 200:
            return response.text  # Return HTML content
        else:
            print(f"Error: Request failed with status code {response.status_code}")
            return None

    def parse_plugins(self, html_content):
        """
        Parses the HTML response to extract plugin details from the results table.
        """
        soup = BeautifulSoup(html_content, "html.parser")
        table = soup.find("table", class_="results-table table")

        data = []
        if table:
            headers = [th.text.strip() for th in table.find("thead").find_all("th")]

            for row in table.find("tbody").find_all("tr"):
                cols = row.find_all("td")
                values = [col.text.strip() for col in cols]
                if values:
                    data.append(dict(zip(headers, values)))  # Convert row to dictionary

        return data

    def run(self):
        """
        Executes the scraper: fetches the page, parses data, and prints results.
        """
        html_content = self.fetch_plugins()
        if html_content:
            parsed_data = self.parse_plugins(html_content)
            print(json.dumps(parsed_data, indent=4, ensure_ascii=False))

def main():
    """
    Main function to handle command-line arguments and execute the scraper.
    """
    parser = argparse.ArgumentParser(
        description="Fetch Tenable plugin search results based on a given keyword."
    )
    parser.add_argument(
        "search_keyword",
        type=str,
        help="Keyword to search for plugins (e.g., 'chrome')."
    )

    args = parser.parse_args()
    
    scraper = TenablePluginScraper(args.search_keyword)
    scraper.run()

if __name__ == "__main__":
    main()
