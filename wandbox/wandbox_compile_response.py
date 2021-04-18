#!/usr/bin/env python
#
# wandbox_compile_response.py
#

"""
Wandbox Compile API response for Python
"""


#
#
class WandboxCompileResponse:

    class JsonResponse:

        def __init__(self, response):
            self.response = response

        def error(self):
            return self.get_value('error')

        def has_error(self):
            return self.has_value('error')

        def compiler_output(self):
            return self.get_value('compiler_output')

        def has_compiler_output(self):
            return self.has_value('compiler_output')

        def compiler_error(self):
            return self.get_value('compiler_error')

        def has_compiler_error(self):
            return self.has_value('compiler_error')

        def program_output(self):
            return self.get_value('program_output')

        def has_program_output(self):
            return self.has_value('program_output')

        def program_error(self):
            return self.get_value('program_error')

        def has_program_error(self):
            return self.has_value('program_error')

        def compiler_message(self):
            return self.get_value('compiler_message')

        def has_compiler_message(self):
            return self.has_value('compiler_message')

        def program_message(self):
            return self.get_value('program_message')

        def has_program_message(self):
            return self.has_value('program_message')

        def signal(self):
            return self.get_value('signal')

        def has_signal(self):
            return self.has_value('signal')

        def url(self):
            return self.get_value('url')

        def has_url(self):
            return self.has_value('url')

        def permlink(self):
            return self.get_value('permlink')

        def has_permlink(self):
            return self.has_value('permlink')

        def status(self):
            return self.get_value('status')

        def has_status(self):
            return self.has_value('status')

        def get_value(self, key):
            if key in self.response:
                return self.response[key]
            return ""

        def has_value(self, key):
            return key in self.response

    class NdJsonResponse:

        def __init__(self, response):
            self.response = response

        def error(self):
            return None

        def has_error(self):
            return False

        def compiler_output(self):
            return self.get_value('CompilerMessageS')

        def has_compiler_output(self):
            return self.has_value('CompilerMessageS')

        def compiler_error(self):
            return self.get_value('CompilerMessageE')

        def has_compiler_error(self):
            return self.has_value('CompilerMessageE')

        def program_output(self):
            return self.get_value('StdOut')

        def has_program_output(self):
            return self.has_value('StdOut')

        def program_error(self):
            return self.get_value('StdErr')

        def has_program_error(self):
            return self.has_value('StdErr')

        def compiler_message(self):
            return self.get_value(['CompilerMessageS', 'CompilerMessageE'])

        def has_compiler_message(self):
            return self.has_value(['CompilerMessageS', 'CompilerMessageE'])

        def program_message(self):
            return self.get_value(['StdOut', 'StdErr'])

        def has_program_message(self):
            return self.has_value(['StdOut', 'StdErr'])

        def signal(self):
            return self.get_value('Signal')

        def has_signal(self):
            return self.has_value('Signal')

        def url(self):
            return self.get_value('Url')

        def has_url(self):
            return self.has_value('Url')

        def permlink(self):
            return self.get_value('Permlink')

        def has_permlink(self):
            return self.has_value('Permlink')

        def status(self):
            return self.get_value('ExitCode')

        def has_status(self):
            return self.has_value('ExitCode')

        def types(self, name):
            if isinstance(name, list):
                return [d for d in self.response if d['type'] in name]
            else:
                return [d for d in self.response if d['type'] == name]

        def get_value(self, name):
            types = self.types(name)
            return "".join(d['data'] for d in types)

        def has_value(self, name):
            if isinstance(name, list):
                return any(d['type'] in name for d in self.response)
            else:
                return any(d['type'] == name for d in self.response)

    def __init__(self, response):
        if isinstance(response, list):
            self.response = WandboxCompileResponse.NdJsonResponse(response)
        else:
            self.response = WandboxCompileResponse.JsonResponse(response)

    def error(self):
        return self.response.error()

    def has_error(self):
        return self.response.has_error()

    def compiler_output(self):
        return self.response.compiler_output()

    def has_compiler_output(self):
        return self.response.has_compiler_output()

    def compiler_error(self):
        return self.response.compiler_error()

    def has_compiler_error(self):
        return self.response.has_compiler_error()

    def program_output(self):
        return self.response.program_output()

    def has_program_output(self):
        return self.response.has_program_output()

    def program_error(self):
        return self.response.program_error()

    def has_program_error(self):
        return self.response.has_program_error()

    def compiler_message(self):
        return self.response.compiler_message()

    def has_compiler_message(self):
        return self.response.has_compiler_message()

    def program_message(self):
        return self.response.program_message()

    def has_program_message(self):
        return self.response.has_program_message()

    def signal(self):
        return self.response.signal()

    def has_signal(self):
        return self.response.signal()

    def url(self):
        return self.response.url()

    def has_url(self):
        return self.response.has_url()

    def permlink(self):
        return self.response.permlink()

    def has_permlink(self):
        return self.response.has_permlink()

    def status(self):
        return self.response.status()

    def has_status(self):
        return self.response.has_status()

    def get_value(self, key):
        return self.response.get_value(key)

    def has_value(self, key):
        return self.response.has_value(key)
