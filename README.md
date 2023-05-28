# Tailscale SSH Notifier
Executes Discord webhook on new tailscale ssh session.

This is a tailscale discord ssh notifier that monitors for new ssh sessions by monitoring the directory where the .cast files are generated.

I imagine at some stage tailscale might add a webhook event for a ssh node login event. But until this time, this cheap hack to deploy on the tailscale recorder seems to work for me.

If a new file is discovered, it fires off a webhook. This has only been test for discord.

---
## Installation

```
$ git clone https://github.com/quasineutral/ts_ssh_notify
$ cd ts_ssh_notify
$ docker build .
```

Modify the docker-compose.yml, update **DISCORD_WEBHOOK_URL** environment variable and *volumes*.


### Note:
There isn't much error handling and this hasn't been extensively tested.
Furthermore, the notification message could do with some improvements. These will come in time, for now this is ok.
