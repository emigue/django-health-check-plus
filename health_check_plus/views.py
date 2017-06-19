from health_check.plugins import plugin_dir
from health_check.views import home

from health_check_plus import settings
from health_check_plus.utils import JsonResponse


def main(request):
    format = request.GET.get('format', None)
    if not format:
        return home(request)
    elif format == "json":
        return main_json(request)


def main_json(request):
    whitelist = set(settings.HEALTH_CHECK_PLUGINS.values())

    str_filter = request.GET.get('checks', None)

    if str_filter:
        filter = str_filter.split(",")
        filtered_names = []
        for alias in filter:
            try:
                filtered_names.append(settings.HEALTH_CHECK_PLUGINS[alias])
            except KeyError:
                raise Exception("Invalid name for filter: {}".format(alias))

        if whitelist:
            whitelist = whitelist.intersection(filtered_names)
        else:
            whitelist = set(filtered_names)

    check_dict_by_ids = {value: key for key, value in settings.HEALTH_CHECK_PLUGINS.iteritems()}

    plugins = []
    working = True
    checked_items = 0
    for plugin_class, plugin in plugin_dir._registry.items():
        identifier = plugin.identifier()
        if not whitelist or (identifier in whitelist):
            plugin = plugin_class()
            if not plugin.status:  # Will return True or None
                working = False
            plugin_json = {'name': check_dict_by_ids[identifier],
                           'identifier': identifier,
                           'status': plugin.status,
                           'pretty_status': plugin.pretty_status()}
            plugins.append(plugin_json)
            checked_items += 1
    plugins.sort(key=lambda x: x['identifier'])

    if checked_items < len(whitelist):
        raise Exception("Some check plugin configured but not loaded")

    if working:
        return JsonResponse(plugins, safe=False)
    else:
        return JsonResponse(plugins, status=500, safe=False)
