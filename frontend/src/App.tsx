import { useEffect, useState } from "react";
import "./App.css";

type Job = {
  id: number;
  type: string;
  status: string;
  run_at: string | null;
  priority: number;
};

function App() {
  const [jobs, setJobs] = useState<Job[]>([]);
  const [error, setError] = useState("");
  const [message, setMessage] = useState("");

  const [jobType, setJobType] = useState("string");
  const [payload, setPayload] = useState("");
  const [priority, setPriority] = useState(0);
  const [runAt, setRunAt] = useState("");

  async function fetchJobs() {
    try {
      const response = await fetch("http://localhost:8000/jobs/");

      if (!response.ok) {
        throw new Error("Failed to fetch jobs");
      }

      const data: Job[] = await response.json();
      setJobs(data);
      setError("");
    } catch (err) {
      setError("Could not load jobs. Is the backend running?");
      console.error(err);
    }
  }

  async function createJob(event: React.FormEvent<HTMLFormElement>) {
    event.preventDefault();
    setError("");
    setMessage("");

    const body = {
      type: jobType,
      payload: { message: payload },
      priority: Number(priority),
      run_at: runAt ? new Date(runAt).toISOString() : null,
    };

    try {
      const response = await fetch("http://localhost:8000/jobs/", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify(body),
      });

      if (!response.ok) {
        throw new Error(await response.text());
      }

      setMessage("Job created successfully!");
      setJobType("string");
      setPayload("");
      setPriority(0);
      setRunAt("");

      await fetchJobs();
    } catch (err) {
      setError(
        err instanceof Error ? err.message : "Could not create job."
      );
    }
  }

  useEffect(() => {
    fetchJobs();

    const interval = setInterval(fetchJobs, 5000);

    return () => clearInterval(interval);
  }, []);

  return (
    <main className="dashboard">
      <header className="page-header">
        <div>
          <h1>Job Scheduler</h1>
          <p>Monitor and manage your scheduled jobs.</p>
        </div>

        <button
          className="secondary-button"
          onClick={fetchJobs}
          type="button"
        >
          Refresh
        </button>
      </header>

      <section className="panel">
        <h2>Create Job</h2>

        <form onSubmit={createJob} className="job-form">
          <label>
            Job Type
            <input
              value={jobType}
              onChange={(event) => setJobType(event.target.value)}
              required
            />
          </label>

          <label>
            Payload
            <textarea
              value={payload}
              onChange={(event) => setPayload(event.target.value)}
              placeholder="Enter your job message..."
              rows={3}
              required
            />
          </label>

          <div className="form-row">
            <label>
              Priority
              <input
                type="number"
                value={priority}
                onChange={(event) =>
                  setPriority(Number(event.target.value))
                }
              />
            </label>

            <label>
              Run At (optional)
              <input
                type="datetime-local"
                value={runAt}
                onChange={(event) => setRunAt(event.target.value)}
              />
            </label>
          </div>

          <button className="primary-button" type="submit">
            Create Job
          </button>
        </form>

        {message && <p className="success-message">{message}</p>}
        {error && <p className="error-message">{error}</p>}
      </section>

      <section className="panel">
        <div className="section-heading">
          <div>
            <h2>Jobs</h2>
            <p>{jobs.length} jobs found</p>
          </div>
        </div>

        {error && jobs.length === 0 ? (
          <p className="error-message">{error}</p>
        ) : jobs.length === 0 ? (
          <p>No jobs yet. Create your first job above.</p>
        ) : (
          <div className="table-wrapper">
            <table>
              <thead>
                <tr>
                  <th>ID</th>
                  <th>Type</th>
                  <th>Status</th>
                  <th>Priority</th>
                  <th>Scheduled At</th>
                </tr>
              </thead>

              <tbody>
                {jobs.map((job) => (
                  <tr key={job.id}>
                    <td>{job.id}</td>
                    <td>{job.type}</td>
                    <td>
                      <span
                        className={`status status-${job.status.toLowerCase()}`}
                      >
                        {job.status}
                      </span>
                    </td>
                    <td>{job.priority}</td>
                    <td>
                      {job.run_at
                        ? new Date(job.run_at).toLocaleString()
                        : "Immediate"}
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        )}
      </section>
    </main>
  );
}

export default App;