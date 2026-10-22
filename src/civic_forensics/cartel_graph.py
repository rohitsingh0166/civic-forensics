"""
civic_forensics.cartel_graph — Bipartite Procurement Cartel Graph & Market Concentration Engine
"""
from typing import List, Tuple, Dict
from collections import defaultdict
import networkx as nx


def build_bipartite_procurement_graph(bids: List[Tuple[str, str, float]]) -> nx.Graph:
    """
    Builds a bipartite NetworkX graph connecting Contractors to Tenders.
    
    Args:
        bids: List of tuples (contractor_id, tender_id, bid_amount).
        
    Returns:
        nx.Graph with bipartite node attributes ('contractor' and 'tender').
    """
    B = nx.Graph()
    for contractor, tender, amount in bids:
        B.add_node(contractor, bipartite=0, node_type="contractor")
        B.add_node(tender, bipartite=1, node_type="tender")
        B.add_edge(contractor, tender, weight=amount)
    return B


def compute_hhi_concentration(market_shares: List[float]) -> float:
    """
    Computes the Herfindahl-Hirschman Index (HHI) for market concentration.
    
    Args:
        market_shares: List of percentage market shares (e.g., [40.0, 30.0, 30.0] summing to 100).
        
    Returns:
        HHI value between 0 and 10,000.
        - HHI < 1500: Unconcentrated / Competitive market.
        - 1500 <= HHI <= 2500: Moderately concentrated.
        - HHI > 2500: Highly concentrated / High Cartel Risk.
    """
    if not market_shares:
        return 0.0
    return float(sum(share ** 2 for share in market_shares))


def detect_contractor_cartel_cliques(
    bids: List[Tuple[str, str, float]],
    min_co_bids: int = 3
) -> List[Dict[str, any]]:
    """
    Detects pairs of contractors that exhibit statistically anomalous co-bidding
    behavior (collusive bidding rings / cover bidding).
    
    Args:
        bids: List of tuples (contractor_id, tender_id, bid_amount).
        min_co_bids: Minimum shared tenders before flagging as suspicious cartel link.
        
    Returns:
        List of suspicious contractor pairs with co-bid counts and shared tender IDs.
    """
    # Map tender -> list of contractors who submitted bids
    tender_contractors = defaultdict(set)
    for contractor, tender, _ in bids:
        tender_contractors[tender].add(contractor)
        
    # Count pairwise co-occurrences across tenders
    co_occurrences = defaultdict(list)
    for tender, contractors in tender_contractors.items():
        sorted_contractors = sorted(list(contractors))
        for i in range(len(sorted_contractors)):
            for j in range(i + 1, len(sorted_contractors)):
                pair = (sorted_contractors[i], sorted_contractors[j])
                co_occurrences[pair].append(tender)
                
    cartel_links = []
    for (c1, c2), tenders in co_occurrences.items():
        if len(tenders) >= min_co_bids:
            cartel_links.append({
                "contractor_1": c1,
                "contractor_2": c2,
                "shared_tenders_count": len(tenders),
                "shared_tenders": tenders,
                "risk_flag": "HIGH_CARTEL_COLLUSION_SUSPECT"
            })
            
    # Sort descending by suspicion frequency
    cartel_links.sort(key=lambda x: x["shared_tenders_count"], reverse=True)
    return cartel_links
