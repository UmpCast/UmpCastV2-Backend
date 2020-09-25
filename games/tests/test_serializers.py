from rest_framework.test import APITestCase


class TestApplicationSerializer(APITestCase):
    def test_create_requesting_user(self):
        pass

    def test_create_user_manager(self):
        pass

    def test_create_not_user_manager(self):
        pass

    def test_create_valid_post(self):
        pass

    def test_create_not_valid_post(self):
        pass

    def test_apply_over_limit(self):
        pass

    def test_apply_under_limit(self):
        pass

    def test_apply_in_league(self):
        pass

    def test_apply_not_in_league(self):
        pass

    def test_post_visibility(self):
        pass

    def test_not_post_visibility(self):
        pass

    def test_applied_to_post(self):
        pass

    def test_not_applied_to_post(self):
        pass

    def test_applied_to_game(self):
        pass

    def test_not_applied_to_game(self):
        pass

    def test_cancel_under_limit(self):
        pass

    def test_cancel_over_limit(self):
        pass


class TestPostSerializer(APITestCase):
    def test_create_valid_game(self):
        pass

    def test_create_not_valid_game(self):
        pass


class TestGameSerializer(APITestCase):
    def test_create_over_title(self):
        pass

    def test_create_under_title(self):
        pass

    def test_create_over_location(self):
        pass

    def test_create_under_location(self):
        pass
