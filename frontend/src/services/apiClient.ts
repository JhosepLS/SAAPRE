// Cliente HTTP del dashboard. Solo habla con la API REST del backend (JSON).
const BASE_URL = import.meta.env.VITE_API_BASE_URL ?? "";

export type Game = "LOL" | "CS2";

export interface ModelStatus {
  game: Game;
  algorithm: string;
  patch_version: string;
  accuracy: number;
  f1_score: number;
  auc_roc: number;
  drift_status: string;
}

async function request<T>(path: string, init?: RequestInit): Promise<T> {
  const response = await fetch(`${BASE_URL}/api/v1${path}`, {
    headers: { "Content-Type": "application/json" },
    ...init,
  });
  if (!response.ok) {
    throw new Error(`Error ${response.status} al consultar ${path}`);
  }
  return (await response.json()) as T;
}

export const apiClient = {
  health: () => request<{ status: string; version: string }>("/health"),
  linkAccount: (game: Game, nickname: string) =>
    request("/players", { method: "POST", body: JSON.stringify({ game, nickname }) }),
  modelStatus: (game: Game) => request<ModelStatus>(`/models/status?game=${game}`),
};
