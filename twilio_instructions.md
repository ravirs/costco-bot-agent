To get your Twilio environment variables, follow these steps:

1. **Create an account / Sign in**: Go to [twilio.com](https://www.twilio.com/) and create a free account or sign in.
2. **Access the Console Dashboard**: Once logged in, go to the Twilio Console homepage.
3. **Find Account SID and Auth Token**:
   - Scroll down the Console homepage to the **Account Info** section.
   - You will see **Account SID**. Copy this exact value for your `TWILIO_ACCOUNT_SID`.
   - Right below it, you will see **Auth Token**. Click the "Show" or eye icon to reveal it, and copy this value for your `TWILIO_AUTH_TOKEN`.
4. **Set up the WhatsApp Sandbox**:
   - In the left sidebar, navigate to **Messaging** -> **Try it out** -> **Send a WhatsApp message**.
   - This opens the WhatsApp Sandbox setup. 
   - You will see a Twilio phone number listed there (usually starting with `whatsapp:+1...`). Copy this exact string for your `TWILIO_WHATSAPP_NUMBER` (make sure to include the `whatsapp:` prefix).
   - Follow the instructions on the screen to connect your personal phone to the sandbox by sending the provided "join code" from your phone to that number.
5. **Set the Webhook URL (Once Deployed)**:
   - Still under Messaging -> Try it out, navigate to the **Sandbox settings** tab.
   - Under the field labeled **"When a message comes in"**, paste your deployed Render URL followed by `/webhook/whatsapp`. 
     *(Example: `https://costco-bot-xyz.onrender.com/webhook/whatsapp`)*
   - Save the settings.

Add these three values to your specific environment settings on Render alongside your Supabase and Gemini keys!
