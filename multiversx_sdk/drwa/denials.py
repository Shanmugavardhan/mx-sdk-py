from dataclasses import dataclass
from typing import Any, Optional


_KNOWN_DENIAL_CODES = {
    "DRWA_KYC_REQUIRED": "kyc_required",
    "DRWA_KYB_REQUIRED": "kyb_required",
    "DRWA_JURISDICTION_BLOCKED": "jurisdiction_blocked",
    "DRWA_INVESTOR_CLASS_BLOCKED": "investor_class_blocked",
    "DRWA_TOKEN_PAUSED": "token_paused",
    "DRWA_TOKEN_EXPIRED": "token_expired",
    "DRWA_METADATA_PROTECTED": "metadata_protected",
    "DRWA_HOLDER_NOT_ALLOWED": "holder_not_allowed",
    "DRWA_RECIPIENT_NOT_ALLOWED": "recipient_not_allowed",
    "DRWA_SENDER_NOT_ALLOWED": "sender_not_allowed",
    "DRWA_COMPLIANCE_STATE_MISSING": "compliance_state_missing",
    "DRWA_AUDITOR_APPROVAL_REQUIRED": "auditor_approval_required",
    "DRWA_GLOBAL_PAUSE": "global_pause",
}


@dataclass
class DrwaDenial:
    domain: str
    identifier: str
    code: str
    message: str
    denial_context: str = ""
    tx_hash: str = ""


def parse_drwa_denial(message: Optional[str]) -> Optional[DrwaDenial]:
    if not message or not message.startswith("DRWA_"):
        return None

    return DrwaDenial(
        domain="drwa",
        identifier=message,
        code=_KNOWN_DENIAL_CODES.get(message, message.removeprefix("DRWA_").lower()),
        message=message,
    )


def decode_drwa_denial(payload: Any) -> Optional[DrwaDenial]:
    if payload is None:
        return None

    if hasattr(payload, "raw"):
        payload = payload.raw

    if not isinstance(payload, dict):
        return None

    drwa = payload.get("drwa")
    if isinstance(drwa, dict):
        identifier = drwa.get("denialCode") or drwa.get("error")
        denial = parse_drwa_denial(identifier)
        if denial:
            denial.message = drwa.get("denialMessage", denial.message)
            denial.denial_context = drwa.get("denialContext", "")
            denial.tx_hash = drwa.get("txHash", payload.get("txHash", ""))
            return denial

    for key in ("returnMessage", "message", "error"):
        denial = parse_drwa_denial(payload.get(key))
        if denial:
            denial.tx_hash = payload.get("txHash", "")
            return denial

    return None


def is_regulated_failure(payload: Any) -> bool:
    return decode_drwa_denial(payload) is not None
