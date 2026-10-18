import { useEffect, useState } from "react";
import { apiClient, type ModelStatus } from "../services/apiClient";

// CU-05 (RF-14): estado del modelo activo y del parche vigente.
export default function ModelStatusPage() {
  const [status, setStatus] = useState<ModelStatus | null>(null);
  const [error, setError] = useState("");

  useEffect(() => {
    apiClient.modelStatus("LOL").then(setStatus).catch((e: Error) => setError(e.message));
  }, []);

  return (
    <main>
      <h1>Estado del modelo</h1>
      {error && <p>{error}</p>}
      {status && (
        <p>
          {status.algorithm} · parche {status.patch_version} · accuracy {status.accuracy}
        </p>
      )}
    </main>
  );
}
