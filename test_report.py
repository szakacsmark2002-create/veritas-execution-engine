from api.query import load_mock_entities
from core.world_state import evaluate_world
from core.report import build_order_report

entities = evaluate_world(load_mock_entities())

target = None
for e in entities:
    if e.id == "002799":
        target = e

print("MATERIALS ON ENTITY:", target.materials)

report = build_order_report(target, entities)
print(report)

