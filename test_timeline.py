from api.query import load_mock_entities
from core.world_state import evaluate_world
from core.timeline import build_timeline

entities = evaluate_world(load_mock_entities())

for e in entities:
    if e.id == "002799":
        timeline = build_timeline(e)
        print(timeline)

