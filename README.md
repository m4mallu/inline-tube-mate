<h1 align="left">
    <a href="https://github.com/m4mallu">Inline Tube Mate (YouTube Downloader)
</a>
</h1>

#### An Inline Telegram bot that can download YouTube videos with permanent thumbnail support

<details>
    <summary><b>About</b></summary>
    <p align="left"></p>
    <ul>
        <li><b><strike>Bot need to be in Inline Mode</strike></b></li>
        <li>Search keyword inline (In bot chat).</li>
        <li>Send a photo to bot to set custom thumbnail permanently.</li>
        <li>The thumbnail will be in all the downloads until clear it in options.</li>
        <li>View the custom thumbnail in option.</li>
        <li>If no thumbnail available, bot will set the default YouTube video thumbnail in downloading.</li>
        <li>If there are authorized users, bot will serve to them only. Else the bot will be in public domain.</li>
    </ul>
</details>
<details>
    <summary><b>@BotFather Commands</b></summary>
    <p align="left"></p>
    
    start - Check alive
    send - broadcast                        As reply to any message
    subs - Count active subscribers
</details>
<details>
    <summary><b>Mandatory Variables</b></summary>
    <p align="left"></p>
    
    API_HASH        Your API Hash from my.telegram.org
    API_ID          Your API ID from my.telegram.org
    BOT_TOKEN       Your Bot Token from BotFather
    AUTH_USERS      Create a list of User Ids to use this bot. (If kept empty, bot will be in public domain)
    SUDO_USERS      Create a list of Super User Ids to use this bot. (For Broadcasting )
    DB_URI          Mandatory when deployed in local
</details>
<details>
    <summary><b>Deploy</b></summary>
    <p align="left"></p>
    <b>1. <u>Deploy to Heroku</u></b><br>
        <a href="https://heroku.com/deploy?template=https://github.com/m4mallu/inline-tube-mate">
            <img height="30px" src="https://img.shields.io/badge/Deploy%20To%20Heroku-blueviolet?style=for-the-badge&logo=heroku">
    </a><br><br>
    <b>2. <u>Deploy to VPS</u></b><br>
    <ul>
        <li>Open a Linux Terminal and run the following commands.</li>
        <li><code>git clone https://github.com/m4mallu/inline-tube-mate</code></li>
        <li><code>cd inline-tube-mate</code></li>
        <li>Create a database URI with the <a href="https://telegra.ph/Clonebot-UI-Help-05-30"><b>TUTORIAL</b></a>.</li>
        <li>Create a <code>config.py</code> file with the mandatory variables and database URI.</li>
        <li>Run the following commands in the same terminal opened.</li>
        <li><code>virtualenv -p python3 venv</code></li>
        <li><code>. ./venv/bin/activate</code></li>
        <li><code>pip3 install -r requirements.txt</code></li>
        <li><code>python3 bot.py</code></li>
    </ul>
</details>
<details>
  <summary><b>Developer</b></summary>
    <p align="left">
        <img alt="GPL3" src ="https://c.tenor.com/10Zdx_RXqgcAAAAC/programming-crazy.gif" width="260px" style="max-width:100%;"/><br>
            <a href="https://t.me/space4renjith"><img src="https://img.shields.io/badge/Renjith-Mangal-orange" height="24">
        </a>&nbsp;
            <a href="https://t.me/rmprojects"><img src="https://img.shields.io/badge/Updates-Channel-orange" height="24">
        </a>
</p>
</details>
<details>
    <summary><b>Donate</b></summary>
    <p align="left"><br>
    <b>Buy me a coffee for the work !</b><br>
    <img src="https://telegra.ph/file/b926b7e8ea84826d81d8a.png" width="260px" style="max-width:100%;"/><br><br>
      <a href="https://www.paypal.me/space4renjith" target="_blank">
        <img src="https://img.shields.io/badge/Donate-Me-blueviolet?style=for-the-badge&logo=paypal">
    </a>
</p>
</details>
<details>
  <summary><b>Credits</b></summary>
    <p align="left">
      <a href="https://github.com/pyrogram/pyrogram">
        <img src="https://img.shields.io/badge/Pyrogram-MTProto%20API-orange?style=for-the-badge&logo=pyrogram" height="32.8">
    </a>
    <a href="https://github.com/SpEcHiDe">
        <img src="https://img.shields.io/badge/-SpEcHiDe-orange" height="32.8">
    </a>
</p>
</details>
<details>
  <summary><b>License</b></summary>
    <p align="left">
    <a href="https://choosealicense.com/licenses/gpl-3.0/">
        <img src="https://img.shields.io/badge/License-GPLv3-blueviolet?style=for-the-badge&logo=gplv3">
    </a>
</p>
</details>
<p align="center">
    <a href="https://t.me/space4renjith">
        <img alt="GPL3" src ="https://telegra.ph/file/c4f778ccfc576a954dd20.gif" width="340" height="214"/>
    </a>
</p>