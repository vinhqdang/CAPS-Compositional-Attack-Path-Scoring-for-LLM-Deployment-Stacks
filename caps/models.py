from typing import List, Optional
from pydantic import BaseModel, Field, field_validator


class Vulnerability(BaseModel):
    id: str = Field(..., description="Unique vulnerability identifier")
    name: str = Field(..., description="Vulnerability name")
    description: str = Field("", description="Detailed description")
    exploitability: float = Field(
        ...,
        ge=0.0,
        le=1.0,
        description="Base probability of exploit, between 0.0 and 1.0",
    )
    impact: float = Field(
        ...,
        ge=0.0,
        le=10.0,
        description="Impact score of the vulnerability, between 0.0 and 10.0",
    )


class Mitigation(BaseModel):
    id: str = Field(..., description="Unique mitigation identifier")
    name: str = Field(..., description="Mitigation name")
    description: str = Field("", description="Detailed description")
    effectiveness: float = Field(
        ...,
        ge=0.0,
        le=1.0,
        description="Mitigation effectiveness rating, between 0.0 and 1.0 (where 1.0 blocks the threat completely)",
    )


class Component(BaseModel):
    id: str = Field(..., description="Unique component identifier")
    name: str = Field(..., description="Human-readable component name")
    type: str = Field(
        ...,
        description="Component type (e.g., user, orchestrator, database, tool, api, attacker)",
    )
    asset_value: float = Field(
        1.0,
        ge=1.0,
        le=10.0,
        description="The value/sensitivity of this component, between 1.0 and 10.0",
    )
    vulnerabilities: List[Vulnerability] = Field(
        default_factory=list, description="Vulnerabilities affecting this component"
    )
    mitigations: List[Mitigation] = Field(
        default_factory=list, description="Active mitigations on this component"
    )

    def get_effective_exploitability(self, vuln_id: str) -> float:
        """Calculate the effective exploitability of a vulnerability after mitigations are applied."""
        vuln = next((v for v in self.vulnerabilities if v.id == vuln_id), None)
        if not vuln:
            return 0.0

        factor = 1.0
        for mit in self.mitigations:
            factor *= (1.0 - mit.effectiveness)

        return vuln.exploitability * factor


class Connection(BaseModel):
    source: str = Field(..., description="Source component ID")
    destination: str = Field(..., description="Destination component ID")
    description: str = Field("", description="Description of communication flow")
    trust_boundary: bool = Field(
        False, description="Whether this connection crosses a trust boundary"
    )


class DeploymentStack(BaseModel):
    name: str = Field(..., description="Stack deployment name")
    description: str = Field("", description="Stack deployment description")
    components: List[Component] = Field(..., description="All components in the deployment")
    connections: List[Connection] = Field(..., description="Data/control flow connections")
    chaining_decay: float = Field(
        0.9,
        ge=0.0,
        le=1.0,
        description="Multiplier decay factor for each hop in an attack path, between 0.0 and 1.0",
    )

    @field_validator("connections")
    @classmethod
    def validate_connections(cls, v: List[Connection], info) -> List[Connection]:
        # Validate that connection endpoints exist in the components list
        # Since components are parsed first, we can check they exist in components list
        # We will do this validation explicitly in the engine or on build, but we can do a basic check.
        return v

    def get_component(self, comp_id: str) -> Optional[Component]:
        return next((c for c in self.components if c.id == comp_id), None)
