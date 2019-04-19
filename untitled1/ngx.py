import os
def wr(key,long):
    str = '''
server {
        listen 80;
        listen [::]:80;


        root /var/www/html;

        index index.html index.htm index.nginx-debian.html;

        server_name ystorm.net;

        location / {
                try_files $uri $uri/ =404;
                rewrite ^/{}/(.*)  ystorm.net/{}/$1 redirect;
        }
}


          '''.format(key,long)

    conf = key + '.conf'
    path_n = '/etc/nginx/sites-enabled/{}'.format(conf)
    with open(path_n,'w') as f:
        f.write(str)