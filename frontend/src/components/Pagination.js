export default function Pagination({ page, totalPages, onChange }) {
  if (totalPages <= 1) return null;

  const pages = [];
  for (let p = 1; p <= totalPages; p++) {
    if (p === 1 || p === totalPages || Math.abs(p - page) <= 1) {
      pages.push(p);
    } else if (pages[pages.length - 1] !== "…") {
      pages.push("…");
    }
  }

  // Updated base button class for translucent glass appearance
  const baseBtn =
    "min-w-[32px] h-8 px-2 rounded-md text-xs border border-white/20 bg-white/5 text-slate-200 hover:bg-white/10 hover:border-white/30 disabled:opacity-30 disabled:hover:bg-white/5 disabled:hover:border-white/20 disabled:cursor-not-allowed transition duration-150 ease-in-out font-medium";

  return (
    <div className="flex items-center justify-center gap-1.5 mt-8">
      {/* Previous Button */}
      <button className={baseBtn} disabled={page <= 1} onClick={() => onChange(page - 1)}>‹</button>
      
      {/* Page Numbers */}
      {pages.map((p, i) =>
        p === "…" ? (
          <span key={`gap-${i}`} className="px-1.5 text-white/40 text-xs font-medium tracking-wider">…</span>
        ) : (
          <button
            key={p}
            onClick={() => onChange(p)}
         
            className={`${baseBtn} ${
              p === page 
                ? "bg-white text-slate-900 border-white hover:bg-white/90 font-semibold shadow-sm scale-105" 
                : ""
            }`}
          >
            {p}
          </button>
        )
      )}
      
    
      <button className={baseBtn} disabled={page >= totalPages} onClick={() => onChange(page + 1)}>›</button>
    </div>
  );
}
