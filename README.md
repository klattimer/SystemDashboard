System Dashboard
-

This project has grown out of a need to have something which I can run on my servers without needing infrastructure or anything which allows me to monitor stuff going on, on that system, I'm not too bothered about aggregation or logging, in this project, I simply want to get information about the current state, periodically and display it in a way which I can survey at a glance.

It *could* be extended to add other features such as SNMP support and other such things, but it's really a simple tool which means instead of sshing into the system, typing a bunch of commands and making sure things are OK, instead I can go to a web page and see everything neatly organised and readable. 

I tried using pydash (https://gitlab.com/k3oni/pydash) to monitor my servers, it wasn't very well designed, the CSS was terrible and full of javascript errors, I first looked at fixing PyDash, but that seemed utterly pointless. So I spent a couple of days writing SystemDashboard.

Installation
---

    SystemDashboard$ virtualenv -p python3 venv
    SystemDashboard$ source venv/bin/activate
    (venv) SystemDashboard$ pip install -r requirements.txt
    (venv) SystemDashboard$ python app.py


Features
---

"So what does it do?"
"That's the beauty of it, it doesn't _/DO/_ anything"

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
- Radar readout of local pingable addresses, helpful to see dropoffs. 

Planned features
---

- SMART monitoring for the disks
- Network interface information
- System Warnings/Errors as popups
- An arbitrary interface for charts and tables
- A template driven UI, at present it's mostly static 
- Reboot and shutdown the system, logging that it is occurring and having a UI which can cope with it offlining 
- A small, efficient javascript library to make it easy to add new modules directly via templates and python code
- Zeroconf to announce itself, and a way of seeing "other" systems which are available to view.

Requirements
---
* mdstat
* cherrypy
* psutil
* netaddr

Javascript libraries used
---
* jquery
* chart.js
* masonry - this may be removed.
* moment.js 
* font awesome 

Screenshots
---

![main](https://github.com/klattimer/SystemDashboard/raw/master/Screenshot/dashboard.png)
![network](https://github.com/klattimer/SystemDashboard/raw/master/Screenshot/dashboard2.png)
![disk](https://github.com/klattimer/SystemDashboard/raw/master/Screenshot/dashboard3.png)
