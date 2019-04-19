from concurrent.futures import ThreadPoolExecutor
from tornado.concurrent import run_on_executor
import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web
import tornado.gen
import json
import short_url
import sql
import ngx



def add(key,long):
     if key != '':
         ngx.wr(key,key)
         return key
     else:
            x = 0;
            for i in key:
                x = x + ord(i)
            res = short_url.encode_url(x)
            sql.insert(res,long,0)
            ngx.wr(key,long)
     return res

class MainHandler(tornado.web.RequestHandler):
    executor = ThreadPoolExecutor(32)
    def get(self):
        """get请求"""
        htmlStr =   '''
                    <!DOCTYPE HTML><html>
                    <meta charset="utf-8">
                    <head><title>Get page</title></head>
                    <body>
                    <form		action="/post"	method="post" >
                    your long index:<br>
                    <input type="text"      name ="long"     /><br>
                    your key:<br>
                    <input type="text"      name ="key"     /><br>
                    <input type="submit"	value="input"	/>
                    </form></body> </html>
                    '''
        self.write(htmlStr)


    @tornado.gen.coroutine
    def post(self):
        '''post接口,获取参数'''
        key = self.get_argument("key",None)
        print(key)
        long = self.get_argument("long",None)
        print(long)
        yield self.coreOperation(key,long)

    @run_on_executor
    def coreOperation(self,key,long):
        '''主函数'''

        result = add(key,long)  #可调用其他压缩函数
        result = json.dumps({'code': 200, 'result': result })
        self.write(result)

if __name__ == "__main__":

    tornado.options.parse_command_line()
    app = tornado.web.Application(handlers=[(r'/post', MainHandler)], autoreload=False, debug=False)
    http_server = tornado.httpserver.HTTPServer(app)
    http_server.listen(8080)
    tornado.ioloop.IOLoop.instance().start()
