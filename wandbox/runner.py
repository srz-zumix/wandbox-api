#!/usr/bin/env python
#
# runner.py
#

"""
Wandbox runner for Python
"""

import sys
import os
import codecs

from .wandbox import Wandbox


def text_transform(value):
    try:
        if isinstance(value, str):
            return value.decode()
        # elif isinstance(value, unicode):
        #     return value.encode('utf_8')
    except Exception:
        pass
    return value


class Runner:
    """wandbox Runner class"""

    def __init__(self, lang, compiler, save, encoding, retry, retry_wait,
                    has_compiler_option_raw=True, prefix_chars='-'):
        self.wandbox = Wandbox()
        if lang is None:
            raise Exception('language is required')
        if compiler is None:
            raise Exception('compiler is required')
        self.language = lang
        self.compiler = compiler
        self.wandbox.compiler(self.compiler)
        self.retry = retry
        self.retry_wait = retry_wait
        self.prefix_chars = prefix_chars
        self.encoding = encoding
        self.switches = None
        self.wandbox.permanent_link(save)
        self.has_compiler_option_raw = has_compiler_option_raw

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
    def GetSwitches(compiler, retry, wait):
        for d in Wandbox.Call(Wandbox.GetCompilerList, retry, wait):
            if d['name'] == compiler:
                if 'switches' in d:
                    return d['switches']

    @staticmethod
    def GetDefaultOptions(compiler, retry, wait):
        opt = []
        for s in Runner.GetSwitches(compiler, retry, wait):
            if s['type'] == 'select':
                opt.append(s['default'])
            elif s['type'] == 'single':
                if s['default']:
                    opt.append(s['name'])
        return opt

    def get_switches(self):
        if not self.switches:
            self.switches = Runner.GetSwitches(self.compiler, self.retry, self.retry_wait)
        return self.switches

    def build_options(self, user_options=None, disable_options=None, use_default=True):
        options = []
        if use_default:
            switches = self.get_switches()
            if switches:
                tmp = [] if user_options is None else user_options
                for s in switches:
                    if s['type'] == 'select':
                        target = s['default']
                        candidate = [x['name'] for x in s['options']]
                        for opt in tmp:
                            if opt in candidate:
                                target = opt
                                tmp.remove(opt)
                                break
                        options.append(target)
                    elif s['type'] == 'single':
                        if s['default'] and (s['default'] not in tmp):
                            options.append(s['name'])
                options.extend(tmp)
        elif user_options:
            options.extend(user_options)
        if disable_options:
            for dis in disable_options:
                if dis in options:
                    options.remove(dis)

        self.wandbox.options(','.join(options))

    def add_compiler_options(self, option):
        if self.has_compiler_option_raw:
            self.wandbox.add_compiler_options(option)

    def build_compiler_options(self, options):
        codes = []
        for opt in options:
            if opt[0] in self.prefix_chars:
                self.add_compiler_options(opt)
            else:
                if os.path.isfile(opt):
                    codes.append(opt)
                else:
                    self.add_compiler_options(opt)
        if len(codes) == 0:
            raise Exception('error: No input source file or not exist')
        main_filepath = codes[0]
        main_files = self.open_code(main_filepath, main_filepath)
        for k, v in main_files.items():
            if k == main_filepath:
                self.wandbox.code(v)
            else:
                self.wandbox.add_file(k, v)

        for filepath_ in codes[1:]:
            filepath = filepath_.strip()
            files = self.open_code(filepath, filepath)
            self.add_compiler_options(filepath)
            for k, v in files.items():
                self.wandbox.add_file(k, v)

    def set_stdin(self, stdin):
        if stdin:
            self.wandbox.stdin(stdin)

    def set_runtime_options(self, commandlines):
        ro = '\n'.join(commandlines)
        ro = ro.replace('\\n', '\n')
        self.wandbox.runtime_options(ro)

    def run(self):
        return Wandbox.Call(lambda : self.wandbox.run(), self.retry, self.retry_wait)

    def dump(self):
        self.wandbox.dump()

    def file_open(self, path, mode):
        if self.encoding:
            file = codecs.open(path, mode, self.encoding)
        else:
            file = open(path, mode)
        return file

    def open_code(self, filepath, filename):
        if not os.path.exists(filepath):
            sys.stderr.write('error: {0}: No such file or directory\n'.format(filepath))
            sys.exit(1)
        return self.make_code(filepath, filename)

    def make_code(self, filepath, filename):
        code = ''
        file = self.file_open(filepath, 'r')
        code = file.read()
        file.close()
        return {filename: code}

    def reset(self):
        pass
