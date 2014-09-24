import webob
import webob.dec
import base64
import requests
import uuid


@webob.dec.wsgify
def app(req):
    res = webob.Response()

    def fail():
        res.status = 404
        return res

    if req.method == 'GET':
        if req.path == '/new':
            discovery_token = uuid.uuid4().hex
            url = 'http://localhost:8500/v1/kv/%s' % (discovery_token,)
            r = requests.put(url, data='[]')
            res.status = 200
            res.body = discovery_token
            return res
        if req.path == '/':
            res.status = 200
            res.content_type = 'text/plain'
            res.body = 'GET /new to get a new discovery token'
            return res
        else:
            parts = req.path.split('/')

            if len(parts) != 2:
                return fail()
            try:
                url = 'http://localhost:8500/v1/kv/%s' % (parts[1],)
                r = requests.get(url)
                if r.status_code == 200:
                    res.status = 200
                    res.content_type = 'application/json'
                    res.body = base64.b64decode(r.json()[0]['Value'])
                    return res
                else:
                    return fail()
            except:
                return fail()
        return None

    elif req.method == 'PUT':
        parts = req.path.split('/')

        if len(parts) != 2:
            fail()
        try:
            url = 'http://localhost:8500/v1/kv/%s' % (parts[1],)
            r = requests.get(url)
            if r.status_code != 200:
                return fail()
            r = requests.put(url, data=req.body)
            if r.status_code == 200:
                res.status = 200
            else:
                return fail()
            return res
        except:
            return fail()
        return fail()
