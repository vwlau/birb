# birb

Reads the rss feed of reddit.com/r/mechmarket/new.rss and pushes a notification using PushBullet whenever a post shows up that has keyword(s) specified in search_terms.txt

birb.timer and birb.service go in /etc/systemd/system

To start:

systemctl daemon-reload

systemctl enable birb.service

systemctl enable birb.timer

systemctl start birb.timer

Check status:

sudo systemctl status birb.service

and/or

systemctl list-timers --all

