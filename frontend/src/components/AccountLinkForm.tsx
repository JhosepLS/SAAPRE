import { useState } from "react";
import { apiClient, type Game } from "../services/apiClient";

// CU-01 / RF-10. React escapa el contenido por defecto; no se usa dangerouslySetInnerHTML.
export default function AccountLinkForm() {
  const [game, setGame] = useState<Game>("LOL");
  const [nickname, setNickname] = useState("");
  const [message, setMessage] = useState("");

  async function submit(event: React.FormEvent) {
    event.preventDefault();
    try {
      await apiClient.linkAccount(game, nickname.trim());
      setMessage("Cuenta vinculada.");
    } catch (error) {
      setMessage((error as Error).message);
    }
  }

  return (
    <form onSubmit={submit}>
      <select value={game} onChange={(e) => setGame(e.target.value as Game)}>
        <option value="LOL">League of Legends</option>
        <option value="CS2">Counter-Strike 2</option>
      </select>
      <input
        value={nickname}
        onChange={(e) => setNickname(e.target.value)}
        minLength={3}
        maxLength={40}
        required
        placeholder="Nickname"
      />
      <button type="submit">Vincular</button>
      {message && <p>{message}</p>}
    </form>
  );
}
