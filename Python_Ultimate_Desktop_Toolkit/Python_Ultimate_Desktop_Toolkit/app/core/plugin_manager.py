import importlib.util
from pathlib import Path


class PluginManager:
    def __init__(self, plugin_dir):
        self.plugin_dir = Path(plugin_dir)
        self.plugin_dir.mkdir(parents=True, exist_ok=True)

    def load_plugins(self):
        plugins = []
        for plugin_file in self.plugin_dir.glob("*.py"):
            if plugin_file.name.startswith("_"):
                continue
            try:
                spec = importlib.util.spec_from_file_location(plugin_file.stem, plugin_file)
                module = importlib.util.module_from_spec(spec)
                spec.loader.exec_module(module)
                if hasattr(module, "create_plugin"):
                    plugins.append(module.create_plugin())
            except Exception as exc:
                print(f"Failed to load plugin {plugin_file}: {exc}")
        return plugins
