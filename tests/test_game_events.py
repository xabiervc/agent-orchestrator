from game_production.events import EventContract, EventResponse, validate_event_contract


def test_event_contract_accepts_unique_responses():
    contract = EventContract("player.damage", (EventResponse("audio", "play", "player_hit"), EventResponse("ui", "update", "health_bar")))
    assert validate_event_contract(contract) == []


def test_event_contract_rejects_duplicate_responses():
    response = EventResponse("audio", "play", "hit")
    assert validate_event_contract(EventContract("damage", (response, response)))
