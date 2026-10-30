DRAGON X — Vercel Webhook Starter

Is folder ko GitHub repository ke ROOT me upload karo. Folder ke andar files ko ek aur folder me mat chhupana.

Files:
- index.py
- requirements.txt
- vercel.json
- set_webhook.py

Vercel setup:
1. Vercel me GitHub repository import karke deploy karo.
2. Project Settings > Environment Variables me ye variables add karo:
   BOT_TOKEN       = BotFather se naya bot token
   WEBHOOK_SECRET  = 32+ characters ka random secret (sirf A-Z, a-z, 0-9, _ aur -)
   OWNER_ID        = apna Telegram numeric user ID
   UPDATE_CHANNEL  = update channel ka https://t.me/... link
   UPDATE_GROUP    = group ka https://t.me/... link
   CONTACT_USERNAME= contact ka https://t.me/... link
3. Environment variables add karne ke baad redeploy karo.
4. Deploy hone ke baad apna domain note karo, jaise:
   https://your-project.vercel.app
5. Termux/Python environment me BOT_TOKEN, WEBHOOK_URL aur WEBHOOK_SECRET set karke:
   python set_webhook.py
   WEBHOOK_URL me https://your-project.vercel.app do.
6. Browser me https://your-project.vercel.app/ kholo. status ok aana chahiye.
7. Telegram me bot ko /start bhejo.

IMPORTANT:
- Purani file me token hard-coded tha. Woh token exposed maana jana chahiye.
  BotFather me us token ko revoke karke naya token banao. Purana token dobara use mat karo.
- Token ko GitHub code me kabhi mat likho. Sirf Vercel Environment Variables me rakho.
- Ye starter /start, /help, basic menu, profile callback aur webhook receive karta hai.
- Ye arbitrary uploaded .py/.js files execute nahi karta; remote terminal, polling,
  background workers, persistent local SQLite/files aur 24x7 child-process hosting
  Vercel Functions par same tarah kaam nahi karte.
- User files ko execute karne wala feature security risk bhi create karta hai.
