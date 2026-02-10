
RAIL_POLICY = {
    "CSR": True,
    "MUNICIPAL": True,
    "RECYCLER": True,
    "CARBON": False,
    "EPR": False
}

def is_withdrawable(rail: str) -> bool:
    return RAIL_POLICY.get(rail, False)
