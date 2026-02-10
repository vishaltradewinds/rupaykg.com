import { useEffect, useState } from "react";

type WalletResponse = {
  withdrawable_balance: number;
  locked_balance: number;
  ledger: unknown;
};

const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL ?? "/api";
const WALLET_BEARER_TOKEN = process.env.NEXT_PUBLIC_WALLET_BEARER_TOKEN;

export default function Wallet() {
  const [data, setData] = useState<WalletResponse | null>(null);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const browserToken = typeof window !== "undefined" ? localStorage.getItem("rupaykg_token") : null;
    const token = browserToken || WALLET_BEARER_TOKEN;

    if (!token) {
      setError("No token found. Set NEXT_PUBLIC_WALLET_BEARER_TOKEN or store rupaykg_token in localStorage.");
      return;
    }

    const headers: HeadersInit = {
      Authorization: `Bearer ${token}`,
    };

    fetch(`${API_BASE_URL}/wallet/me`, { headers })
      .then(async (response) => {
        if (!response.ok) {
          throw new Error(`Wallet API failed with status ${response.status}`);
        }

        return response.json();
      })
      .then(setData)
      .catch((err: Error) => {
        setError(err.message);
      });
  }, []);

  if (error) {
    return <div>Failed to load wallet data: {error}</div>;
  }

  if (!data) return <div>Loading...</div>;

  return (
    <div>
      <h2>Withdrawable ₹{data.withdrawable_balance}</h2>
      <h3>Locked ₹{data.locked_balance}</h3>
      <pre>{JSON.stringify(data.ledger, null, 2)}</pre>
    </div>
  );
}
