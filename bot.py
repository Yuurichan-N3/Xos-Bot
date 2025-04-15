import requests
import json
import secrets
import logging
import time
from eth_account import Account
from eth_account.messages import encode_defunct
from web3 import Web3
from hashlib import sha3_256
from rich.logging import RichHandler
from rich.console import Console
from rich.table import Table

# Initialize rich console
console = Console()

# Configure logging with RichHandler
logging.basicConfig(
    level="INFO",
    format="%(message)s",
    datefmt="[%Y-%m-%d %H:%M:%S]",
    handlers=[RichHandler(rich_tracebacks=True, console=console)]
)
logger = logging.getLogger("CryptoInkBot")

# Display banner
banner = """
╔══════════════════════════════════════════════╗
║       🌟 Xos auto Reff - Wallet Automator    ║
║   Automate wallet creation and token earning!║
║  Developed by: https://t.me/sentineldiscus   ║
╚══════════════════════════════════════════════╝
"""
console.print(banner, style="bold cyan")

# Configuration
PROJECT_ID = "7f8bd096752366cf84c52aa43f99504b"
BASE_URL = "https://rpc.walletconnect.org/v1"
WEB3MODAL_URL = "https://api.web3modal.org"
X_INK_API = "https://api.x.ink/v1"
CHAIN_ID = "eip155:42161"

# Generate a new wallet
def generate_wallet():
    priv_key = "0x" + secrets.token_hex(32)
    account = Account.from_key(priv_key)
    return {
        "address": account.address,
        "private_key": priv_key
    }

def get_wallets():
    params = {
        "projectId": PROJECT_ID,
        "st": "appkit",
        "sv": "html-ethers-1.6.8",
        "page": 1,
        "chains": CHAIN_ID,
        "entries": 4
    }
    headers = {
        "referer": "https://x.ink/",
        "sec-ch-ua": '"Google Chrome";v="135", "Not-A.Brand";v="8", "Chromium";v="135"',
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": '"Windows"',
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36"
    }
    try:
        response = requests.get(f"{WEB3MODAL_URL}/getWallets", params=params, headers=headers)
        response.raise_for_status()
        logger.info("Successfully fetched wallet data.", extra={"markup": True})
        return response.json()
    except requests.RequestException as e:
        logger.error(f"Failed to fetch wallet data: {e}", extra={"markup": True})
        return None

def get_identity(wallet_address, client_id):
    params = {
        "projectId": PROJECT_ID,
        "sender": wallet_address,
        "clientId": client_id
    }
    headers = {
        "accept": "*/*",
        "accept-language": "id-ID,id;q=0.9,ja-ID;q=0.8,ja;q=0.7,en-ID;q=0.6,en;q=0.5,en-US;q=0.4",
        "origin": "https://x.ink",
        "referer": "https://x.ink/",
        "sec-ch-ua": '"Google Chrome";v="135", "Not-A.Brand";v="8", "Chromium";v="135"',
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": '"Windows"',
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36"
    }
    try:
        response = requests.get(f"{BASE_URL}/identity/{wallet_address}", params=params, headers=headers)
        response.raise_for_status()
        logger.info("Successfully fetched identity data.", extra={"markup": True})
        return response.json()
    except requests.RequestException as e:
        logger.error(f"Failed to fetch identity data: {e}", extra={"markup": True})
        return None

def get_sign_message(wallet_address):
    params = {
        "walletAddress": wallet_address
    }
    headers = {
        "accept": "application/json, text/plain, */*",
        "accept-language": "id-ID,id;q=0.9,ja-ID;q=0.8,ja;q=0.7,en-ID;q=0.6,en;q=0.5,en-US;q=0.4",
        "origin": "https://x.ink",
        "referer": "https://x.ink/",
        "sec-ch-ua": '"Google Chrome";v="135", "Not-A.Brand";v="8", "Chromium";v="135"',
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": '"Windows"',
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36"
    }
    try:
        response = requests.get(f"{X_INK_API}/get-sign-message2", params=params, headers=headers)
        response.raise_for_status()
        logger.info("Successfully fetched sign message.", extra={"markup": True})
        return response.json()
    except requests.RequestException as e:
        logger.error(f"Failed to fetch sign message: {e}", extra={"markup": True})
        return None

def verify_signature(wallet_address, sign_message, signature, referrer):
    url = f"{X_INK_API}/verify-signature2"
    headers = {
        "accept": "application/json, text/plain, */*",
        "accept-language": "id-ID,id;q=0.9,ja-ID;q=0.8,ja;q=0.7,en-ID;q=0.6,en;q=0.5,en-US;q=0.4",
        "content-type": "application/json",
        "origin": "https://x.ink",
        "referer": "https://x.ink/",
        "sec-ch-ua": '"Google Chrome";v="135", "Not-A.Brand";v="8", "Chromium";v="135"',
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": '"Windows"',
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36"
    }
    payload = {
        "walletAddress": wallet_address,
        "referrer": referrer,
        "signMessage": sign_message,
        "signature": "0x" + signature if not signature.startswith("0x") else signature
    }
    try:
        response = requests.post(url, headers=headers, json=payload)
        response.raise_for_status()
        logger.info("[green]Signature verification successful![/green]", extra={"markup": True})
        return response.json()
    except requests.RequestException as e:
        logger.error(f"[red]Signature verification failed: {e}[/red]", extra={"markup": True})
        return None

