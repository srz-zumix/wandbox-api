#!/usr/bin/env python
#
# wandbox.py
#

"""
Wandbox API for Python
"""

import sys
import requests
import json

from time import sleep
from requests.exceptions import HTTPError as RHTTPError
from requests.exceptions import ConnectionError as RConnectionError
from requests.exceptions import ConnectTimeout as RConnectTimeout


def text_transform(value):
    try:
        if isinstance(value, str):
            return value.decode()
        # elif isinstance(value, unicode):
        #     return value.encode('utf_8')
    except Exception:
        pass
    return value


#
#
class Wandbox:
    """wandbox api class"""

    # api_url = 'http://melpon.org/wandbox/api'
    api_url = 'https://wandbox.org/api'
    timeout_ = (3.0, 60.0 * 5)

    def __init__(self):
        self.reset()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.reset()
        return False

    @staticmethod
    def GetCompilerList():
        """
        get compiler list
        """
        response = requests.get(Wandbox.api_url + '/list.json', timeout=3.0)
        response.raise_for_status()
        return response.json()

    def get_compiler_list(self):
        """
        get compiler list
        .. deprecated:: 0.3.4
        """
        return Wandbox.GetCompilerList()

    @staticmethod
    def GetPermlink(link):
        """
        get wandbox permanet link
        """
        response = requests.get(Wandbox.api_url + '/permlink/' + link, timeout=3.0)
        response.raise_for_status()
        return response.json()

    @staticmethod
    def GetTemplate(name):
        """
        get template
        """
        response = requests.get(Wandbox.api_url + '/template/' + name, timeout=3.0)
        response.raise_for_status()
        return response.json()

    @property
    def timeout(self):
        return self.timeout_

    @timeout.setter
    def timeout(self, v):
        self.timeout_ = v

    def get_permlink(self, link):
        """
        get wandbox permanet link
        .. deprecated:: 0.3.4
        """
        return Wandbox.GetPermlink(link)

    def run(self):
        """
        excute on wandbox
        """
        headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
        payload = json.dumps(self.parameter)
        response = requests.post(self.api_url + '/compile.json', data=payload, headers=headers, timeout=self.timeout_)
        response.raise_for_status()
        try:
            return response.json()
        except json.decoder.JSONDecodeError as e:
            response.status_code = 500
            raise RHTTPError(e, response=response)

    def code(self, code):
        """
        set main source code
        """
        self.parameter.update({'code': code})

    def add_file(self, filename, code):
        """
        append file
        """
        if 'codes' in self.parameter:
            for f in self.parameter['codes']:
                if f['file'] == filename:
                    return
            self.parameter['codes'].append({'file': filename, 'code': code})
        else:
            self.parameter.update({'codes': [{'file': filename, 'code': code}]})

    def compiler(self, name):
        """
        set compiler name
        """
        self.parameter.update({'compiler': name})

    def options(self, options_str):
        """
        set wandbox options
        """
        self.parameter.update({'options': options_str})

    def stdin(self, input_str):
        """
        set stdin buffer
        """
        self.parameter.update({'stdin': input_str})

    def compiler_options(self, options_str):
        """
        set wandbox defined compiler options
        """
        if options_str is None:
            if 'compiler-option-raw' in self.parameter:
                del self.parameter['compiler-option-raw']
        else:
            self.parameter.update({'compiler-option-raw': options_str})

    def add_compiler_options(self, options_str):
        """
        set compiler options
        """
        if 'compiler-option-raw' not in self.parameter:
            self.compiler_options(options_str)
        else:
            option = self.parameter['compiler-option-raw']
            if len(option) > 0:
                option += '\n'
            option += options_str
            self.parameter.update({'compiler-option-raw': option})

    def runtime_options(self, options_str):
        """
        set runtime options
        """
        if options_str is None:
            if 'runtime-option-raw' in self.parameter:
                del self.parameter['runtime-option-raw']
        else:
            self.parameter.update({'runtime-option-raw': options_str})

    def add_runtime_options(self, options_str):
        """
        set runtime options
        """
        if 'runtime-option-raw' not in self.parameter:
            self.runtime_options(options_str)
        else:
            option = self.parameter['runtime-option-raw']
            if len(option) > 0:
                option += '\n'
            option += options_str
            self.parameter.update({'runtime-option-raw': option})

    def permanent_link(self, enable):
        """
        wandbox permanet link to enable
        """
        self.parameter.update({'save': enable})

    def dump(self):
        """
        dump parameters
        """
        print(self.parameter)

    def reset(self):
        """
        reset parametes
        """
        self.parameter = {'code': ''}

    @staticmethod
    def Call(action, retries, retry_wait):
        try:
            return action()
        except (RHTTPError, RConnectionError, RConnectTimeout) as e:

            def is_retry(e):
                if e is None:
                    return False
                if e.response is None:
                    return False
                return e.response.status_code in [500, 502, 503, 504]

            retries -= 1
            if is_retry(e) and retries > 0:
                try:
                    print(e.message)
                except Exception:
                    pass
                print('wait {0}sec...'.format(retry_wait))
                sleep(retry_wait)
                return Wandbox.Call(action, retries, retry_wait)
            else:
                raise
        except Exception:
            raise

    @staticmethod
    def ShowParameter(response):
        r = response
        if 'compiler' in r:
            print('compiler:' + r['compiler'])
        if 'options' in r:
            print('options:' + r['options'])
        if 'compiler-option-raw' in r:
            print('compiler-option-raw:' + r['compiler-option-raw'])
        if 'runtime-option-raw' in r:
            print('runtime-option-raw' + r['runtime-option-raw'])
        if 'created-at' in r:
            print(r['created-at'])

    @staticmethod
    def ShowResult(r, stderr=False):
        if 'error' in r:
            print(r['error'])
            return 1
        if stderr:
            if 'compiler_output' in r:
                print('compiler_output:')
                print(text_transform(r['compiler_output']))
            if 'compiler_error' in r:
                sys.stderr.write(text_transform(r['compiler_error']))
            if 'program_output' in r:
                print('program_output:')
                print(text_transform(r['program_output']))
            if 'program_error' in r:
                sys.stderr.write(text_transform(r['program_error']))
        else:
            if 'compiler_message' in r:
                print('compiler_message:')
                print(text_transform(r['compiler_message']))
            if 'program_message' in r:
                print('program_message:')
                print(text_transform(r['program_message']))
        if 'url' in r:
            print('permlink: ' + r['permlink'])
            print('url: ' + r['url'])
        if 'signal' in r:
            print('signal: ' + r['signal'])

        if 'status' in r:
            return int(r['status'])
        return 1

    @staticmethod
    def GetResult(r, key):
        if 'error' in r:
            return 1, r['error']
        elif key in r:
            return 0, r[key]
        return 0, ''

    @staticmethod
    def GetSwitches(compiler, retry, wait):
        for d in Wandbox.Call(Wandbox.GetCompilerList, retry, wait):
            if d['name'] == compiler:
                if 'switches' in d:
                    return d['switches']

    @staticmethod
    def GetDefaultOptions(compiler, retry, wait):
        opt = []
        for s in Wandbox.GetSwitches(compiler, retry, wait):
            if s['type'] == 'select':
                opt.append(s['default'])
            elif s['type'] == 'single':
                if s['default']:
                    opt.append(s['name'])
        return opt


if __name__ == '__main__':
    with Wandbox() as w:
        w.compiler('gcc-head')
        w.options('warning,gnu++1y')
        w.compiler_options('-Dx=hogefuga\n-O3')
        w.code('#include <iostream>\nint main() { int x = 0; std::cout << "hoge" << std::endl; }')
        print(w.run())
