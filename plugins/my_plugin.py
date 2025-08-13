from airflow.plugins_manager import AirflowPlugin
class MyMinimalPlugin(AirflowPlugin):
    name = "my_minimal_plugin"
    operators = []
    hooks = []
    executors = []
    macros = []
    appbuilder_views = []
    appbuilder_menu_items = []
