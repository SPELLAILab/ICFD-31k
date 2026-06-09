"""
Cryptocurrency and NFT Domain Entities
Used for cross-domain testing of fraud detection models
"""

# Fake crypto exchanges (fraudulent)
FAKE_EXCHANGES = [
    "CryptoMaxPro", "BitVaultX", "ChainTrade Plus", "QuantumCrypto",
    "SafeCoinEx", "EliteBlockchain", "MegaCryptoHub", "PrimeCoinDesk"
]

# Real crypto exchanges (for legitimate comparison)
REAL_EXCHANGES = [
    "Coinbase", "Binance", "Kraken", "Gemini", "Crypto.com"
]

# Cryptocurrency names
CRYPTOCURRENCIES = [
    "Bitcoin", "Ethereum", "USDT", "BNB", "XRP", "Cardano", "Solana",
    "Dogecoin", "Polygon", "Litecoin", "Shiba Inu", "Avalanche"
]

# Fake tokens (for scams)
FAKE_TOKENS = [
    "MoonSafe", "ElonRocket", "SafeMars", "BabyDoge2.0", "QuantumCoin",
    "MetaFloki", "TrustVault", "DiamondHands", "RocketMoon", "SafeGem"
]

# NFT platforms
NFT_PLATFORMS = [
    "OpenSea", "Rarible", "Foundation", "SuperRare", "Nifty Gateway"
]

# Fake NFT projects (scams)
FAKE_NFT_PROJECTS = [
    "Bored Ape Knockoffs", "Crypto Punks 2.0", "Meta Monkeys Elite",
    "Diamond Dolphins", "Pixel Legends", "Galaxy Gorillas", "Cyber Cats Premium"
]

# Crypto wallets
CRYPTO_WALLETS = [
    "MetaMask", "Trust Wallet", "Coinbase Wallet", "Ledger", "Trezor",
    "Phantom", "Exodus", "Atomic Wallet"
]

# Blockchain networks
BLOCKCHAIN_NETWORKS = [
    "Ethereum Mainnet", "Binance Smart Chain", "Polygon", "Solana", 
    "Avalanche C-Chain", "Arbitrum", "Optimism"
]

# Investment return promises (fraudulent)
FAKE_RETURNS = [
    "50% monthly returns", "guaranteed 200% in 90 days", "10x in 6 months",
    "passive income of $5000/month", "300% APY", "triple your crypto in 30 days"
]

# Scam tactics
SCAM_TACTICS = [
    "limited time offer", "exclusive whitelist", "celebrity partnership",
    "AI-powered trading bot", "secret algorithm", "insider information",
    "guaranteed profits", "risk-free investment", "pre-sale discount"
]

# Smart contract actions (malicious)
MALICIOUS_ACTIONS = [
    "approve unlimited spending", "transfer all tokens", "drain wallet",
    "set approval for all", "emergency withdrawal", "claim airdrop"
]

# Legitimate crypto terms (for contrast)
LEGITIMATE_TERMS = [
    "decentralized exchange", "peer-to-peer", "blockchain verification",
    "cold storage", "hardware wallet", "two-factor authentication",
    "know your customer (KYC)", "anti-money laundering (AML)"
]

# Recovery scam services
FAKE_RECOVERY_SERVICES = [
    "CryptoRecoveryPro", "BlockchainForensics247", "LostCoinExperts",
    "ScamRefundSpecialists", "BitcoinRecoveryHub"
]

# Mining operations (fake)
FAKE_MINING_OPERATIONS = [
    "CloudHashPro", "MegaMining Solutions", "QuantumHashPower",
    "EliteMiningFarm", "CryptoCloudMining"
]
