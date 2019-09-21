# -*- coding:utf-8 -*-
class UserAgentMiddleware:
    def __init__(self, get_response=None):
        pass

    def process_request(self, request):
        print(request)

    def process_response(self, request, response):
        pass
