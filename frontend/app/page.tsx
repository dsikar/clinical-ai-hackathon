"use client";

import { useCallback, useState } from "react";

type ProcessingState = "idle" | "uploading" | "processing" | "ready" | "error";

export default function HomePage() {
  const [selectedFile, setSelectedFile] = useState<File | null>(null);
  const [state, setState] = useState<ProcessingState>("idle");
  const [downloadUrl, setDownloadUrl] = useState<string>("");
  const [message, setMessage] = useState<string>("Upload an MDT Word document to begin.");

  const handleFileChange = useCallback((event: React.ChangeEvent<HTMLInputElement>) => {
    const file = event.target.files?.[0];
    setSelectedFile(file ?? null);
    setMessage(file ? `Ready to upload: ${file.name}` : "Upload an MDT Word document to begin.");
    setState("idle");
    setDownloadUrl("");
  }, []);

  const handleUpload = useCallback(async () => {
    if (!selectedFile) {
      setMessage("Please choose a .docx file first.");
      return;
    }

    setState("uploading");
    setMessage("Uploading document…");

    try {
      // Placeholder: simulate a backend call that triggers the Python extractor.
      await new Promise((resolve) => setTimeout(resolve, 1200));
      setState("processing");
      setMessage("Processing MDT tables…");

      await new Promise((resolve) => setTimeout(resolve, 1500));

      // Placeholder blob; replace by fetch to backend once implemented.
      const blob = new Blob(["Excel content placeholder"], { type: "application/vnd.ms-excel" });
      const url = URL.createObjectURL(blob);
      setDownloadUrl(url);
      setState("ready");
      setMessage("Extraction complete. Download the workbook below.");
    } catch (error) {
      console.error(error);
      setState("error");
      setMessage("Something went wrong. Please try again.");
    }
  }, [selectedFile]);

  const handleDownload = useCallback(() => {
    if (!downloadUrl) {
      return;
    }
    const link = document.createElement("a");
    link.href = downloadUrl;
    link.download = "generated-database.xlsx";
    link.click();
  }, [downloadUrl]);

  return (
    <main style={styles.main}>
      <section style={styles.card}>
        <h1 style={styles.heading}>Clinical AI MDT Extractor</h1>
        <p style={styles.subheading}>
          Upload the MDT outcome Word document to generate a prototype Excel database. The backend Python pipeline
          will parse tables, extract staging, and return a styled workbook.
        </p>

        <label htmlFor="file-input" style={styles.fileLabel}>
          <input
            id="file-input"
            type="file"
            accept=".doc,.docx"
            onChange={handleFileChange}
            style={styles.fileInput}
          />
          <span>{selectedFile ? selectedFile.name : "Choose MDT .docx file"}</span>
        </label>

        <button type="button" onClick={handleUpload} style={styles.primaryButton} disabled={state === "uploading" || state === "processing"}>
          {state === "uploading" ? "Uploading…" : state === "processing" ? "Processing…" : "Generate Workbook"}
        </button>

        <p style={styles.statusMessage}>{message}</p>

        <button
          type="button"
          onClick={handleDownload}
          style={{
            ...styles.secondaryButton,
            opacity: downloadUrl ? 1 : 0.4,
            cursor: downloadUrl ? "pointer" : "not-allowed"
          }}
          disabled={!downloadUrl}
        >
          Download Excel
        </button>
      </section>
    </main>
  );
}

const styles: Record<string, React.CSSProperties> = {
  main: {
    display: "flex",
    minHeight: "100vh",
    alignItems: "center",
    justifyContent: "center",
    padding: "2rem"
  },
  card: {
    width: "100%",
    maxWidth: "640px",
    backgroundColor: "#ffffff",
    borderRadius: "1.25rem",
    padding: "2.5rem",
    boxShadow: "0 25px 60px rgba(15, 23, 42, 0.15)",
    border: "1px solid rgba(99, 102, 241, 0.2)"
  },
  heading: {
    margin: 0,
    fontSize: "2rem",
    color: "#1f2937"
  },
  subheading: {
    marginTop: "0.75rem",
    marginBottom: "1.5rem",
    color: "#4b5563",
    lineHeight: 1.5
  },
  fileLabel: {
    display: "block",
    width: "100%",
    padding: "1rem",
    border: "1px dashed #a5b4fc",
    borderRadius: "0.75rem",
    textAlign: "center" as const,
    marginBottom: "1.5rem",
    cursor: "pointer",
    color: "#4f46e5",
    fontWeight: 600,
    backgroundColor: "#f5f3ff"
  },
  fileInput: {
    display: "none"
  },
  primaryButton: {
    width: "100%",
    padding: "0.95rem 1.5rem",
    fontSize: "1rem",
    fontWeight: 600,
    borderRadius: "0.75rem",
    border: "none",
    backgroundColor: "#4f46e5",
    color: "#ffffff",
    cursor: "pointer"
  },
  secondaryButton: {
    marginTop: "1.5rem",
    width: "100%",
    padding: "0.95rem 1.5rem",
    fontSize: "1rem",
    fontWeight: 600,
    borderRadius: "0.75rem",
    border: "1px solid #d1d5db",
    backgroundColor: "#f9fafb",
    color: "#374151"
  },
  statusMessage: {
    marginTop: "1rem",
    color: "#374151",
    minHeight: "1.5rem"
  }
};
