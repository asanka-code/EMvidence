# EMvidence

## About
EMvidence is a tool that can be used to gather insights from electromagnetic (EM) side-channel emissions of computers.

Run the start.sh shell script to start the web service.

TODO:

- Dashboard should display a summary of data and supported features of the framework.
- Settings page should facilitate adding a new user.

## Setting up EMvidence:

1. Install and start Nginx web server:
```
sudo apt-get install nginx
sudo service nginx start
```

2. Copy the files and directories of the EMvidence flask app into the Nginx web root directory (/var/www/html).

3. Create an nginx configuration file called "emvidenceapp" using the following command.
	
	sudo nano /etc/nginx/sites-available/emvidenceapp

Add the following content to that file.
```
server {
	listen 80 default_server;
	listen [::]:80;

	root /var/www/html;

	server_name example.com;

	location /static {
	    alias /var/www/html/static;
	}

	location / {
	    try_files $uri @wsgi;
	}

	location @wsgi {
	    proxy_pass http://unix:/tmp/gunicorn.sock;
	    include proxy_params;
	}

	location ~* .(ogg|ogv|svg|svgz|eot|otf|woff|mp4|ttf|css|rss|atom|js|jpg|jpeg|gif|png|ico|zip|tgz|gz|rar|bz2|doc|xls|exe|ppt|tar|mid|midi|wav|bmp|rtf)$ {
	    access_log off;
	    log_not_found off;
	    expires max;
	}
}
```

4. Change the symbolic link to the emvidenceapp in the sites-enabled directory of nginx.

	cd /etc/nginx/sites-enabled/
	sudo rm default
	sudo ln -s /etc/nginx/sites-available/emvidenceapp .

5. Test the nginx settings and if there are no issues, reload the nginx service.

	sudo nginx -t 
	sudo service nginx reload

6. Install the Gunicorn WSGI server.

	sudo apt install gunicorn3

7.  Start WSGI server with the following command.

	sudo gunicorn3 --bind=unix:/tmp/gunicorn.sock --workers=4 --chdir /var/www/html main:app

Now, open a web browser and goto 'localhost' to access the EMvidence web interface.


## Requirements:

1. Disabling Web browser caching (Firefox) :
    Type in the address bar **about:config**, then press the button **i'l be careful i promise**. Then type in the bar **browser.cache.disk.enable**. Then double click on it to make it  **false**. Do the same with **browser.cache.memory.enable**. Then, exit firefox and restart-it.
