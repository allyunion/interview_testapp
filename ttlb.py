#!/usr/bin/python3

"""Demonstration of Time to Last Byte (TTLB)"""

import argparse
import asyncio
from pprint import pprint
import time
from urllib import request
from warnings import warn

class ServerTest:
    """Class to test the server"""

    def __init__(self, host, port, rps):
        """ServerTest takes parameters of ServerTest(host, port, rps)
           where rps is requests per second"""
        self.host = host
        self.port = port
        self.url = 'http://{}:{}'.format(host, port)
        self.rps = rps

    async def execute_test(self):
        """Execute the test"""
        try:
            with request.urlopen(self.url) as response:
                start = time.time()
                data = response.read()
                end = time.time()
                return (response.getcode(), data, end - start)
        except request.URLError:
            return (504, '{}', 0)

    def do_tests(self):
        """Loop continuously and sleep 1 second between each execution of
           concurrent execute_tests * rps"""
        while True:
            loop = asyncio.get_event_loop()
            results = loop.run_until_complete(asyncio.gather(*[
                self.execute_test() for i in range(0, self.rps)]))
            errors = [result[0] == 200 for result in results]
            pprint(results)
            if False in errors:
                warn(('Warning: One or more errors detected in last'
                      ' batch of {} queries').format(self.rps))
            else:
                print('No errors in last batch of {} queries'.format(self.rps))
            errors = [x[0] == 200 for x in results]
            if False in errors:
                warn("Warning: Received non-200 status code response!")
            time.sleep(1)

def main():
    """Main function"""

    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--host",
        default="localhost",
        help="Specify the host")
    parser.add_argument(
        "--port",
        default=8080,
        help="Specify the port")
    parser.add_argument(
        "--rps",
        default=100,
        help="Requests per second")
    args = parser.parse_args()
    tests = ServerTest(args.host, args.port, args.rps)
    tests.do_tests()

if __name__ == "__main__":
    main()
