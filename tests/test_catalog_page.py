import pytest
from page_objects import CatalogPage

@pytest.mark.reserv
def test_search_form(browser, base_url):
    catalog_page = CatalogPage(browser, base_url)
    assert catalog_page.find_product_category('tablet'), "Отсутствует товар категории tablet"
    assert catalog_page.carusel(), "нет баннера брендов"
    assert catalog_page.display_settings(), "нет панели настройки отображения"
    assert catalog_page.product_list(), "нет списка товаров"
    assert catalog_page.pagination_buttons(), "нет кнопок пагинации"