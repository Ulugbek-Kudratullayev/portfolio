# Ulug'bek Kudratullayev — Portfolio

3D interactive portfolio: Next.js frontend (Vercel) + Django REST backend (Railway).
Design based on [3D-interactive-portfolio](https://github.com/Abhiz2411/3D-interactive-portfolio)
(originally by Naresh Khatri), rebuilt to serve all content from a Django API.

```
portfolio/
├── backend/    Django 6 + DRF — projects API, contact form, admin panel
├── frontend/   Next.js 14 — 3D keyboard (Spline), GSAP/Framer Motion animations
└── scripts/    Asset generation (Pillow)
```

## Backend (Django → Railway)

```bash
cd backend
python -m venv .venv && .venv\Scripts\activate
pip install -r requirements.txt
python manage.py migrate
python manage.py seed_projects        # seeds 76 projects (10 featured)
python manage.py createsuperuser
python manage.py runserver            # http://127.0.0.1:8000
```

API: `/api/projects/`, `/api/projects/?featured=true`, `/api/projects/<slug>/`,
`/api/contact/` (POST, throttled 5/hour), `/api/health/`.
Admin: `/admin/` — manage projects (featured flags, descriptions, cover images)
and read contact messages.

### Railway deploy

```bash
cd backend
railway init
railway add --database postgres
railway up
railway domain
```

Set variables: `SECRET_KEY` (random), `DEBUG=False`,
`CORS_ALLOWED_ORIGINS=https://<your-vercel-domain>`.
`DATABASE_URL` and `RAILWAY_PUBLIC_DOMAIN` are injected automatically.
Migrations + seeding run on every deploy (see `railway.json` startCommand).

## Frontend (Next.js → Vercel)

```bash
cd frontend
npm install
npm run dev                           # http://localhost:3000
```

Env (`.env.local`): `NEXT_PUBLIC_API_URL=http://127.0.0.1:8000`

If the API is unreachable the site falls back to a bundled snapshot
(`src/data/projects-fallback.json`), so it always renders.

### Vercel deploy

- Import the GitHub repo, set **Root Directory = `frontend`**.
- Env var: `NEXT_PUBLIC_API_URL=https://<railway-domain>`.
- Or with CLI: `cd frontend && vercel --prod`.

After the first deploy, add the final Vercel domain to the backend's
`CORS_ALLOWED_ORIGINS` (Vercel preview URLs `*.vercel.app` are already allowed).

## Content management

All projects/descriptions live in the Django DB. To re-seed from the scan
snapshot edit `backend/data/projects_seed.json` + the `FEATURED` overlay in
`backend/portfolio_api/management/commands/seed_projects.py` and run
`python manage.py seed_projects` (idempotent, matches by slug).

Generated cover images: `python scripts/generate_assets.py` (needs Pillow).
