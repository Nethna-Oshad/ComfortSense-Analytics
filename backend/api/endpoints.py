from fastapi import APIRouter
from pydantic import BaseModel, Field

from backend.core.feature_fusion import fuse_features

router = APIRouter(tags=["comfort"])


class ComfortRequest(BaseModel):
    air_temperature: float = Field(..., description="Indoor air temperature")
    mean_radiant_temperature: float | None = Field(
        default=None, description="Mean radiant temperature"
    )
    humidity: float | None = Field(default=None, ge=0, le=100)


class ComfortResponse(BaseModel):
    features: dict[str, float]
    comfort_score: float | None = None
    message: str


@router.post("/comfort", response_model=ComfortResponse)
def get_comfort_score(request: ComfortRequest) -> ComfortResponse:
    """Prepare comfort features for a future trained model."""
    input_features = request.model_dump(exclude_none=True)
    features = fuse_features(input_features)
    return ComfortResponse(
        features=features,
        message="Model prediction will be enabled after a trained model is added.",
    )
