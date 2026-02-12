from api.query import load_mock_entities
from core.world_state import evaluate_world
from core.impact import calculate_operational_impact

entities = evaluate_world(load_mock_entities())

target = None
for e in entities:
    if e.id == "002799":
        target = e

impact = calculate_operational_impact(target, entities)
print(impact)

