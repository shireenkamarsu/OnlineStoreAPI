import requests
import pytest
import json
from routes.Routes import Routes
from payloads.Payload import Payload
from utils.date_utils import validate_cart_dates_within_range
from dataclasses import asdict


class TestCartAPI:

    @pytest.fixture(autouse=True)
    def init_class_vars(self, setup):
        self.base_url = setup["base_url"]
        self.config = setup["config_reader"]
        self.category = "jewelery"
        self.payload = Payload()

    def test_get_all_carts(self):
        res = requests.get(self.base_url + Routes.GET_ALL_CARTS)
        assert res.status_code == 200
        data = res.json()
        # print(json.dumps(data,indent=4))
        assert len(data) > 0

    def test_get_cart_by_id(self):
        cart_id = self.config.get_property("cartId")
        endpoint = self.base_url + Routes.GET_CART_BY_ID.format(id=cart_id)
        res = requests.get(endpoint)
        assert res.status_code == 200
        data = res.json()
        # print(json.dumps(data,indent=4))
        assert len(data) > 0

    def test_carts_by_date_range(self):
        start_date = self.config.get_property("startdate")
        end_date = self.config.get_property("enddate")
        endpoint = self.base_url + Routes.GET_CARTS_BY_DATE_RANGE.format(startdate=start_date, enddate=end_date)
        res = requests.get(endpoint)
        assert res.status_code == 200
        data = res.json()
        # print(json.dumps(data,indent=4))
        assert len(data) > 0
        cart_dates = [item["date"] for item in data]
        assert validate_cart_dates_within_range(cart_dates, start_date, end_date)

    def test_get_user_cart(self):
        user_id = self.config.get_property("userId")
        endpoint = self.base_url + Routes.GET_USER_CART.format(userId=user_id)
        response = requests.get(endpoint)
        assert response.status_code == 200
        data = response.json()
        # print(json.dumps(data, indent=4))
        for item in data:
            assert item["userId"] == int(user_id)

    def test_get_cart_with_limit(self):
        limit = self.config.get_property("limit")
        endpoint = self.base_url + Routes.GET_CARTS_WITH_LIMIT.format(limit=limit)
        res = requests.get(endpoint)
        assert res.status_code == 200
        data = res.json()
        # print(json.dumps(data,indent=4))
        assert len(data) == int(limit)

    def test_get_cart_sorted_desc(self):
        endpoint = self.base_url + Routes.GET_CARTS_SORTED.format(order="desc")
        res = requests.get(endpoint)
        assert res.status_code == 200
        data = res.json()
        # print(json.dumps(data,indent=4))
        ids = [item['id'] for item in data]
        assert ids == sorted(ids, reverse=True)

    def test_get_cart_sorted_asc(self):
        endpoint = self.base_url + Routes.GET_CARTS_SORTED.format(order="asc")
        res = requests.get(endpoint)
        assert res.status_code == 200
        data = res.json()
        # print(json.dumps(data,indent=4))
        ids = [item['id'] for item in data]
        assert ids == sorted(ids)

    def test_create_cart(self):
        user_id = self.config.get_property("userId")
        cart = self.payload.cart_payload(user_id)
        response = requests.post(
            self.base_url + Routes.CREATE_CART,
            json=asdict(cart)
        )
        assert response.status_code == 201
        data = response.json()
        # print(json.dumps(data,indent=4))
        assert data["id"] is not None
        assert data["userId"] is not None
        assert len(data["products"]) > 0

    def test_update_cart(self):
        user_id = self.config.get_property("userId")
        cart_id = self.config.get_property("cartId")
        cart = self.payload.cart_payload(user_id=user_id)
        endpoint = self.base_url + Routes.UPDATE_USER.format(id=cart_id)
        response = requests.put(
            endpoint,
            json=asdict(cart)
        )
        assert response.status_code == 200
        data = response.json()
        # print(json.dumps(data, indent=4))
        assert data["products"][0]["productId"] is not None
        assert len(data["products"]) > 0

    def test_delete_cart(self):
        cart_id = self.config.get_property("cartId")
        endpoint = self.base_url + Routes.DELETE_CART.format(id=cart_id)
        response = requests.delete(endpoint)
        assert response.status_code == 200
        data = response.json()
        # print(json.dumps(data,indent=4))