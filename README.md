# femascloud-auto-puncher
Automatically punch in and out for femascloud server

## Get started
1. Please create `.env` and provide environment variables in it. For `PUNCH_MINUTE`, `PUNCH_HOUR`, `PUNCH_DAY_OF_WEEK`, and `TIMEZONE`, please refer to [`celery`](https://docs.celeryq.dev/en/stable/userguide/periodic-tasks.html) for the setting.
```
ACCOUNT=
PASSWORD=
SUBDOMAIN=
PUNCH_MINUTE=
PUNCH_HOUR=
PUNCH_DAY_OF_WEEK=
TIMEZONE=
```
2. Provide `user_id` in the `indolent.txt`, which are the `user_id` of those who want to automatically punch in and out. `indolent.txt` should be in the following format. If you don't know what your `user_id` is, please see the following section.
```
2
9
23
101
```
3. Make sure you have `docker-compose`, then:
```bash
docker-compose up --build -d
```
4. Everything is done!

## How to get known with `user_id`
Leverage `FemasPuncher` to get your user_id! Please make sure you have install all the packages in the `requirements.txt` before execute the following code.
```python
from puncher import FemasPuncher

with FemasPuncher(
    account="ACCOUNT",
    password="PASSWORD",
    subdomain="SUBDOMAIN",
) as femas_puncher:
    print(femas_puncher.user_id)
```