"use client";
import { useEffect, useState } from "react";
import { ApiProject, fetchProjects } from "@/lib/api";

export function useApiProjects(options: { featured?: boolean } = {}) {
  const [projects, setProjects] = useState<ApiProject[]>([]);
  const [isLoading, setIsLoading] = useState(true);

  const featured = options.featured ?? false;

  useEffect(() => {
    let cancelled = false;
    fetchProjects({ featured })
      .then((data) => {
        if (!cancelled) setProjects(data);
      })
      .finally(() => {
        if (!cancelled) setIsLoading(false);
      });
    return () => {
      cancelled = true;
    };
  }, [featured]);

  return { projects, isLoading };
}
