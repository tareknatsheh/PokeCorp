from pydantic import ValidationError
import pytest
from Model.Entities import Trainer

def test_can_create_correct_trainer_instance():
    trainer = Trainer(id=1, name="Ash", town="Pallet Town")
    assert trainer.id == 1
    assert trainer.name == "Ash"
    assert trainer.town == "Pallet Town"

def test_cant_create_wrong_trainer_instance():
    with pytest.raises(ValidationError):
        Trainer(id=-1, name="Ash", town="Pallet Town")  # invalid id
    with pytest.raises(ValidationError):
        Trainer(id=1, name="", town="Pallet Town")  # no name
    with pytest.raises(ValidationError):
        Trainer(id=1, name="Ash", town="")  # no town
    with pytest.raises(ValidationError):
        Trainer(id=1, name="A" * 51, town="Pallet Town")  # name too long
    with pytest.raises(ValidationError):
        Trainer(id=1, name="Ash", town="P" * 51)  # town name too long