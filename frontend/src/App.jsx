import { useState } from "react";
import "./App.css";

const API_URL = "http://127.0.0.1:8000/predict";

// Number fields: the "name" must match the backend field names exactly
const NUMBER_FIELDS = [
  { name: "no_of_dependents", label: "Number of Dependents", min: 0, max: 5 },
  { name: "income_annum", label: "Annual Income", min: 1 },
  { name: "loan_amount", label: "Loan Amount", min: 1 },
  { name: "loan_term", label: "Loan Term (years)", min: 2, max: 20 },
  { name: "cibil_score", label: "CIBIL Score", min: 300, max: 900 },
  { name: "residential_assets_value", label: "Residential Assets Value", min: -100000 },
  { name: "commercial_assets_value", label: "Commercial Assets Value", min: 0 },
  { name: "luxury_assets_value", label: "Luxury Assets Value", min: 0 },
  { name: "bank_asset_value", label: "Bank Asset Value", min: 0 },
];

const INITIAL_FORM = {
  no_of_dependents: "",
  education: "Graduate",
  self_employed: "No",
  income_annum: "",
  loan_amount: "",
  loan_term: "",
  cibil_score: "",
  residential_assets_value: "",
  commercial_assets_value: "",
  luxury_assets_value: "",
  bank_asset_value: "",
};

function App() {
  const [form, setForm] = useState(INITIAL_FORM);
  const [result, setResult] = useState("");
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);

  // Update one field in the form
  const handleChange = (e) => {
    setForm({ ...form, [e.target.name]: e.target.value });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setResult("");
    setError("");
    setLoading(true);

    // Convert the number fields from text to numbers
    const payload = { ...form };
    NUMBER_FIELDS.forEach((f) => {
      payload[f.name] = Number(form[f.name]);
    });

    try {
      const response = await fetch(API_URL, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(payload),
      });
      const data = await response.json();

      if (response.ok) {
        setResult(data.prediction);
      } else if (response.status === 422) {
        // Invalid input: show which fields have problems
        const messages = data.detail.map(
          (d) => `${d.loc[d.loc.length - 1]}: ${d.msg}`
        );
        setError("Invalid input. " + messages.join("; "));
      } else {
        setError(data.detail || "Something went wrong on the server.");
      }
    } catch (err) {
      setError(
        "Cannot connect to the server. Make sure the backend is running on port 8000."
      );
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="container">
      <h1>Loan Prediction</h1>

      <form className="loan-form" onSubmit={handleSubmit}>
        <h2>Loan Application Form</h2>

        <div className="form-grid">
          {/* Dropdown: education */}
          <label>
            Education
            <select name="education" value={form.education} onChange={handleChange}>
              <option value="Graduate">Graduate</option>
              <option value="Not Graduate">Not Graduate</option>
            </select>
          </label>

          {/* Dropdown: self employed */}
          <label>
            Self Employed
            <select
              name="self_employed"
              value={form.self_employed}
              onChange={handleChange}
            >
              <option value="No">No</option>
              <option value="Yes">Yes</option>
            </select>
          </label>

          {/* All number inputs */}
          {NUMBER_FIELDS.map((f) => (
            <label key={f.name}>
              {f.label}
              <input
                type="number"
                name={f.name}
                min={f.min}
                max={f.max}
                value={form[f.name]}
                onChange={handleChange}
                required
              />
            </label>
          ))}
        </div>

        <button type="submit" disabled={loading}>
          {loading ? "Predicting..." : "Predict Loan"}
        </button>
      </form>

      {error && <div className="message error">{error}</div>}

      {result && (
        <div className="result">
          <h2>Prediction Result</h2>
          <p
            className={
              result === "Loan Approved" ? "result-text approved" : "result-text rejected"
            }
          >
            {result}
          </p>
        </div>
      )}
    </div>
  );
}

export default App;    