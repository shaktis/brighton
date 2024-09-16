import json
import logging
import os
import time
from typing import Dict, List

import requests
from jinja2 import Environment, PackageLoader, select_autoescape

logger = logging.getLogger(__name__)


class StoreServiceException(Exception):
    pass


class StoreService:
    """
    Service façade for stores
    """
    STORES_LIST_URL = os.environ.get('STORES_LIST_URL')

    @classmethod
    def download_stores_list(cls) -> None:
        """
        download list of stores (json) from API
        :return:
        """
        request_timeout = 5
        if not cls.STORES_LIST_URL:
            raise StoreServiceException(
                "Please configure env variable STORES_LIST_URL in .env file located in the root folder.")
        logger.info(f"Downloading stores list from url: {cls.STORES_LIST_URL}")
        try:
            start = time.time()
            r = requests.get(cls.STORES_LIST_URL, timeout=request_timeout)
            logger.debug(f"HTTP request for stores list completed in {time.time() - start:.2f}s")
            r.raise_for_status()
            if r.status_code == 200:
                current_dir = os.path.dirname(__file__)
                with open(os.path.join(current_dir, 'bristore.json'), 'w') as f:
                    f.write(r.text)
                logger.info(f"Saved stores list in {time.time() - start:.2f}s")
            else:
                raise StoreServiceException(
                    f"Failed to download stores list because the status code was {r.status_code}. Expected 200")
        except requests.HTTPError as err:
            raise StoreServiceException(f"Failed to download stores list because of HTTP error {err}")
        except requests.exceptions.Timeout:
            raise StoreServiceException(
                f"Failed to download stores list because the request timed out after {request_timeout} seconds")

    @classmethod
    def get_stores(cls, force_download=False) -> List[Dict]:
        """
        return list of stores downloading the stores if required
        :param force_download:
        :return:
        """
        current_dir = os.path.dirname(__file__)
        stores_list_file_path = os.path.join(current_dir, 'bristore.json')
        if not os.path.exists(stores_list_file_path) or force_download:
            if force_download:
                logger.info("Force downloading stores list...")
            else:
                logger.info("Stores list not found. Downloading stores list...")
            cls.download_stores_list()
        with open(os.path.join(current_dir, 'bristore.json')) as input_json:
            return list(json.load(input_json).values())

    @classmethod
    def create_stores_list_html_view(cls, recreate_view_file=False):
        current_dir = os.path.dirname(__file__)
        view_file = os.path.join(current_dir, 'stores.html')
        if os.path.exists(view_file) and not recreate_view_file:
            logger.debug(f"{view_file} exists = {os.path.exists(view_file)} recreate_view_file = {recreate_view_file}")
            return
        env = Environment(
            loader=PackageLoader("brighton"),
            autoescape=select_autoescape()
        )
        template = env.get_template("stores.html")
        stores_html: str = template.render(stores=cls.get_stores(recreate_view_file))
        with open(view_file, 'w') as output:
            output.write(stores_html)
        logger.info(f"Successfully created stores HTML view file -- {view_file}")

    @classmethod
    def get_store_count_by_state(cls) -> Dict[str, int]:
        result = dict()
        stores = cls.get_stores()
        for store in stores:
            store_state = store.get('state')
            if not store_state:
                continue
            count: int = result.setdefault(store_state, 0)
            result[store_state] = count + 1
            # sort dict by keys (state)
        return dict(sorted(result.items()))

    @classmethod
    def print_store_count_by_state(cls):
        print("Store counts sorted by state code")
        for state, ct in cls.get_store_count_by_state().items():
            print(state, ' ==> ', ct)
