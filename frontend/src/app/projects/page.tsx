"use client";
import Image from "next/image";
import Link from "next/link";
import React, { useMemo, useState } from "react";

import { coverFor } from "@/data/projects";
import { useApiProjects } from "@/hooks/use-projects";
import { cn } from "@/lib/utils";

function Page() {
  const { projects, isLoading } = useApiProjects();
  const [category, setCategory] = useState<string>("All");

  const categories = useMemo(() => {
    const unique = Array.from(new Set(projects.map((p) => p.category)));
    return ["All", ...unique.sort()];
  }, [projects]);

  const visible =
    category === "All"
      ? projects
      : projects.filter((p) => p.category === category);

  return (
    <div className="container mx-auto md:px-[50px] xl:px-[150px] text-zinc-300 min-h-screen">
      <h1 className="text-4xl mt-[100px] mb-[30px]">Projects</h1>
      <div className="flex flex-wrap gap-2 mb-[40px]">
        {categories.map((item) => (
          <button
            key={item}
            onClick={() => setCategory(item)}
            className={cn(
              "text-xs px-3 py-1 rounded-full border-[.5px] border-zinc-600 transition-colors",
              category === item
                ? "bg-zinc-200 text-zinc-900"
                : "bg-transparent text-zinc-400 hover:text-zinc-200"
            )}
          >
            {item}
          </button>
        ))}
      </div>
      {isLoading && <p className="text-zinc-500 mb-10">Loading projects…</p>}
      <ul className="grid md:grid-cols-2 lg:grid-cols-3 gap-10 place-content-around pb-20">
        {visible.map((project) => (
          <li
            className="w-full max-w-[340px] border-[.5px] rounded-md border-zinc-600 overflow-hidden"
            key={project.slug}
            style={{ backdropFilter: "blur(2px)" }}
          >
            <div className="h-[200px] relative">
              <Image
                src={coverFor(project)}
                alt={`Cover of ${project.title}`}
                className="w-full h-[200px] rounded-t-md bg-zinc-900 object-cover"
                width={340}
                height={200}
              />
              <div className="absolute top-2 right-2 text-[10px] bg-black/70 px-2 py-1 rounded-full">
                {project.category}
              </div>
            </div>
            <div className="p-4 text-zinc-300">
              <h2 className="text-xl">{project.title}</h2>
              <p className="mt-2 text-xs text-zinc-500 line-clamp-4">
                {project.description_en || project.description_uz}
              </p>
              <p className="mt-3 text-[10px] text-zinc-600 line-clamp-2">
                {project.tech_stack_raw}
              </p>
              <div className="flex gap-3 mt-3">
                {project.live_url && (
                  <Link
                    href={project.live_url}
                    target="_blank"
                    className="text-xs underline underline-offset-4 hover:text-zinc-100"
                  >
                    Live
                  </Link>
                )}
                {project.github_url && (
                  <Link
                    href={project.github_url}
                    target="_blank"
                    className="text-xs underline underline-offset-4 hover:text-zinc-100"
                  >
                    GitHub
                  </Link>
                )}
              </div>
            </div>
          </li>
        ))}
      </ul>
    </div>
  );
}

export default Page;
