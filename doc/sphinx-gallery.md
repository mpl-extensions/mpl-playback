# Sphinx-gallery integration


`mpl-playback` provides a custom [sphinx-gallery scraper](https://sphinx-gallery.github.io/stable/advanced.html#write-a-custom-image-scraper) which allows you automatically generate gifs for your interactive maptlotlib plots in your sphinx gallery. This custom scraper will generate a gif if there is a playback json file available, and otherwise will fall back to the default matplotlib scraper.

To enable the custom scraper add the following to your `conf.py`


```python
from mpl_playback.scraper import matplotlib_scraper
sphinx_gallery_conf = {
    # ... the rest of your normal config
    "image_scrapers": (matplotlib_scraper),
}
```

then the scraper will automatically pick up any playback files that are in the same directory as the examples.
