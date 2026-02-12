from api.query import load_mock_entities
from core.world_state import evaluate_world
from core.simulation import calculate_time_impact, simulate_inbound_delay

entities = evaluate_world(load_mock_entities())

impact = calculate_time_impact(entities)
simulation = simulate_inbound_delay(entities, delay_hours=48)

print("IMPACT:", impact)
print("SIMULATION:", simulation)

