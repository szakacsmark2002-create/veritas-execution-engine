from datetime import datetime, timedelta
from typing import List

from core.model import (
    Entity,
    EntityType,
    State,
    StateStatus,
    Constraint,
    ConstraintType,
    TimeWindow,
    Material,
    MaterialStatus,
)

# FIXED deterministic time (enterprise snapshot stability)
FIXED_NOW = datetime(2026, 2, 11, 22, 0, 0)


def load_mock_entities() -> List[Entity]:

    now = FIXED_NOW

    return [

        # -------------------------
        # BLOCKED ORDER (material)
        # -------------------------
        Entity(
            id="002799",
            type=EntityType.ORDER,
            state=State(
                status=StateStatus.BLOCKED,
                reason="material missing"
            ),
            time=TimeWindow(
                start=now - timedelta(hours=6),
                eta=now + timedelta(hours=2)
            ),
            constraint=Constraint(
                type=ConstraintType.MATERIAL_MISSING
            ),
            materials=[
                Material(
                    id="MAT-888",
                    status=MaterialStatus.MISSING,
                    required_qty=100,
                    available_qty=0
                ),
                Material(
                    id="MAT-999",
                    status=MaterialStatus.INBOUND,
                    required_qty=50,
                    available_qty=10,
                    eta=now + timedelta(hours=3)
                )
            ]
        ),

        # -------------------------
        # DELAYED ORDER (time)
        # -------------------------
        Entity(
            id="002800",
            type=EntityType.ORDER,
            state=State(
                status=StateStatus.DELAYED,
                reason="time delay"
            ),
            time=TimeWindow(
                start=now - timedelta(hours=10),
                eta=now - timedelta(hours=1),
                delay_minutes=60
            ),
            constraint=Constraint(
                type=ConstraintType.TIME_DELAY
            ),
            materials=[]
        ),

        # -------------------------
        # AT RISK ORDER (dependency)
        # -------------------------
        Entity(
            id="002801",
            type=EntityType.ORDER,
            state=State(
                status=StateStatus.AT_RISK,
                reason="dependency"
            ),
            time=TimeWindow(
                start=now - timedelta(hours=2),
                eta=now + timedelta(hours=5)
            ),
            constraint=Constraint(
                type=ConstraintType.DEPENDENCY
            ),
            materials=[]
        ),
    ]

