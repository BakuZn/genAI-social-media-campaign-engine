"""
Base abstract generator class for structuring channel specific content generation.
"""
from abc import ABC, abstractmethod

class BasePostGenerator(ABC):
    @abstractmethod
    def generate(self, brief_data: dict) -> dict:
        """
        Generate content based on parsed brief dataset.
        """
        pass
