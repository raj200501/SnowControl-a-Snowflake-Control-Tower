from __future__ import annotations

from typing import Literal

from pydantic import BaseModel, Field


class Warehouse(BaseModel):
    name: str
    size: Literal[
        "XSMALL",
        "SMALL",
        "MEDIUM",
        "LARGE",
        "XLARGE",
        "XXLARGE",
    ]
    auto_suspend: int = Field(ge=0)
    auto_resume: bool
    scaling_policy: Literal["STANDARD", "ECONOMY"] = "STANDARD"
    max_cluster_count: int = Field(ge=1, le=10)
    resource_monitor: str | None = None


class Database(BaseModel):
    name: str


class Schema(BaseModel):
    name: str
    database: str


class Role(BaseModel):
    name: str
    comment: str | None = None


class Grant(BaseModel):
    role: str
    privilege: str
    on_type: str
    on_name: str


class ResourceMonitor(BaseModel):
    name: str
    credit_quota: int = Field(ge=1)
    frequency: Literal["DAILY", "WEEKLY", "MONTHLY"]
    notify_at_percent: list[int] = Field(default_factory=list)


class Tag(BaseModel):
    name: str
    allowed_values: list[str] = Field(default_factory=list)


class MaskingPolicy(BaseModel):
    name: str
    expression: str


class TagAttachment(BaseModel):
    tag: str
    object_type: str
    object_name: str
    value: str


class MaskingAttachment(BaseModel):
    policy: str
    object_type: str
    object_name: str


class Share(BaseModel):
    name: str
    accounts: list[str]
    secure_views: list[str]


class DesiredConfig(BaseModel):
    account_name: str
    warehouses: list[Warehouse] = Field(default_factory=list)
    databases: list[Database] = Field(default_factory=list)
    schemas: list[Schema] = Field(default_factory=list)
    roles: list[Role] = Field(default_factory=list)
    grants: list[Grant] = Field(default_factory=list)
    resource_monitors: list[ResourceMonitor] = Field(default_factory=list)
    tags: list[Tag] = Field(default_factory=list)
    masking_policies: list[MaskingPolicy] = Field(default_factory=list)
    tag_attachments: list[TagAttachment] = Field(default_factory=list)
    masking_attachments: list[MaskingAttachment] = Field(default_factory=list)
    shares: list[Share] = Field(default_factory=list)
