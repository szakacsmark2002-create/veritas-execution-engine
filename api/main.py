from fastapi import FastAPI
from pydantic import BaseModel
from api.query import load_mock_entities
from core.world_state import evaluate_world
from core.report import build_order_report
from core.material_impact import calculate_material_impact
from core.snapshot import WorldSnapshot
from core.execution import ExecutionContext

app = FastAPI(
    title="SACO – Operational Truth Layer",
    version="0.2.0",
    description="Deterministic Operational Control Engine    powered by Mark"
)


class AskRequest(BaseModel):
    question: str


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/ask")
def ask(req: AskRequest):
    """
    Universal ask endpoint (deterministic + snapshot).
    """
    raw_entities = load_mock_entities()
    entities = evaluate_world(raw_entities)

    snapshot = WorldSnapshot(raw_entities)
    context = ExecutionContext(req.question, snapshot)

    q = req.question.lower()

    # ---- MATERIAL IMPACT ----
    if "mat-" in q:
        tokens = q.replace("_", "-").split()
        material_id = None

        for t in tokens:
            if t.startswith("mat-"):
                material_id = t.upper()
                break

        if not material_id:
            result = {"error": "Material ID not found in question"}
            context.attach_result(result)
            return {"meta": context.__dict__, "data": result}

        result = calculate_material_impact(material_id, entities)
        context.attach_result(result)
        return {"meta": context.__dict__, "data": result}

    # ---- ORDER REPORT ----
    if "order" in q or "ordere" in q or "ordine" in q:
        order_id = "".join(ch for ch in q if ch.isdigit())

        for e in entities:
            if e.id == order_id:
                result = build_order_report(e, entities)
                context.attach_result(result)
                return {"meta": context.__dict__, "data": result}

        result = {"error": f"Order {order_id} not found"}
        context.attach_result(result)
        return {"meta": context.__dict__, "data": result}

    result = {
        "message": "Question understood, but no handler matched yet"
    }

    context.attach_result(result)
    return {"meta": context.__dict__, "data": result}

