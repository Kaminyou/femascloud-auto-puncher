from http import HTTPStatus
import typing as t

import requests
from bs4 import BeautifulSoup


class FemasPuncher:

    def __init__(self, account: str, password: str, subdomain: str):
        self.account = account
        self.password = password
        self.subdomain = subdomain

    def get_api(self, api_name: str) -> str:
        return f"https://femascloud.com/{self.subdomain}" + api_name

    def __enter__(self):
        self.session = requests.Session()
        r = self.session.get(self.get_api("/accounts/login"))

        headers = {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',  # noqa
            'Accept-Language': 'zh-TW,zh;q=0.9',
            'Cache-Control': 'max-age=0',
            'Connection': 'keep-alive',
            'Origin': 'https://femascloud.com',
            'Referer': 'https://femascloud.com/aetherai1/accounts/login',
            'Sec-Fetch-Dest': 'document',
            'Sec-Fetch-Mode': 'navigate',
            'Sec-Fetch-Site': 'same-origin',
            'Sec-Fetch-User': '?1',
            'Upgrade-Insecure-Requests': '1',
        }

        data = {
            'data[Account][username]': self.account,
            'data[Account][passwd]': self.password,
            'data[remember]': '0',
        }

        r = self.session.post(
            self.get_api("/Accounts/login"),
            headers=headers,
            data=data,
        )
        soup = BeautifulSoup(r.text, "html.parser")
        self.user_id = soup.find(
            "input",
            {"name": "data[EboardBrowser][user_id]"},
        ).attrs["value"]

        return self

    def __exit__(self, type, value, traceback):
        self.session.close()

    def punch_in_myself(self):
        self.punch_in(user_id=self.user_id)

    def punch_out_myself(self):
        self.punch_out(user_id=self.user_id)

    def punch_in(self, user_id: t.Union[int, str]):
        headers = {
            'Accept': 'text/javascript, text/html, application/xml, text/xml, */*',  # noqa
            'Accept-Language': 'zh-TW,zh;q=0.9,en-US;q=0.8,en;q=0.7,zh-CN;q=0.6,ja;q=0.5',  # noqa
            'Connection': 'keep-alive',
            'Content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
            'Origin': 'https://femascloud.com',
            'Referer': 'https://femascloud.com/aetherai1/users/main?from=/Accounts/login?ext=html',  # noqa
            'Sec-Fetch-Dest': 'empty',
            'Sec-Fetch-Mode': 'cors',
            'Sec-Fetch-Site': 'same-origin',
            'X-Prototype-Version': '1.7',
            'X-Requested-With': 'XMLHttpRequest',
            'X-Update': 'clock_listing',
        }

        data = {
            '_method': 'POST',
            'data[ClockRecord][user_id]': str(user_id),
            'data[AttRecord][user_id]': str(user_id),
            'data[ClockRecord][shift_id]': '10',
            'data[ClockRecord][period]': '1',
            'data[ClockRecord][clock_type]': 'S',
            'data[ClockRecord][latitude]': '',
            'data[ClockRecord][longitude]': '',
        }

        r = self.session.post(
            self.get_api("/users/clock_listing"),
            headers=headers,
            data=data,
        )

        if r.status_code != HTTPStatus.OK:
            raise requests.exceptions.HTTPError(f"status {r.status_code}")

    def punch_out(self, user_id: t.Union[int, str]):
        headers = {
            'Accept': 'text/javascript, text/html, application/xml, text/xml, */*',  # noqa
            'Accept-Language': 'zh-TW,zh;q=0.9,en-US;q=0.8,en;q=0.7,zh-CN;q=0.6,ja;q=0.5',  # noqa
            'Connection': 'keep-alive',
            'Content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
            'Origin': 'https://femascloud.com',
            'Referer': 'https://femascloud.com/aetherai1/users/main?from=/Accounts/login?ext=html',  # noqa
            'Sec-Fetch-Dest': 'empty',
            'Sec-Fetch-Mode': 'cors',
            'Sec-Fetch-Site': 'same-origin',
            'X-Prototype-Version': '1.7',
            'X-Requested-With': 'XMLHttpRequest',
            'X-Update': 'clock_listing',
        }

        data = {
            '_method': 'POST',
            'data[ClockRecord][user_id]': str(user_id),
            'data[AttRecord][user_id]': str(user_id),
            'data[ClockRecord][shift_id]': '10',
            'data[ClockRecord][period]': '1',
            'data[ClockRecord][clock_type]': 'E',
            'data[ClockRecord][latitude]': '',
            'data[ClockRecord][longitude]': '',
        }

        r = self.session.post(
            self.get_api("/users/clock_listing"),
            headers=headers,
            data=data,
        )

        if r.status_code != HTTPStatus.OK:
            raise requests.exceptions.HTTPError(f"status {r.status_code}")
