"""
civic_forensics.image_hash — 64-bit Difference Hash (dHash) & Perceptual Forensics
"""
from typing import Union
from PIL import Image
import numpy as np


def compute_dhash(image_source: Union[str, Image.Image], hash_size: int = 8) -> int:
    """
    Computes a 64-bit difference hash (dHash) tracking horizontal intensity gradients.
    
    Args:
        image_source: File path (str) or PIL Image instance.
        hash_size: Width of the grid (default 8 yields 8x8 = 64-bit integer hash).
        
    Returns:
        64-bit integer hash representing visual structural signature.
    """
    if isinstance(image_source, str):
        img = Image.open(image_source)
    else:
        img = image_source
        
    # 1. Convert to grayscale and resize to (hash_size + 1, hash_size)
    # The extra column is needed to compute adjacent column differences
    gray_resized = img.convert("L").resize(
        (hash_size + 1, hash_size),
        Image.Resampling.LANCZOS
    )
    
    # 2. Extract pixels as 2D numpy array
    pixels = np.array(gray_resized, dtype=np.int64)
    
    # 3. Compute boolean difference between adjacent columns
    difference = pixels[:, 1:] > pixels[:, :-1]
    
    # 4. Pack boolean matrix into 64-bit integer
    decimal_hash = 0
    for bit in difference.flatten():
        decimal_hash = (decimal_hash << 1) | int(bit)
        
    return decimal_hash


def hamming_distance(hash1: int, hash2: int) -> int:
    """
    Computes bitwise Hamming distance between two 64-bit integer hashes.
    Uses Brian Kernighan's bit-counting algorithm for O(number of set bits).
    
    Args:
        hash1: First 64-bit integer hash.
        hash2: Second 64-bit integer hash.
        
    Returns:
        Integer count of differing bits (0 to 64).
    """
    x = hash1 ^ hash2
    distance = 0
    while x:
        distance += 1
        x &= x - 1
    return distance


def are_images_duplicate(
    image1: Union[str, Image.Image],
    image2: Union[str, Image.Image],
    threshold: int = 10
) -> bool:
    """
    Evaluates whether two construction site photos are perceptual duplicates.
    
    Args:
        image1: Path or PIL image of first proof.
        image2: Path or PIL image of second proof.
        threshold: Max allowable bit difference (default <= 10 flags duplicates).
        
    Returns:
        True if Hamming distance <= threshold (duplicate fraud detected), False otherwise.
    """
    h1 = compute_dhash(image1)
    h2 = compute_dhash(image2)
    return hamming_distance(h1, h2) <= threshold
