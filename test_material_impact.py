from api.query import load_mock_entities
from core.world_state import evaluate_world
from core.material_impact import calculate_material_impact

entities = evaluate_world(load_mock_entities())

print(calculate_material_impact("MAT-888", entities))

