"""Utility functions for FSM context management."""


def get_required(ctx: dict, key: str):
    """Get a required value from the context dictionary."""
    value = ctx.get(key)
    if value is None:
        raise ValueError(f"Context must include a non-null '{key}'")
    return value
