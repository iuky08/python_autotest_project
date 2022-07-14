import allure 
import pytest



@allure.parent_suite('parent suite')
@allure.epic('epic')
@allure.suite('suite')
@allure.feature('feature')
@allure_story('story')
@allure.title('title')
@pytest.mark.parametrize('input_field_value',[i for i in range(len(input_field_value))] )
