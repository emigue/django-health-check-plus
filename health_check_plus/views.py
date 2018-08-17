import copy

from django.http import JsonResponse
from health_check.views import MainView
from health_check.plugins import plugin_dir


class StatusOptionalCheckView(MainView):
    humanize_plugin_name = {
        'DatabaseBackend': 'db',
        'CacheBackend': 'cache',
        'CeleryHealthCheck': 'celery',
        'DefaultFileStorageHealthCheck': 'storage'
    }

    def get(self, request, *args, **kwargs):
        plugins = []
        errors = []
        for plugin_class, options in plugin_dir._registry:
            plugin = plugin_class(**copy.deepcopy(options))
            if self._plugin_in_queryparams(request, plugin):
                plugin.run_check()
                plugins.append(plugin)
                errors += plugin.errors
        plugins.sort(key=lambda x: x.identifier())
        status_code = 500 if errors else 200

        if 'application/json' in request.META.get('HTTP_ACCEPT', '') or request.GET.get('format') == 'json':
            return self.render_to_response_json(plugins, status_code)

        return self.render_to_response({'plugins': plugins}, status=status_code)

    def _plugin_in_queryparams(self, request, plugin):
        if 'checks' in request.GET:
            plugins_to_check = request.GET.get('checks', '').split(',')
            return self.humanize_plugin_name.get(plugin.identifier(), plugin.identifier()) in plugins_to_check
        return True


class StatusCheckPingView(MainView):

    def get(self, request, *args, **kwargs):
        return JsonResponse({}, status=200)
