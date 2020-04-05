"""
Module to implement a plugin that looks for hard tabs in the files.
"""
from plugin_manager import Plugin, PluginDetails


class RuleMd046(Plugin):
    """
    Class to implement a plugin that looks for hard tabs in the files.
    """

    def get_details(self):
        """
        Get the details for the plugin.
        """
        return PluginDetails(
            # code
            plugin_name="code-block-style",
            plugin_id="MD046",
            plugin_enabled_by_default=True,
            plugin_description="Code block style",
        ) # https://github.com/DavidAnson/markdownlint/blob/master/doc/Rules.md#md045---images-should-have-alternate-text-alt-text
        # Parameters: style ("consistent", "fenced", "indented"; default "consistent")

    def starting_new_file(self):
        """
        Event that the a new file to be scanned is starting.
        """

    def next_line(self, line):
        """
        Event that a new line is being processed.
        """

    def completed_file(self):
        """
        Event that the file being currently scanned is now completed.
        """