import Link from "next/link";

export default function Home() {
  return (
    <main className="flex min-h-screen items-center justify-center">
      <Link
        href="/dashboard"
        className="text-xl underline"
      >
        Go to Resume Screening
      </Link>
    </main>
  );
}
