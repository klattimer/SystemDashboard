System Dashboard
--

I tried using pydash to monitor my server, it wasn't very well designed, the CSS was terrible and full of javascript errors. So I spent a couple of days writing SystemDashboard, it's a fairly simple sort of thing. I'll add screenshots and video later detailing it.

This is an initial release, I hope that others will want to contribute to this. I've made it fairly modular but that itself is incomplete... Really just trying to get it out of the door.

Features
---

- Monitor current CPU usage on each core
- Monitor disk usage
- Monitor disk read writes
- Monitor network traffic
- Monitor top processes
- Monitor listening processes and connections
- Monitor logged in users
- Monitor syslog (this is an incomplete feature right now, eventually you'll be able to select the log file)
- Monitor raid rebuild status
- Monitor raid disk status
- Monitor sensor readings for temperature
- Monitor disk temperature

Requirements
---
* mdstat
* cherrypy
* psutil

Uses
---
* jquery
* chart.js
* masonry
* moment.js 
