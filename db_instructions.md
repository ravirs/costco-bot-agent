To get your SUPABASE_URL and SUPABASE_KEY, follow these steps:

1. **Create an account / Sign in**: Go to https://supabase.com/ and sign in or create a free account.
2. **Create a New Project**:
   - Click "New project" on your dashboard.
   - Choose your organization, give the project a name (e.g., "costco-bot"), and define a strong database password.
   - Select a region close to your users (or your Render server).
   - Click "Create new project". It will take a few minutes to provision the database.
3. **Get your API Keys**:
   - Once the project is ready, look at the sidebar on the left and click the **Settings** gear icon (bottom left).
   - In the settings menu, select **API**.
   - Here you will find two values you need:
      - **Project URL**: This is your `SUPABASE_URL` (looks like `https://xxxxxx.supabase.co`).
      - **Project API Keys**: Under this section, find the key labeled `anon` `public`. This is your `SUPABASE_KEY`.

**IMPORTANT**: Since the bot depends on specific tables being present, you must also create the tables in your new Supabase database.

4. **Run SQL Setup**:
   - In the Supabase dashboard navigation sidebar, click on **SQL Editor**.
   - Click "New Query" and paste the following SQL commands to create the necessary tables:

```sql
-- Create users table
CREATE TABLE users (
    whatsapp_number TEXT PRIMARY KEY,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT timezone('utc'::text, now()) NOT NULL
);

-- Create receipts table
CREATE TABLE receipts (
    receipt_number TEXT PRIMARY KEY,
    user_id TEXT REFERENCES users(whatsapp_number),
    image_url TEXT,
    date_of_purchase TEXT
);

-- Create items table
CREATE TABLE items (
    id UUID DEFAULT uuid_generate_v4() PRIMARY KEY,
    receipt_id TEXT REFERENCES receipts(receipt_number),
    item_number TEXT NOT NULL,
    name TEXT NOT NULL,
    purchase_price REAL NOT NULL,
    current_price REAL,
    status TEXT DEFAULT 'tracking',
    last_checked TIMESTAMP WITH TIME ZONE DEFAULT timezone('utc'::text, now()) NOT NULL
);
```
   - Click the "Run" button to execute the query and setup your database schema.

Once you have those two keys, you can put them into your `.env` file locally or directly into your Render environment variables!
