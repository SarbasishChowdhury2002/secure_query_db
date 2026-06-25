from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel
from typing import List

from app.services.query_service import QueryService
from app.blockchain.ledger import BlockchainLogger
from app.config import get_settings

settings = get_settings()

# ==============================
# App setup
# ==============================
app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    description="Secure query processing over encrypted and sharded databases"
)

# Single shared instances
blockchain = BlockchainLogger()
service = QueryService(blockchain)

# Load dataset into shards on startup
from app.experiments.dataset_generator import generate_dataset
from app.db import shard1, shard2, shard3

dataset = generate_dataset(1000)
shard1.load_dataset(dataset[0::3])
shard2.load_dataset(dataset[1::3])
shard3.load_dataset(dataset[2::3])


# ==============================
# Request / Response models
# ==============================
class QueryRequest(BaseModel):
    user_identifier: str
    user_role: str
    keywords: List[str]


class QueryResult(BaseModel):
    shard_name: str
    query_time_ms: float
    keyword_count: int
    result_count: int
    trapdoors: dict
    block_hash: str
    prev_hash: str
    results: List[dict]


class HealthResponse(BaseModel):
    status: str
    app_name: str
    version: str


# ==============================
# Routes
# ==============================

@app.get("/", response_model=HealthResponse)
def health_check():
    """Health check — confirms API is running"""
    return HealthResponse(
        status="ok",
        app_name=settings.APP_NAME,
        version=settings.APP_VERSION
    )


@app.post("/query", response_model=QueryResult)
def run_query(request: QueryRequest):
    """
    Execute a secure query over encrypted sharded database.
    - Generates trapdoors from keywords
    - Routes to correct shard
    - Returns decrypted results (if role permits)
    - Logs to blockchain audit trail
    """
    try:
        result = service.run_query(
            user_identifier=request.user_identifier,
            user_role=request.user_role,
            keywords=request.keywords
        )

        return QueryResult(
            shard_name=result["shard_name"],
            query_time_ms=round(result["query_time"] * 1000, 4),
            keyword_count=result["keyword_count"],
            result_count=result["result_count"],
            trapdoors=result["trapdoors"],
            block_hash=result["block_hash"],
            prev_hash=result["prev_hash"],
            results=result["results"]
        )

    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )

    except PermissionError as e:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You are not authorized to perform this action"
        )

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Internal server error: {str(e)}"
        )


@app.get("/health/blockchain")
def blockchain_health():
    """Check if the audit log chain is valid and untampered"""
    is_valid = blockchain.verify_chain()
    return {
        "chain_valid": is_valid,
        "total_blocks": len(blockchain.chain),
        "status": "✅ VALID" if is_valid else "❌ TAMPERED"
    }