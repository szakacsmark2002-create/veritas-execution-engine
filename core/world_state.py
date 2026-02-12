from typing import List
from core.model import Entity, State, StateStatus, Constraint, ConstraintType


def evaluate_entity(entity: Entity) -> Entity:
    """
    Decide starea entității pe baza constrângerilor.
    """
    if entity.constraint:
        if entity.constraint.type == ConstraintType.MATERIAL_MISSING:
            entity.state = State(
                status=StateStatus.BLOCKED,
                reason="material missing"
            )
        elif entity.constraint.type == ConstraintType.TIME_DELAY:
            entity.state = State(
                status=StateStatus.DELAYED,
                reason="time delay"
            )
        else:
            entity.state = State(
                status=StateStatus.AT_RISK,
                reason="constraint detected"
            )
    else:
        entity.state = State(
            status=StateStatus.OK,
            reason="no constraints"
        )

    return entity


def evaluate_world(entities: List[Entity]) -> List[Entity]:
    """
    Evaluează starea întregii lumi (snapshot).
    """
    return [evaluate_entity(e) for e in entities]

