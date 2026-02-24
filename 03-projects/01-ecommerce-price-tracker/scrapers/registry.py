from scrapers.tiki_scraper import fetch_tiki_product

SCRAPER_REGISTRY = {
    "tiki": fetch_tiki_product,
    # "tgdd": fetch_tgdd_product,
}
