"use client";

import { useRouter } from "next/navigation";

import { useEffect, useState } from "react";
import { supabase } from "@/lib/supabase";

export default function LoginPage() {



  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [message, setMessage] = useState("");
  const router = useRouter();

useEffect(() => {
  const checkSession = async () => {
    const { data } = await supabase.auth.getSession();
    if (data.session) {
      router.push("/dashboard");
    }
  };
  checkSession();
}, [router]);


  const signUp = async () => {
    const { error } = await supabase.auth.signUp({
      email,
      password,
    });

    setMessage(error ? error.message : "Signup successful");
  };

  const signIn = async () => {
  const { error } = await supabase.auth.signInWithPassword({
    email,
    password,
  });

  if (error) {
    setMessage(error.message);
  } else {
    router.push("/dashboard");
  }
};


  return (
    <main className="flex min-h-screen items-center justify-center">
      <div className="w-96 space-y-4 border p-6 rounded">
        <h2 className="text-xl font-bold text-center">Login</h2>

        <input
          className="w-full border p-2"
          type="email"
          placeholder="Email"
          value={email}
          onChange={(e) => setEmail(e.target.value)}
        />

        <input
          className="w-full border p-2"
          type="password"
          placeholder="Password"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
        />

        <button
          className="w-full bg-black text-white p-2"
          onClick={signIn}
        >
          Sign In
        </button>

        <button
          className="w-full border p-2"
          onClick={signUp}
        >
          Sign Up
        </button>

        {message && (
          <p className="text-center text-sm text-red-600">
            {message}
          </p>
        )}
      </div>
    </main>
  );
}
