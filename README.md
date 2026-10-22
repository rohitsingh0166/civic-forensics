# civic-forensics 🔍🏛️

[![PyPI Version](https://img.shields.io/badge/pypi-v0.1.0-blue.svg?style=for-the-badge&logo=pypi&logoColor=white)](https://github.com/rohitsingh0166/civic-forensics)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg?style=for-the-badge)](https://opensource.org/licenses/MIT)
[![Python 3.9+](https://img.shields.io/badge/python-3.9+-blue.svg?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![SIH 2026 Ready](https://img.shields.io/badge/Civic%20Tech-SIH%202026%20MoSPI-brightgreen?style=for-the-badge)](https://sih.gov.in)

> **Institutional-grade forensic auditing library for municipal civic works, public infrastructure tenders, and government expenditure vigilance.**

Developed by **Rohit Singh** (B.Tech CSE - AIML, ABES Engineering College) as part of the **MPLADS-AI continuous surveillance initiative for the Ministry of Statistics and Programme Implementation (MoSPI)**.

---

## ⚡ The Civic Problem
Public infrastructure audits in developing economies face two widespread anomalies:
1. **Photographic Proof Reuse (Ghost Works):** Contractors upload the same construction photograph across multiple fiscal years or different geographic tender IDs to claim unearned milestone disbursements.
2. **Procurement Cartels & Cover Bidding:** Interconnected contractor rings submit collusive bids across tenders to manipulate market prices while maintaining artificial competition.

`civic-forensics` provides lightweight, mathematical, zero-cloud forensic primitives to audit these anomalies in real time.

---

## 📦 Installation

```bash
pip install civic-forensics
```

*(Or install locally in editable development mode:)*
```bash
git clone https://github.com/rohitsingh0166/civic-forensics.git
cd civic-forensics
pip install -e .
```

---

## 🚀 5-Line Usage Quickstart

### 1. Photographic Duplicate Forensics (64-bit dHash)
```python
from civic_forensics import are_images_duplicate, compute_dhash, hamming_distance

# Evaluates whether two site photos are duplicate fraud (Hamming distance <= 10)
is_fraud = are_images_duplicate("site_work_2024.jpg", "claimed_site_2025.jpg")

if is_fraud:
    print("🚨 VIGILANCE ALERT: Duplicate photographic proof reused across fiscal years!")
```

### 2. Bipartite Procurement Cartel & HHI Market Concentration
```python
from civic_forensics import compute_hhi_concentration, detect_contractor_cartel_cliques

# District market shares across contractors (summing to 100%)
market_shares = [55.0, 35.0, 10.0]
hhi = compute_hhi_concentration(market_shares)

print(f"Herfindahl-Hirschman Index: {hhi}")
# HHI = 4350.0 (> 2500 flags severe cartel / monopolistic risk)

# Detect contractor pairs colluding across tenders
bids = [
    ("Firm_A", "Tender_1", 100000), ("Firm_B", "Tender_1", 102000),
    ("Firm_A", "Tender_2", 200000), ("Firm_B", "Tender_2", 204000),
    ("Firm_A", "Tender_3", 300000), ("Firm_B", "Tender_3", 305000),
]
cartels = detect_contractor_cartel_cliques(bids, min_co_bids=3)
print(f"Detected Collusive Pair: {cartels[0]['contractor_1']} & {cartels[0]['contractor_2']}")
```

---

## 🔬 Mathematical Formulations

### 1. 64-Bit Difference Hash (dHash)
The difference hash tracks relative horizontal intensity gradients rather than absolute RGB values, making it resilient to camera gamma shifts, JPEG compression, and daylight variations:

$$\text{Bit}(i, j) = \begin{cases} 1 & \text{if } P(i, j+1) > P(i, j) \\ 0 & \text{otherwise} \end{cases}$$

The bitwise Hamming distance measures visual divergence:

$$D_H(H_1, H_2) = \sum_{k=0}^{63} (H_1 \oplus H_2)_k$$

### 2. Herfindahl-Hirschman Index (HHI)
$$\text{HHI} = \sum_{i=1}^{N} s_i^2$$
Where $s_i$ is the percentage market share of contractor $i$. $\text{HHI} > 2500$ indicates a highly concentrated cartel ecosystem.

---

## 📄 License
Released under the **MIT License**. Free for public sector audit agencies, civic hackathons, and open data researchers.
