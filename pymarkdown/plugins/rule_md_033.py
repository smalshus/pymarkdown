"""
Module to implement a plugin that looks for inline HTML in the files.
"""

from typing import List, cast

from pymarkdown.general.parser_helper import ParserHelper
from pymarkdown.plugin_manager.plugin_details import (
    PluginDetails,
    PluginDetailsV3,
    QueryConfigItem,
)
from pymarkdown.plugin_manager.plugin_scan_context import PluginScanContext
from pymarkdown.plugin_manager.rule_plugin import RulePlugin
from pymarkdown.tokens.markdown_token import MarkdownToken
from pymarkdown.tokens.raw_html_markdown_token import RawHtmlMarkdownToken
from pymarkdown.tokens.text_markdown_token import TextMarkdownToken


class RuleMd033(RulePlugin):
    """
    Class to implement a plugin that looks for inline HTML in the files.
    """

    def __init__(self) -> None:
        super().__init__()
        self.__allowed_elements: List[str] = []
        self.__allow_first_image_element: bool = False
        self.__is_next_html_block_start: bool = False
        self.__is_first_element: bool = False
        self.__is_first_html_block: bool = False

    def get_details(self) -> PluginDetails:
        """
        Get the details for the plugin.
        """
        return PluginDetailsV3(
            plugin_name="no-inline-html",
            plugin_id="MD033",
            plugin_enabled_by_default=True,
            plugin_description="Inline HTML",
            plugin_version="0.6.0",
            plugin_url="https://pymarkdown.readthedocs.io/en/latest/plugins/rule_md033.md",
            plugin_configuration="allowed_elements, allow_first_image_element",
        )

    def initialize_from_config(self) -> None:
        """
        Event to allow the plugin to load configuration information.
        """
        self.__allow_first_image_element = (
            self.plugin_configuration.get_boolean_property_with_default(
                "allow_first_image_element", True
            )
        )
        allowed_elements = self.plugin_configuration.get_string_property_with_default(
            "allowed_elements",
            "!--,![CDATA[,!DOCTYPE",
        )
        self.__allowed_elements = []
        if allowed_elements := allowed_elements.strip(" "):
            for next_element in allowed_elements.split(","):
                if next_element := next_element.strip(" "):
                    self.__allowed_elements.append(next_element)
                else:
                    raise ValueError(
                        "Elements in the comma-separated list cannot be empty."
                    )

    def query_config(self) -> List[QueryConfigItem]:
        """
        Query to find out the configuration that the rule is using.
        """
        return [
            QueryConfigItem(
                "allow_first_image_element", self.__allow_first_image_element
            ),
            QueryConfigItem("allowed_elements", ",".join(self.__allowed_elements)),
        ]

    def starting_new_file(self) -> None:
        """
        Event that the a new file to be scanned is starting.
        """
        self.__is_next_html_block_start = False
        self.__is_first_html_block = False
        self.__is_first_element = True

    def __look_for_html_start(
        self, context: PluginScanContext, token: MarkdownToken, tag_text: str
    ) -> None:
        # sourcery skip: extract-method, inline-immediately-returned-variable
        full_tag_text = tag_text.lower()
        if tag_text.startswith("/"):
            return
        if tag_text.startswith("![CDATA["):
            tag_text = "![CDATA["
        elif tag_text.startswith("!--"):
            tag_text = "!--"
        elif tag_text.startswith("!DOCTYPE"):
            tag_text = "!DOCTYPE"
        else:
            _, tag_text = ParserHelper.collect_until_one_of_characters_verified(
                tag_text, 0, " \n\t/>"
            )
        extra_data = f"Element: {tag_text}"

        if (
            self.__is_first_html_block
            and self.__allow_first_image_element
            and tag_text.lower() == "h1"
        ):
            is_first_image_element = full_tag_text.endswith("</h1>")
            if is_first_image_element:
                full_tag_text = full_tag_text[: -len("</h1>")]
                end_of_start_heading_index = full_tag_text.find(">")
                assert end_of_start_heading_index != -1
                full_tag_text = full_tag_text[end_of_start_heading_index + 1 :]
                end_of_image_index = full_tag_text.find(">")
                is_first_image_element = (
                    full_tag_text.startswith("<img")
                    and end_of_image_index == len(full_tag_text) - 1
                )
        else:
            is_first_image_element = False

        if not is_first_image_element and tag_text not in self.__allowed_elements:
            self.report_next_token_error(
                context, token, extra_error_information=extra_data
            )

    def next_token(self, context: PluginScanContext, token: MarkdownToken) -> None:
        """
        Event that a new token is being processed.
        """
        if token.is_inline_raw_html:
            self.__is_first_html_block = False
            raw_html_token = cast(RawHtmlMarkdownToken, token)
            self.__look_for_html_start(context, raw_html_token, raw_html_token.raw_tag)
        elif token.is_html_block:
            self.__is_next_html_block_start = True
            self.__is_first_html_block = self.__is_first_element
        elif token.is_text and self.__is_next_html_block_start:
            text_token = cast(TextMarkdownToken, token)
            self.__look_for_html_start(context, text_token, text_token.token_text[1:])
        else:
            self.__is_next_html_block_start = False

        self.__is_first_element = False
