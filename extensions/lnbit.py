import os
import requests
from dotenv import load_dotenv
from typing import Dict, Any, Optional, List

# Load environment variables from .env file
load_dotenv()

class LNBitsAPI:
    def __init__(self):
        self.base_url = os.getenv("LNBITS_URL")
        self.admin_key = os.getenv("LNBITS_ADMIN_KEY")
        self.headers = {"X-Api-Key": self.admin_key, "Content-Type": "application/json"}

    def create_wallet(self, user_name: str) -> Optional[Dict[str, Any]]:
        url = f"{self.base_url}/api/v1/wallets"
        data = {"name": user_name, "user_id": "generated_user_id"}
        response = requests.post(url, json=data, headers=self.headers)
        return response.json() if response.ok else None

    def get_wallet_balance(self, wallet_key: str) -> Optional[Dict[str, Any]]:
        url = f"{self.base_url}/api/v1/wallet"
        headers = {"X-Api-Key": wallet_key}
        response = requests.get(url, headers=headers)
        return response.json() if response.ok else None

    def create_invoice(self, wallet_key: str, amount: int, memo: str = "Discord Bot Payment") -> Optional[Dict[str, Any]]:
        url = f"{self.base_url}/api/v1/payments"
        headers = {"X-Api-Key": wallet_key}
        data = {"out": False, "amount": amount, "memo": memo}
        response = requests.post(url, json=data, headers=headers)
        return response.json() if response.ok else None

    def pay_invoice(self, wallet_key: str, bolt11: str) -> Optional[Dict[str, Any]]:
        url = f"{self.base_url}/api/v1/payments"
        headers = {"X-Api-Key": wallet_key}
        data = {"out": True, "bolt11": bolt11}
        response = requests.post(url, json=data, headers=headers)
        return response.json() if response.ok else None

    def get_transactions(self, wallet_key: str, limit: int = 5) -> Optional[List[Dict[str, Any]]]:
        url = f"{self.base_url}/api/v1/payments"
        headers = {"X-Api-Key": wallet_key}
        params = {"limit": limit}
        response = requests.get(url, headers=headers, params=params)
        return response.json() if response.ok else None

    def internal_transfer(self, from_wallet_key: str, to_wallet_inkey: str, amount: int, memo: str = "Zap from Discord") -> Optional[Dict[str, Any]]:
        invoice = self.create_invoice(to_wallet_inkey, amount, memo)
        if not invoice or "payment_request" not in invoice:
            return None
        return self.pay_invoice(from_wallet_key, invoice["payment_request"])
