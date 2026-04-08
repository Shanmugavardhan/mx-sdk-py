from multiversx_sdk.drwa import decode_drwa_denial, parse_drwa_denial


def test_parse_drwa_denial():
    denial = parse_drwa_denial("DRWA_KYC_REQUIRED")

    assert denial is not None
    assert denial.domain == "drwa"
    assert denial.identifier == "DRWA_KYC_REQUIRED"
    assert denial.code == "kyc_required"


def test_decode_drwa_denial():
    denial = decode_drwa_denial(
        {
            "txHash": "abc",
            "drwa": {
                "denialCode": "DRWA_GLOBAL_PAUSE",
                "denialMessage": "DRWA_GLOBAL_PAUSE",
                "denialContext": "destination",
            },
        }
    )

    assert denial is not None
    assert denial.code == "global_pause"
    assert denial.tx_hash == "abc"
    assert denial.denial_context == "destination"
