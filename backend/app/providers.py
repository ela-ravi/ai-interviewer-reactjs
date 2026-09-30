"""OpenAI-compatible provider catalog. Add a provider by adding one entry."""

PROVIDERS = {
    "groq": {
        "label": "Groq",
        "base_url": "https://api.groq.com/openai/v1",
        "default_model": "openai/gpt-oss-120b",
    },
}


def public_providers():
    """Fields safe to send to the browser. No base URL, no key."""
    return [
        {"id": provider_id, "label": spec["label"], "default_model": spec["default_model"]}
        for provider_id, spec in PROVIDERS.items()
    ]


def resolve(provider_id, model=None):
    spec = PROVIDERS.get(provider_id)
    if not spec:
        raise ValueError(f"Unknown provider: {provider_id}")
    chosen = (model or "").strip() or spec["default_model"]
    return {"base_url": spec["base_url"], "model": chosen}


def _check():
    groq = resolve("groq")
    assert groq["base_url"] == "https://api.groq.com/openai/v1"
    assert groq["model"] == "openai/gpt-oss-120b"
    try:
        resolve("nope")
    except ValueError:
        pass
    else:
        raise SystemExit("resolve('nope') should raise")

    from app.services.interview_service import InterviewSession

    session = InterviewSession(
        "s", "Python", "Dev",
        api_key="test-key",
        base_url=groq["base_url"],
        model=groq["model"],
    )
    data = session.to_dict()
    assert "api_key" not in data
    assert "test-key" not in str(data)
    print("providers ok")


if __name__ == "__main__":
    _check()
