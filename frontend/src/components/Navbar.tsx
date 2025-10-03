"use client";
import Link from "next/link";

export default function Navbar() {
  const links = [
    { href: "/", label: "Dashboard" },
    { href: "/submit", label: "Submit" },
    { href: "/indicators", label: "Indicators" },
    { href: "/packages", label: "Packages" },
    { href: "/feeds", label: "Feeds" },
    { href: "/apikeys", label: "API Keys" },
    { href: "/alerts", label: "Alerts" },
  ];
  return (
    <nav className="bg-slate-900 border-b border-slate-800 px-4 py-3 flex gap-6">
      {links.map((l) => (
        <Link key={l.href} href={l.href} className="hover:text-cyan-300">
          {l.label}
        </Link>
      ))}
    </nav>
  );
}
