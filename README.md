# Tailscale SSH Notifier
This is a tailscale discord ssh notifier that monitors for new ssh sessions by looking at the log files.

*Only works for discord?*

I imagine at some stage tailscale might add a webhook event for a ssh node login event. But until this time, this cheap hack to deploy on the tailscale recorder seems to work for me.

---
To run this, please update the DISCORD_WEBHOOK_URL environment variable in the docker-compose.yml file.
