"""Seed the Project table from data/projects_seed.json.

The JSON is the output of a full D: drive project scan (Uzbek descriptions).
A curated overlay marks featured projects and adds English descriptions.
Idempotent: re-running updates existing rows by slug.
"""

import json
from pathlib import Path

from django.conf import settings
from django.core.management.base import BaseCommand
from django.utils.text import slugify

from portfolio_api.models import Project

SEED_FILE = Path(settings.BASE_DIR) / "data" / "projects_seed.json"

# Maps keywords found in the raw tech string -> normalized frontend icon keys.
TECH_KEYWORD_MAP = {
    "django": "django",
    "drf": "django",
    "fastapi": "fastapi",
    "flask": "flask",
    "react native": "react",
    "react": "react",
    "next.js": "next",
    "nextjs": "next",
    "vue": "vue",
    "flutter": "flutter",
    "dart": "flutter",
    "python": "python",
    "typescript": "ts",
    "javascript": "js",
    "vanilla js": "js",
    "tailwind": "tailwind",
    "bootstrap": "bootstrap",
    "postgres": "postgres",
    "mysql": "mysql",
    "sqlite": "sqlite",
    "mongodb": "mongo",
    "redis": "redis",
    "docker": "docker",
    "firebase": "firebase",
    "node": "node",
    "express": "express",
    "nestjs": "node",
    "aiogram": "telegram",
    "telethon": "telegram",
    "telegram": "telegram",
    "opencv": "opencv",
    "pytorch": "pytorch",
    "yolo": "pytorch",
    "scikit-learn": "sklearn",
    "xgboost": "sklearn",
    "three.js": "three",
    "socket.io": "sockerio",
    "channels": "sockerio",
    "prisma": "prisma",
    "celery": "celery",
    "php": "php",
    "html": "html",
    "css": "css",
    "vite": "vite",
    "openai": "openai",
    "gemini": "openai",
    "leaflet": "leaflet",
    "chart.js": "chartjs",
    "recharts": "chartjs",
}

PLATFORM_MAP = [
    ("web + mobil", Project.Platform.FULLSTACK),
    ("web + desktop", Project.Platform.WEB),
    ("mobil", Project.Platform.MOBILE),
    ("desktop", Project.Platform.DESKTOP),
    ("bot", Project.Platform.BOT),
    ("cli", Project.Platform.CLI),
    ("web", Project.Platform.WEB),
]

