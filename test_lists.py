from core.model import Entity, EntityType, State, StateStatus
from core.lists import list_problematic_entities

entities = [
    Entity(
        id="ORDER_OK",
        type=EntityType.ORDER,
        state=State(status=StateStatus.OK)
    ),
    Entity(
        id="ORDER_DELAYED",
        type=EntityType.ORDER,
        state=State(status=StateStatus.DELAYED)
    ),
    Entity(
        id="ORDER_BLOCKED",
        type=EntityType.ORDER,
        state=State(status=StateStatus.BLOCKED)
    ),
]

sorted_entities = list_problematic_entities(entities)

for e in sorted_entities:
    print(e.id, e.state.status)

