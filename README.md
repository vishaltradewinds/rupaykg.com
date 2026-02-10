# RupayKG Enterprise

RupayKG is a monorepo with:
- **FastAPI backend** in `backend/`
- **Next.js frontend** in `frontend/`

This project now includes a production-ready Docker Compose setup for **Hostinger VPS** deployments.

## 1) Environment setup

Copy and edit the environment file before any deployment:

```bash
cp .env.example .env
```

Minimum production values:
- `ENV=prod`
- `SYSTEM_STATUS=ACTIVE`
- `MONGODB_URI=mongodb://mongo:27017` (for Docker Compose internal network)
- `JWT_SECRET=<strong-random-secret>`
- `BACKEND_CORS_ORIGINS=https://your-domain.com`
- `NEXT_PUBLIC_WALLET_BEARER_TOKEN=<optional>`

> For Hostinger setup in this repo, `NEXT_PUBLIC_API_URL` is injected as `/api` in compose so frontend and backend work under one domain.

---

## 2) Deploying to Hostinger VPS (recommended)

### Prerequisites on VPS

Install Docker + Docker Compose plugin on Ubuntu:

```bash
sudo apt-get update
sudo apt-get install -y ca-certificates curl gnupg
sudo install -m 0755 -d /etc/apt/keyrings
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /etc/apt/keyrings/docker.gpg
sudo chmod a+r /etc/apt/keyrings/docker.gpg

echo \
  "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.gpg] https://download.docker.com/linux/ubuntu \
  $(. /etc/os-release && echo "$VERSION_CODENAME") stable" | \
  sudo tee /etc/apt/sources.list.d/docker.list > /dev/null

sudo apt-get update
sudo apt-get install -y docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin
```

### Deployment steps

```bash
git clone <your-repo-url> /opt/rupaykg-enterprise
cd /opt/rupaykg-enterprise
cp .env.example .env
nano .env

./deploy/hostinger-deploy.sh
```

This launches:
- `frontend` on internal port `3000`
- `backend` on internal port `8080`
- `mongo` for persistence
- `nginx` exposing ports `80/443`

### Health check

```bash
curl http://<server-ip>/api/health
```

Expected response:

```json
{"status":"ok"}
```

---

## 3) TLS/HTTPS on Hostinger

The Nginx container includes paths for Let's Encrypt cert mounting:
- `deploy/certbot/conf`
- `deploy/certbot/www`

You can attach certbot in your VPS workflow and mount issued certs into Nginx, then extend `deploy/nginx/default.conf` for SSL server blocks.

---

## 4) Local development

### Frontend

```bash
cd frontend
npm install
npm run dev
```

### Backend

```bash
cd backend
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload --host 0.0.0.0 --port 8080
```

---

## 5) Useful operations on VPS

```bash
# service status
docker compose -f deploy/docker-compose.hostinger.yml ps

# logs
docker compose -f deploy/docker-compose.hostinger.yml logs -f --tail=100

# restart
docker compose -f deploy/docker-compose.hostinger.yml restart

# shutdown
docker compose -f deploy/docker-compose.hostinger.yml down
```
