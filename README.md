<a name="readme-top"></a>

<div align="center">
<img height="120" src="https://registry.npmmirror.com/@lobehub/assets-emoji-anim/1.0.0/files/assets/robot.webp">

# SARR
Smart Automated Review Responder(SARR) is an open-source python tool that get's user reviews from your apps (Google Play & Apple Appstore) and uses OpenAI GPT API to write a customized response to them. 

![LOGO](/images/image.png)

</div>

---

## Guide

Add your app configurations to `apps.json` following below structure

```json
[
  {
    "name": "Play App Name",
    "summary": "Play App Summary",
    "id": "package-name (com.aravi.me)",
    "supportEmail": "support@aravi.me",
    "store": "play"
  },
  {
    "name": "App Store Name",
    "summary": "App Store Summary",
    "id": "appId from appstoreconnect",
    "supportEmail": "support@aravi.me",
    "store": "apple"
  }
]
```

You need to setup environment variables 

```env
ASC_ADMIN_KEY=YOUR-APPSTORECONNECT-ADMIN-KEY
ASC_ADMIN_KEY_ID=YOUR-APPSTORECONNECT-ADMIN-KEY-ID
ASC_DEV_KEY=YOUR-APPSTORECONNECT-DEV-KEY
ASC_DEV_KEY_ID=YOUR-APPSTORECONNECT-DEV-KEY-ID
ASC_ISSUER_ID=YOUR-APPSTORECONNECT-ISSUER-ID
OPENAI_KEY=sk-XXXXXXXXXXXXXXXXXXXXXXXX
PLAY_DEVELOPER_ADMIN_JSON=YOUR-PLAY-DEVELOPER-ADMIN-JSON
```

and then just run the app with 

```bash
python3 app.py
```

Simple as that, or you could fully automate it by deploying it to Railway and run a cron job.


---
**An Aravind Chowdary Production**


