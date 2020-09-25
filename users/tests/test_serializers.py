from rest_framework.test import APITestCase


class TestUserSerializer(APITestCase):
    def test_create_equal_passwords(self):
        pass

    def test_create_not_equal_passwords(self):
        pass

    def test_create_no_password1(self):
        pass

    def test_create_no_password2(self):
        pass

    def test_update_equal_passwords(self):
        pass

    def test_update_not_equal_passwords(self):
        pass

    def test_update_no_password1(self):
        pass

    def test_update_no_password2(self):
        pass


class TestUserLeagueStatusSerializer(APITestCase):
    def test_create_only_user_field(self):
        pass

    def test_create_only_league_field(self):
        pass

    def test_apply_level_parameters(self):
        pass

    def test_apply_level_incorrect_league(self):
        pass
