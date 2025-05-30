"""
Module to provide processing for the fenced leaf blocks.
"""

import logging
from typing import List, Optional, Tuple, cast

from pymarkdown.block_quotes.block_quote_data import BlockQuoteData
from pymarkdown.container_blocks.container_grab_bag import ContainerGrabBag
from pymarkdown.container_blocks.container_helper import ContainerHelper
from pymarkdown.general.constants import Constants
from pymarkdown.general.parser_helper import ParserHelper
from pymarkdown.general.parser_logger import ParserLogger
from pymarkdown.general.parser_state import ParserState
from pymarkdown.general.position_marker import PositionMarker
from pymarkdown.general.tab_helper import TabHelper
from pymarkdown.inline.inline_backslash_helper import InlineBackslashHelper
from pymarkdown.leaf_blocks.leaf_block_helper import LeafBlockHelper
from pymarkdown.tokens.fenced_code_block_markdown_token import (
    FencedCodeBlockMarkdownToken,
)
from pymarkdown.tokens.list_start_markdown_token import ListStartMarkdownToken
from pymarkdown.tokens.markdown_token import EndMarkdownToken, MarkdownToken
from pymarkdown.tokens.stack_token import (
    FencedCodeBlockStackToken,
    ListStackToken,
    ParagraphStackToken,
    StackToken,
)
from pymarkdown.tokens.text_markdown_token import TextMarkdownToken

POGGER = ParserLogger(logging.getLogger(__name__))

# pylint: disable=too-many-lines


