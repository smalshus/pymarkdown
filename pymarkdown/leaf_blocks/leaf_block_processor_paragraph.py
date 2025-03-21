"""
Module to provide processing for the leaf blocks.
"""

import logging
from typing import List, Optional, Tuple, cast

from pymarkdown.block_quotes.block_quote_data import BlockQuoteData
from pymarkdown.general.constants import Constants
from pymarkdown.general.parser_helper import ParserHelper
from pymarkdown.general.parser_logger import ParserLogger
from pymarkdown.general.parser_state import ParserState
from pymarkdown.general.position_marker import PositionMarker
from pymarkdown.general.tab_helper import TabHelper
from pymarkdown.tokens.blank_line_markdown_token import BlankLineMarkdownToken
from pymarkdown.tokens.markdown_token import MarkdownToken
from pymarkdown.tokens.paragraph_markdown_token import ParagraphMarkdownToken
from pymarkdown.tokens.stack_token import (
    BlockQuoteStackToken,
    ListStackToken,
    ParagraphStackToken,
)
from pymarkdown.tokens.text_markdown_token import TextMarkdownToken

POGGER = ParserLogger(logging.getLogger(__name__))


class LeafBlockProcessorParagraph:
    """
    Class to provide processing for the leaf blocks.
    """

    # pylint: disable=too-many-arguments
    @staticmethod
    def parse_paragraph(
        parser_state: ParserState,
        position_marker: PositionMarker,
        extracted_whitespace: str,
        block_quote_data: BlockQuoteData,
        text_removed_by_container: Optional[str],
        original_line: str,
    ) -> List[MarkdownToken]:
        """
        Handle the parsing of a paragraph.
        """
        POGGER.debug(">>text_removed_by_container>>:$:<<", text_removed_by_container)
        POGGER.debug(">>extracted_whitespace>>:$:<<", extracted_whitespace)
        POGGER.debug("position_marker.text_to_parse=:$:", position_marker.text_to_parse)
        POGGER.debug("position_marker.index_number=:$:", position_marker.index_number)
        POGGER.debug("position_marker.index_indent=:$:", position_marker.index_indent)

        if parser_state.no_para_start_if_empty and position_marker.index_number >= len(
            position_marker.text_to_parse
        ):
            POGGER.debug("Escaping paragraph due to empty w/ blank")
            return [
                BlankLineMarkdownToken(
                    extracted_whitespace, position_marker, len(extracted_whitespace)
                )
            ]

        POGGER.debug(
            "parse_paragraph>block_quote_data.stack_count>$>block_quote_data.current_count>$<",
            block_quote_data.stack_count,
            block_quote_data.current_count,
        )

        container_index, adjusted_whitespace_length = (
            parser_state.find_last_container_on_stack(),
            0,
        )
        if container_index > 0:
            adjusted_whitespace_length = (
                LeafBlockProcessorParagraph.__adjust_paragraph_for_containers(
                    parser_state,
                    container_index,
                    extracted_whitespace,
                    adjusted_whitespace_length,
                )
            )

        POGGER.debug("extracted_whitespace=:$:", extracted_whitespace)
        POGGER.debug("adjusted_whitespace_length=:$:", adjusted_whitespace_length)
        (
            new_tokens,
            extracted_whitespace,
            did_add_paragraph_token,
        ) = LeafBlockProcessorParagraph.__handle_paragraph_prep(
            parser_state,
            block_quote_data,
            position_marker,
            extracted_whitespace,
            original_line,
        )
        POGGER.debug("new_tokens=:$:", new_tokens)
        POGGER.debug("extracted_whitespace=:$:", extracted_whitespace)
        POGGER.debug("did_add_paragraph_token=:$:", did_add_paragraph_token)
        POGGER.debug(
            "position_marker.text_to_parse=:$:",
            position_marker.text_to_parse[position_marker.index_number :],
        )

        adjusted_index = position_marker.index_number
        if did_add_paragraph_token and ParserHelper.is_character_at_index_one_of(
            position_marker.text_to_parse, adjusted_index, Constants.ascii_whitespace
        ):
            POGGER.debug(
                "position_marker.text_to_parse=:$:", position_marker.text_to_parse
            )
            POGGER.debug("adjusted_index=:$:", adjusted_index)
            adjusted_index, extracted_whitespace = (
                ParserHelper.extract_ascii_whitespace_verified(
                    position_marker.text_to_parse, adjusted_index
                )
            )
            POGGER.debug("adjusted_index=:$:", adjusted_index)
            POGGER.debug("extracted_whitespace=:$:", extracted_whitespace)

        new_tokens.append(
            LeafBlockProcessorParagraph.__parse_paragraph_create_text_token(
                parser_state,
                position_marker,
                adjusted_index,
                extracted_whitespace,
                original_line,
            )
        )
        return new_tokens

    # pylint: enable=too-many-arguments

    @staticmethod
    def __parse_paragraph_create_text_token(
        parser_state: ParserState,
        position_marker: PositionMarker,
        adjusted_index: int,
        extracted_whitespace: str,
        original_line: str,
    ) -> TextMarkdownToken:
        text_to_parse = position_marker.text_to_parse[adjusted_index:]
        POGGER.debug("--add-text-token--")
        POGGER.debug("text_to_parse=:$:", text_to_parse)
        POGGER.debug("extracted_whitespace=:$:", extracted_whitespace)
        POGGER.debug("original_line=:$:", original_line)

        (
            corrected_tab_text,
            corrected_extracted_whitespace,
        ) = LeafBlockProcessorParagraph.__calculate_corrected_tab_text(
            parser_state,
            original_line,
            text_to_parse,
            extracted_whitespace,
            adjusted_index,
        )
        POGGER.debug("corrected_tab_text=:$:", corrected_tab_text)
        POGGER.debug(
            "corrected_extracted_whitespace=:$:", corrected_extracted_whitespace
        )

        return TextMarkdownToken(
            text_to_parse,
            corrected_extracted_whitespace,
            position_marker=position_marker,
            tabified_text=corrected_tab_text,
        )

    @staticmethod
    def __calculate_corrected_tab_text(
        parser_state: ParserState,
        original_line: str,
        text_to_parse: str,
        extracted_whitespace: str,
        adjusted_index: int,
    ) -> Tuple[str, str]:
        corrected_tab_text = ""
        if ParserHelper.tab_character in original_line:
            (
                corrected_extracted_whitespace,
                original_line,
                checked_whitespace_for_tab,
                is_block_quote_container,
            ) = LeafBlockProcessorParagraph.__calculate_corrected_tab_text_prefix(
                parser_state, extracted_whitespace, text_to_parse, original_line
            )
            POGGER.debug("checked_whitespace_for_tab=:$:", checked_whitespace_for_tab)
            POGGER.debug("is_block_quote_container=:$:", is_block_quote_container)

            if original_line.endswith(text_to_parse):
                corrected_index = len(original_line) - len(text_to_parse)
                assert corrected_index >= 0, "Index cannot be negative."
                corrected_tab_text = original_line[corrected_index:]
                assert (
                    corrected_tab_text == text_to_parse
                ), "Constructed string must equal provided text."
            else:
                POGGER.debug("original_line=:$:", original_line)
                POGGER.debug("text_to_parse=:$:", text_to_parse)
                initial_offset = (
                    adjusted_index
                    if checked_whitespace_for_tab and not is_block_quote_container
                    else 0
                )
                POGGER.debug("initial_offset=:$:", initial_offset)
                corrected_tab_text, _, _ = TabHelper.find_detabify_string_verified(
                    original_line,
                    text_to_parse,
                    use_proper_traverse=True,
                    initial_offset=initial_offset,
                )
                POGGER.debug("adj_text_to_parse=:$:", corrected_tab_text)
                corrected_index = 0
        else:
            corrected_extracted_whitespace = extracted_whitespace
        return corrected_tab_text, corrected_extracted_whitespace

    # pylint: disable=too-many-locals
    @staticmethod
    def __calculate_corrected_tab_text_prefix(
        parser_state: ParserState,
        extracted_whitespace: str,
        text_to_parse: str,
        original_line: str,
    ) -> Tuple[str, str, bool, bool]:
        POGGER.debug("extracted_whitespace=:$:", extracted_whitespace)
        split_tab_with_block_quote_suffix = True
        checked_whitespace_for_tab = False
        is_block_quote_container = False
        if extracted_whitespace:
            first_non_whitespace_character = text_to_parse[0]
            first_non_whitespace_character_index = original_line.find(
                first_non_whitespace_character
            )
            corrected_extracted_whitespace = original_line[
                :first_non_whitespace_character_index
            ]
            POGGER.debug(
                "corrected_extracted_whitespace=:$:", corrected_extracted_whitespace
            )
            last_container_index = parser_state.find_last_container_on_stack()
            last_container_token = parser_state.token_stack[last_container_index]
            is_block_quote_container = last_container_token.is_block_quote
            (
                corrected_prefix,
                corrected_suffix,
                split_tab,
                split_tab_with_block_quote_suffix,
            ) = TabHelper.match_tabbed_whitespace(
                extracted_whitespace, corrected_extracted_whitespace
            )
            checked_whitespace_for_tab = True
            POGGER.debug("split_tab=:$:", split_tab)
            POGGER.debug(
                "split_tab_with_block_quote_suffix=:$:",
                split_tab_with_block_quote_suffix,
            )
            POGGER.debug("extracted_whitespace=:$:", extracted_whitespace)
            if split_tab:
                if split_tab_with_block_quote_suffix:
                    TabHelper.adjust_block_quote_indent_for_tab(parser_state)
                else:
                    alternate_leading_space = (
                        corrected_prefix
                        if corrected_prefix and "\t" in corrected_prefix
                        else None
                    )
                    TabHelper.adjust_block_quote_indent_for_tab(
                        parser_state,
                        corrected_prefix + corrected_suffix,
                        original_line=original_line,
                        alternate_list_leading_space=alternate_leading_space,
                    )

            corrected_extracted_whitespace = corrected_suffix
            original_line = original_line[first_non_whitespace_character_index:]
        else:
            corrected_extracted_whitespace = extracted_whitespace
        return (
            corrected_extracted_whitespace,
            original_line,
            checked_whitespace_for_tab,
            is_block_quote_container,
        )

    # pylint: enable=too-many-locals

    @staticmethod
    def __adjust_paragraph_for_containers(
        parser_state: ParserState,
        container_index: int,
        extracted_whitespace: str,
        adjusted_whitespace_length: int,
    ) -> int:
        if not parser_state.token_stack[container_index].is_block_quote:
            top_list_token = cast(
                ListStackToken, parser_state.token_stack[container_index]
            )
            POGGER.debug(">>list-owners>>$", top_list_token)
            adjusted_whitespace_length = (
                LeafBlockProcessorParagraph.__adjust_paragraph_for_list(
                    top_list_token, extracted_whitespace
                )
            )
        POGGER.debug(">>adjusted_whitespace_length>>$", adjusted_whitespace_length)
        return adjusted_whitespace_length

    @staticmethod
    def __adjust_paragraph_for_list(
        top_list_token: ListStackToken, extracted_whitespace: str
    ) -> int:
        ex_ws_length = len(extracted_whitespace)
        POGGER.debug(">>owners-indent>>$", top_list_token.indent_level)
        POGGER.debug(">>ws_before_marker>>$", top_list_token.ws_before_marker)
        POGGER.debug(">>ws_after_marker>>$", top_list_token.ws_after_marker)
        POGGER.debug(">>last_new_list_token>>$", top_list_token.last_new_list_token)
        POGGER.debug(">>extracted_whitespace>>$", ex_ws_length)

        dominant_indent, original_list_indent, indent_delta = (
            (
                top_list_token.last_new_list_token.indent_level
                if top_list_token.last_new_list_token
                else top_list_token.indent_level
            ),
            top_list_token.indent_level - 2,
            (
                top_list_token.ws_after_marker - 1
                if top_list_token.ws_after_marker > 1
                else 0
            ),
        )
        POGGER.debug(">>dominant_indent>>$>>", dominant_indent)
        original_text_indent = (
            ex_ws_length
            + top_list_token.indent_level
            - top_list_token.ws_before_marker
            - indent_delta
        )
        POGGER.debug(">>original_list_indent>>$>>", original_list_indent)
        POGGER.debug(">>original_text_indent>$>>", original_text_indent)
        return (
            dominant_indent - original_text_indent
            if dominant_indent > original_text_indent >= 4
            else 0
        )

    @staticmethod
    def __handle_paragraph_prep_block_reduce(
        parser_state: ParserState,
        position_marker: PositionMarker,
        extracted_whitespace: str,
    ) -> List[MarkdownToken]:
        new_tokens, _ = parser_state.close_open_blocks_fn(
            parser_state,
            only_these_blocks=[BlockQuoteStackToken],
            include_block_quotes=True,
        )
        _ = (position_marker, extracted_whitespace)
        # if new_tokens:
        # assert parser_state.token_stack[-1].is_list, "Must be within list block."
        # search_index = len(parser_state.token_stack)
        # leading_space_length = (
        #     len(extracted_whitespace) + position_marker.index_indent
        # )
        # did_once = False
        # while parser_state.token_stack[search_index - 1].is_list:
        #     list_token = cast(
        #         ListStackToken, parser_state.token_stack[search_index - 1]
        #     )
        #     if list_token.indent_level <= leading_space_length:
        #         break
        #     search_index -= 1
        #     did_once = True
        # if did_once:
        #     # POGGER.debug("lsl $", parser_state.token_stack[search_index])
        #     end_token = cast(EndMarkdownToken, new_tokens[-1])
        #     end_token.set_extra_end_data(None)

        #     (
        #         container_level_tokens,
        #         _,
        #     ) = parser_state.close_open_blocks_fn(
        #         parser_state,
        #         until_this_index=search_index,
        #         include_lists=True,
        #         caller_can_handle_requeue=False,
        #         requeue_reset=True,
        #     )
        #     new_tokens.extend(container_level_tokens)
        return new_tokens

    @staticmethod
    def __handle_paragraph_prep(
        parser_state: ParserState,
        block_quote_data: BlockQuoteData,
        position_marker: PositionMarker,
        extracted_whitespace: str,
        original_line: str,
    ) -> Tuple[List[MarkdownToken], str, bool]:
        # In cases where the list ended on the same line as we are processing, the
        # container tokens will not yet be added to the token_document.  As such,
        # make sure to construct a "proper" list that takes those into account
        # before checking to see if this is an issue.
        adjusted_document = parser_state.token_document[:]
        assert (
            parser_state.same_line_container_tokens is not None
        ), "Should have some tokens."
        adjusted_document.extend(parser_state.same_line_container_tokens)
        did_add_paragraph_token = False

        if (
            len(adjusted_document) >= 2
            and adjusted_document[-1].is_blank_line
            and adjusted_document[-2].is_any_list_token
        ):
            (
                _,
                last_list_index,
            ) = LeafBlockProcessorParagraph.verify_list_in_process(parser_state)
            new_tokens, _ = parser_state.close_open_blocks_fn(
                parser_state, until_this_index=last_list_index
            )
        elif block_quote_data.stack_count != 0 and block_quote_data.current_count == 0:
            new_tokens = (
                LeafBlockProcessorParagraph.__handle_paragraph_prep_block_reduce(
                    parser_state, position_marker, extracted_whitespace
                )
            )
        else:
            new_tokens = []

        if not parser_state.token_stack[-1].is_paragraph:
            if ParserHelper.tab_character in original_line:
                extracted_whitespace = (
                    LeafBlockProcessorParagraph.__paragraph_prep_whitespace_with_tab(
                        parser_state,
                        position_marker,
                        original_line,
                        extracted_whitespace,
                    )
                )

            new_paragraph_token = ParagraphMarkdownToken(
                extracted_whitespace, position_marker
            )
            parser_state.token_stack.append(ParagraphStackToken(new_paragraph_token))
            new_tokens.append(new_paragraph_token)
            extracted_whitespace = ""
            did_add_paragraph_token = True
        return new_tokens, extracted_whitespace, did_add_paragraph_token

    @staticmethod
    def __paragraph_prep_whitespace_with_tab(
        parser_state: ParserState,
        position_marker: PositionMarker,
        original_line: str,
        extracted_whitespace: str,
    ) -> str:
        POGGER.debug(">>text_to_parse>>$>>", position_marker.text_to_parse)
        POGGER.debug(">>index_number>>$>>", position_marker.index_number)

        POGGER.debug(">>original_line>:$:<", original_line)
        POGGER.debug(
            ">>position_marker.text_to_parse[position_marker.index_number:]>:$:<",
            position_marker.text_to_parse[position_marker.index_number :],
        )
        (
            _,
            _,
            rest_of_string_index,
        ) = TabHelper.find_detabify_string(
            original_line,
            position_marker.text_to_parse[position_marker.index_number :],
            use_proper_traverse=True,
        )
        POGGER.debug(">>rest_of_string_index>>$>>", rest_of_string_index)
        prefix = original_line[:rest_of_string_index]
        if prefix and ParserHelper.tab_character in prefix:
            POGGER.debug(">>extracted_whitespace>:$:<", extracted_whitespace)
            POGGER.debug(">>prefix>:$:<", prefix)
            (
                corrected_prefix,
                extracted_whitespace,
                split_tab,
                split_tab_with_block_quote_suffix,
            ) = TabHelper.match_tabbed_whitespace(extracted_whitespace, prefix)
            POGGER.debug(">>corrected_prefix>:$:<", corrected_prefix)
            POGGER.debug(">>corrected_suffix>:$:<", extracted_whitespace)
            POGGER.debug(">>split_tab>>$>>", split_tab)
            if split_tab:
                if split_tab_with_block_quote_suffix:
                    TabHelper.adjust_block_quote_indent_for_tab(parser_state)
                else:
                    alternate_leading_space = (
                        corrected_prefix
                        if corrected_prefix and "\t" in corrected_prefix
                        else None
                    )
                    TabHelper.adjust_block_quote_indent_for_tab(
                        parser_state,
                        corrected_prefix + extracted_whitespace,
                        original_line=original_line,
                        alternate_list_leading_space=alternate_leading_space,
                    )
        return extracted_whitespace

    @staticmethod
    def check_for_list_in_process(parser_state: ParserState) -> Tuple[bool, int]:
        """
        From the end of the stack, check to see if there is already a list in progress.
        """

        stack_index = len(parser_state.token_stack) - 1
        while stack_index >= 0 and not parser_state.token_stack[stack_index].is_list:
            stack_index -= 1
        return stack_index >= 0, stack_index

    @staticmethod
    def verify_list_in_process(parser_state: ParserState) -> Tuple[bool, int]:
        """
        From the end of the stack, verify that there is already a list in progress.
        """
        did_find_list, stack_index = (
            LeafBlockProcessorParagraph.check_for_list_in_process(parser_state)
        )
        assert did_find_list, "List must exist on the stack."
        return did_find_list, stack_index
