from rest_framework.test import APITestCase


class NotificationMixin(object):
    def test_create_under_subject(self):
        pass

    def test_create_over_subject(self):
        pass

    def test_create_under_message(self):
        pass

    def test_create_over_message(self):
        pass


class TestUmpCastNotificationSerializer(NotificationMixin, APITestCase):
    pass


class TestLeagueNotificationSerializer(NotificationMixin, APITestCase):
    pass


class TestGameNotificationSerializer(NotificationMixin, APITestCase):
    pass


class TestApplicationNotificationSerializer(NotificationMixin, APITestCase):
    pass
