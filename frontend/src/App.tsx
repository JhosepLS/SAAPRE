import { useState } from "react";
import AnalysisPage from "./pages/AnalysisPage";
import ModelStatusPage from "./pages/ModelStatusPage";

export default function App() {
  const [view, setView] = useState<"analysis" | "model">("analysis");
  return (
    <>
      <nav>
        <button onClick={() => setView("analysis")}>Análisis</button>
        <button onClick={() => setView("model")}>Estado del modelo</button>
      </nav>
      {view === "analysis" ? <AnalysisPage /> : <ModelStatusPage />}
    </>
  );
}
