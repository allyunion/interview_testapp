#!/usr/bin/python3

"""Demonstration of Time to Last Byte (TTLB)"""

import asyncio
from pprint import pprint
import json
import time
from urllib import request

class ServerTest(object):
    """Class to test the server"""

    def __init__(self, host, port, rps):
        self.host = host
        self.port = port
        self.url = 'http://{}:{}'.format(host, port)
        self.rps = rps
        
    async def execute_test(self):
        try:
            with request.urlopen(self.url) as response:
                start = time.time()
                data = response.read()
                end = time.time()
                return (response.getcode(), data, end - start)
        except request.URLError:
            return (504, '{}', 0)

    def do_tests(self):
        while True:
            loop = asyncio.get_event_loop()
            results = loop.run_until_complete(asyncio.gather(*[
                self.execute_test() for i in range(0, self.rps)]))
            pprint(results)
            time.sleep(1)


