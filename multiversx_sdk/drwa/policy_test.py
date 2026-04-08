from multiversx_sdk.drwa import get_drwa_policy_summary, is_drwa_token


def test_get_drwa_policy_summary():
    summary = get_drwa_policy_summary(
        {
            "drwa": {
                "regulated": True,
                "policyId": "policy-1",
                "tokenPolicyVersion": 4,
                "globalPause": False,
                "strictAuditorMode": True,
            }
        }
    )

    assert summary is not None
    assert summary.regulated is True
    assert summary.policy_id == "policy-1"
    assert summary.token_policy_version == 4
    assert summary.strict_auditor_mode is True
    assert is_drwa_token({"drwa": {"regulated": True}}) is True
