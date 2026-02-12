from enum import Enum
from typing import Optional, Dict, Any, List
from datetime import datetime
from pydantic import BaseModel


# =========================
# UNIVERSAL ENUMS
# =========================

class EntityType(str, Enum):
    ORDER = "order"
    MATERIAL = "material"
    FLOW = "flow"
    PROCESS = "process"
    LOCATION = "location"
    RESOURCE = "resource"


class StateStatus(str, Enum):
    OK = "ok"
    PARTIAL = "partial"
    BLOCKED = "blocked"
    DELAYED = "delayed"
    AT_RISK = "at_risk"


class ConstraintType(str, Enum):
    MATERIAL_MISSING = "material_missing"
    INSUFFICIENT_STOCK = "insufficient_stock"
    TIME_DELAY = "time_delay"
    CAPACITY_LIMIT = "capacity_limit"
    DEPENDENCY = "dependency"
    UNKNOWN = "unknown"


class MaterialStatus(str, Enum):
    IN_STOCK = "in_stock"
    MISSING = "missing"
    INBOUND = "inbound"
     
# =========================
# CORE UNIVERSAL MODELS
# =========================

class TimeWindow(BaseModel):
    start: Optional[datetime] = None
    end: Optional[datetime] = None
    eta: Optional[datetime] = None
    delay_minutes: Optional[int] = None


class State(BaseModel):
    status: StateStatus
    reason: Optional[str] = None


class Constraint(BaseModel):
    type: ConstraintType
    details: Optional[Dict[str, Any]] = None


class Material(BaseModel):
    id: str
    status: MaterialStatus
    required_qty: int
    available_qty: int
    eta: Optional[datetime] = None


class Entity(BaseModel):
    id: str
    type: EntityType
    state: State
    time: Optional[TimeWindow] = None
    constraint: Optional[Constraint] = None
    materials: Optional[List[Material]] = None

