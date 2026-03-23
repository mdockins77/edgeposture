# EdgePosture — Deployment Guide
# Run these commands in order from your Windows Terminal / PowerShell

# ============================================================
# STEP 1: CREATE D1 DATABASE
# ============================================================
# Run this once. Copy the database_id it gives you.

cd C:\Users\miked\edgeposture\worker-api
wrangler d1 create edgeposture-db

# >> COPY the database_id from the output
# >> Open worker-api/wrangler.toml
# >> Replace "REPLACE_WITH_YOUR_D1_ID" with the real ID

# ============================================================
# STEP 2: RUN D1 MIGRATION
# ============================================================

wrangler d1 execute edgeposture-db --file=migrations/0001_init.sql

# ============================================================
# STEP 3: CREATE KV NAMESPACE
# ============================================================

wrangler kv namespace create CACHE

# >> COPY the id from the output
# >> Open worker-api/wrangler.toml
# >> Replace "REPLACE_WITH_YOUR_KV_ID" with the real ID

# ============================================================
# STEP 4: SET JWT SECRET
# ============================================================
# This will prompt you to type a secret value.
# Use a long random string like: EdgePosture_JWT_2025_xK9mP3qR

wrangler secret put JWT_SECRET

# ============================================================
# STEP 5: DEPLOY THE WORKER API
# ============================================================

wrangler deploy

# Note the URL it gives you (something like edgeposture-api.YOUR-SUBDOMAIN.workers.dev)
# We'll set up the custom domain api.edgepostureapp.com in the dashboard after.

# ============================================================
# STEP 6: BUILD & DEPLOY THE SCANNER APP (edgepostureapp.com)
# ============================================================

cd C:\Users\miked\edgeposture\edgepostureapp
npm install
npm run build
wrangler pages deploy dist --project-name=edgepostureapp

# ============================================================
# STEP 7: DEPLOY THE MARKETING SITE (edgeposture.ai)
# ============================================================

cd C:\Users\miked\edgeposture\edgeposture-ai
wrangler pages deploy . --project-name=edgeposture-ai

# ============================================================
# STEP 8: DEPLOY THE CONSULTING SITE (getedgeposture.com)
# ============================================================

cd C:\Users\miked\edgeposture\getedgeposture
wrangler pages deploy . --project-name=getedgeposture

# ============================================================
# STEP 9: CONNECT CUSTOM DOMAINS (Cloudflare Dashboard)
# ============================================================
# For each Pages project, go to:
# dash.cloudflare.com > Workers & Pages > [project] > Custom Domains
#
# edgeposture-ai      → edgeposture.ai
# edgepostureapp      → edgepostureapp.com
# getedgeposture      → getedgeposture.com
# edgeposture-api     → api.edgepostureapp.com  (Worker route)
#
# Since all 3 domains are already in your CF account, this is
# just a few clicks — CF handles the DNS and SSL automatically.

# ============================================================
# STEP 10: UPDATE API URL IN SCANNER APP
# ============================================================
# Once api.edgepostureapp.com is live, the API const in
# edgepostureapp/src/App.jsx already points to it.
# If you want to test locally first, temporarily change it to:
# const API = 'https://edgeposture-api.YOUR-SUBDOMAIN.workers.dev'

# ============================================================
# LOCAL DEVELOPMENT
# ============================================================

# Terminal 1 - Run the Worker locally:
cd C:\Users\miked\edgeposture\worker-api
wrangler dev

# Terminal 2 - Run the React app locally:
cd C:\Users\miked\edgeposture\edgepostureapp
npm run dev
# Open http://localhost:5173

# ============================================================
# USEFUL COMMANDS
# ============================================================

# View D1 database content:
wrangler d1 execute edgeposture-db --command="SELECT * FROM scans LIMIT 10"

# View Worker logs in real-time:
wrangler tail

# Redeploy worker after changes:
cd C:\Users\miked\edgeposture\worker-api && wrangler deploy

# Redeploy scanner app after changes:
cd C:\Users\miked\edgeposture\edgepostureapp && npm run build && wrangler pages deploy dist --project-name=edgepostureapp
