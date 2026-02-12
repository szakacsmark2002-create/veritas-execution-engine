from core.model import Entity, EntityType, State, StateStatus, Constraint, ConstraintType
from core.world_state import evaluate_world

entities = [
    Entity(
        id="ORDER_1",
        type=EntityType.ORDER,
        state=State(status=StateStatus.OK),
        constraint=Constraint(type=ConstraintType.MATERIAL_MISSING)
    ),
    Entity(
        id="ORDER_2",
        type=EntityType.ORDER,
        state=State(status=StateStatus.OK)
    )
]

evaluated = evaluate_world(entities)

for e in evaluated:
    print(e.id, e.state.status, e.state.reason)

