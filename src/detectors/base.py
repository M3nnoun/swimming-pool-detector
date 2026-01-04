from abc import ABC, abstractmethod
from typing import List, Tuple

class PoolDetector(ABC):
    """Common interface for all pool detection strategies"""

    @abstractmethod
    def detect(self, image_path: str) -> List[Tuple[int, int]]:
        """
        Returns list of (x,y) points defining the pool boundary (clockwise)
        Returns empty list if no pool was detected
        """
        pass

    @property
    def name(self) -> str:
        return self.__class__.__name__.replace("Detector", "").lower()