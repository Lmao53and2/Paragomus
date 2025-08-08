# agents/model_registry.py

model_providers = {}

def register_provider(name, cls):
    model_providers[name.lower()] = cls

def create_model_instance(provider, model_name, api_key):
    cls = model_providers.get(provider.lower())
    if not cls:
        raise ValueError(f"Unknown provider: {provider}")
    return cls(id=model_name, api_key=api_key)
