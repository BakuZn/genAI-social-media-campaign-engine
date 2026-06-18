"""
Module for loading and parsing event briefs (PDFs, Markdown, or raw text)
and converting them into structured Pydantic objects.
"""
from typing import List, Optional
from pydantic import BaseModel, Field

class AgriculturalEventBrief(BaseModel):
    """
    Data model representing a structured agricultural event brief.
    Used for parsing input documents and validating LLM-extracted metadata.
    """
    event_name: str = Field(
        ...,
        description="The official name of the agricultural event (e.g., 'Bayer Crop Science Innovation Summit 2024')."
    )
    location: str = Field(
        ...,
        description="The specific venue or city where the event is taking place."
    )
    state: str = Field(
        ...,
        description="The geographic state or region of the event."
    )
    date: str = Field(
        ...,
        description="The scheduled date or date range of the event (e.g., 'October 12-14, 2024')."
    )
    crop: List[str] = Field(
        default_factory=list,
        description="The primary crop(s) focused on during the event (e.g., 'Corn', 'Soybeans', 'Wheat')."
    )
    seed_product: List[str] = Field(
        default_factory=list,
        description="Specific Bayer seed brands or products being showcased (e.g., 'DEKALB®', 'Asgrow®')."
    )
    crop_protection_product: List[str] = Field(
        default_factory=list,
        description="Specific Bayer crop protection products featured (e.g., 'Roundup®', 'Fox Xpro®', 'Luna®')."
    )
    target_audience: List[str] = Field(
        default_factory=list,
        description="The intended demographic for the campaign (e.g., 'Agronomists', 'Large-scale Farmers', 'Retailers')."
    )
    campaign_objective: str = Field(
        ...,
        description="The primary goal of the campaign (e.g., 'Drive event registrations', 'Increase product awareness')."
    )
    language: List[str] = Field(
        default_factory=list,
        description="The target language(s) for the generated campaign content (e.g., 'English', 'Spanish', 'Portuguese')."
    )
    key_messages: List[str] = Field(
        default_factory=list,
        description="The core value propositions or key takeaways that must be included in the marketing copy."
    )
