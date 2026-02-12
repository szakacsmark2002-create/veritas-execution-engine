from core.model import Entity, EntityType, State, StateStatus

order = Entity(
    id="002799",
    type=EntityType.ORDER,
    state=State(
        status=StateStatus.BLOCKED,
        reason="material missing"
    )
)

print(order)

