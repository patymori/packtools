"""Just to ease the access to the files.
"""
import os

_CWD = os.path.dirname(os.path.abspath(__file__))


default_catalog = {
        'NAME': 'SciELO Style Catalog for Packtools',

        # Validation schemas: XSD or DTD files.
        'SCH_SCHEMAS': {
            'sps-1.1': os.path.join(_CWD, 'scielo-style-1.1.sch'),
            'sps-1.2': os.path.join(_CWD, 'scielo-style-1.2.sch'),
            'sps-1.3': os.path.join(_CWD, 'scielo-style-1.3.sch'),
            'sps-1.4': os.path.join(_CWD, 'scielo-style-1.4.sch'),
            'sps-1.5': os.path.join(_CWD, 'scielo-style-1.5.sch'),
            'sps-1.6': os.path.join(_CWD, 'scielo-style-1.6.sch'),
            'sps-1.7': os.path.join(_CWD, 'scielo-style-1.7.sch'),
            'sps-1.8': os.path.join(_CWD, 'scielo-style-1.8.sch'),

            # Collection-specific schema
            'scielo-br': os.path.join(_CWD, 'scielo-br.sch'),
        },
        'DTDS': {
            'JATS-journalpublishing1.dtd': os.path.join(
                _CWD, 'jats-publishing-dtd-1.0/JATS-journalpublishing1.dtd'),
            'journalpublishing3.dtd': os.path.join(
                _CWD, 'pmc-publishing-dtd-3.0/journalpublishing3.dtd'),
        },

        # XML Catalog - OASIS Standard.
        'XML_CATALOG': os.path.join(_CWD, 'scielo-publishing-schema.xml'),

        # HTML GENERATOR default constants
        'HTML_GEN_XSLTS': {
            'root-html-1.2.xslt': os.path.join(_CWD, 'htmlgenerator/root-html-1.2.xslt'),
            'root-html-2.0.xslt': os.path.join(_CWD, 'htmlgenerator/root-html-2.0.xslt'),
        },
        'HTML_GEN_DEFAULT_PRINT_CSS_PATH': os.path.join(_CWD,
            'htmlgenerator/static/scielo-bundle-print.css'),
        'HTML_GEN_DEFAULT_CSS_PATH': os.path.join(_CWD,
            'htmlgenerator/static/scielo-article-standalone.css'),
        'HTML_GEN_DEFAULT_JS_PATH': os.path.join(_CWD,
            'htmlgenerator/static/scielo-article-standalone-min.js'),

        # As a general rule, only the latest 2 versions are supported simultaneously.
        'CURRENTLY_SUPPORTED_VERSIONS': os.environ.get(
            'PACKTOOLS_SUPPORTED_SPS_VERSIONS', 'sps-1.7:sps-1.8').split(':'),

        'ALLOWED_PUBLIC_IDS': (
            '-//NLM//DTD JATS (Z39.96) Journal Publishing DTD v1.0 20120330//EN',
            '-//NLM//DTD JATS (Z39.96) Journal Publishing DTD v1.1 20151215//EN',
        ),
        # doctype public ids for sps <= 1.1
        'ALLOWED_PUBLIC_IDS_LEGACY': (
            '-//NLM//DTD JATS (Z39.96) Journal Publishing DTD v1.0 20120330//EN',
            '-//NLM//DTD Journal Publishing DTD v3.0 20080202//EN',
        ),
}

# Python>=3.5 is possible to use the syntax: SCHEMAS = {**SCH_SCHEMAS, **DTDS}
# https://docs.python.org/dev/whatsnew/3.5.html#pep-448-additional-unpacking-generalizations
default_catalog['SCHEMAS'] = dict(default_catalog['SCH_SCHEMAS'])
default_catalog['SCHEMAS'].update(default_catalog['DTDS'])


class Catalog(object):
    """A catalog is a namespace that groups constants together and makes them
    accessible through *dot* accessors.
    """
    ISO3166_CODES = os.path.join(_CWD, 'iso3166-codes.json')

    def __init__(self, **kwargs):
        for name, value in kwargs.items():
            setattr(self, name, value)


class CatalogLoader(object):

    def _load_plugin_if_exists(self):
        """Returns the plugged-in Catalog if it exists or None.
        """
        from pkg_resources import iter_entry_points
        for entry_point in iter_entry_points(group='packtools.catalog', name=None):
            if entry_point.name == 'packtools_catalog':
                return entry_point.load()

        return None

    def load(self, default):
        """Returns the plugged-in Catalog if it exists or otherwise the default
        catalog.
        """
        plugged_catalog = self._load_plugin_if_exists()
        if plugged_catalog:
            return Catalog(**plugged_catalog)
        else: 
            return Catalog(**default)


catalog = CatalogLoader().load(default=default_catalog)
