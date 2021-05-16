# Bugs - General

## Priority 1 - Must Solve Before Initial

- command line and configuration documentation

## Priority 2 - Like To Solve Before Initial

- test_md026_good_unordered_list_into_atx_into_paragraph should not need to test
  - what is the effect of changing the ordering of a blank that closes a list so the blank comes last
- MD041 requires metadata
  - implement MD043 at the same time
  - implement MD025 at the same time
- __is_container_end_token, __is_leaf_end_token --> put into markdown_token?
- plugins list, enabled default and current not taking up so much space
- pragma tests need to remove `disable_consistency_checks=True`

- implement missing rules
- yaml support for front-matter
- better format for "plugins info"
- show url for failed rules as option

- track down uses of rehydrate_index in consistency checks and make to have cases to verify that each is updating properly, including multi
  - leading_text_index - verify_line_and... ~715
  - see 213c.  doesn't seem to have enough information to properly reconstruct
  - compare to 213d which does
  - _215, 229gx, 229ga, 229hx, 229ha,
  - test_fenced_code_blocks_098c, _extra_05x, _extra_05a, _extra_06xx, _extra_06xa
  - test_paragraph_extra_j0ea
  - test_paragraph_series_n_bq_t_nl_bq_fb_nl_without_bq

- make sure to generated ordered/unordered tests to make sure both covered
  - every unordered tests should have an ordered counterpart
  - every ordered tests should have an unordered counterpart

- take `__consume_text_for_image_alt_text` and other functions like it and move as much as possible into token classes
  - TransformToGfmListLooseness.__handle_block_quote_start
- switch from bq to list and back again
  - switch from list to bq and back again
  - 270 and check for indent levels after

- LRD + FCB in list/block
  - test_fenced_code_blocks_extra_02a
  - test_fenced_code_blocks_extra_03a
  - test_fenced_code_blocks_extra_06a
- LRD + HTML in list/block
  - test_html_blocks_extra_02x
  - test_html_blocks_extra_02a
  - test_html_blocks_extra_03a
  - test_html_blocks_extra_04a
  - test_html_blocks_extra_05a
  - test_html_blocks_extra_06a
- same as these, but with an extra level of list or block

## Priority 3 - Like To Solve in next 3 m

- [mypy?](https://mypy.readthedocs.io/en/stable/getting_started.html)

- determine which errors to print and which to log
- (performance) debug: search for any cases where adding a call to `is_debug_enabled` would be helpful
- (performance) assert: do as little as possible to ensure better performance
- (performance) else: ??
- (performance) replace MarkdownToken properties like is_block_quote_end with more performant?
- (performance) count_characters_in_text
- (performance) can further eliminate len() calls by looking for places can calculate once and pass to child functions
- (performance) order of "if" conditions in critical areas
- (performance) are all "x and x.blah" requiring the "x" check first? can factor out?
- (performance) ParserHelper functions can be further optimized? i.e. __remove_backspaces_from_text and how combines
- (performance) handle_inline_backslash
- (performance) handle_character_reference

- (maintenance) look for cases where = True or = False, and see if can do an assignment
  easlier i.e. if x: d_a_d = False else: d_a_d = True

- (maintenance) clean up pylint warning suppressions where possible
  - too-many-locals
  - too-many-statements
  - too-many-branches
  - too-many-nested-blocks
  - too-many-lines
  - too-many-instance?

- more tests that include tab characters
- look for places where common access patterns can be used i.e. link_title
  - `= len(parser_state.token_stack`
- HTML and Fenced Blocks and better handling of capturing newlines to avoid counting token height
- cases like 183 where first non-ws character is an inline specifier
  - can this be fixed in a way that does not require the other fix to add
   starting_whitespace after the fact?
- make better use of `index_indent`
- why does `__revert_token_to_normal_text_token` require TextMarkdown.copy instead of `replacement_token = text_token_to_replace.create_copy()`?
- image token handling confusing and non-standard
- fenced code block handling of line/col could be better
- LRD and block quote interaction - process_link_reference_definition - search for XXXXX
- `LOGGER.debug("handle_block_quote_section>>fenced")` and collapse?

## Priority 4 - Like To Solve in next 6 m

- verifying vs validating?
- bqp:check_for_lazy_handling, why exclude tb?
- unify 2 separate calculations in `__pre_list` function
- raise requeue_line_info instead of returning it?  worried about recursion points
- replace calculate_last_line with calculate_deltas with some work?
- is_complete_html_end_tag can be more concise, but worth it?
- modify_end_string. inline?
- is_valid_tag_name refactor using ParserHelper?
  - extract_html_attribute_name and others to use "in" where possible instead of "or"
- __calculate_full_deltas - calc_deltas from ParserHelper?
- __process_inline_text_block - calc_deltas from ParserHelper?
- is_length_less_than_or_equal_to(extracted_whitespace, 3) - calc once at start of leaf block proc?
- is_character_at_index_one_of inside of where? collect function?
- __parse_line_for_leaf_blocks - why calling count_of_block_quotes_on_stack so often?

## Bugs - General - Uncategorized

- None

## Ask talk.commonmark.org

- test_link_reference_definitions_extra_02b vs test_link_reference_definitions_extra_02c

## Bugs - Tabs

- should be able to have tabs and not trigger bad tokens, should be excluded?
- check is_length_less_than_or_equal_to to see if any issues with tabs
  - most likely in conjunction with starting another type of block
- 004
  - tab is consumed as part of list prefix, not recorded anywhere, assumed to be spaces
- variations on 005, mostly wired up for scenario
  - what about tabs with plain icode? different depths?
- effect of lists and blocks with 1 tab and differing amounts of whitespace on followed text i.e. `- \tfoo' should produced a list item with foo, no icb as it would equate to 2 spaces
- 235, 236, 252, 255
  - need to account for the fact that indent may not be all spaces all the time
  - for indented code blocks, starts at the start of the icb, else at the first non-ws

## Features - Extensions

- front matter
- tables
- task list items
- strikethrough
- disallowed raw html
- autolinks extension

## Features - Correctness - Whitespace and Punctuation

- go through each use of extract_whitespace and validate whether it should be e_space or e_whitespace
- scan GFM and ensure Unicode whitespace uses actual Unicode whitespace, not just whitespace
- complete list of Unicode punctuation characters
- Atx headings only consider space, not whitespace?
  - impact to MD018 to MD021?

## Features - Correctness

- go back and see if can replace some of the end token fiddling with start_markdown_token
- go through any case that uses lazy and do un-lazy example
- samples that end without a blank line, and add a blank line?

## Features - Performance

- reduce html_helper functions?
  - i.e. html_helper contains 2 for various elements?
- collect_until_one_of_characters with backslashes?
- rewrite transform to allow it to consume a Markdown file as it goes
- modify parse_blocks_pass to consume lines as it goes, instead of requiring entire string in memory

## document current restrictions

- nested block quotes and nested lists are okay, but not together