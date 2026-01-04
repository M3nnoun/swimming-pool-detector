from pathlib import Path
from typing import List, Tuple

def save_coordinates(
    polygons: List[List[Tuple[int, int]]], 
    filepath: str | Path
) -> None:
    """
    Save coordinates of ALL detected pools with clear separation
    Input: list of polygons (each polygon is list of (x,y) points)
    """
    Path(filepath).parent.mkdir(parents=True, exist_ok=True)
    
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write("Detected Swimming Pool Boundary Coordinates\n")
        f.write("==========================================\n\n")
        
        if not polygons:
            f.write("No pools detected.\n")
            return

        for i, polygon in enumerate(polygons, 1):
            f.write(f"--- Pool {i}  ({len(polygon)} points) ---\n")
            for point in polygon:
                x, y = point  # now safe - point is Tuple[int,int]
                f.write(f"{x}, {y}\n")
            f.write("\n")  # empty line between pools