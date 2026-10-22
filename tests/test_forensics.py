"""
tests/test_forensics.py — Comprehensive Unit Verification for civic-forensics
"""
import pytest
from PIL import Image, ImageDraw
from civic_forensics import (
    compute_dhash,
    hamming_distance,
    are_images_duplicate,
    build_bipartite_procurement_graph,
    compute_hhi_concentration,
    detect_contractor_cartel_cliques
)


def create_synthetic_test_image(pattern: str = "gradient") -> Image.Image:
    img = Image.new("RGB", (100, 100), color=(255, 255, 255))
    draw = ImageDraw.Draw(img)
    if pattern == "gradient":
        for i in range(100):
            draw.line([(i, 0), (i, 100)], fill=(i * 2, i * 2, i * 2))
    elif pattern == "box":
        draw.rectangle([(20, 20), (80, 80)], fill=(0, 0, 0))
    return img


def test_dhash_and_hamming_distance():
    img1 = create_synthetic_test_image("gradient")
    img2 = create_synthetic_test_image("gradient")
    
    hash1 = compute_dhash(img1)
    hash2 = compute_dhash(img2)
    
    # Identical images must yield Hamming distance of 0
    assert hash1 == hash2
    assert hamming_distance(hash1, hash2) == 0
    assert are_images_duplicate(img1, img2, threshold=5) is True


def test_distinct_images_yield_high_distance():
    img_grad = create_synthetic_test_image("gradient")
    img_box = create_synthetic_test_image("box")
    
    hash_grad = compute_dhash(img_grad)
    hash_box = compute_dhash(img_box)
    
    dist = hamming_distance(hash_grad, hash_box)
    # Different patterns should have significant distance
    assert dist > 10
    assert are_images_duplicate(img_grad, img_box, threshold=5) is False


def test_bipartite_graph_construction():
    bids = [
        ("Contractor_A", "Tender_101", 500000.0),
        ("Contractor_B", "Tender_101", 520000.0),
        ("Contractor_A", "Tender_102", 300000.0),
    ]
    graph = build_bipartite_procurement_graph(bids)
    
    assert graph.number_of_nodes() == 4  # 2 contractors + 2 tenders
    assert graph.number_of_edges() == 3
    assert graph.nodes["Contractor_A"]["node_type"] == "contractor"
    assert graph.nodes["Tender_101"]["node_type"] == "tender"


def test_hhi_concentration_index():
    # Monopoly (100% share) -> HHI = 100^2 = 10,000
    monopoly = [100.0]
    assert compute_hhi_concentration(monopoly) == 10000.0
    
    # Competitive market (10 firms with 10% each) -> 10 * 100 = 1,000
    competitive = [10.0] * 10
    assert compute_hhi_concentration(competitive) == 1000.0
    
    # Duopoly (50% each) -> 50^2 + 50^2 = 5,000 (> 2500 High Cartel Risk)
    duopoly = [50.0, 50.0]
    assert compute_hhi_concentration(duopoly) == 5000.0


def test_detect_contractor_cartel_cliques():
    # Simulated cover bidding ring: Contractor_X and Contractor_Y bid together on 4 tenders
    bids = [
        ("Contractor_X", "Tender_1", 100.0),
        ("Contractor_Y", "Tender_1", 105.0),
        ("Contractor_X", "Tender_2", 200.0),
        ("Contractor_Y", "Tender_2", 210.0),
        ("Contractor_X", "Tender_3", 300.0),
        ("Contractor_Y", "Tender_3", 305.0),
        ("Contractor_Z", "Tender_4", 400.0),
    ]
    
    cartel_suspects = detect_contractor_cartel_cliques(bids, min_co_bids=3)
    assert len(cartel_suspects) == 1
    assert cartel_suspects[0]["contractor_1"] == "Contractor_X"
    assert cartel_suspects[0]["contractor_2"] == "Contractor_Y"
    assert cartel_suspects[0]["shared_tenders_count"] == 3
