from rest_framework import status
from django.urls import reverse
from rest_framework.test import APIClient
from model_bakery import baker
from rest_framework.decorators import action
from rest_framework.response import Response


class OrderedModelUpdateMixin(object):
    def to(self, order, extra_update=None):
        """
        Move object to a certain position, updating all affected objects to move accordingly up or down.
        """
        if not isinstance(order, int):
            raise TypeError(
                "Order value must be set using an 'int', not using a '{0}'.".format(
                    type(order).__name__
                )
            )

        order_field_name = self.order_field_name
        if order is None or getattr(self, order_field_name) == order:
            # object is already at desired position
            return
        qs = self.get_ordering_queryset()
        extra_update = {} if extra_update is None else extra_update
        if getattr(self, order_field_name) > order:
            qs.below_instance(self).above(order, inclusive=True).increase_order(
                **extra_update
            )
        else:
            qs.above_instance(self).below(order, inclusive=True).decrease_order(
                **extra_update
            )
        setattr(self, order_field_name, order)
        self.save(update_fields=['order'])


class MoveOrderedModelMixin(object):

    @action(detail=True, methods=['patch'])
    def move(self, request, pk):
        assert hasattr(self, 'move_filter_variable'), (
            'move_filter_variable required'
        )
        assert hasattr(self, 'move_filter_value'), (
            'move_filter_value required'
        )

        obj = self.get_object()
        filter_dict = {
            self.move_filter_variable: getattr(obj, self.move_filter_value)
        }

        obj_set = self.get_queryset().filter(**filter_dict)
        order = int(request.data.get('order', None))

        if order is None:
            return Response({"error": "missing parameters"}, status=status.HTTP_400_BAD_REQUEST)
        if order < obj_set.get_min_order() or order > obj_set.get_max_order():
            return Response({"order": ["order value out of range"]}, status=status.HTTP_400_BAD_REQUEST)
        obj.to(order)
        return Response(status=status.HTTP_200_OK)


class ObjectMixin(object):
    """
    Handle object create/returns for detail views
    """
    object = None

    def get_object(self):
        assert hasattr(self, 'create_object'), (
            'create_object is required and not defined'
        )
        if self.object is None:
            self.object = self.create_object()
        return self.object

    def restart_object(self):
        assert hasattr(self, 'create_object'), (
            'create_object is required and not defined'
        )
        self.object = self.create_object()


class TestSetupMixin(object):
    """
    Initialize APITestCase with client and super-user login to avoid permissions
    """

    def setUp(self):
        self.client = APIClient()
        self.user = baker.make('users.User', is_superuser=True)
        self.client.force_authenticate(user=self.user)


class TestCreateMixin(object):
    """
    For a given model, test create endpoint
    """
    valid_create = None

    def get_valid_create(self):
        assert self.valid_create is not None, (
            "'%s' should either include a `valid_create` attribute, "
            "or override the `get_valid_create()` method."
            % self.__class__.__name__
        )
        return self.valid_create

    def test_create(self):
        required_attrs = ['basename', 'client']
        for attr in required_attrs:
            assert hasattr(self, attr), ('{} is required and not defined'.format(attr))

        create_url = reverse(''.join([self.basename, '-list']))
        response = self.client.post(create_url, data=self.get_valid_create())

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)


class TestRetrieveMixin(ObjectMixin):
    """
    For a given model, test retrieve endpoint
    """

    def test_retrieve(self):
        required_attrs = ['basename', 'client']
        for attr in required_attrs:
            assert hasattr(self, attr), ('{} is required and not defined'.format(attr))

        kwargs = {
            'pk': self.get_object().pk
        }
        retrieve_url = reverse(''.join([self.basename, '-detail']), kwargs=kwargs)
        response = self.client.get(retrieve_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class TestUpdateMixin(ObjectMixin):
    """
    For a given model, test update endpoint
    """
    valid_update = None

    def get_valid_update(self):
        assert self.valid_update is not None, (
            "'%s' should either include a `valid_update` attribute, "
            "or override the `get_valid_update()` method."
            % self.__class__.__name__
        )
        return self.valid_update

    def test_update(self):
        required_attrs = ['basename', 'client']
        for attr in required_attrs:
            assert hasattr(self, attr), ('{} is required and not defined'.format(attr))

        kwargs = {
            'pk': self.get_object().pk
        }
        update_url = reverse(''.join([self.basename, '-detail']), kwargs=kwargs)
        response = self.client.patch(update_url, data=self.get_valid_update())

        self.assertEqual(response.status_code, status.HTTP_200_OK)


class TestDeleteMixin(ObjectMixin):
    """
    For a given model, test delete endpoint
    """

    def test_delete(self):
        required_attrs = ['basename', 'client']
        for attr in required_attrs:
            assert hasattr(self, attr), ('{} is required and not defined'.format(attr))

        kwargs = {
            'pk': self.get_object().pk
        }
        delete_url = reverse(''.join([self.basename, '-detail']), kwargs=kwargs)

        response = self.client.delete(delete_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.restart_object()


class TestListMixin(object):
    """
    For a given model, test list endpoint
    """

    def test_list(self):
        required_attrs = ['basename', 'client']
        for attr in required_attrs:
            assert hasattr(self, attr), ('{} is required and not defined'.format(attr))

        list_url = reverse(''.join([self.basename, '-list']))
        response = self.client.get(list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class TestFilterMixin(object):
    """
    For a given model, test list endpoint with filter query-params
    """
    filter_queries = None

    def get_filter_queries(self):
        assert self.filter_queries is not None, (
            "'%s' should either include a `filter_queries` attribute, "
            "or override the `get_filter_queries()` method."
            % self.__class__.__name__
        )
        return self.filter_queries

    def test_filter(self):
        required_attrs = ['basename', 'client', 'filter_fields']
        for attr in required_attrs:
            assert hasattr(self, attr), ('{} is required and not defined'.format(attr))

        list_url = reverse(''.join([self.basename, '-list']))
        filter_queries = self.get_filter_queries()

        for field in self.filter_fields:
            for query in filter_queries.get(field):
                query_url = ''.join([list_url, '?', field, '=', query])
                response = self.client.get(query_url)
                self.assertEqual(response.status_code, status.HTTP_200_OK)


class TestModelMixin(TestCreateMixin, TestRetrieveMixin, TestUpdateMixin,
                        TestDeleteMixin, TestListMixin, TestFilterMixin, TestSetupMixin):
    """
    Provide setup and testing for CRUD, List, List-Filter operations
    """
