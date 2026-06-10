import SlideShow from "@/components/slide-show";
import { Button } from "@/components/ui/button";
import { TypographyH3, TypographyP } from "@/components/ui/typography";
import { ArrowUpRight } from "lucide-react";
import Link from "next/link";
import { ReactNode } from "react";
import { RiNextjsFill, RiNodejsFill, RiReactjsFill } from "react-icons/ri";
import {
  SiBootstrap,
  SiCelery,
  SiChartdotjs,
  SiCss3,
  SiDjango,
  SiDocker,
  SiExpress,
  SiFastapi,
  SiFirebase,
  SiFlask,
  SiFlutter,
  SiHtml5,
  SiJavascript,
  SiLeaflet,
  SiMongodb,
  SiMysql,
  SiOpencv,
  SiOpenai,
  SiPhp,
  SiPostgresql,
  SiPrisma,
  SiPython,
  SiPytorch,
  SiRedis,
  SiScikitlearn,
  SiSocketdotio,
  SiSqlite,
  SiTailwindcss,
  SiTelegram,
  SiThreedotjs,
  SiTypescript,
  SiVite,
  SiVuedotjs,
} from "react-icons/si";
import { ApiProject } from "@/lib/api";

const BASE_PATH = "/assets/projects-screenshots";

const ProjectsLinks = ({ live, repo }: { live?: string; repo?: string }) => {
  if (!live && !repo) return null;
  return (
    <div className="flex flex-col md:flex-row items-center justify-start gap-3 my-3 mb-8">
      {live && (
        <Link
          className="font-mono underline flex gap-2"
          rel="noopener"
          target="_new"
          href={live}
        >
          <Button variant={"default"} size={"sm"}>
            Visit Website
            <ArrowUpRight className="ml-3 w-5 h-5" />
          </Button>
        </Link>
      )}
      {repo && (
        <Link
          className="font-mono underline flex gap-2"
          rel="noopener"
          target="_new"
          href={repo}
        >
          <Button variant={"default"} size={"sm"}>
            Github
            <ArrowUpRight className="ml-3 w-5 h-5" />
          </Button>
        </Link>
      )}
    </div>
  );
};

export type Skill = {
  title: string;
  bg: string;
  fg: string;
  icon: ReactNode;
};

export const PROJECT_SKILLS: Record<string, Skill> = {
  next: { title: "Next.js", bg: "black", fg: "white", icon: <RiNextjsFill /> },
  node: { title: "Node.js", bg: "black", fg: "white", icon: <RiNodejsFill /> },
  react: { title: "React", bg: "black", fg: "white", icon: <RiReactjsFill /> },
  vue: { title: "Vue.js", bg: "black", fg: "white", icon: <SiVuedotjs /> },
  flutter: { title: "Flutter", bg: "black", fg: "white", icon: <SiFlutter /> },
  django: { title: "Django", bg: "black", fg: "white", icon: <SiDjango /> },
  fastapi: { title: "FastAPI", bg: "black", fg: "white", icon: <SiFastapi /> },
  flask: { title: "Flask", bg: "black", fg: "white", icon: <SiFlask /> },
  python: { title: "Python", bg: "black", fg: "white", icon: <SiPython /> },
  js: { title: "JavaScript", bg: "black", fg: "white", icon: <SiJavascript /> },
  ts: { title: "TypeScript", bg: "black", fg: "white", icon: <SiTypescript /> },
  html: { title: "HTML5", bg: "black", fg: "white", icon: <SiHtml5 /> },
  css: { title: "CSS3", bg: "black", fg: "white", icon: <SiCss3 /> },
  tailwind: {
    title: "Tailwind",
    bg: "black",
    fg: "white",
    icon: <SiTailwindcss />,
  },
  bootstrap: {
    title: "Bootstrap",
    bg: "black",
    fg: "white",
    icon: <SiBootstrap />,
  },
  vite: { title: "Vite", bg: "black", fg: "white", icon: <SiVite /> },
  postgres: {
    title: "PostgreSQL",
    bg: "black",
    fg: "white",
    icon: <SiPostgresql />,
  },
  mysql: { title: "MySQL", bg: "black", fg: "white", icon: <SiMysql /> },
  sqlite: { title: "SQLite", bg: "black", fg: "white", icon: <SiSqlite /> },
  mongo: { title: "MongoDB", bg: "black", fg: "white", icon: <SiMongodb /> },
  redis: { title: "Redis", bg: "black", fg: "white", icon: <SiRedis /> },
  docker: { title: "Docker", bg: "black", fg: "white", icon: <SiDocker /> },
  firebase: {
    title: "Firebase",
    bg: "black",
    fg: "white",
    icon: <SiFirebase />,
  },
  express: { title: "Express", bg: "black", fg: "white", icon: <SiExpress /> },
  telegram: {
    title: "Telegram API",
    bg: "black",
    fg: "white",
    icon: <SiTelegram />,
  },
  opencv: { title: "OpenCV", bg: "black", fg: "white", icon: <SiOpencv /> },
  pytorch: { title: "PyTorch", bg: "black", fg: "white", icon: <SiPytorch /> },
  sklearn: {
    title: "scikit-learn",
    bg: "black",
    fg: "white",
    icon: <SiScikitlearn />,
  },
  three: { title: "Three.js", bg: "black", fg: "white", icon: <SiThreedotjs /> },
  sockerio: {
    title: "WebSocket",
    bg: "black",
    fg: "white",
    icon: <SiSocketdotio />,
  },
  prisma: { title: "Prisma", bg: "black", fg: "white", icon: <SiPrisma /> },
  celery: { title: "Celery", bg: "black", fg: "white", icon: <SiCelery /> },
  php: { title: "PHP", bg: "black", fg: "white", icon: <SiPhp /> },
  openai: { title: "AI API", bg: "black", fg: "white", icon: <SiOpenai /> },
  leaflet: { title: "Leaflet", bg: "black", fg: "white", icon: <SiLeaflet /> },
  chartjs: {
    title: "Charts",
    bg: "black",
    fg: "white",
    icon: <SiChartdotjs />,
  },
};

