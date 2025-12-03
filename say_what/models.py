"""Core data models for the say-what framework."""

from typing import Dict, List, Optional, Any
from datetime import datetime
from pydantic import BaseModel, Field


class TestResult(BaseModel):
    """Result from a single test question."""
    question_id: str
    question: str
    answer: str
    score: float = Field(ge=0.0, le=1.0)
    metrics: Dict[str, Any] = Field(default_factory=dict)
    timestamp: datetime = Field(default_factory=datetime.now)
    error: Optional[str] = None


class PlatformResult(BaseModel):
    """Results from testing a single AI platform."""
    platform_name: str
    model_name: str
    test_results: List[TestResult]
    overall_score: float = Field(ge=0.0, le=1.0)
    timestamp: datetime = Field(default_factory=datetime.now)
    metadata: Dict[str, Any] = Field(default_factory=dict)


class BenchmarkRun(BaseModel):
    """Complete benchmark run across all platforms."""
    run_id: str
    platform_results: List[PlatformResult]
    timestamp: datetime = Field(default_factory=datetime.now)
    benchmark_version: str = "1.0"
