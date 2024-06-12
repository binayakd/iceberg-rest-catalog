from iceberg_rest.settings import settings
from pyiceberg.catalog.sql import SqlCatalog


class Catalog:
    instance = None

    def __new__(cls):
        if cls.instance is None:
            cls.instance = _create_catalog()
        return cls.instance


def _create_catalog():
    catalog_settings = {
        "uri": settings.CATALOG_JDBC_URI,
        "warehouse": settings.CATALOG_WAREHOUSE,
        "s3.endpoint": settings.CATALOG_S3_ENDPOINT,
        "s3.access-key-id": settings.AWS_ACCESS_KEY_ID,
        "s3.secret-access-key": settings.AWS_SECRET_ACCESS_KEY,
    }
    catalog = SqlCatalog(catalog_settings.catalog_name, **catalog_settings)
    # (TODO): remove this
    # recreate the db everytime app restarts
    catalog.destroy_tables()
    catalog.create_tables()
    return catalog


def get_catalog() -> Catalog:
    return Catalog()
