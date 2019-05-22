# coding: utf8

import logging
import six

log = logging.getLogger(__name__)

def configure(main_config):
    config = {}
    schema = {
        'ckanext.theme.api.geoextent.name.autocomplete.url': {
            'default': u'https://www.data.gouv.fr/api/1/spatial/zones/suggest?q={}&size={}'},
        'ckanext.theme.api.geoextent.bbox.url': {
            'default': u'https://www.data.gouv.fr/api/1/spatial/zone/{}'},
    }
    errors = []
    for i in schema:
        v = None
        if i in main_config:
            v = main_config[i]
        elif i.replace('ckanext.', '') in main_config:
            log.warning('theme configuration options should be prefixed with \'ckanext.\'. ' +
                        'Please update {0} to {1}'.format(i.replace('ckanext.', ''), i))

        if v:
            if 'parse' in schema[i]:
                v = (schema[i]['parse'])(v)
            try:
                if 'validate' in schema[i]:
                    (schema[i]['validate'])(v)
                config[i] = v
            except ConfigError as e:
                errors.append(str(e))
        elif schema[i].get('required', False):
            errors.append('Configuration parameter {} is required'.format(i))
        elif schema[i].get('required_if', False) and schema[i]['required_if'] in main_config:
            errors.append('Configuration parameter {} is required when {} is present'.format(i,
                                                                                             schema[i][
                                                                                                 'required_if']))
        elif 'default' in schema[i]:
            config[i] = schema[i]['default']
    if len(errors):
        raise ConfigError("\n".join(errors))

    # make sure all the strings in the config are unicode formatted
    for key, value in config.iteritems():
        if isinstance(value, str):
            config[key] = six.text_type(value, encoding='utf-8')
    return config


class ConfigError(Exception):
    pass