import { useEffect, useState, useCallback } from "react";
import api from "../api/client";
import { useAuth } from "../context/AuthContext";
import LeadCard from "../components/LeadCard";
import Pagination from "../components/Pagination";

const REGIONS = ["India", "Southeast Asia", "Middle East", "Europe"];

export default function Dashboard() {
  const { logout } = useAuth();

  const [selectedRegions, setSelectedRegions] = useState([]);
  const [searching, setSearching] = useState(false);
  const [searchError, setSearchError] = useState(null);

  // Option B:
  // Dashboard starts empty until Run Search is clicked.
  const [hasSearched, setHasSearched] = useState(false);

  const [leads, setLeads] = useState([]);
  const [page, setPage] = useState(1);
  const [totalPages, setTotalPages] = useState(1);
  const [total, setTotal] = useState(0);
  const [search, setSearch] = useState("");
  const [loadingLeads, setLoadingLeads] = useState(false);

  // Drawer
  const [selectedLead, setSelectedLead] = useState(null);

  const toggleRegion = (region) => {
    setSelectedRegions((prev) =>
      prev.includes(region)
        ? prev.filter((r) => r !== region)
        : [...prev, region]
    );
  };

  const fetchLeads = useCallback(async (pageArg, searchArg) => {
    try {
      setLoadingLeads(true);

      const { data } = await api.get("/api/results/", {
        params: {
          page: pageArg,
          limit: 12,
          search: searchArg || undefined,
        },
      });

      setLeads(data.data);
      setTotalPages(data.pagination.totalPages);
      setTotal(data.pagination.total);
    } catch (err) {
      console.error(err);
    } finally {
      setLoadingLeads(false);
    }
  }, []);

  // Pagination/Search works ONLY after first search
  useEffect(() => {
    if (!hasSearched) return;

    fetchLeads(page, search);
  }, [page, search, hasSearched, fetchLeads]);

  const runSearch = async () => {
    if (selectedRegions.length === 0) {
      setSearchError("Select at least one region first.");
      return;
    }

    setSearchError(null);
    setSearching(true);

    try {
      await api.post("/api/search/", {
        regions: selectedRegions,
        include_maps: true,
        include_directories: true,
      });

      setHasSearched(true);
      setPage(1);

      await fetchLeads(1, search);
    } catch (err) {
      setSearchError(
        err.response?.data?.detail ||
          "Couldn't reach backend. Is FastAPI running?"
      );
    } finally {
      setSearching(false);
    }
  };

  const handleExport = async () => {
    try {
      const res = await api.get("/api/export/csv", {
        responseType: "blob",
      });

      const url = window.URL.createObjectURL(
        new Blob([res.data])
      );

      const link = document.createElement("a");

      link.href = url;
      link.download = "leads_export.csv";

      document.body.appendChild(link);

      link.click();

      link.remove();

      window.URL.revokeObjectURL(url);
    } catch (err) {
      console.error(err);
    }
  };

  const DetailRow = ({ label, value }) => (
    <div className="border-b border-white/10 py-3">
      <p className="text-xs uppercase tracking-wider text-slate-400 mb-1">
        {label}
      </p>

      <p className="text-white break-words">
        {value || "Not Available"}
      </p>
    </div>
  );

  return (    <div
      style={{
        background: "#020024",
        backgroundImage:
          "linear-gradient(90deg, rgba(2,0,36,1) 0%, rgba(9,9,121,1) 11%, rgba(0,212,255,1) 100%)",
      }}
      className="min-h-screen text-slate-100 p-8 relative overflow-hidden"
    >
      <div className="max-w-6xl mx-auto">

        {/* Header */}

        <div className="flex items-start justify-between mb-8">

          <div>

            <h1 className="text-3xl font-bold text-white mb-2">
              Lead Generation Dashboard
            </h1>

            <p className="text-slate-300">
              Pharma and Manufacturing Leads
            </p>

          </div>

          <button
            onClick={logout}
            className="bg-white/10 hover:bg-white/20 border border-white/20 px-4 py-2 rounded-lg"
          >
            Sign Out
          </button>

        </div>

        {/* Search Panel */}

        <div className="bg-white/10 backdrop-blur-lg rounded-xl border border-white/20 p-6 mb-8">

          <h2 className="text-sm uppercase tracking-wider font-semibold mb-5">

            Source New Leads

          </h2>

          <div className="flex flex-wrap gap-3 mb-6">

            {REGIONS.map((region) => (

              <button
                key={region}
                onClick={() => toggleRegion(region)}
                className={`px-4 py-2 rounded-lg transition

                ${
                  selectedRegions.includes(region)
                    ? "bg-white text-slate-900"
                    : "bg-white/5 hover:bg-white/10 border border-white/10"
                }
                
                `}
              >
                {region}
              </button>

            ))}

          </div>

          <button
            onClick={runSearch}
            disabled={searching}
            className="bg-cyan-500 hover:bg-cyan-400 disabled:opacity-40 px-6 py-3 rounded-lg font-semibold"
          >
            {searching ? "Searching..." : "Run Search"}
          </button>

          {searchError && (

            <p className="text-red-400 mt-4">

              {searchError}

            </p>

          )}

        </div>

        {/* Search */}

        {hasSearched && (

          <div className="flex justify-between items-center flex-wrap gap-4 mb-6">

            <input
              value={search}
              onChange={(e) => {
                setPage(1);
                setSearch(e.target.value);
              }}
              placeholder="Search company..."
              className="bg-white/10 border border-white/20 rounded-lg px-4 py-3 w-80 outline-none"
            />

            <div className="flex items-center gap-4">

              <span>

                {total} Leads

              </span>

              <button
                onClick={handleExport}
                className="bg-green-500 hover:bg-green-400 px-5 py-3 rounded-lg font-semibold"
              >
                Export CSV
              </button>

            </div>

          </div>

        )}

        {/* BEFORE SEARCH */}

        {!hasSearched && (

          <div className="bg-white/5 border border-white/10 rounded-xl p-16 text-center">

            <h2 className="text-2xl font-semibold mb-3">

              Welcome 👋

            </h2>

            <p className="text-slate-400">

              Select one or more regions above and click
              <strong> Run Search </strong>
              to load leads.

            </p>

          </div>

        )}

        {/* LOADING */}

        {hasSearched && loadingLeads && (

          <div className="bg-white/5 rounded-xl p-16 text-center">

            <p className="animate-pulse">

              Loading Leads...

            </p>

          </div>

        )}

        {/* NO RESULTS */}

        {hasSearched &&
          !loadingLeads &&
          leads.length === 0 && (

            <div className="bg-white/5 rounded-xl p-16 text-center">

              <p>

                No Leads Found

              </p>

            </div>

        )}

        {/* CARDS */}

        {hasSearched &&
          !loadingLeads &&
          leads.length > 0 && (

          <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-6">

            {leads.map((lead, i) => (

              <LeadCard
                key={lead.id}
                lead={lead}
                index={(page - 1) * 12 + i + 1}
                onSelect={() => setSelectedLead(lead)}
              />

            ))}

          </div>

        )}

        {hasSearched && (

          <div className="mt-8 flex justify-center">

            <Pagination
              page={page}
              totalPages={totalPages}
              onChange={setPage}
            />

          </div>

        )}

      </div>      {/* DETAILS DRAWER */}

      {selectedLead && (
        <>
          {/* Overlay */}
          <div
            className="fixed inset-0 bg-black/60 backdrop-blur-sm z-40"
            onClick={() => setSelectedLead(null)}
          />

          {/* Drawer */}
          <div className="fixed top-0 right-0 h-full w-full max-w-md bg-slate-900 border-l border-white/10 shadow-2xl z-50 overflow-y-auto transition-all duration-300">

            {/* Header */}

            <div className="sticky top-0 bg-slate-900 border-b border-white/10 p-5 flex justify-between items-center">

              <h2 className="text-xl font-bold text-white">
                Company Details
              </h2>

              <button
                onClick={() => setSelectedLead(null)}
                className="w-10 h-10 rounded-full hover:bg-white/10 flex items-center justify-center text-xl"
              >
                ✕
              </button>

            </div>

            <div className="p-6">

              {/* Company Image */}

              {selectedLead.image_url ? (

                <img
                  src={selectedLead.image_url}
                  alt={selectedLead.company_name}
                  className="w-full h-52 rounded-xl object-cover mb-6"
                />

              ) : (

                <div className="w-full h-52 rounded-xl bg-slate-800 flex items-center justify-center mb-6">

                  <span className="text-7xl font-bold text-slate-500">

                    {selectedLead.company_name?.charAt(0).toUpperCase()}

                  </span>

                </div>

              )}

              {/* Company Name */}

              <h1 className="text-2xl font-bold mb-6">

                {selectedLead.company_name}

              </h1>

              {/* Information */}

              <DetailRow
                label="Address"
                value={selectedLead.address}
              />

              <DetailRow
                label="Region"
                value={selectedLead.region}
              />

              <DetailRow
                label="Country"
                value={selectedLead.country}
              />

              <DetailRow
                label="Industry"
                value={selectedLead.industry}
              />

              <DetailRow
                label="Phone"
                value={selectedLead.phone}
              />

              <DetailRow
                label="Email"
                value={selectedLead.email}
              />

              <DetailRow
                label="QA Status"
                value={selectedLead.qa_status}
              />

              <DetailRow
                label="Source"
                value={selectedLead.source}
              />

              <DetailRow
                label="Scraped At"
                value={selectedLead.scraped_at}
              />

              {selectedLead.website && (

                <a
                  href={selectedLead.website}
                  target="_blank"
                  rel="noreferrer"
                  className="mt-8 block w-full bg-cyan-500 hover:bg-cyan-400 text-center py-3 rounded-lg font-semibold transition"
                >
                  Visit Website ↗
                </a>

              )}

            </div>

          </div>

        </>
      )}

    </div>
  );
}