def save_to_wallets_json(wallet_data):
    try:
        try:
            with open("wallets.json", "r") as f:
                data = json.load(f)
        except FileNotFoundError:
            data = []
        
        data.append(wallet_data)
        
        with open("wallets.json", "w") as f:
            json.dump(data, f, indent=2)
        logger.info("[cyan]Wallet data saved to wallets.json.[/cyan]", extra={"markup": True})
    except Exception as e:
        logger.error(f"[red]Failed to save wallet data: {e}[/red]", extra={"markup": True})

def save_to_tokens_json(token):
    try:
        try:
            with open("tokens.json", "r") as f:
                data = json.load(f)
        except FileNotFoundError:
            data = []
        
        if token not in data:
            data.append(token)
        
        with open("tokens.json", "w") as f:
            json.dump(data, f, indent=2)
        logger.info("[cyan]Token saved to tokens.json.[/cyan]", extra={"markup": True})
    except Exception as e:
        logger.error(f"[red]Failed to save token: {e}[/red]", extra={"markup": True})

def display_summary(wallet_address, token):
    table = Table(title="CryptoInk Bot - Wallet Summary", show_header=True, header_style="bold magenta")
    table.add_column("Field", style="cyan")
    table.add_column("Value", style="green")
    table.add_row("Wallet Address", wallet_address)
    table.add_row("Token", token[:30] + "..." if token else "None")
    console.print(table)

def main():
    # Input referrer once
    referrer = console.input("[bold yellow]Enter referrer code (or press Enter for default '9U25GX'): [/bold yellow]").strip() or "9U25GX"
    logger.info(f"[yellow]Using referrer code: {referrer}[/yellow]", extra={"markup": True})

    iteration = 0
    while True:
        iteration += 1
        logger.info(f"[bold blue]Starting iteration {iteration}...[/bold blue]", extra={"markup": True})

        # Generate new wallet
        wallet = generate_wallet()
        wallet_address = wallet["address"]
        private_key = wallet["private_key"]
        logger.info(f"[green]New wallet created: {wallet_address}[/green]", extra={"markup": True})

        # Get wallets
        wallets = get_wallets()
        if not wallets:
            logger.error("[red]Stopping due to wallet fetch failure.[/red]", extra={"markup": True})
            break

        # Generate client ID
        client_id = f"did:key:z6Mk{secrets.token_hex(32)}"

        # Get identity
        identity = get_identity(wallet_address, client_id)
        if not identity:
            logger.error("[red]Stopping due to identity fetch failure.[/red]", extra={"markup": True})
            break

        # Get sign message
        sign_message_response = get_sign_message(wallet_address)
        if not sign_message_response:
            logger.error("[red]Stopping due to sign message fetch failure.[/red]", extra={"markup": True})
            break
        sign_message = sign_message_response.get("message")
        if not sign_message:
            logger.error("[red]No sign message received.[/red]", extra={"markup": True})
            break
        logger.info("[green]Sign message received.[/green]", extra={"markup": True})

        # Sign the message
        try:
            eth_message = f"\x19Ethereum Signed Message:\n{len(sign_message)}{sign_message}"
            message_hash = sha3_256(eth_message.encode("utf-8")).hexdigest()
            logger.info("[cyan]Message hash created.[/cyan]", extra={"markup": True})

            message = encode_defunct(text=sign_message)
            signed_message = Account.sign_message(message, private_key=private_key)
            signature = signed_message.signature.hex()
            logger.info("[cyan]Signature generated.[/cyan]", extra={"markup": True})

            recovered_address = Account.recover_message(message, signature=signature)
            if recovered_address.lower() != wallet_address.lower():
                logger.error("[red]Local signature verification failed: address mismatch.[/red]", extra={"markup": True})
                break
            logger.info("[green]Local signature verification successful.[/green]", extra={"markup": True})
        except Exception as e:
            logger.error(f"[red]Failed to sign message: {e}[/red]", extra={"markup": True})
            break

        # Verify signature with server
        verification = verify_signature(wallet_address, sign_message, signature, referrer)
        token = None
        if verification:
            wallet_data = {
                "address": wallet_address,
                "private_key": private_key,
                "verification_response": verification
            }
            save_to_wallets_json(wallet_data)

            # Extract token
            token = verification.get("token", None) if isinstance(verification, dict) else verification
            if token:
                save_to_tokens_json(token)
            else:
                logger.warning("[yellow]No token found in verification response.[/yellow]", extra={"markup": True})

            # Display summary table
            display_summary(wallet_address, token)
        else:
            logger.error("[red]Server signature verification failed.[/red]", extra={"markup": True})

        logger.info("[blue]Iteration completed. Starting next in 2 seconds...[/blue]", extra={"markup": True})
        time.sleep(2)  # Brief pause between iterations

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        logger.info("[yellow]Bot stopped by user.[/yellow]", extra={"markup": True})
        console.print("[bold green]Thank you for using CryptoInk Bot![/bold green]")