# Featured overlay keyed by the exact "nomi" value in the seed JSON.
FEATURED = {
    "Tavsiya Tizimi": {
        "order": 1,
        "title": "Product Recommendation System",
        "description_en": (
            "A personalized product recommendation engine for e-commerce built on "
            "collaborative filtering. Implements 6 algorithms (User-Based CF, "
            "Item-Based CF, SVD, content-based TF-IDF, hybrid and popularity) over "
            "10,000+ real products from Uzum.uz, with JWT auth, an admin panel and "
            "Swagger API docs."
        ),
    },
    "E-Library": {
        "order": 2,
        "title": "E-Library — Protected Digital Library",
        "description_en": (
            "A university digital library where students read books strictly online: "
            "per-user PDF watermarking, blocked downloads/printing, a 6-role access "
            "system, reading activity logs and a statistics dashboard in 4 languages."
        ),
    },
    "EduBMI — IELTS Mock Test Platform": {
        "order": 3,
        "title": "EduBMI — IELTS Mock Test Platform",
        "description_en": (
            "A full-stack IELTS Academic simulation platform with Listening, Reading "
            "and Writing modules: 40-question tests, automatic band scoring, passage "
            "highlighting, audio playback and teacher grading workflows."
        ),
    },
    "EcoMonitor": {
        "order": 4,
        "title": "EcoMonitor — Community Environmental Monitoring",
        "description_en": (
            "A civic platform where citizens report environmental problems (waste, "
            "air/water pollution, tree cutting) with photos and location. Reports "
            "appear on an interactive map, moderators review them and statuses are "
            "tracked with rich statistics."
        ),
    },
    "Fermerlar Maktabi": {
        "order": 5,
        "title": "Farmers' School — E-Learning Platform",
        "description_en": (
            "A distance-learning platform for farmers covering agriculture, livestock "
            "and greenhouse technology: role-based cabinets, courses and lessons, "
            "auto-graded tests, PDF certificates, news, a forum and weather data."
        ),
    },
    "Masters UZ": {
        "order": 6,
        "title": "Masters UZ — Beauty Booking Platform",
        "description_en": (
            "A web + mobile platform for finding beauty professionals in Uzbekistan "
            "and booking them online. Masters manage profiles, portfolios, "
            "certificates and finances through a Flutter app; clients browse and book "
            "on the web."
        ),
    },
    "Shifo Radar": {
        "order": 7,
        "title": "Shifo Radar — Hospital Bed Tracker",
        "description_en": (
            "A real-time hospital bed availability platform consisting of a Django "
            "backend, web frontend and Flutter mobile app, with OneID authentication, "
            "QR-code lookups and live statistics dashboards."
        ),
    },
    "SIEM Platform": {
        "order": 8,
        "title": "SIEM Platform — Security Monitoring",
        "description_en": (
            "An enterprise-grade Security Information and Event Management system: "
            "log collection, 8-tier threat detection, real-time alerts, RBAC, "
            "incident management and Telegram notifications."
        ),
    },
    "AqlliDavomat — Yuzni Tanish Orqali Davomat": {
        "order": 9,
        "title": "AqlliDavomat — Face Recognition Attendance",
        "description_en": (
            "An automatic student attendance system powered by face recognition: "
            "real-time monitoring, attendance journals, group management, statistics "
            "and alerts, built with Django, React and OpenCV."
        ),
    },
    "MyRamadan": {
        "order": 10,
        "title": "MyRamadan — Ramadan Companion App",
        "description_en": (
            "A feature-complete Flutter app for Ramadan: precise suhoor/iftar times "
            "with GPS city detection, smart notifications, fasting and water "
            "tracking, Quran reading plans, daily tasks and duas — fully offline."
        ),
    },
}


def normalize_tech(raw: str) -> list[str]:
    lowered = raw.lower()
    keys: list[str] = []
    for keyword, key in TECH_KEYWORD_MAP.items():
        if keyword in lowered and key not in keys:
            keys.append(key)
    return keys


def map_platform(raw: str) -> str:
    lowered = raw.lower()
    for keyword, platform in PLATFORM_MAP:
        if keyword in lowered:
            return platform
    return Project.Platform.WEB


class Command(BaseCommand):
    help = "Seed portfolio projects from data/projects_seed.json (idempotent)."

    def handle(self, *args, **options):
        entries = json.loads(SEED_FILE.read_text(encoding="utf-8"))
        created, updated = 0, 0

        for entry in entries:
            name = entry["nomi"]
            overlay = FEATURED.get(name, {})
            features = [
                feature.strip()
                for feature in entry.get("imkoniyatlar", "").split(",")
                if feature.strip()
            ]
            defaults = {
                "title": overlay.get("title", name),
                "category": entry.get("kategoriya", ""),
                "platform": map_platform(entry.get("platforma", "")),
                "description_uz": entry.get("tavsif", ""),
                "description_en": overlay.get("description_en", ""),
                "tech_stack": normalize_tech(entry.get("texnologiyalar", "")),
                "tech_stack_raw": entry.get("texnologiyalar", "")[:500],
                "features": features,
                "is_featured": name in FEATURED,
                "order": overlay.get("order", 100),
            }
            _, was_created = Project.objects.update_or_create(
                slug=slugify(name)[:120], defaults=defaults
            )
            if was_created:
                created += 1
            else:
                updated += 1

        self.stdout.write(
            self.style.SUCCESS(
                f"Seeded projects: {created} created, {updated} updated, "
                f"{len(FEATURED)} featured."
            )
        )
