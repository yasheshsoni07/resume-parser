"use client";


import { useState, useEffect } from "react";
import { supabase } from "@/lib/supabase";
import { useRouter } from "next/navigation";

import { Session } from "@supabase/supabase-js";


export default function Dashboard() {
  const router = useRouter();

  const [userId, setUserId] = useState<string | null>(null);

  const [resume, setResume] = useState<File | null>(null);
  const [requirement, setRequirement] = useState("");
  const [result, setResult] = useState<any>(null);
  const [loading, setLoading] = useState(false);

  useEffect(() => {
  const getUser = async () => {
    const { data } = await supabase.auth.getSession();
    if (!data.session) {
      router.push("/login");
    } else {
      setUserId(data.session.user.id);
    }
  };
  getUser();
}, [router]);


  const handleSubmit = async () => {
    if (!resume || !requirement) {
      alert("Please upload resume and enter requirement");
      return;
    }

    setLoading(true);
    setResult(null);

    const formData = new FormData();
    formData.append("resume_file", resume);
    formData.append("job_requirement", requirement);
    formData.append("user_id", userId!);
    
    const response = await fetch("http://127.0.0.1:8000/screen", {
      method: "POST",
      body: formData,
    });

    const data = await response.json();
    setResult(data);
    setLoading(false);
  };

  const logout = async () => {
    await supabase.auth.signOut();
    router.push("/login");
  };

  return (
    <main className="min-h-screen p-8 max-w-xl mx-auto space-y-6">
      <div className="flex justify-between items-center">
        <h1 className="text-2xl font-bold">Resume Screening</h1>
        <button onClick={logout} className="text-sm underline">
          Logout
        </button>
      </div>

      <input
        type="file"
        accept=".pdf"
        onChange={(e) => setResume(e.target.files?.[0] || null)}
      />

      <textarea
        className="w-full border p-2"
        rows={3}
        placeholder="Enter job requirement"
        value={requirement}
        onChange={(e) => setRequirement(e.target.value)}
      />

      <button
        onClick={handleSubmit}
        className="bg-black text-white px-4 py-2"
        disabled={loading}
      >
        {loading ? "Screening..." : "Screen Resume"}
      </button>

      {result && (
        <div className="border p-4 rounded">
          <p className="font-bold">
            Decision: {result.decision}
          </p>
          <p className="text-sm">
            Reason: {result.reason}
          </p>
        </div>
      )}
    </main>
  );
}
