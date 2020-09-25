from rest_framework.test import APITestCase


class TestLeagueSerializer(APITestCase):
    def test_create_is_manager(self):
        pass

    def test_create_is_not_manager(self):
        pass


class TestDivisionSerializer(APITestCase):
    def test_create_valid_league(self):
        pass

    def test_create_not_valid_league(self):
        pass


class TestRoleSerializer(APITestCase):
    def test_create_valid_division(self):
        pass

    def test_create_not_valid_division(self):
        pass


class TestLevelSerializer(APITestCase):
    def test_create_valid_league(self):
        pass

    def test_create_not_valid_league(self):
        pass

    def test_create_roles_in_league(self):
        pass

    def test_create_roles_not_in_league(self):
        pass

    def test_create_only_league(self):
        pass
