import argparse
import hashlib
import json
from pathlib import Path

import requests
from blessings import Terminal
from fake_headers import Headers
from pygments import formatters, highlight, lexers
from requests.adapters import HTTPAdapter

t = Terminal()


class BaseExtractor:
    @property
    def requests(self):
        session = requests.Session()
        session.mount("http://", HTTPAdapter(max_retries=3))
        session.mount("https://", HTTPAdapter(max_retries=3))
        return session

    def fetch_website(self, url):
        headers = Headers(headers=True).generate()
        res = self.requests.get(url, timeout=1.0, headers=headers)

        if res.status_code != 200:
            raise Exception("Status code is not 200")

        return res.text


class ValidationMaker:
    def __init__(self):
        parser = argparse.ArgumentParser(description="Create a Validation Entry based on a website.")
        parser.add_argument("url", help="Website URL")
        parser.add_argument("--dest-dir", required=True, help="Destination directory")
        parser.add_argument(
            "--overwrite", help="Overwrite Validation Entry", default=None, action=argparse.BooleanOptionalAction
        )
        parser.add_argument(
            "--respirator_type", help="Type of the respirator", choices=["PFF1", "PFF2", "PFF3", "KN95"]
        )
        parser.add_argument(
            "--spandex", help="Respirator has spandex?", default=None, action=argparse.BooleanOptionalAction
        )
        parser.add_argument("--quantity", help="Quantity of respirators", type=int)
        parser.add_argument("--price", help="Price of the package", type=float)
        parser.add_argument(
            "--exhalation-valve",
            help="Exhalation Valve is present?",
            default=None,
            action=argparse.BooleanOptionalAction,
        )
        parser.add_argument("--approval-certificate", help="This mask has approval ceriticate?", type=int)

        self.args = parser.parse_args()

    @property
    def encoded_url(self):
        return hashlib.sha1(self.args.url.encode("utf-8")).hexdigest()

    def run(self):
        base_path = Path(self.args.dest_dir)
        data_file = base_path / f"{self.encoded_url}.data"
        json_file = base_path / f"{self.encoded_url}.json"

        if data_file.exists() and json_file.exists() and not self.args.overwrite:
            print(
                f"{t.magenta}Validation Entry already exists. Skipping!\n"
                f"Use the parameter --overwrite if you want to overwrite the files.{t.normal}"
            )
            return

        print(f"{t.magenta}Fetching website content...{t.normal} (URL: {self.args.url})")
        content = BaseExtractor().fetch_website(self.args.url)
        print(f"{t.green}{len(content)} bytes fetched! {t.normal}")

        with data_file.open("w+") as file:
            file.write(content)

        options = {
            "approval_certificate": self.args.approval_certificate,
            "exhalation_valve": self.args.exhalation_valve,
            "price": self.args.price,
            "quantity": self.args.quantity,
            "respirator_type": self.args.respirator_type,
            "spandex": self.args.spandex,
            "url": self.args.url,
            "data_file": f"{self.encoded_url}.data",
        }

        with json_file.open("w+") as file:
            json.dump(options, file, sort_keys=True, indent=4)

        print(f"{t.magenta}Configuration generated: {t.normal}")
        colorful_json = highlight(
            # pylint: disable=E1101
            json.dumps(options, sort_keys=True, indent=4),
            lexers.JsonLexer(),
            formatters.TerminalFormatter(),
        )
        print(colorful_json)
        print(f"{t.bold_green}Files saved in {self.args.dest_dir} as {self.encoded_url}.[json/data] {t.normal}")


if __name__ == "__main__":
    ValidationMaker().run()
