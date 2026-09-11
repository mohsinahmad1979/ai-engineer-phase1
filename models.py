from typing import Literal

from pydantic import BaseModel, ConfigDict, Field


class LogAnalysisSchema(BaseModel):
    model_config = ConfigDict(extra="forbid")

    error_class: str = Field(
        description="The full .NET exception or class name where the failure occurred."
    )
    root_cause: str = Field(
        description="A concise summary of why the failure happened."
    )
    line_number: str = Field(
        description="The specific line number or code file, if available. Use 'Unknown' if not found."
    )
    recommended_fix: str = Field(
        description="A clean, optimized, production-ready C# code snippet or config fix."
    )
    severity_level: Literal["CRITICAL", "WARNING", "INFO"] = Field(
        description="Categorise as CRITICAL, WARNING, or INFO."
    )
