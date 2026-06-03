import React, { useState } from "react";
import axios from "axios";

function App() {
  const [file, setFile] = useState(null);
  const [jobDescription, setJobDescription] = useState("");
  const [result, setResult] = useState(null);
  const [history, setHistory] = useState([]);

  const handleUpload = async () => {
    if (!file) {
      alert("Please upload a resume");
      return;
    }

    const formData = new FormData();
    formData.append("resume", file);
    formData.append("job_description", jobDescription);

    try {
      const response = await axios.post(
        "http://16.170.173.131/upload",
        formData
      );

      console.log(response.data);
      setResult(response.data);
    } catch (error) {
      console.log(error);
      alert(JSON.stringify(error.response?.data || error.message));
    }
  };

  const fetchHistory = async () => {
    try {
      const response = await axios.get(
        "http://16.170.173.131/history"
      );

      setHistory(Array.isArray(response.data) ? response.data : []);
    } catch (error) {
      console.log(error);
      alert("Failed to fetch history");
    }
  };

  return (
    <div className="min-h-screen bg-slate-950 text-white flex items-center justify-center p-6">
      <div className="w-full max-w-4xl bg-slate-900 rounded-3xl shadow-2xl p-8 border border-slate-800">

        <h1 className="text-5xl font-bold text-center mb-2 bg-gradient-to-r from-cyan-400 to-purple-500 bg-clip-text text-transparent">
          AI Resume Analyzer
        </h1>

        <p className="text-center text-slate-400 mb-8">
          Analyze your resume against any job description
        </p>

        <div className="space-y-6">

          <input
            type="file"
            onChange={(e) => setFile(e.target.files[0])}
            className="w-full p-3 bg-slate-800 rounded-xl border border-slate-700"
          />

          <textarea
            rows="6"
            placeholder="Paste Job Description Here..."
            value={jobDescription}
            onChange={(e) => setJobDescription(e.target.value)}
            className="w-full p-4 bg-slate-800 border border-slate-700 rounded-xl text-white"
          />

          <button
            onClick={handleUpload}
            className="w-full py-4 rounded-xl bg-gradient-to-r from-cyan-500 to-purple-600 font-bold text-lg hover:scale-105 transition-all duration-300"
          >
            Analyze Resume
          </button>

          <button
            onClick={fetchHistory}
            className="w-full py-4 rounded-xl bg-slate-700 font-bold text-lg hover:bg-slate-600 transition-all duration-300"
          >
            View History
          </button>

        </div>

        {result && (
          <div className="mt-10">

            <h2 className="text-3xl font-bold mb-4">
              ATS Score: {result.ats_score}%
            </h2>

            <div className="w-full bg-slate-700 rounded-full h-6 mb-8 overflow-hidden">
              <div
                className="h-6 rounded-full bg-gradient-to-r from-green-400 to-cyan-500"
                style={{ width: `${result.ats_score}%` }}
              />
            </div>

            <div className="grid md:grid-cols-2 gap-6">

              <div className="bg-slate-800 p-5 rounded-2xl">
                <h3 className="text-green-400 text-xl font-bold mb-3">
                  Matched Skills
                </h3>

                <div className="flex flex-wrap gap-2">
                  {(Array.isArray(result.matched_skills)
                    ? result.matched_skills
                    : String(result.matched_skills || "")
                        .split(",")
                        .filter(Boolean)
                  ).map((skill, index) => (
                    <span
                      key={index}
                      className="bg-green-500/20 text-green-300 px-3 py-1 rounded-full"
                    >
                      {skill}
                    </span>
                  ))}
                </div>
              </div>

              <div className="bg-slate-800 p-5 rounded-2xl">
                <h3 className="text-red-400 text-xl font-bold mb-3">
                  Missing Skills
                </h3>

                <div className="flex flex-wrap gap-2">
                  {(Array.isArray(result.missing_skills)
                    ? result.missing_skills
                    : String(result.missing_skills || "")
                        .split(",")
                        .filter(Boolean)
                  ).map((skill, index) => (
                    <span
                      key={index}
                      className="bg-red-500/20 text-red-300 px-3 py-1 rounded-full"
                    >
                      {skill}
                    </span>
                  ))}
                </div>
              </div>

            </div>

            {result.suggestions && result.suggestions.length > 0 && (
              <div className="mt-8 bg-slate-800 p-5 rounded-2xl">
                <h3 className="text-yellow-400 text-xl font-bold mb-3">
                  AI Suggestions
                </h3>

                <ul className="space-y-2">
                  {result.suggestions.map((suggestion, index) => (
                    <li
                      key={index}
                      className="text-slate-200"
                    >
                      • {suggestion}
                    </li>
                  ))}
                </ul>
              </div>
            )}

          </div>
        )}

        {history.length > 0 && (
          <div className="mt-10">

            <h2 className="text-3xl font-bold mb-6">
              Resume History
            </h2>

            {history.map((item) => (
              <div
                key={item.id}
                className="bg-slate-800 p-5 rounded-2xl mb-4 border border-slate-700"
              >
                <p>
                  <strong>File:</strong> {item.filename}
                </p>

                <p>
                  <strong>ATS Score:</strong> {item.ats_score}%
                </p>

                <p>
                  <strong>Matched Skills:</strong> {item.matched_skills}
                </p>

                <p>
                  <strong>Missing Skills:</strong> {item.missing_skills}
                </p>

                <p>
                  <strong>Date:</strong> {item.created_at}
                </p>
              </div>
            ))}

          </div>
        )}

      </div>
    </div>
  );
}

export default App;