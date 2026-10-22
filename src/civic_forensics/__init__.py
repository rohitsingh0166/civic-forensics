"""
civic_forensics — Modular Forensic Auditing Library for Municipal Infrastructure
Author: Rohit Singh (rohitsingh0166)
License: MIT
"""

from .image_hash import compute_dhash, hamming_distance, are_images_duplicate
from .cartel_graph import build_bipartite_procurement_graph, compute_hhi_concentration, detect_contractor_cartel_cliques

__version__ = "0.1.0"
__all__ = [
    "compute_dhash",
    "hamming_distance",
    "are_images_duplicate",
    "build_bipartite_procurement_graph",
    "compute_hhi_concentration",
    "detect_contractor_cartel_cliques"
]
