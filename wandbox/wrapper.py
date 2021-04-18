#!/usr/bin/env python
#
# wrapper.py
#

"""
Wandbox API Wrapper for Python
"""

from .wandbox import Wandbox
import fnmatch


class Wrapper:
    def __init__(self, printer=print):
        self.compiler_list = None
        self.printer = printer

    def format_indent(self, value, indent=0):
        return '{0}{1}'.format(' ' * indent, value)

    def format_default(self, name, indent=0):
        return '{0}{1} (default)'.format(' ' * indent, name)

    def languages(self, language, retry, retry_wait, verbose=False):
        if language:
            self.printer(language)
        else:
            r = self.get_compiler_list(retry, retry_wait)
            langs = map(lambda x: x['language'], r)
            self.printer('\n'.join(sorted(set(langs), key=str.lower)))

    def compilers(self, language, compiler, retry, retry_wait, verbose=False):
        r = self.get_compiler_list(retry, retry_wait)
        for d in r:
            if language:
                if language == d['language']:
                    if (compiler is None) or (fnmatch.fnmatch(d['name'], compiler)):
                        if verbose:
                            self.printer('{0}: {1}'.format(d['language'], d['name']))
                        else:
                            self.printer(d['name'])
            else:
                if (compiler is None) or (fnmatch.fnmatch(d['name'], compiler)):
                    self.printer('{0}: {1}'.format(d['language'], d['name']))

    def options(self, language, compiler, retry, retry_wait, verbose=False):
        r = self.get_compiler_list(retry, retry_wait)
        for d in r:
            prefix = ''
            indent = 0
            if language:
                if language != d['language']:
                    continue
            else:
                prefix = '{0}: '.format(d['language'])
            if compiler:
                if not fnmatch.fnmatch(d['name'], compiler):
                    continue
            if (compiler is None) or (fnmatch.fnmatch(d['name'], compiler)):
                prefix += '{0}: '.format(d['name'])
                indent = 2
            if 'switches' in d:
                switches = d['switches']
                self.printer(prefix)
                for s in switches:
                    if s['type'] == 'select':
                        default_option = s['default']
                        if 'name' in s:
                            self.printer(self.format_indent(s['name'], indent))
                        else:
                            self.printer(self.format_default(default_option, indent))
                        for o in s['options']:
                            if (o['name'] == default_option) and ('name' in s):
                                self.printer(self.format_default(o['name'], indent + 2))
                            else:
                                self.printer(self.format_indent(o['name'], indent + 2))
                    elif s['type'] == 'single':
                        if s['default']:
                            self.printer(self.format_default(s['name'], indent))
                        else:
                            self.printer(self.format_indent(s['name'], indent))

    def get_compiler_list(self, retry, retry_wait):
        if self.compiler_list is None:
            r = Wandbox.Call(Wandbox.GetCompilerList, retry, retry_wait)
            r = sorted(r, key=lambda val: val['language'].lower())
            self.compiler_list = r
        return self.compiler_list

    def resolve_compiler(self, language, compiler, retry, retry_wait, no_head=False):
        cond = '*'
        if compiler:
            if fnmatch.translate(compiler) == compiler:
                return None, None
            cond = compiler
        elif language is None:
            return None, None
        r = self.get_compiler_list(retry, retry_wait)
        for d in r:
            if language and language != d['language']:
                continue
            if no_head and 'head' in d['name']:
                continue
            if fnmatch.fnmatch(d['name'], cond):
                return d['language'], d['name']
        return None, None

    def find_compilers(self, list_json, language, compiler):
        find = []
        for d in list_json:
            if language and language != d['language']:
                continue
            if (compiler is None) or (fnmatch.fnmatch(d['name'], compiler)):
                find.append(d)
        return find

    def find_compiler(self, list_json, language, compiler):
        compiler = self.find_compilers(list_json, language, compiler)
        if len(compiler) != 1:
            raise Exception('Detected multiple compilers. Please specify so that it becomes one. --language='
                                + str(language) + ' --compiler=' + str(compiler))
        return compiler[0]

    def get_template(self, name, retry, retry_wait):
        return Wandbox.Call(lambda : Wandbox.GetTemplate(name), retry, retry_wait)

    def get_template_code(self, language, compiler, retry, retry_wait):
        r = self.get_compiler_list(retry, retry_wait)
        compiler = self.find_compiler(r, language, compiler)
        template_name = compiler['templates'][0]
        template = self.get_template(template_name, retry, retry_wait)
        return template['code']

    def get_user(self, session, retry, retry_wait):
        return Wandbox.Call(lambda : Wandbox.GetUser(session), retry, retry_wait)
