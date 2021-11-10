def add_auth_request(aresponses):
    aresponses.add('demo.s20.online', '/v2api/auth/login', 'POST', {'token': 'api-token'})