// Tech keys that render in the "Frontend" dock; everything else goes to "Backend".
const FRONTEND_KEYS = new Set([
  "react",
  "next",
  "vue",
  "flutter",
  "js",
  "ts",
  "html",
  "css",
  "tailwind",
  "bootstrap",
  "vite",
  "three",
  "leaflet",
  "chartjs",
]);

export type Project = {
  id: string;
  category: string;
  title: string;
  src: string;
  screenshots: string[];
  skills: { frontend: Skill[]; backend: Skill[] };
  content: React.ReactNode;
  github?: string;
  live?: string;
};

function categoryKey(category: string): string {
  const c = category.toLowerCase();
  if (c.includes("ai") || c.includes("ml")) return "ai";
  if (c.includes("mobil")) return "mobile";
  if (c.includes("bot")) return "bot";
  if (c.includes("desktop")) return "desktop";
  if (c.includes("kiber") || c.includes("siem") || c.includes("security"))
    return "security";
  if (c.includes("bmi") || c.includes("kurs") || c.includes("o'quv"))
    return "edu";
  if (c.includes("cli") || c.includes("skill") || c.includes("vosita"))
    return "tools";
  return "web";
}

export function coverFor(project: ApiProject): string {
  if (project.cover_image) return project.cover_image;
  if (project.is_featured) return `${BASE_PATH}/generated/${project.slug}.png`;
  return `${BASE_PATH}/generated/cat-${categoryKey(project.category)}.png`;
}

function splitSkills(techKeys: string[]): {
  frontend: Skill[];
  backend: Skill[];
} {
  const frontend: Skill[] = [];
  const backend: Skill[] = [];
  for (const key of techKeys) {
    const skill = PROJECT_SKILLS[key];
    if (!skill) continue;
    (FRONTEND_KEYS.has(key) ? frontend : backend).push(skill);
  }
  return { frontend, backend };
}

export function apiProjectToProject(p: ApiProject): Project {
  const cover = coverFor(p);
  const screenshots = [cover, ...(p.screenshots ?? [])];
  const description = p.description_en || p.description_uz;
  return {
    id: p.slug,
    category: p.category,
    title: p.title,
    src: cover,
    screenshots,
    skills: splitSkills(p.tech_stack ?? []),
    live: p.live_url || undefined,
    github: p.github_url || undefined,
    content: (
      <div>
        <TypographyP className="font-mono">{description}</TypographyP>
        <ProjectsLinks live={p.live_url || undefined} repo={p.github_url || undefined} />
        {p.features?.length > 0 && (
          <>
            <TypographyH3 className="my-4 mt-8">Key Features</TypographyH3>
            <ul className="list-disc ml-6">
              {p.features.map((feature) => (
                <li className="font-mono" key={feature}>
                  {feature}
                </li>
              ))}
            </ul>
          </>
        )}
        {p.tech_stack_raw && (
          <>
            <TypographyH3 className="my-4 mt-8">Tech Stack</TypographyH3>
            <p className="font-mono mb-2">{p.tech_stack_raw}</p>
          </>
        )}
        <SlideShow images={screenshots} />
      </div>
    ),
  };
}
