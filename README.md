# birb

Reads the rss feed of reddit.com/r/mechmarket/new/.rss using feedparser and pushes a notification using PushBullet using pushbullet.py whenever a post shows up that has keyword(s) specified in search_terms.json. search_terms.json is editable through a simple web interface powered by Flask and uWSGI. 

birb.timer, birb.service, and uwsgi.service go in /etc/systemd/system

To start:

sudo systemctl daemon-reload

sudo systemctl enable birb.service

sudo systemctl enable birb.timer

sudo systemctl enable uwsgi.service

sudo systemctl start birb.timer

sudo systemctl start uwsgi.service

Check status:

sudo systemctl status birb.service

sudo systemctl status uwsgi.service

and/or

systemctl list-timers --all

