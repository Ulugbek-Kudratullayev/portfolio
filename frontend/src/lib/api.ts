/**
 * Client for the Django portfolio backend (Railway).
 * Falls back to a bundled snapshot when the API is unreachable,
 * so the site never renders an empty projects section.
 */

import fallbackProjects from "@/data/projects-fallback.json";

export const API_URL =
  process.env.NEXT_PUBLIC_API_URL ?? "http://127.0.0.1:8000";

export interface ApiProject {
  slug: string;
  title: string;
  category: string;
  platform: string;
  description_en: string;
  description_uz: string;
  tech_stack: string[];
  tech_stack_raw: string;
  features: string[];
  cover_image: string | null;
  screenshots: string[];
  live_url: string;
  github_url: string;
  is_featured: boolean;
  order: number;
}

interface ApiListResponse {
  count: number;
  results: ApiProject[];
}

async function fetchPage(url: string): Promise<ApiListResponse> {
  const res = await fetch(url, { headers: { Accept: "application/json" } });
  if (!res.ok) {
    throw new Error(`API responded with ${res.status}`);
  }
  return res.json();
}

export async function fetchProjects(
  options: { featured?: boolean } = {}
): Promise<ApiProject[]> {
  const params = new URLSearchParams();
  if (options.featured) params.set("featured", "true");
  params.set("ordering", "order");
  try {
    const data = await fetchPage(`${API_URL}/api/projects/?${params}`);
    if (!data.results?.length) throw new Error("API returned no projects");
    return data.results;
  } catch {
    const snapshot = fallbackProjects as ApiProject[];
    return options.featured ? snapshot.filter((p) => p.is_featured) : snapshot;
  }
}

export interface ContactPayload {
  fullName: string;
  email: string;
  message: string;
}

export async function sendContactMessage(
  payload: ContactPayload
): Promise<void> {
  const res = await fetch(`${API_URL}/api/contact/`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({
      full_name: payload.fullName,
      email: payload.email,
      message: payload.message,
    }),
  });
  if (!res.ok) {
    const data = await res.json().catch(() => ({}));
    const detail =
      typeof data === "object" && data
        ? Object.values(data).flat().join(" ")
        : "";
    throw new Error(detail || `Request failed with ${res.status}`);
  }
}
