from dataclasses import dataclass
from typing import Any, Optional


@dataclass
class DrwaPolicySummary:
    regulated: bool
    policy_id: str = ""
    token_policy_version: Optional[int] = None
    global_pause: bool = False
    strict_auditor_mode: bool = False


def get_drwa_policy_summary(payload: Any) -> Optional[DrwaPolicySummary]:
    if payload is None:
        return None

    if hasattr(payload, "raw"):
        payload = payload.raw

    if not isinstance(payload, dict):
        return None

    drwa = payload.get("drwa")
    if not isinstance(drwa, dict):
        return None

    version = drwa.get("tokenPolicyVersion")
    if version is not None:
        version = int(version)

    return DrwaPolicySummary(
        regulated=bool(drwa.get("regulated") or drwa.get("enabled") or drwa.get("isDrwa")),
        policy_id=str(drwa.get("policyId", "")),
        token_policy_version=version,
        global_pause=bool(drwa.get("globalPause")),
        strict_auditor_mode=bool(drwa.get("strictAuditorMode")),
    )


def is_drwa_token(payload: Any) -> bool:
    summary = get_drwa_policy_summary(payload)
    return bool(summary and summary.regulated)