class FencedLeafBlockProcessor:
    """
    Class to provide processing for the fenced leaf blocks.
    """

    __fenced_start_tilde = "~"
    __fenced_start_backtick = "`"
    __fenced_code_block_start_characters = (
        f"{__fenced_start_tilde}{__fenced_start_backtick}"
    )

    # pylint: disable=too-many-arguments
    @staticmethod
    def is_fenced_code_block(
        parser_state: ParserState,
        line_to_parse: str,
        start_index: int,
        extracted_whitespace: str,
        original_line: str,
        index_indent: int,
        skip_whitespace_check: bool = False,
    ) -> Tuple[bool, Optional[int], Optional[int], Optional[int], Optional[int]]:
        """
        Determine if we have the start of a fenced code block.
        """

        after_fence_index: Optional[int] = None
        position_marker = PositionMarker(0, 0, "", index_indent)
        extracted_whitespace = LeafBlockHelper.realize_leading_whitespace(
            parser_state, position_marker, extracted_whitespace, original_line
        )

        if (
            skip_whitespace_check
            or TabHelper.is_length_less_than_or_equal_to(extracted_whitespace, 3)
        ) and ParserHelper.is_character_at_index_one_of(
            line_to_parse,
            start_index,
            FencedLeafBlockProcessor.__fenced_code_block_start_characters,
        ):
            POGGER.debug("ifcb:collected_count>:$:<$<<", line_to_parse, start_index)
            collected_count, new_index = ParserHelper.collect_while_character_verified(
                line_to_parse, start_index, line_to_parse[start_index]
            )
            POGGER.debug(
                "ifcb:collected_count:$, new_index:$", collected_count, new_index
            )
            after_fence_index = new_index
            (
                non_whitespace_index,
                _,
            ) = ParserHelper.extract_ascii_whitespace(line_to_parse, new_index)

            if collected_count >= 3:
                POGGER.debug("ifcb:True")
                POGGER.debug("ifcb:collected_count=$", collected_count)
                POGGER.debug("ifcb:non_whitespace_index=$", non_whitespace_index)
                POGGER.debug("ifcb:after_fence_index=$", after_fence_index)
                return (
                    True,
                    non_whitespace_index,
                    after_fence_index,
                    collected_count,
                    new_index,
                )
        return False, None, None, None, None

    # pylint: enable=too-many-arguments

    # pylint: disable=too-many-arguments
    @staticmethod
    def parse_fenced_code_block(
        parser_state: ParserState,
        position_marker: PositionMarker,
        extracted_whitespace: str,
        original_line: str,
        detabified_original_start_index: int,
        block_quote_data: BlockQuoteData,
        grab_bag: ContainerGrabBag,
    ) -> Tuple[List[MarkdownToken], str]:
        """
        Handle the parsing of a fenced code block
        """

        POGGER.debug(
            "line>>$>>index>>$>>",
            position_marker.text_to_parse,
            position_marker.index_number,
        )
        POGGER.debug(
            "parse_fenced_code_block:extracted_whitespace-->$<--", extracted_whitespace
        )
        new_tokens: List[MarkdownToken] = []
        (
            is_fence_start,
            non_whitespace_index,
            after_fence_index,
            collected_count,
            new_index,
        ) = FencedLeafBlockProcessor.is_fenced_code_block(
            parser_state,
            position_marker.text_to_parse,
            position_marker.index_number,
            extracted_whitespace,
            original_line,
            position_marker.index_indent,
        )
        if is_fence_start and not parser_state.token_stack[-1].is_html_block:
            POGGER.debug("parse_fenced_code_block:fenced")
            assert (
                non_whitespace_index is not None
                and after_fence_index is not None
                and collected_count is not None
                and new_index is not None
            ), "If is_fence_start, all these must be defined."
            if parser_state.token_stack[-1].is_fenced_code_block:
                POGGER.debug("parse_fenced_code_block:check fence end")
                FencedLeafBlockProcessor.__check_for_fenced_end(
                    parser_state,
                    position_marker,
                    collected_count,
                    extracted_whitespace,
                    new_tokens,
                    after_fence_index,
                    original_line,
                    detabified_original_start_index,
                )
            else:
                POGGER.debug("parse_fenced_code_block:check fence start")
                new_tokens = FencedLeafBlockProcessor.__process_fenced_start(
                    parser_state,
                    position_marker,
                    non_whitespace_index,
                    collected_count,
                    extracted_whitespace,
                    original_line,
                    new_index,
                    block_quote_data,
                    after_fence_index,
                    grab_bag,
                )
        elif parser_state.token_stack[-1].is_fenced_code_block:
            POGGER.debug("parse_fenced_code_block:already in")
            extracted_whitespace = (
                FencedLeafBlockProcessor.__parse_fenced_code_block_already_in(
                    parser_state,
                    extracted_whitespace,
                    original_line,
                    position_marker.text_to_parse,
                    grab_bag.indent_used_by_list,
                )
            )
            POGGER.debug("parse_fenced_code_block:already in-->$", extracted_whitespace)
        return new_tokens, extracted_whitespace

    # pylint: enable=too-many-arguments

    @staticmethod
    def __check_for_fenced_end_with_split_tab(
        parser_state: ParserState, position_marker: PositionMarker, original_line: str
    ) -> Tuple[bool, str]:
        reconstructed_line = position_marker.text_to_parse
        was_indented = not parser_state.token_stack[-2].is_document
        if is_bq_start := original_line.startswith(">"):
            indent_prefix: Optional[str] = None
        else:
            indent_prefix = " " * position_marker.index_indent
        (
            _,
            adj_original_index,
            split_tab,
        ) = TabHelper.find_tabified_string(
            original_line,
            reconstructed_line,
            abc=is_bq_start,
            was_indented=was_indented,
            reconstruct_prefix=indent_prefix,
        )
        split_tab_whitespace = original_line[:adj_original_index]

        return split_tab, split_tab_whitespace

    # pylint: disable=too-many-arguments
    @staticmethod
    def __check_for_fenced_end(
        parser_state: ParserState,
        position_marker: PositionMarker,
        collected_count: int,
        extracted_whitespace: str,
        new_tokens: List[MarkdownToken],
        after_fence_index: int,
        original_line: str,
        detabified_original_start_index: int,
    ) -> None:
        # POGGER.debug("pfcb->end")
        # POGGER.debug("extracted_whitespace:$:", extracted_whitespace)
        # POGGER.debug("position_marker.text_to_parse:$:", position_marker.text_to_parse)
        # POGGER.debug(
        #     "len(position_marker.text_to_parse):$:", len(position_marker.text_to_parse)
        # )
        # POGGER.debug("after_fence_index:$:", after_fence_index)
        # POGGER.debug(
        #     "detabified_original_start_index:$:", detabified_original_start_index
        # )

        # POGGER.debug("original_line:$:", original_line)
        only_spaces_after_fence = True
        split_tab = False
        split_tab_whitespace: Optional[str] = None
        if ParserHelper.tab_character in original_line:
            (
                after_fence_index,
                only_spaces_after_fence,
                extracted_whitespace,
                split_tab,
            ) = FencedLeafBlockProcessor.__check_for_fenced_end_with_tab(
                parser_state,
                position_marker,
                original_line,
                detabified_original_start_index,
                collected_count,
                extracted_whitespace,
            )
            if split_tab:
                (
                    split_tab,
                    split_tab_whitespace,
                ) = FencedLeafBlockProcessor.__check_for_fenced_end_with_split_tab(
                    parser_state, position_marker, original_line
                )

        after_fence_and_spaces_index, extracted_spaces = (
            ParserHelper.extract_spaces_verified(
                position_marker.text_to_parse, after_fence_index
            )
        )
        # POGGER.debug("after_fence_and_spaces_index:$:", after_fence_and_spaces_index)

        fenced_token = cast(FencedCodeBlockStackToken, parser_state.token_stack[-1])
        # POGGER.debug("fenced_token.code_fence_character:$:", fenced_token.code_fence_character)
        # POGGER.debug("position_marker.text_to_parse[position_marker.index_number]:$:", position_marker.text_to_parse[position_marker.index_number])
        # POGGER.debug("collected_count:$:", collected_count)
        # POGGER.debug("fenced_token.fence_character_count:$:", fenced_token.fence_character_count)
        # POGGER.debug("after_fence_and_spaces_index:$:", after_fence_and_spaces_index)
        # POGGER.debug("len(position_marker.text_to_parse):$:", len(position_marker.text_to_parse))
        # POGGER.debug("only_spaces_after_fence:$:", only_spaces_after_fence)

        if (
            fenced_token.code_fence_character
            == position_marker.text_to_parse[position_marker.index_number]
            and collected_count >= fenced_token.fence_character_count
            and after_fence_and_spaces_index >= len(position_marker.text_to_parse)
            and only_spaces_after_fence
        ):
            if split_tab:
                TabHelper.adjust_block_quote_indent_for_tab(
                    parser_state, split_tab_whitespace
                )

            new_end_token = parser_state.token_stack[
                -1
            ].generate_close_markdown_token_from_stack_token(
                extracted_whitespace,
                extra_end_data=f"{extracted_spaces}:{collected_count}",
            )

            new_tokens.append(new_end_token)
            del parser_state.token_stack[-1]

    # pylint: enable=too-many-arguments

    # pylint: disable=too-many-arguments, too-many-locals
    @staticmethod
    def __check_for_fenced_end_with_tab(
        parser_state: ParserState,
        position_marker: PositionMarker,
        original_line: str,
        detabified_original_start_index: int,
        collected_count: int,
        extracted_whitespace: str,
    ) -> Tuple[int, bool, str, bool]:
        (
            after_fence_index,
            adj_end,
            fence_string,
        ) = FencedLeafBlockProcessor.__calculate_fenced_vars(
            collected_count, original_line, detabified_original_start_index
        )

        original_fence_string_index = original_line.find(fence_string)
        assert (
            original_fence_string_index != -1
        ), "fence_string must be in original line"
        after_fence_in_original = original_line[
            original_fence_string_index + collected_count :
        ]

        _, after_space_in_original_index = ParserHelper.collect_while_character(
            after_fence_in_original, 0, " "
        )
        only_spaces_after_fence = after_space_in_original_index == len(
            after_fence_in_original
        )

        was_indented = not parser_state.token_stack[-2].is_document
        indent_prefix: Optional[str] = (
            None
            if original_line.startswith(">")
            else " " * position_marker.index_indent
        )

        _, adj_original_index, split_tab = TabHelper.find_tabified_string(
            original_line,
            extracted_whitespace + adj_end,
            was_indented=was_indented,
            reconstruct_prefix=indent_prefix,
        )

        _, new_extracted_whitespace = ParserHelper.extract_spaces_verified(
            original_line, adj_original_index
        )

        return (
            after_fence_index,
            only_spaces_after_fence,
            new_extracted_whitespace,
            split_tab,
        )

    # pylint: enable=too-many-arguments, too-many-locals

    @staticmethod
    def __calculate_fenced_vars(
        collected_count: int, original_line: str, detabified_original_start_index: int
    ) -> Tuple[int, str, str]:
        detabified_original_line = TabHelper.detabify_string(original_line)
        adj_original_line = detabified_original_line[detabified_original_start_index:]

        after_whitespace_index, _ = ParserHelper.extract_spaces_verified(
            adj_original_line, 0
        )
        after_fence_index = after_whitespace_index + collected_count
        adj_end = adj_original_line[after_whitespace_index:]
        fence_string = adj_original_line[after_whitespace_index:after_fence_index]
        assert fence_string in original_line, "fence_string must be in original line"
        return after_fence_index, adj_end, fence_string

    @staticmethod
    def __process_fenced_start_adjust(
        parser_state: ParserState,
        position_marker: PositionMarker,
        new_tokens: List[MarkdownToken],
    ) -> None:
        pre_fenced_block_index = len(parser_state.token_stack) - 2
        if parser_state.token_stack[pre_fenced_block_index].is_list:
            additional_column_delta = (
                cast(
                    ListStackToken, parser_state.token_stack[pre_fenced_block_index]
                ).indent_level
                - position_marker.index_indent
            )
        else:
            additional_column_delta = 0
        fenced_token = cast(FencedCodeBlockMarkdownToken, new_tokens[-1])
        assert fenced_token.is_fenced_code_block
        new_position_marker = PositionMarker(
            line_number=fenced_token.line_number,
            index_number=fenced_token.column_number - 1 + additional_column_delta,
            text_to_parse="",
            index_indent=0,
        )
        new_fenced_token = FencedCodeBlockMarkdownToken(
            fence_character=fenced_token.fence_character,
            fence_count=fenced_token.fence_count,
            extracted_text=fenced_token.extracted_text,
            pre_extracted_text=fenced_token.pre_extracted_text,
            text_after_extracted_text=fenced_token.text_after_extracted_text,
            pre_text_after_extracted_text=fenced_token.pre_text_after_extracted_text,
            extracted_whitespace=fenced_token.extracted_whitespace,
            extracted_whitespace_before_info_string=fenced_token.extracted_whitespace_before_info_string,
            position_marker=new_position_marker,
        )
        fenced_stack_token = parser_state.token_stack[-1]
        fenced_stack_token.reset_matching_markdown_token(new_fenced_token)
        adjusted_token_list = new_tokens[:-1]
        adjusted_token_list.append(new_fenced_token)
        new_tokens.clear()
        new_tokens.extend(adjusted_token_list)

    # pylint: disable=too-many-boolean-expressions
    @staticmethod
    def __process_fenced_start_kludge(
        parser_state: ParserState,
        position_marker: PositionMarker,
        new_tokens: List[MarkdownToken],
    ) -> None:
        if (
            len(parser_state.token_stack) == 3
            and parser_state.token_stack[-2].is_list
            and len(new_tokens) == 4
            and new_tokens[-2].is_block_quote_end
            and new_tokens[-3].is_list_end
            and new_tokens[-4].is_block_quote_end
        ):
            list_end_token = cast(EndMarkdownToken, new_tokens[-3])
            list_start_token = cast(
                ListStartMarkdownToken, list_end_token.start_markdown_token
            )
            assert list_start_token.leading_spaces is not None
            leading_space_split = list_start_token.leading_spaces.split("\n")
            assert len(leading_space_split) >= 2

            # Looks a bit weird, but we need to adjust the second last leading space.
            POGGER.debug("__process_fenced_start>>list_token>>$", list_start_token)
            POGGER.debug(
                "__process_fenced_start_kludge>>list_start_token>>$",
                list_start_token,
            )
            last_leading_space = list_start_token.remove_last_leading_space()
            POGGER.debug(
                "__process_fenced_start_kludge>>list_start_token>>$",
                list_start_token,
            )
            assert last_leading_space is not None
            POGGER.debug(
                "__process_fenced_start_kludge>>list_start_token>>$",
                list_start_token,
            )
            list_start_token.remove_last_leading_space()
            POGGER.debug(
                "__process_fenced_start_kludge>>list_start_token>>$",
                list_start_token,
            )
            POGGER.debug("__process_fenced_start>>list_token>>$", list_start_token)
            list_start_token.add_leading_spaces(" " * position_marker.index_indent)
            list_start_token.add_leading_spaces(last_leading_space)
            POGGER.debug("__process_fenced_start>>list_token>>$", list_start_token)

    # pylint: enable=too-many-boolean-expressions

    # pylint: disable=too-many-arguments
    @staticmethod
    def __process_fenced_start(
        parser_state: ParserState,
        position_marker: PositionMarker,
        non_whitespace_index: int,
        collected_count: int,
        extracted_whitespace: str,
        original_line: str,
        new_index: int,
        block_quote_data: BlockQuoteData,
        after_fence_index: int,
        grab_bag: ContainerGrabBag,
    ) -> List[MarkdownToken]:
        POGGER.debug("pfcb->check")
        new_tokens: List[MarkdownToken] = []
        if (
            position_marker.text_to_parse[position_marker.index_number]
            == FencedLeafBlockProcessor.__fenced_start_tilde
            or FencedLeafBlockProcessor.__fenced_start_backtick
            not in position_marker.text_to_parse[non_whitespace_index:]
        ):
            POGGER.debug("pfcb->start")

            (
                old_top_of_stack,
                new_tokens,
                adjusted_corrected_prefix,
            ) = FencedLeafBlockProcessor.__add_fenced_tokens(
                parser_state,
                position_marker,
                non_whitespace_index,
                collected_count,
                extracted_whitespace,
                original_line,
                new_index,
                block_quote_data,
                after_fence_index,
                grab_bag,
            )

            POGGER.debug("new_tokens-->$<<", new_tokens)
            POGGER.debug("StackToken-->$<<", parser_state.token_stack[-1])
            POGGER.debug(
                "StackToken>start_markdown_token-->$<<",
                parser_state.token_stack[-1].matching_markdown_token,
            )
            FencedLeafBlockProcessor.__process_fenced_start_kludge(
                parser_state, position_marker, new_tokens
            )

            removed_char_length = (
                len(adjusted_corrected_prefix)
                if adjusted_corrected_prefix is not None
                else None
            )
            before_correct_length = len(new_tokens)
            LeafBlockHelper.correct_for_leaf_block_start_in_list(
                parser_state,
                position_marker.index_indent,
                old_top_of_stack,
                new_tokens,
                block_quote_data,
                alt_removed_chars_at_start=removed_char_length,
                original_line=original_line,
            )

            # TODO restructure this so we do not have to do this kludge
            # need to place the correct_for_leaf_block_start_in_list call before
            # we create the fenced token
            POGGER.debug("new_tokens-->$<<", new_tokens)
            if before_correct_length != len(new_tokens):
                FencedLeafBlockProcessor.__process_fenced_start_adjust(
                    parser_state, position_marker, new_tokens
                )
        return new_tokens

    # pylint: enable=too-many-arguments

    @staticmethod
    def __parse_fenced_code_block_already_in(
        parser_state: ParserState,
        extracted_whitespace: str,
        original_line: str,
        line_to_parse: str,
        indent_used_by_list: Optional[str],
    ) -> str:
        fenced_token = cast(FencedCodeBlockStackToken, parser_state.token_stack[-1])
        if fenced_token.whitespace_start_count and extracted_whitespace:
            POGGER.debug("original_line>:$:<", original_line)
            POGGER.debug("extracted_whitespace>:$:<", extracted_whitespace)
            current_whitespace_length = TabHelper.calculate_length(extracted_whitespace)
            POGGER.debug("current_whitespace_length>>$", current_whitespace_length)
            whitespace_left_count = max(
                0,
                current_whitespace_length - fenced_token.whitespace_start_count,
            )
            whitespace_used_count = current_whitespace_length - whitespace_left_count
            POGGER.debug("previous_ws>>$", current_whitespace_length)
            POGGER.debug("whitespace_left>:$:<", whitespace_left_count)
            (
                do_normal_processing,
                removed_whitespace,
                whitespace_padding,
            ) = FencedLeafBlockProcessor.__parse_fenced_code_block_already_in_with_tab(
                parser_state,
                whitespace_used_count,
                whitespace_left_count,
                original_line,
                line_to_parse,
                current_whitespace_length,
                indent_used_by_list,
            )
            if do_normal_processing:
                removed_whitespace = ParserHelper.create_replace_with_nothing_marker(
                    ParserHelper.repeat_string(
                        ParserHelper.space_character,
                        current_whitespace_length - whitespace_left_count,
                    )
                )
                whitespace_padding = ParserHelper.repeat_string(
                    ParserHelper.space_character, whitespace_left_count
                )
            extracted_whitespace = f"{removed_whitespace}{whitespace_padding}"
        POGGER.debug("extracted_whitespace>:$:<", extracted_whitespace)
        return extracted_whitespace

    # pylint: disable=too-many-arguments, too-many-locals
    @staticmethod
    def __parse_fenced_code_block_already_in_with_tab(
        parser_state: ParserState,
        whitespace_used_count: int,
        whitespace_left_count: int,
        original_line: str,
        line_to_parse: str,
        current_whitespace_length: int,
        indent_used_by_list: Optional[str],
    ) -> Tuple[bool, str, str]:
        do_normal_processing = True
        removed_whitespace = ""
        whitespace_padding = ""
        if whitespace_left_count and "\t" in original_line:
            if original_line.startswith("\t\t"):
                whitespace_padding = "\t"
                removed_whitespace = ParserHelper.create_replace_with_nothing_marker(
                    "\t"
                )
                do_normal_processing = False

                last_container_token = parser_state.token_stack[-2]
                assert last_container_token.is_list
                list_stack_token = cast(ListStackToken, last_container_token)
                list_markdown_token = cast(
                    ListStartMarkdownToken, list_stack_token.matching_markdown_token
                )
                POGGER.debug(
                    "__parse_fenced_code_block_already_in_with_tab>>list_markdown_token>>$",
                    list_markdown_token,
                )
                list_markdown_token.remove_last_leading_space()
                POGGER.debug(
                    "__parse_fenced_code_block_already_in_with_tab>>list_markdown_token>>$",
                    list_markdown_token,
                )
            else:
                ex_space, ex_space_index, split_tab = TabHelper.find_tabified_string(
                    original_line,
                    line_to_parse,
                    use_proper_traverse=True,
                    reconstruct_prefix=indent_used_by_list,
                )
                modified_ex_space_index = (
                    ex_space_index + 1 if split_tab else ex_space_index
                )

                (last_good_space_index, _, detabified_ex_space) = (
                    TabHelper.search_for_tabbed_prefix(
                        ex_space, modified_ex_space_index, whitespace_used_count
                    )
                )

                do_normal_processing = len(detabified_ex_space) == whitespace_used_count
                if not do_normal_processing:
                    (
                        removed_whitespace,
                        whitespace_padding,
                    ) = FencedLeafBlockProcessor.__parse_fenced_code_block_already_in_with_tab_whitespace(
                        ex_space,
                        last_good_space_index,
                        detabified_ex_space,
                        whitespace_used_count,
                        current_whitespace_length,
                    )
        return do_normal_processing, removed_whitespace, whitespace_padding

    # pylint: enable=too-many-arguments, too-many-locals

    @staticmethod
    def __parse_fenced_code_block_already_in_with_tab_whitespace(
        ex_space: str,
        last_good_space_index: int,
        detabified_ex_space: str,
        whitespace_used_count: int,
        current_whitespace_length: int,
    ) -> Tuple[str, str]:
        tab_prefix = ex_space[: last_good_space_index - 1]
        split_tab_character = ex_space[last_good_space_index - 1]
        whitespace_left = detabified_ex_space[whitespace_used_count:]

        removed_whitespace = (
            ParserHelper.create_replace_with_nothing_marker(tab_prefix)
            if tab_prefix
            else ""
        )
        removed_whitespace += ParserHelper.create_replacement_markers(
            split_tab_character, whitespace_left
        )
        whitespace_padding = ParserHelper.repeat_string(
            ParserHelper.space_character,
            current_whitespace_length - len(detabified_ex_space),
        )
        return removed_whitespace, whitespace_padding

    # pylint: disable=too-many-arguments, too-many-locals
    @staticmethod
    def __add_fenced_tokens(
        parser_state: ParserState,
        position_marker: PositionMarker,
        non_whitespace_index: int,
        collected_count: int,
        extracted_whitespace: str,
        original_line: str,
        new_index: int,
        block_quote_data: BlockQuoteData,
        after_fence_index: int,
        grab_bag: ContainerGrabBag,
    ) -> Tuple[StackToken, List[MarkdownToken], Optional[str]]:
        (
            line_to_parse,
            non_whitespace_index,
            extracted_whitespace_before_info_string,
            extracted_whitespace,
            split_tab,
            corrected_prefix_length,
            extracted_text,
            text_after_extracted_text,
            split_tab_whitespace,
            adjusted_corrected_prefix,
        ) = FencedLeafBlockProcessor.__add_fenced_tokens_prepare(
            position_marker,
            original_line,
            new_index,
            non_whitespace_index,
            collected_count,
            extracted_whitespace,
            after_fence_index,
        )

        return FencedLeafBlockProcessor.__add_fenced_tokens_create(
            parser_state,
            position_marker,
            extracted_whitespace,
            extracted_whitespace_before_info_string,
            corrected_prefix_length,
            collected_count,
            extracted_text,
            text_after_extracted_text,
            line_to_parse,
            split_tab,
            block_quote_data,
            split_tab_whitespace,
            adjusted_corrected_prefix,
            grab_bag,
        )

    # pylint: enable=too-many-arguments, too-many-locals

    # pylint: disable=too-many-arguments
    @staticmethod
    def __add_fenced_tokens_calc(
        parser_state: ParserState,
        position_marker: PositionMarker,
        split_tab: bool,
        block_quote_data: BlockQuoteData,
        split_tab_whitespace: Optional[str],
        extracted_whitespace: str,
        grab_bag: ContainerGrabBag,
    ) -> Tuple[StackToken, List[MarkdownToken], int, str, Optional[str]]:
        old_top_of_stack = parser_state.token_stack[-1]
        new_tokens, _ = parser_state.close_open_blocks_fn(
            parser_state,
            only_these_blocks=[ParagraphStackToken],
        )

        split_tab, extracted_whitespace, whitespace_prefix = (
            ContainerHelper.reduce_containers_if_required(
                parser_state,
                position_marker,
                block_quote_data,
                new_tokens,
                split_tab,
                extracted_whitespace,
                grab_bag,
            )
        )
        if split_tab:
            TabHelper.adjust_block_quote_indent_for_tab(
                parser_state,
                extracted_whitespace=split_tab_whitespace,
                fenced_switch_enabled=True,
            )
            whitespace_count_delta = -1
        else:
            whitespace_count_delta = 0

        return (
            old_top_of_stack,
            new_tokens,
            whitespace_count_delta,
            extracted_whitespace,
            whitespace_prefix,
        )

    # pylint: enable=too-many-arguments

    # pylint: disable=too-many-locals, too-many-arguments
    @staticmethod
    def __add_fenced_tokens_prepare(
        position_marker: PositionMarker,
        original_line: str,
        new_index: int,
        non_whitespace_index: int,
        collected_count: int,
        extracted_whitespace: str,
        after_fence_index: int,
    ) -> Tuple[
        str,
        int,
        str,
        str,
        bool,
        int,
        str,
        str,
        Optional[str],
        Optional[str],
    ]:
        (
            line_to_parse,
            non_whitespace_index,
            extracted_whitespace_before_info_string,
            extracted_whitespace,
            split_tab,
            corrected_prefix_length,
            split_tab_whitespace,
            adjusted_corrected_prefix,
        ) = FencedLeafBlockProcessor.__add_fenced_tokens_with_tab(
            position_marker,
            original_line,
            new_index,
            non_whitespace_index,
            collected_count,
            extracted_whitespace,
            after_fence_index,
        )

        (
            _,
            proper_end_index,
        ) = ParserHelper.collect_backwards_while_one_of_characters(
            line_to_parse, -1, Constants.ascii_whitespace
        )
        adjusted_string = line_to_parse[:proper_end_index]
        non_whitespace_index = min(non_whitespace_index, len(adjusted_string))

        (
            after_extracted_text_index,
            extracted_text,
        ) = ParserHelper.extract_until_spaces_verified(
            adjusted_string, non_whitespace_index
        )
        return (
            line_to_parse,
            non_whitespace_index,
            extracted_whitespace_before_info_string,
            extracted_whitespace,
            split_tab,
            corrected_prefix_length,
            extracted_text,
            line_to_parse[after_extracted_text_index:],
            split_tab_whitespace,
            adjusted_corrected_prefix,
        )

    # pylint: enable=too-many-locals, too-many-arguments

    # pylint: disable=too-many-arguments, too-many-locals
    @staticmethod
    def __add_fenced_tokens_create(
        parser_state: ParserState,
        position_marker: PositionMarker,
        extracted_whitespace: str,
        extracted_whitespace_before_info_string: str,
        corrected_prefix_length: int,
        collected_count: int,
        extracted_text: str,
        text_after_extracted_text: str,
        line_to_parse: str,
        split_tab: bool,
        block_quote_data: BlockQuoteData,
        split_tab_whitespace: Optional[str],
        adjusted_corrected_prefix: Optional[str],
        grab_bag: ContainerGrabBag,
    ) -> Tuple[StackToken, List[MarkdownToken], Optional[str]]:
        (
            old_top_of_stack,
            new_tokens,
            whitespace_start_count,
            extracted_whitespace,
            whitespace_prefix,
        ) = FencedLeafBlockProcessor.__add_fenced_tokens_calc(
            parser_state,
            position_marker,
            split_tab,
            block_quote_data,
            split_tab_whitespace,
            extracted_whitespace,
            grab_bag,
        )

        pre_extracted_text, pre_text_after_extracted_text = (
            extracted_text,
            text_after_extracted_text,
        )

        extracted_text = InlineBackslashHelper.handle_backslashes(
            parser_state.parse_properties, extracted_text
        )
        text_after_extracted_text = InlineBackslashHelper.handle_backslashes(
            parser_state.parse_properties, text_after_extracted_text
        )

        if pre_extracted_text == extracted_text:
            pre_extracted_text = ""
        if pre_text_after_extracted_text == text_after_extracted_text:
            pre_text_after_extracted_text = ""
        if whitespace_prefix:
            extracted_whitespace = whitespace_prefix + extracted_whitespace

        new_token = FencedCodeBlockMarkdownToken(
            position_marker.text_to_parse[position_marker.index_number],
            collected_count,
            extracted_text,
            pre_extracted_text,
            text_after_extracted_text,
            pre_text_after_extracted_text,
            extracted_whitespace,
            extracted_whitespace_before_info_string,
            position_marker,
        )
        new_tokens.append(new_token)
        whitespace_start_count += (
            TabHelper.calculate_length(split_tab_whitespace, 0)
            if split_tab_whitespace is not None
            else TabHelper.calculate_length(
                extracted_whitespace, corrected_prefix_length
            )
        )
        parser_state.token_stack.append(
            FencedCodeBlockStackToken(
                code_fence_character=line_to_parse[position_marker.index_number],
                fence_character_count=collected_count,
                whitespace_start_count=whitespace_start_count,
                matching_markdown_token=new_token,
            )
        )
        return old_top_of_stack, new_tokens, adjusted_corrected_prefix

    # pylint: enable=too-many-arguments, too-many-locals

    # pylint: disable=too-many-arguments
    @staticmethod
    def __add_fenced_tokens_with_tab(
        position_marker: PositionMarker,
        original_line: str,
        new_index: int,
        non_whitespace_index: int,
        collected_count: int,
        extracted_whitespace: str,
        after_fence_index: int,
    ) -> Tuple[str, int, str, str, bool, int, Optional[str], Optional[str]]:
        split_tab = False
        corrected_prefix_length = 0
        line_to_parse = position_marker.text_to_parse
        split_tab_whitespace: Optional[str] = None
        adjusted_corrected_prefix: Optional[str] = None
        if ParserHelper.tab_character in original_line:
            (
                fence_string,
                adj_original_line,
                split_tab,
                extracted_whitespace,
                corrected_prefix_length,
                split_tab_whitespace,
                adjusted_corrected_prefix,
            ) = FencedLeafBlockProcessor.__add_fenced_tokens_with_tab_calc(
                original_line,
                line_to_parse,
                new_index,
                collected_count,
                after_fence_index,
                extracted_whitespace,
            )

            line_to_parse = adj_original_line
            new_index = line_to_parse.find(fence_string)
            new_index += len(fence_string)

            (
                non_whitespace_index,
                extracted_whitespace_before_info_string,
            ) = ParserHelper.extract_ascii_whitespace_verified(line_to_parse, new_index)
        else:
            (
                _,
                extracted_whitespace_before_info_string,
            ) = ParserHelper.extract_ascii_whitespace_verified(line_to_parse, new_index)
        return (
            line_to_parse,
            non_whitespace_index,
            extracted_whitespace_before_info_string,
            extracted_whitespace,
            split_tab,
            corrected_prefix_length,
            split_tab_whitespace,
            adjusted_corrected_prefix,
        )

    # pylint: enable=too-many-arguments

    # pylint: disable=too-many-arguments, too-many-locals
    @staticmethod
    def __add_fenced_tokens_with_tab_calc(
        original_line: str,
        line_to_parse: str,
        new_index: int,
        collected_count: int,
        after_fence_index: int,
        extracted_whitespace: str,
    ) -> Tuple[str, str, bool, str, int, Optional[str], Optional[str]]:
        fence_string = line_to_parse[new_index - collected_count : new_index]
        split_tab = False
        corrected_prefix_length = 0
        split_tab_whitespace: Optional[str] = None
        adjusted_corrected_prefix: Optional[str] = None

        adj_original_line, _, _ = TabHelper.find_detabify_string(
            original_line, line_to_parse, use_proper_traverse=True
        )

        if adj_original_line is None:
            adj_original_line = (
                FencedLeafBlockProcessor.__add_fenced_tokens_with_tab_calc_prefix(
                    line_to_parse,
                    original_line,
                    new_index,
                    collected_count,
                    after_fence_index,
                )
            )

        fence_string_index = original_line.find(fence_string)
        assert fence_string_index != -1, "fence string must be in original line"
        if prefix := original_line[:fence_string_index]:
            (
                corrected_prefix,
                corrected_suffix,
                split_tab,
                _,
            ) = TabHelper.match_tabbed_whitespace(extracted_whitespace, prefix)
            extracted_whitespace = corrected_suffix
            corrected_prefix_length = len(corrected_prefix)
            if split_tab:
                split_tab_whitespace = corrected_prefix + corrected_suffix
                adjusted_corrected_prefix = corrected_prefix
        return (
            fence_string,
            adj_original_line,
            split_tab,
            extracted_whitespace,
            corrected_prefix_length,
            split_tab_whitespace,
            adjusted_corrected_prefix,
        )

    # pylint: enable=too-many-arguments, too-many-locals

    @staticmethod
    def __add_fenced_tokens_with_tab_calc_prefix(
        line_to_parse: str,
        original_line: str,
        new_index: int,
        collected_count: int,
        after_fence_index: int,
    ) -> str:
        line_suffix = line_to_parse[new_index - collected_count : after_fence_index]
        line_suffix_index = original_line.find(line_suffix)
        assert line_suffix_index != -1, "line_suffix must be in original_line"
        return original_line[line_suffix_index:]

    # pylint: disable=too-many-arguments
    @staticmethod
    def handle_fenced_code_block(
        parser_state: ParserState,
        position_marker: PositionMarker,
        leaf_token_whitespace: str,
        new_tokens: List[MarkdownToken],
        original_line: str,
        detabified_original_start_index: int,
        block_quote_data: BlockQuoteData,
        grab_bag: ContainerGrabBag,
    ) -> bool:
        """
        Take care of the processing for fenced code blocks.
        """
        if (
            parser_state.token_stack[-1].was_link_definition_started
            or parser_state.token_stack[-1].was_table_block_started
        ):
            return False

        POGGER.debug(">>__handle_fenced_code_block>>start")
        POGGER.debug(">>leaf_token_whitespace>:$:<", leaf_token_whitespace)
        (
            fenced_tokens,
            leaf_token_whitespace,
        ) = FencedLeafBlockProcessor.parse_fenced_code_block(
            parser_state,
            position_marker,
            leaf_token_whitespace,
            original_line,
            detabified_original_start_index,
            block_quote_data,
            grab_bag,
        )
        POGGER.debug(">>leaf_token_whitespace>:$:<", leaf_token_whitespace)
        if fenced_tokens:
            new_tokens.extend(fenced_tokens)
            POGGER.debug(">>new_tokens>>$", new_tokens)
        elif parser_state.token_stack[-1].is_fenced_code_block:
            POGGER.debug(">>still in fenced block>:$:<", original_line)
            POGGER.debug(">>leaf_token_whitespace>:$:<", leaf_token_whitespace)
            token_text = position_marker.text_to_parse[position_marker.index_number :]
            if ParserHelper.tab_character in original_line:
                (
                    leaf_token_whitespace,
                    token_text,
                ) = FencedLeafBlockProcessor.__handle_fenced_code_block_with_tab(
                    parser_state,
                    position_marker,
                    original_line,
                    leaf_token_whitespace,
                    token_text,
                )
            new_tokens.append(
                TextMarkdownToken(
                    token_text,
                    leaf_token_whitespace,
                    position_marker=position_marker,
                )
            )
            POGGER.debug(">>new_tokens>>$", new_tokens)
        else:
            return False
        return True

    # pylint: enable=too-many-arguments

    @staticmethod
    def __handle_fenced_code_block_with_tab_and_extracted_whitespace(
        new_extracted_whitespace: str,
        adj_original_index: int,
        whitespace_start_count: int,
        extracted_whitespace: str,
    ) -> str:
        new_index = 0
        POGGER.debug("new_index>:$:<", new_index)
        while new_index < len(new_extracted_whitespace):
            before_count = new_extracted_whitespace[: new_index + 1]
            POGGER.debug("before_count>:$:<", before_count)
            detabified_before_count = TabHelper.detabify_string(
                before_count, adj_original_index
            )
            POGGER.debug("detabified_before_count>:$:<", detabified_before_count)
            detabified_before_count_length = len(detabified_before_count)
            POGGER.debug(
                "detabified_before_count_length>:$:<",
                detabified_before_count_length,
            )
            POGGER.debug("whitespace_start_count>:$:<", whitespace_start_count)
            if detabified_before_count_length >= whitespace_start_count:
                after_count = new_extracted_whitespace[len(before_count) :]
                break
            new_index += 1
            POGGER.debug("new_index>:$:<", new_index)

        POGGER.debug("new_extracted_whitespace>:$:<", new_extracted_whitespace)
        POGGER.debug(
            "detabified_before_count_length>:$:<", detabified_before_count_length
        )
        POGGER.debug("whitespace_start_count>:$:<", whitespace_start_count)
        if detabified_before_count_length < whitespace_start_count:
            assert (
                before_count == new_extracted_whitespace
            ), "If we do not have enough length, before_count must equal new_extracted_whitespace."
            after_count = ""
        POGGER.debug("before_count>:$:<", before_count)
        POGGER.debug("after_count>:$:<", after_count)

        POGGER.debug("new_extracted_whitespace>:$:<", new_extracted_whitespace)
        POGGER.debug("extracted_whitespace>:$:<", extracted_whitespace)
        replacement_string = after_count or ParserHelper.replace_noop_character

        new_extracted_whitespace = ParserHelper.create_replacement_markers(
            extracted_whitespace, replacement_string
        )
        POGGER.debug("new_extracted_whitespace>:$:<", new_extracted_whitespace)
        return new_extracted_whitespace

    @staticmethod
    def __handle_fenced_code_block_with_tab_starts_tab(
        original_line: str, reconstructed_line: str, resolved_leaf_token_whitespace: str
    ) -> Tuple[str, int, bool]:
        adj_original = reconstructed_line
        adj_original_index = original_line.find(reconstructed_line)
        assert adj_original_index != -1, "reconstructed_line must be in original line."
        assert original_line.endswith(
            reconstructed_line
        ), "Reconstructed_line must end the original line to verify it was built properly."
        original_line_prefix = original_line[: -len(reconstructed_line)]
        split_tab = original_line_prefix.endswith(">")

        resolved_leaf_token_whitespace = TabHelper.detabify_string(
            resolved_leaf_token_whitespace, adj_original_index
        )
        return adj_original, adj_original_index, split_tab

    @staticmethod
    def __handle_fenced_code_block_with_tab_not_starts_tab(
        original_line: str,
        reconstructed_line: str,
        position_marker: PositionMarker,
        was_indented: bool,
    ) -> Tuple[str, int, bool, Optional[str]]:
        if is_bq_start := original_line.startswith(">"):
            indent_prefix = None
        else:
            indent_prefix = " " * position_marker.index_indent
        (
            adj_original,
            adj_original_index,
            split_tab,
        ) = TabHelper.find_tabified_string(
            original_line,
            reconstructed_line,
            abc=is_bq_start,
            was_indented=was_indented,
            reconstruct_prefix=indent_prefix,
        )
        split_tab_whitespace: Optional[str] = None
        if split_tab:
            split_tab_whitespace = original_line[:adj_original_index]
            if not is_bq_start:
                adj_original_index += position_marker.index_indent
        return (
            adj_original,
            adj_original_index,
            split_tab,
            split_tab_whitespace,
        )

    @staticmethod
    def __handle_fenced_code_block_with_tab(
        parser_state: ParserState,
        position_marker: PositionMarker,
        original_line: str,
        leaf_token_whitespace: str,
        token_text: str,
    ) -> Tuple[str, str]:
        fenced_stack_token = cast(
            FencedCodeBlockStackToken, parser_state.token_stack[-1]
        )
        whitespace_start_count = fenced_stack_token.whitespace_start_count
        was_indented = not parser_state.token_stack[-2].is_document

        resolved_leaf_token_whitespace = ParserHelper.remove_all_from_text(
            leaf_token_whitespace
        )
        reconstructed_line = resolved_leaf_token_whitespace + token_text
        split_tab_whitespace: Optional[str] = None
        if reconstructed_line[0] == "\t":
            (
                adj_original,
                adj_original_index,
                split_tab,
            ) = FencedLeafBlockProcessor.__handle_fenced_code_block_with_tab_starts_tab(
                original_line, reconstructed_line, resolved_leaf_token_whitespace
            )
            reconstructed_line_has_tab = split_tab
        else:
            (
                adj_original,
                adj_original_index,
                split_tab,
                split_tab_whitespace,
            ) = FencedLeafBlockProcessor.__handle_fenced_code_block_with_tab_not_starts_tab(
                original_line, reconstructed_line, position_marker, was_indented
            )
            reconstructed_line_has_tab = True

        (
            leaf_token_whitespace,
            token_text,
        ) = FencedLeafBlockProcessor.__handle_fenced_code_block_with_tab_whitespace(
            parser_state,
            leaf_token_whitespace,
            adj_original,
            adj_original_index,
            whitespace_start_count,
            reconstructed_line_has_tab,
            split_tab,
            split_tab_whitespace,
        )
        return leaf_token_whitespace, token_text

    # pylint: disable=too-many-arguments
    @staticmethod
    def __handle_fenced_code_block_with_tab_whitespace(
        parser_state: ParserState,
        leaf_token_whitespace: str,
        adj_original: str,
        adj_original_index: int,
        whitespace_start_count: int,
        reconstructed_line_has_tab: bool,
        split_tab: bool,
        split_tab_whitespace: Optional[str],
    ) -> Tuple[str, str]:
        space_end_index, extracted_whitespace = ParserHelper.extract_spaces_verified(
            adj_original, 0
        )
        # assert space_end_index != -1

        # detabified_extracted_whitespace = TabHelper.detabify_string(
        #     extracted_whitespace, adj_original_index
        # )
        # assert detabified_extracted_whitespace == resolved_leaf_token_whitespace

        new_extracted_whitespace = extracted_whitespace
        if new_extracted_whitespace and whitespace_start_count:
            # assert not was_indented, "TOoDO: huh?"
            new_extracted_whitespace = FencedLeafBlockProcessor.__handle_fenced_code_block_with_tab_and_extracted_whitespace(
                new_extracted_whitespace,
                adj_original_index,
                whitespace_start_count,
                extracted_whitespace,
            )

        if reconstructed_line_has_tab:
            leaf_token_whitespace = new_extracted_whitespace
        token_text = adj_original[space_end_index:]
        if split_tab:
            TabHelper.adjust_block_quote_indent_for_tab(
                parser_state, split_tab_whitespace
            )

        return leaf_token_whitespace, token_text

    # pylint: enable=too-many-arguments
