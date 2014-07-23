# Copyright (c) 2013. Librato, Inc.
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#     * Redistributions of source code must retain the above copyright
#       notice, this list of conditions and the following disclaimer.
#     * Redistributions in binary form must reproduce the above copyright
#       notice, this list of conditions and the following disclaimer in the
#       documentation and/or other materials provided with the distribution.
#     * Neither the name of Librato, Inc. nor the names of project contributors
#       may be used to endorse or promote products derived from this software
#       without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND
# ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
# DISCLAIMED. IN NO EVENT SHALL LIBRATO, INC. BE LIABLE FOR ANY
# DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES
# (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
# LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND
# ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
# (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
# SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.


class ClientError(Exception):
    """4xx client exceptions"""
    def __init__(self, code, msg=None):
        self.code = code
        msg = "[%s] %s" % (code, msg)
        Exception.__init__(self, msg)


class BadRequest(ClientError):
    """400 Forbidden"""
    def __init__(self, msg=None):
        ClientError.__init__(self, 400, msg)


class Unauthorized(ClientError):
    """401 Unauthorized"""
    def __init__(self, msg=None):
        ClientError.__init__(self, 401, msg)


class Forbidden(ClientError):
    """403 Forbidden"""
    def __init__(self, msg=None):
        ClientError.__init__(self, 403, msg)


class NotFound(ClientError):
    """404 Forbidden"""
    def __init__(self, msg=None):
        ClientError.__init__(self, 404, msg)

CODES = {
    400: BadRequest,
    401: Unauthorized,
    403: Forbidden,
    404: NotFound
}

# Parse error hash from the API
class ErrorMessageParser(object):
    # See http://dev.librato.com/v1/responses-errors
    # Examples:
    # {
    #   "errors": {
    #     "params": {
    #       "name":["is not present"],
    #       "start_time":["is not a number"]
    #      }
    #    }
    #  }
    #
    #
    # {
    #   "errors": {
    #     "request": [
    #       "Please use secured connection through https!",
    #       "Please provide credentials for authentication."
    #     ]
    #   }
    # }

    @classmethod
    def parse(self, error_resp):
        errors = error_resp['errors']
        messages = []
        for key in errors:
            for v in errors[key]:
                msg = "%s: %s" % (key, v)
                if isinstance(errors[key], dict):
                    msg += ": "
                    # Join error messages with commas
                    msg += ", ".join(errors[key][v])
                messages.append(msg)
        return ", ".join(messages)

# http://dev.librato.com/v1/responses-errors
def get(code, resp_data):
    if resp_data:
        msg = ErrorMessageParser.parse(resp_data)
    if code in CODES:
        return CODES[code](msg)
    else:
        return ClientError(code, msg)
