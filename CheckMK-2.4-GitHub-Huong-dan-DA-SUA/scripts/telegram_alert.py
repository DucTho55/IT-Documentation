#!/usr/bin/env python3
# Telegram alert notification for Checkmk
# Bulk: no

import os
import sys
import urllib.parse
import urllib.request
from pathlib import Path

CONFIG = Path('/omd/sites/cmk/var/telegram_bot.conf')


def main():
    values = CONFIG.read_text(encoding='utf-8').splitlines()
    if len(values) < 2 or not values[0].strip() or not values[1].strip():
        raise ValueError('Telegram configuration is missing token or chat ID')
    token, chat_id = values[:2]
    what = os.environ.get('NOTIFY_WHAT', 'SERVICE')
    host = os.environ.get('NOTIFY_HOSTNAME', 'Unknown')
    event = os.environ.get('NOTIFY_NOTIFICATIONTYPE', 'PROBLEM')
    if what == 'HOST':
        service = 'Host availability'
        state = os.environ.get('NOTIFY_HOSTSTATE', 'UNKNOWN')
        detail = os.environ.get('NOTIFY_HOSTOUTPUT', '')
    else:
        service = os.environ.get('NOTIFY_SERVICEDESC', 'Unknown')
        state = os.environ.get('NOTIFY_SERVICESTATE', 'UNKNOWN')
        detail = os.environ.get('NOTIFY_SERVICEOUTPUT', '')

    msg = (f'CHECKMK ALERT\nEvent: {event}\nHost: {host}\n'
           f'Service: {service}\nState: {state}\nDetails: {detail}')
    form = urllib.parse.urlencode({'chat_id': chat_id, 'text': msg}).encode('utf-8')
    request = urllib.request.Request(
        f'https://api.telegram.org/bot{token}/sendMessage',
        data=form, method='POST')
    with urllib.request.urlopen(request, timeout=15) as response:
        if response.status != 200:
            raise RuntimeError('Telegram returned non-200 response')


if __name__ == '__main__':
    try:
        main()
    except Exception as exc:
        print(f'Telegram notification failed: {exc}', file=sys.stderr)
        sys.exit(1)
