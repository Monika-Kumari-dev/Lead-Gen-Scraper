import { useState } from "react";
import { useAuth } from "../context/AuthContext";

export default function Login() {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState(null);
  const [loading, setLoading] = useState(false);
  const { login } = useAuth();

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError(null);
    setLoading(true);
    try {
      await login(email, password);
    } catch (err) {
      setError(err.response?.data?.detail || "Login failed");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div 
      style={{
        background: '#020024',
        backgroundImage: 'linear-gradient(90deg, rgba(2, 0, 36, 1) 0%, rgba(9, 9, 121, 1) 11%, rgba(0, 212, 255, 1) 100%)'
      }}
      className="min-h-screen text-slate-100 flex items-center justify-center p-8"
    >
      <form 
        onSubmit={handleSubmit} 
     
        className="bg-white/10 backdrop-blur-md border border-white/20 rounded-xl p-10 w-full max-w-md min-h-[440px] flex flex-col justify-center shadow-xl"
      >
        <h1 className="text-2xl font-semibold mb-1">Lead Gen Dashboard</h1>
        <p className="text-slate-300/70 text-sm mb-8">Sign in to continue</p>

        <label className="block text-xs text-slate-300 font-medium mb-1.5">Email Address</label>
        <input
          type="email"
          value={email}
          onChange={(e) => setEmail(e.target.value)}
          required
          autoFocus
     
          className="w-full bg-white/5 border border-white/20 rounded-md px-3 py-2.5 text-sm mb-6 text-white placeholder-slate-400 focus:outline-none focus:border-white/60 focus:bg-white/10 transition"
          placeholder="name@company.com"
        />

        <label className="block text-xs text-slate-300 font-medium mb-1.5">Password</label>
        <input
          type="password"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
          required
   
          className="w-full bg-white/5 border border-white/20 rounded-md px-3 py-2.5 text-sm mb-6 text-white placeholder-slate-400 focus:outline-none focus:border-white/60 focus:bg-white/10 transition"
          placeholder="••••••••"
        />

        {error && <p className="text-red-400 text-xs mb-4 font-medium">{error}</p>}

        <button
          type="submit"
          disabled={loading}
          className="w-full mt-auto bg-white/20 hover:bg-white/30 border border-white/30 disabled:opacity-40 text-white py-2.5 rounded-md text-sm font-semibold transition duration-200 ease-in-out shadow-sm"
        >
          {loading ? "Signing in…" : "Sign in"}
        </button>
      </form>
    </div>
  );
}
