from core.model import Entity, EntityType, State, StateStatus, Constraint, ConstraintType
from core.explain import explain_entity

order = Entity(
    id="002799",
    type=EntityType.ORDER,
    state=State(
        status=StateStatus.BLOCKED,
        reason="material missing"
    ),
    constraint=Constraint(
        type=ConstraintType.MATERIAL_MISSING
    )
)

explanation = explain_entity(order)
print(explanation)

