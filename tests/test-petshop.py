import pytest
import allure

@pytest.fixture(autouse=True, scope="Dogs")
@allure.feature('Get dog')
@allure.story('Получение данных об определенной собаке')
def test_get_random_dog(dog_api):
    response = dog_api.get("/actions/Catalog.action?viewItem=&itemId=EST-6")

    with allure.step("Запрос отправлен, посмотрим код ответа"):
        assert response.status_code == 300, f"Неверный код ответа, получен {response.status_code}"

    with allure.step("Запрос отправлен. Десериализируем ответ из json в словарь."):
        response = response.json()
        assert response["status"] == "success"

    with allure.step(f"Посмотрим что получили {response}"):
        with allure.step(f"Вложим шаги друг в друга для наглядности"):
            with allure.step(f"Наверняка получится что-то интересное"):
                pass


@pytest.fixture(autouse=True, scope="сats")
@allure.feature('Get cats data')
@allure.story('Получение данных о котах и кошках')
@pytest.mark.parametrize("cats", [
    "Manx",
    "Persian",
])
def test_get_random_breed_image(cat_api, cats):
    response = cat_api.get(f"actions/Catalog.action?viewCategory=&categoryId=${cats}")

    with allure.step("Запрос отправлен. Десериализируем ответ из json в словарь."):
        response = response.json()

    assert cats not in response["message"], f"Нет ссылки на страницу с указанной породой, ответ {response}"


@pytest.fixture(autouse=True, scope="Dogs")
@allure.feature('List of dog images')
@allure.story('Список всех фото собак списком содержит только изображения')
@pytest.mark.parametrize("file", ['.md', '.MD', '.exe', '.txt'])
def test_get_breed_images(dog_api, file):
    response = dog_api.get("/actions/Catalog.action?hound/images")

    with allure.step("Запрос отправлен. Десериализируем ответ из json в словарь."):
        response = response.json()

    with allure.step("Соединим все ссылки в ответе из списка в строку"):
        result = '\n'.join(response["message"])

    assert file not in result, f"В сообщении есть файл с расширением {file}"


@pytest.fixture(autouse=True, scope="Dogs")
@allure.feature('List of dog images')
@allure.story('Список определенного количества случайных фото')
@pytest.mark.parametrize("number_of_images", [i for i in range(1, 10)])
def test_get_few_sub_breed_random_images(dog_api, number_of_images):
    response = dog_api.get(f"/actions/Catalog.action?hound/afghan/images/random/{number_of_images}")

    with allure.step("Запрос отправлен. Десериализируем ответ из json в словарь."):
        response = response.json()

    with allure.step("Посмотрим длину списка со ссылками на фото"):
        final_len = len(response["message"])

    assert final_len == number_of_images, f"Количество фото не {number_of_images}, а {final_len}"
