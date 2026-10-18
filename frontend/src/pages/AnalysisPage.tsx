import AccountLinkForm from "../components/AccountLinkForm";
import PatchSelector from "../components/PatchSelector";
import PerformanceCharts from "../components/PerformanceCharts";

// CU-02 / CU-03 / CU-04 (RF-08, RF-13)
export default function AnalysisPage() {
  return (
    <main>
      <h1>Análisis de rendimiento</h1>
      <AccountLinkForm />
      <PatchSelector />
      <PerformanceCharts />
    </main>
  );
}
