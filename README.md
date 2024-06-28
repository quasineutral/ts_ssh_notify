# Tailscale SSH Notifier
Executes Discord webhook request when a new tailscale ssh session is discovered on your tsrecorder instance.

This is a tailscale discord ssh notifier that monitors for new ssh sessions by monitoring the directory where the .cast files are generated.

I imagine at some stage tailscale might add a webhook event for a ssh node login event. At that point this script will be redundant.

---
## Installation

```
$ git clone https://github.com/quasineutral/ts_ssh_notify
$ cd ts_ssh_notify
$ docker build .
```

Create a .env file with the following content:

```
DISCORD_WEBHOOK_URL=https://discord.com/api/webhooks/...
```


### Note:
There isn't much error handling and this hasn't been extensively tested.