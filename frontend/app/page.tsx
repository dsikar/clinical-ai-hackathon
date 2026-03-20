"use client";

import Image from "next/image";
import { useCallback, useState } from "react";

type ProcessingState = "idle" | "uploading" | "processing" | "ready" | "error";

export default function HomePage() {
  const [selectedFile, setSelectedFile] = useState<File | null>(null);
  const [state, setState] = useState<ProcessingState>("idle");
  const [downloadUrl, setDownloadUrl] = useState<string>("");
  const [reportUrl, setReportUrl] = useState<string>("");
  const [message, setMessage] = useState<string>(
    "Upload an MDT Word document to begin.",
  );

  const handleFileChange = useCallback(
    (event: React.ChangeEvent<HTMLInputElement>) => {
      const file = event.target.files?.[0];
      setSelectedFile(file ?? null);
      setMessage(
        file
          ? `Ready to upload: ${file.name}`
          : "Upload an MDT Word document to begin.",
      );
      setState("idle");
      setDownloadUrl("");
    },
    [],
  );

  const handleClear = useCallback(() => {
    setSelectedFile(null);
    setDownloadUrl("");
    setReportUrl("");
    setState("idle");
    setMessage("Upload an MDT Word document to begin.");
    const input = document.getElementById(
      "file-input",
    ) as HTMLInputElement | null;
    if (input) {
      input.value = "";
    }
  }, []);

  const handleUpload = useCallback(async () => {
    if (!selectedFile) {
      setMessage("Please choose a .docx file first.");
      return;
    }

    setState("uploading");
    setMessage("Uploading document…");

    try {
      const formData = new FormData();
      formData.append("file", selectedFile);

      const apiBase = process.env.NEXT_PUBLIC_MDT_API_BASE_URL;
      setState("processing");
      setMessage("Processing MDT tables…");

      console.log("api url : ", apiBase);
      const response = await fetch(`${apiBase}/extract`, {
        method: "POST",
        body: formData,
      });

      if (!response.ok) {
        const detail = await response.json().catch(() => ({}));
        throw new Error(detail?.detail ?? "Extraction failed");
      }

      const payload = (await response.json()) as {
        workbook_base64: string;
        report: string;
      };
      const workbookBytes = Uint8Array.from(
        atob(payload.workbook_base64),
        (char) => char.charCodeAt(0),
      );
      const workbookBlob = new Blob(
        [workbookBytes],
        {
          type: "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        },
      );
      const workbookUrl = URL.createObjectURL(workbookBlob);
      setDownloadUrl(workbookUrl);

      const reportBlob = new Blob([payload.report], {
        type: "text/plain;charset=utf-8",
      });
      const reportObjectUrl = URL.createObjectURL(reportBlob);
      setReportUrl(reportObjectUrl);

      setState("ready");
      setMessage("Extraction complete. Download the workbook and report below.");
    } catch (error) {
      console.error(error);
      setState("error");
      setMessage(
        error instanceof Error
          ? error.message
          : "Something went wrong. Please try again.",
      );
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

  const handleReportDownload = useCallback(() => {
    if (!reportUrl) {
      return;
    }
    const link = document.createElement("a");
    link.href = reportUrl;
    link.download = "coverage-report.txt";
    link.click();
  }, [reportUrl]);

  return (
    <main style={styles.main}>
      <section style={styles.card}>
        <div style={styles.logoWrapper}>
          <Image
            src="/assets/nhs2.jpg"
            alt="NHS Logo"
            width={120}
            height={48}
            priority
          />
        </div>
        <h1 style={styles.heading}>Clinical AI MDT Extractor</h1>
        <p style={styles.subheading}>
          Upload the MDT outcome Word document to generate a prototype Excel
          database. The backend Python pipeline will parse tables, extract
          staging, and return a styled workbook.
        </p>

        <label htmlFor="file-input" style={styles.fileLabel}>
          <input
            id="file-input"
            type="file"
            accept=".doc,.docx"
            onChange={handleFileChange}
            style={styles.fileInput}
          />
          <span>
            {selectedFile ? selectedFile.name : "Choose MDT .docx file"}
          </span>
        </label>

        <button
          type="button"
          onClick={handleUpload}
          style={styles.primaryButton}
          disabled={state === "uploading" || state === "processing"}
        >
          {state === "uploading"
            ? "Uploading…"
            : state === "processing"
              ? "Processing…"
              : "Generate Workbook"}
        </button>

        <button
          type="button"
          onClick={handleClear}
          style={{ ...styles.secondaryButton, marginTop: "0.75rem" }}
          disabled={!selectedFile}
        >
          Clear Selection
        </button>

        <p style={styles.statusMessage}>{message}</p>

        <button
          type="button"
          onClick={handleDownload}
          style={{
            ...styles.secondaryButton,
            opacity: downloadUrl ? 1 : 0.4,
            cursor: downloadUrl ? "pointer" : "not-allowed",
          }}
          disabled={!downloadUrl}
        >
          Download Excel
        </button>

        <button
          type="button"
          onClick={handleReportDownload}
          style={{
            ...styles.secondaryButton,
            opacity: reportUrl ? 1 : 0.4,
            cursor: reportUrl ? "pointer" : "not-allowed",
            marginTop: "1rem",
          }}
          disabled={!reportUrl}
        >
          Download Report
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
    padding: "2rem",
  },
  card: {
    width: "100%",
    maxWidth: "640px",
    backgroundColor: "#ffffff",
    borderRadius: "1.25rem",
    padding: "2.5rem",
    boxShadow: "0 25px 60px rgba(15, 23, 42, 0.15)",
    border: "1px solid rgba(99, 102, 241, 0.2)",
  },
  logoWrapper: {
    display: "flex",
    justifyContent: "center",
    marginBottom: "1.5rem",
  },
  heading: {
    margin: 0,
    fontSize: "2rem",
    color: "#1f2937",
  },
  subheading: {
    marginTop: "0.75rem",
    marginBottom: "1.5rem",
    color: "#4b5563",
    lineHeight: 1.5,
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
    backgroundColor: "#f5f3ff",
  },
  fileInput: {
    display: "none",
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
    cursor: "pointer",
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
    color: "#374151",
  },
  statusMessage: {
    marginTop: "1rem",
    color: "#374151",
    minHeight: "1.5rem",
  },
};
