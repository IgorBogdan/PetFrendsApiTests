from api import PetFrends
from settings import email, password
import os

pf = PetFrends()

def test_get_api_key(email=email, password=password):
    status, result = pf.get_api_key(email, password)
    assert status == 200
    assert 'key' in result


def test_Invalid_get_api_key(email=email, password=password):
        status, result = pf.get_api_key(email, password)
        assert status == 403


def test_get_all_pets_with_valid_key(filter=''):
    _, auth_key = pf.get_api_key(email, password)
    status, result = pf.get_list_of_pets(auth_key, filter)
    assert status == 200
    assert len(result['pets']) > 0


def test_create_pet(name='Урюк', animal_type='человек', age='37'):
        _, auth_key = pf.get_api_key(email, password)
        status, result = pf.create_pet(auth_key, name, animal_type, age)
        assert status == 200
        assert result['name'] == name

def test_create_pet_no_data(name='', animal_type='', age=''):
    _, auth_key = pf.get_api_key(email, password)
    status, result = pf.create_pet(auth_key, name, animal_type, age)
    assert status == 200
    assert result['name'] == name

def test_update_pet_info(name='барсик', animal_type='cat', age=11):
    _, auth_key = pf.get_api_key(email, password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")
    if len(my_pets['pets']) > 0:
        status, result = pf.update_pet_info(auth_key, my_pets['pets'][1]['id'], name, animal_type, age)
        assert status == 200
        assert result['name'] == name
    else:
        raise Exception("There is no pets")


def test_create_pet_with_incorrect(name='0000', animal_type='0000',age='1000'):
        _, auth_key = pf.get_api_key(email, password)
        status, result = pf.create_pet(auth_key, name, animal_type, age)
        assert status == 200
        assert result['name'] == name

def test_add_new_pet_no_photo_with_invalid_age(name='Шатун', animal_type='медведь', age='бурый'):

    _, auth_key = pf.get_api_key(email, password)

    status, result = pf.create_pet(auth_key, name, animal_type, age)

    assert status == 200




def test_successful_update_self_pet_info(name='Джек', animal_type='Воробей', age=59):

    _, auth_key = pf.get_api_key(email, password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    if len(my_pets['pets']) == 0:
        pf.create_pet(auth_key, "симка", "собакен", "1")
        _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    if len(my_pets['pets']) > 0:
        status, result = pf.update_pet_info(auth_key, my_pets['pets'][0]['id'], name, animal_type, age)

        assert status == 200
        assert result['name'] == name

        pet_id = my_pets['pets'][0]['id']
        pf.delete_pet(auth_key, pet_id)
    else:
        raise Exception("There is no pets")

def test_add_new_pet(name='Valet', animal_type='cat', age='7', pet_photo='images/барсик.jpg'):

    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)

    _, auth_key = pf.get_api_key(email, password)

    status, result = pf.add_new_pet(auth_key, name, animal_type, age, pet_photo)

    assert status == 200
    assert result['name'] == name

def test_add_new_pet_no_data(name='', animal_type='', age='', pet_photo='images/бегимот.jpg'):

    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)

    _, auth_key = pf.get_api_key(email, password)

    status, result = pf.add_new_pet(auth_key, name, animal_type, age, pet_photo)

    assert status == 200
    assert result['name'] == name