"""
Minimal JSON-file storage for the MVP.

No real database yet (see PROJECT_CONTEXT.md §10) — episodes are
persisted as one JSON file each under `data/episodes/`. This is
deliberately simple so the pipeline is testable end-to-end before
investing in Postgres/SQLAlchemy. Swap this out for a real DB layer
once the pipeline itself is proven; the function signatures here
(save_episode/load_episode/list_episodes) are the seam to replace.
"""

import json
import os
from dataclasses import asdict
from datetime import datetime, timezone
from typing import Any

from app.config import settings


def _episodes_dir() -> str:
    path = os.path.join(settings.data_dir, "episodes")
    os.makedirs(path, exist_ok=True)
    return path


def save_episode(episode_id: str, data: dict[str, Any]) -> None:
    data = dict(data)
    data.setdefault("created_at", datetime.now(timezone.utc).isoformat())
    path = os.path.join(_episodes_dir(), f"{episode_id}.json")
    with open(path, "w") as f:
        json.dump(data, f, indent=2, default=lambda o: asdict(o) if hasattr(o, "__dataclass_fields__") else str(o))


def load_episode(episode_id: str) -> dict[str, Any] | None:
    path = os.path.join(_episodes_dir(), f"{episode_id}.json")
    if not os.path.exists(path):
        return None
    with open(path) as f:
        return json.load(f)


def list_episodes() -> list[dict[str, Any]]:
    episodes = []
    for filename in sorted(os.listdir(_episodes_dir())):
        if filename.endswith(".json"):
            with open(os.path.join(_episodes_dir(), filename)) as f:
                episodes.append(json.load(f))
    return episodes
