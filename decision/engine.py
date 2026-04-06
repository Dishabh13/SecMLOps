def decide_risk(suspicious, adversarial, rate_limited, integrity_ok, validation_error=None):
    if not integrity_ok:
        return {
            "status": "blocked",
            "risk_level": "CRITICAL",
            "reason": "Model integrity verification failed.",
            "allow_prediction": False,
        }

    if rate_limited:
        return {
            "status": "blocked",
            "risk_level": "HIGH",
            "reason": "Too many requests. Rate limit exceeded.",
            "allow_prediction": False,
        }

    if validation_error:
        return {
            "status": "blocked",
            "risk_level": "HIGH",
            "reason": validation_error,
            "allow_prediction": False,
        }

    if adversarial:
        return {
            "status": "blocked",
            "risk_level": "HIGH",
            "reason": "Adversarial input detected.",
            "allow_prediction": False,
        }

    if suspicious:
        return {
            "status": "allowed_with_warning",
            "risk_level": "MEDIUM",
            "reason": "Input looks suspicious. Review the result carefully.",
            "allow_prediction": True,
        }

    return {
        "status": "allowed",
        "risk_level": "LOW",
        "reason": "Request passed all security checks.",
        "allow_prediction": True,
    }
