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
import ndjson

from time import sleep
from requests.exceptions import HTTPError as RHTTPError
from requests.exceptions import ConnectionError as RConnectionError
from requests.exceptions import ConnectTimeout as RConnectTimeout
from .wandbox_compile_response import WandboxCompileResponse


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
        get wandbox permanent link
        """
        response = requests.get(Wandbox.api_url + '/permlink/' + link, timeout=3.0)
        response.raise_for_status()
        return response.json()

    def get_permlink(self, link):
        """
        get wandbox permanent link
        .. deprecated:: 0.3.4
        """
        return Wandbox.GetPermlink(link)

    @staticmethod
    def GetTemplate(name):
        """
        get template
        """
        response = requests.get(Wandbox.api_url + '/template/' + name, timeout=3.0)
        response.raise_for_status()
        return response.json()

    @staticmethod
    def GetUser(session):
        """
        get user
        """
        response = requests.get(Wandbox.api_url + '/user.json', params={'session': session}, timeout=3.0)
        response.raise_for_status()
        return response.json()

    def create_permlink(self, ndjson):
        """
        get run_ndjson permlink
        """
        headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
        params = {}
        params.update({'compiler': self.parameter['compiler']})
        params.update({'login': False})
        params.update({'code': self.parameter['code']})
        if 'codes' in self.parameter:
            params.update({'codes': self.parameter['codes']})
        if 'options' in self.parameter:
            params.update({'options': self.parameter['options']})
        if 'stdin' in self.parameter:
            params.update({'stdin': self.parameter['stdin']})
        if 'compiler-option-raw' in self.parameter:
            params.update({'compiler-option-raw': self.parameter['compiler-option-raw']})
        if 'runtime-option-raw' in self.parameter:
            params.update({'runtime-option-raw': self.parameter['runtime-option-raw']})
        params.update({'results': ndjson})
        payload = json.dumps(params)
        response = requests.post(self.api_url + '/permlink', data=payload, headers=headers, timeout=self.timeout_)
        response.raise_for_status()
        return response.json()

    @property
    def timeout(self):
        return self.timeout_

    @timeout.setter
    def timeout(self, v):
        self.timeout_ = v

    def run(self):
        """
        excute on wandbox
        """
        headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
        payload = json.dumps(self.parameter)
        url = self.api_url + '/compile.json'
        response = requests.post(url, data=payload, headers=headers, timeout=self.timeout_)
        response.raise_for_status()
        try:
            return response.json()
        except json.decoder.JSONDecodeError as e:
            response.status_code = 500
            raise RHTTPError(e, response=response)

    def run_ndjson(self):
        """
        excute on wandbox (ndjson)
        """
        headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
        payload = json.dumps(self.parameter)
        url = self.api_url + '/compile.ndjson'
        response = requests.post(url, data=payload, headers=headers, stream=True, timeout=self.timeout_)
        response.raise_for_status()
        try:
            r = response.json(cls=ndjson.Decoder)
            if 'save' in self.parameter:
                if self.parameter['save']:
                    permlink = self.create_permlink(r)
                    r.append({'type': 'Url', 'data': permlink['url']})
                    r.append({'type': 'Permlink', 'data': permlink['permlink']})
            return r
        except Exception as e:
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
    def ShowParameter(r):
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
    def ShowResult(response, stderr=False):
        r = WandboxCompileResponse(response)
        if r.has_error():
            print(r.error())
            return 1
        if stderr:
            if r.has_compiler_output():
                print('compiler_output:')
                print(text_transform(r.compiler_output()))
            if r.has_compiler_error():
                sys.stderr.write(text_transform(r.compiler_error()))
            if r.has_program_output():
                print('program_output:')
                print(text_transform(r.program_output()))
            if r.has_program_error():
                sys.stderr.write(text_transform(r.program_error()))
        else:
            if r.has_compiler_message():
                print('compiler_message:')
                print(text_transform(r.compiler_message()))
            if r.has_program_message():
                print('program_message:')
                print(text_transform(r.program_message()))
        if r.has_url():
            print('permlink: ' + r.permlink())
            print('url: ' + r.url())
        if r.has_signal():
            print('signal: ' + r.signal())

        if r.has_status():
            return int(r.status())
        return 1

    @staticmethod
    def GetResult(response, key):
        r = WandboxCompileResponse(response)
        if r.has_error():
            return 1, r.error()
        return 0, r.get_value(key)

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
