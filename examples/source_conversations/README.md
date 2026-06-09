# Source Conversations

This directory contains 2 representative full conversations from each fraud umbrella.

## Format

Each JSON file includes:

- `transcript`: Timestamped speaker turns
- `chunk_level_analysis`: Progressive annotations at 3-second intervals
- `final_slow_thinking_rationale`: Detailed reasoning for verdict
- `final_verdict`: YES (fraud) or NO (legitimate)
- `scenario`: Scenario metadata and policy rules
- `key_entities`: Extracted organizations, products, PII
- `session_id`: Unique conversation identifier

## Organization

Conversations are organized by fraud umbrella:

- `banking/`: Bank and payment fraud
- `ecommerce/`: E-commerce and marketplace scams
- `emergency/`: Emergency impersonation and extortion
- `government/`: Government service impersonation
- `healthcare/`: Healthcare and insurance fraud
- `jobs/`: Job recruitment scams
- `loan/`: Loan shark harassment and fraud
- `lottery_travel/`: Lottery and travel prize scams
- `tech/`: Tech support and account fraud
- `utility/`: Utility bill and service scams

Each folder contains 2 randomly selected conversations.
