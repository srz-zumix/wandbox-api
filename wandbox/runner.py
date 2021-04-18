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


class Runner:
    """wandbox Runner class"""

    def __init__(self, lang, compiler, save, encoding, retry, retry_wait, prefix_chars='-'):
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
        self.has_compiler_option_raw = True
        self.has_runtime_option_raw = True

    def get_switches(self):
        if not self.switches:
            self.switches = Wandbox.GetSwitches(self.compiler, self.retry, self.retry_wait)
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

    def add_commandline_options(self, option):
        if self.has_compiler_option_raw:
            self.wandbox.add_compiler_options(option)
        elif self.has_runtime_option_raw:
            self.wandbox.add_runtime_options(option)

    def build_compiler_options(self, options):
        codes = []
        if options[-1] == '-':
            options.pop(-1)
            codes.append('-')

        for opt in options:
            if opt[0] in self.prefix_chars:
                self.add_commandline_options(opt)
            else:
                if os.path.isfile(opt):
                    codes.append(opt)
                else:
                    self.add_commandline_options(opt)
        if len(codes) == 0:
            raise Exception('error: No input source file or not exist')
        main_filepath = codes[0]
        main_files = self.open_main_code(main_filepath, main_filepath)
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

    def run_nd(self):
        return Wandbox.Call(lambda : self.wandbox.run_ndjson(), self.retry, self.retry_wait)

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

    def open_main_code(self, filepath, filename):
        if filename == '-':
            return self.make_code(sys.stdin, filepath, filename)
        else:
            return self.open_code(filepath, filename)

    def open_code(self, filepath, filename):
        if not os.path.exists(filepath):
            sys.stderr.write('error: {0}: No such file or directory\n'.format(filepath))
            sys.exit(1)
        with self.file_open(filepath, 'r') as file:
            return self.make_code(file, filepath, filename)

    def make_code(self, file, filepath, filename):
        code = file.read()
        return {filename: code}

    def reset(self):
        pass
