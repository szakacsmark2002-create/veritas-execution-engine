from api.query import load_mock_entities
from core.world_state import evaluate_world
from core.sla import evaluate_sla

entities = evaluate_world(load_mock_entities())

for e in entities:
    sla = evaluate_sla(e)
    print(e.id, sla)

