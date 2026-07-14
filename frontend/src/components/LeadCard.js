export default function LeadCard({ lead, index, onSelect }) {
  const initial = lead.company_name?.charAt(0)?.toUpperCase() || "?";

  const qaColor =
    lead.qa_status === "pass"
      ? "text-green-400"
      : lead.qa_status === "fail"
      ? "text-red-400"
      : "text-yellow-300";

 const handleCardClick = () => {
  if (typeof onSelect === "function") {
    onSelect();
  }
};

  return (
    <div
      onClick={handleCardClick}
      className="cursor-pointer bg-white/5 hover:bg-white/10 border border-white/10 hover:border-cyan-400 rounded-xl overflow-hidden transition-all duration-300 hover:-translate-y-1 hover:shadow-2xl"
    >
      {/* Header */}
      <div className="h-24 bg-white/5 border-b border-white/10 flex items-center justify-center">

        {lead.image_url ? (
          <img
            src={lead.image_url}
            alt={lead.company_name}
            className="w-full h-full object-cover"
          />
        ) : (
          <span className="text-3xl font-bold text-white/70">
            {initial}
          </span>
        )}

      </div>

      {/* Body */}
      <div className="p-5">

        <div className="flex justify-between items-start gap-3 mb-2">

          <h3 className="font-semibold text-white leading-snug group-hover:text-cyan-300">

            {lead.company_name}

          </h3>

          <span className="text-[10px] bg-white/10 px-2 py-1 rounded">

            #{index}

          </span>

        </div>

        <p className="text-sm text-slate-300 mb-4">

          {[lead.region, lead.industry]
            .filter(Boolean)
            .join(" • ") || "No Industry"}

        </p>

        <div className="border-t border-white/10 pt-3 flex justify-between items-center">

          <span className={`font-semibold capitalize ${qaColor}`}>

            {lead.qa_status || "unchecked"}

          </span>

          {lead.website && (
            <button
              onClick={(e) => {
                e.stopPropagation();
                window.open(lead.website, "_blank");
              }}
              className="text-cyan-400 hover:text-cyan-300 text-sm underline"
            >
              Website ↗
            </button>
          )}

        </div>

      </div>
    </div>
  );
}