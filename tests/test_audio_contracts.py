from game_production.audio import AudioContract, validate_audio_contract


def test_audio_contract_requires_event_for_sfx():
    assert validate_audio_contract(AudioContract("hit", "sound_effect", license_name="generated"))


def test_audio_contract_accepts_declared_asset():
    contract = AudioContract("hit", "sound_effect", event="player.damage", license_name="generated", variations=2)
    assert validate_audio_contract(contract) == []
