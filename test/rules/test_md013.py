"""
Module to provide tests related to the MD013 rule.
"""

import os
from test.markdown_scanner import MarkdownScanner
from test.rules.utils import execute_query_configuration_test, pluginQueryConfigTest

import pytest

# pylint: disable=too-many-lines


@pytest.mark.rules
def test_md013_bad_configuration_line_length() -> None:
    """
    Test to verify that a configuration error is thrown when supplying the
    line_length value with a string that is not an integer.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_path = os.path.join(
        "test", "resources", "rules", "md013", "good_small_line.md"
    )
    supplied_arguments = [
        "--set",
        "plugins.md013.line_length=not-integer",
        "--strict-config",
        "scan",
        source_path,
    ]

    expected_return_code = 1
    expected_output = ""
    expected_error = (
        "BadPluginError encountered while configuring plugins:\n"
        + "The value for property 'plugins.md013.line_length' must be of type 'int'."
    )

    # Act
    execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


@pytest.mark.rules
def test_md013_bad_configuration_line_length_zero() -> None:
    """
    Test to verify that a configuration error is thrown when supplying the
    line_length value with an integer that is 0.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_path = os.path.join(
        "test", "resources", "rules", "md013", "good_small_line.md"
    )
    supplied_arguments = [
        "--set",
        "plugins.md013.line_length=$#0",
        "--strict-config",
        "scan",
        source_path,
    ]

    expected_return_code = 1
    expected_output = ""
    expected_error = (
        "BadPluginError encountered while configuring plugins:\n"
        + "The value for property 'plugins.md013.line_length' is not valid: Allowable values are any integer greater than 0."
    )

    # Act
    execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


@pytest.mark.rules
def test_md013_bad_configuration_heading_line_length() -> None:
    """
    Test to verify that a configuration error is thrown when supplying the
    heading_line_length value with a string that is not an integer.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_path = os.path.join(
        "test", "resources", "rules", "md013", "good_small_line.md"
    )
    supplied_arguments = [
        "--set",
        "plugins.md013.heading_line_length=not-integer",
        "--strict-config",
        "scan",
        source_path,
    ]

    expected_return_code = 1
    expected_output = ""
    expected_error = (
        "BadPluginError encountered while configuring plugins:\n"
        + "The value for property 'plugins.md013.heading_line_length' must be of type 'int'."
    )

    # Act
    execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


@pytest.mark.rules
def test_md013_bad_configuration_headings_active() -> None:
    """
    Test to verify that a configuration error is thrown when supplying the
    headings value with a string that is not a boolean.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_path = os.path.join(
        "test", "resources", "rules", "md013", "good_small_line.md"
    )
    supplied_arguments = [
        "--set",
        "plugins.md013.headings=not-integer",
        "--strict-config",
        "scan",
        source_path,
    ]

    expected_return_code = 1
    expected_output = ""
    expected_error = (
        "BadPluginError encountered while configuring plugins:\n"
        + "The value for property 'plugins.md013.headings' must be of type 'bool'."
    )

    # Act
    execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


@pytest.mark.rules
def test_md013_bad_configuration_code_block_line_length() -> None:
    """
    Test to verify that a configuration error is thrown when supplying the
    code_block_line_length value with a string that is not an integer.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_path = os.path.join(
        "test", "resources", "rules", "md013", "good_small_line.md"
    )
    supplied_arguments = [
        "--set",
        "plugins.md013.code_block_line_length=not-integer",
        "--strict-config",
        "scan",
        source_path,
    ]

    expected_return_code = 1
    expected_output = ""
    expected_error = (
        "BadPluginError encountered while configuring plugins:\n"
        + "The value for property 'plugins.md013.code_block_line_length' must be of type 'int'."
    )

    # Act
    execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


@pytest.mark.rules
def test_md013_bad_configuration_code_blocks_active() -> None:
    """
    Test to verify that a configuration error is thrown when supplying the
    code_blocks value with a string that is not a boolean.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_path = os.path.join(
        "test", "resources", "rules", "md013", "good_small_line.md"
    )
    supplied_arguments = [
        "--set",
        "plugins.md013.code_blocks=not-integer",
        "--strict-config",
        "scan",
        source_path,
    ]

    expected_return_code = 1
    expected_output = ""
    expected_error = (
        "BadPluginError encountered while configuring plugins:\n"
        + "The value for property 'plugins.md013.code_blocks' must be of type 'bool'."
    )

    # Act
    execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


@pytest.mark.rules
def test_md013_bad_configuration_strict_mode() -> None:
    """
    Test to verify that a configuration error is thrown when supplying the
    strict value with a string that is not a boolean.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_path = os.path.join(
        "test", "resources", "rules", "md013", "good_small_line.md"
    )
    supplied_arguments = [
        "--set",
        "plugins.md013.strict=not-integer",
        "--strict-config",
        "scan",
        source_path,
    ]

    expected_return_code = 1
    expected_output = ""
    expected_error = (
        "BadPluginError encountered while configuring plugins:\n"
        + "The value for property 'plugins.md013.strict' must be of type 'bool'."
    )

    # Act
    execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


@pytest.mark.rules
def test_md013_bad_configuration_stern_mode() -> None:
    """
    Test to verify that a configuration error is thrown when supplying the
    stern value with a string that is not a boolean.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_path = os.path.join(
        "test", "resources", "rules", "md013", "good_small_line.md"
    )
    supplied_arguments = [
        "--set",
        "plugins.md013.stern=not-integer",
        "--strict-config",
        "scan",
        source_path,
    ]

    expected_return_code = 1
    expected_output = ""
    expected_error = (
        "BadPluginError encountered while configuring plugins:\n"
        + "The value for property 'plugins.md013.stern' must be of type 'bool'."
    )

    # Act
    execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


@pytest.mark.rules
def test_md013_good_small_line() -> None:
    """
    Test to make sure this rule does not trigger with a document that
    contains a single line with 38 characters.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_path = os.path.join(
        "test", "resources", "rules", "md013", "good_small_line.md"
    )
    supplied_arguments = [
        "scan",
        source_path,
    ]

    expected_return_code = 0
    expected_output = ""
    expected_error = ""

    # Act
    execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


@pytest.mark.rules
def test_md013_good_small_line_with_config() -> None:
    """
    Test to make sure this rule does trigger with a document that
    contains a single line with 38 characters, with configuration
    setting the maximum line length to 25.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_path = os.path.join(
        "test", "resources", "rules", "md013", "good_small_line.md"
    )
    supplied_arguments = [
        "--set",
        "plugins.md013.line_length=$#25",
        "--strict-config",
        "scan",
        source_path,
    ]

    expected_return_code = 1
    expected_output = (
        f"{source_path}:1:1: "
        + "MD013: Line length "
        + "[Expected: 25, Actual: 38] (line-length)"
    )
    expected_error = ""

    # Act
    execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


@pytest.mark.rules
def test_md013_good_medium_line() -> None:
    """
    Test to make sure this rule does not trigger with a document that
    contains a single line with 80 characters.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_path = os.path.join(
        "test", "resources", "rules", "md013", "good_medium_line.md"
    )
    supplied_arguments = [
        "scan",
        source_path,
    ]

    expected_return_code = 0
    expected_output = ""
    expected_error = ""

    # Act
    execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


@pytest.mark.rules
def test_md013_good_medium_line_with_config() -> None:
    """
    Test to make sure this rule does trigger with a document that
    contains a single line with 80 characters with a configured maximum
    line length of 80.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_path = os.path.join(
        "test", "resources", "rules", "md013", "good_medium_line.md"
    )
    supplied_arguments = [
        "--set",
        "plugins.md013.line_length=$#50",
        "--strict-config",
        "scan",
        source_path,
    ]

    expected_return_code = 1
    expected_output = (
        f"{source_path}:1:1: "
        + "MD013: Line length "
        + "[Expected: 50, Actual: 80] (line-length)"
    )
    expected_error = ""

    # Act
    execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


@pytest.mark.rules
def test_md013_good_long_line() -> None:
    """
    Test to make sure this rule does trigger with a document that
    contains a single line with 80 characters.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_path = os.path.join(
        "test", "resources", "rules", "md013", "good_long_line.md"
    )
    supplied_arguments = [
        "scan",
        source_path,
    ]

    expected_return_code = 1
    expected_output = (
        f"{source_path}:1:1: "
        + "MD013: Line length "
        + "[Expected: 80, Actual: 100] (line-length)"
    )
    expected_error = ""

    # Act
    execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


@pytest.mark.rules
def test_md013_good_long_line_with_config() -> None:
    """
    Test to make sure this rule does not trigger with a document that
    contains a single line with 80 characters with a configured maximum
    line length of 110.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_path = os.path.join(
        "test", "resources", "rules", "md013", "good_long_line.md"
    )
    supplied_arguments = [
        "--set",
        "plugins.md013.line_length=$#110",
        "--strict-config",
        "scan",
        source_path,
    ]

    expected_return_code = 0
    expected_output = ""
    expected_error = ""

    # Act
    execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


@pytest.mark.rules
def test_md013_good_medium_line_with_long_last_word() -> None:
    """
    Test to make sure this rule does not trigger with a document that
    contains a single line the crosses the normal 80 character limit
    with a 31 character last "word".
    """

    # Arrange
    scanner = MarkdownScanner()
    source_path = os.path.join(
        "test",
        "resources",
        "rules",
        "md013",
        "good_medium_line_with_very_long_last_word.md",
    )
    supplied_arguments = [
        "scan",
        source_path,
    ]

    expected_return_code = 0
    expected_output = ""
    expected_error = ""

    # Act
    execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


@pytest.mark.rules
def test_md013_good_medium_line_with_long_last_word_with_config_strict() -> None:
    """
    Test to make sure this rule does trigger with a document that
    contains a single line the crosses the normal 80 character limit
    with a 31 character last "word" and strict mode active.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_path = os.path.join(
        "test",
        "resources",
        "rules",
        "md013",
        "good_medium_line_with_very_long_last_word.md",
    )
    supplied_arguments = [
        "--set",
        "plugins.md013.strict=$!True",
        "--strict-config",
        "scan",
        source_path,
    ]

    expected_return_code = 1
    expected_output = (
        f"{source_path}:1:1: "
        + "MD013: Line length "
        + "[Expected: 80, Actual: 102] (line-length)"
    )
    expected_error = ""

    # Act
    execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


@pytest.mark.rules
def test_md013_good_medium_line_with_long_last_word_with_config_stern() -> None:
    """
    Test to make sure this rule does not trigger with a document that
    contains a single line the crosses the normal 80 character limit
    with a 31 character last "word" and stern mode active.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_path = os.path.join(
        "test",
        "resources",
        "rules",
        "md013",
        "good_medium_line_with_very_long_last_word.md",
    )
    supplied_arguments = [
        "--set",
        "plugins.md013.stern=$!True",
        "--strict-config",
        "scan",
        source_path,
    ]

    expected_return_code = 1
    expected_output = (
        f"{source_path}:1:1: "
        + "MD013: Line length "
        + "[Expected: 80, Actual: 102] (line-length)"
    )
    expected_error = ""

    # Act
    execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


@pytest.mark.rules
def test_md013_bad_medium_line_with_long_last_word() -> None:
    """
    Test to make sure this rule does trigger with a document that
    contains a single line with multiple words past the 80 character
    boundary.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_path = os.path.join(
        "test",
        "resources",
        "rules",
        "md013",
        "bad_medium_line_with_very_long_last_word.md",
    )
    supplied_arguments = [
        "scan",
        source_path,
    ]

    expected_return_code = 1
    expected_output = (
        f"{source_path}:1:1: "
        + "MD013: Line length "
        + "[Expected: 80, Actual: 102] (line-length)"
    )
    expected_error = ""

    # Act
    execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


@pytest.mark.rules
def test_md013_bad_medium_line_with_long_last_word_with_config_strict() -> None:
    """
    Test to make sure this rule does trigger with a document that
    contains a single line with multiple words past the 80 character
    boundary and strict mode.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_path = os.path.join(
        "test",
        "resources",
        "rules",
        "md013",
        "bad_medium_line_with_very_long_last_word.md",
    )
    supplied_arguments = [
        "--set",
        "plugins.md013.strict=$!True",
        "--strict-config",
        "scan",
        source_path,
    ]

    expected_return_code = 1
    expected_output = (
        f"{source_path}:1:1: "
        + "MD013: Line length "
        + "[Expected: 80, Actual: 102] (line-length)"
    )
    expected_error = ""

    # Act
    execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


@pytest.mark.rules
def test_md013_bad_medium_line_with_long_last_word_with_config_stern() -> None:
    """
    Test to make sure this rule does trigger with a document that
    contains a single line with multiple words past the 80 character
    boundary and stern mode.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_path = os.path.join(
        "test",
        "resources",
        "rules",
        "md013",
        "bad_medium_line_with_very_long_last_word.md",
    )
    supplied_arguments = [
        "--set",
        "plugins.md013.stern=$!True",
        "--strict-config",
        "scan",
        source_path,
    ]

    expected_return_code = 0
    expected_output = ""
    expected_error = ""

    # Act
    execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


@pytest.mark.rules
def test_md013_bad_paragraph_with_long_line_in_middle() -> None:
    """
    Test to make sure this rule does trigger with a document that
    contains a multiple lines with a very long line in the middle.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_path = os.path.join(
        "test",
        "resources",
        "rules",
        "md013",
        "bad_paragraph_with_long_line_in_middle.md",
    )
    supplied_arguments = [
        "scan",
        source_path,
    ]

    expected_return_code = 1
    expected_output = (
        f"{source_path}:3:1: "
        + "MD013: Line length "
        + "[Expected: 80, Actual: 91] (line-length)"
    )
    expected_error = ""

    # Act
    execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


@pytest.mark.rules
def test_md013_good_fenced_code_block() -> None:
    """
    Test to make sure this rule does not trigger with a document that
    contains a good line within a fenced code block.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_path = os.path.join(
        "test", "resources", "rules", "md013", "good_fenced_code_block.md"
    )
    supplied_arguments = [
        "scan",
        source_path,
    ]

    expected_return_code = 0
    expected_output = ""
    expected_error = ""

    # Act
    execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


@pytest.mark.rules
def test_md013_bad_fenced_code_block() -> None:
    """
    Test to make sure this rule does trigger with a document that
    contains a long line within a fenced code block.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_path = os.path.join(
        "test", "resources", "rules", "md013", "bad_fenced_code_block.md"
    )
    supplied_arguments = [
        "scan",
        source_path,
    ]

    expected_return_code = 1
    expected_output = f"{source_path}:6:1: MD013: Line length [Expected: 80, Actual: 146] (line-length)"
    expected_error = ""

    # Act
    execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


@pytest.mark.rules
def test_md013_bad_fenced_code_block_with_config() -> None:
    """
    Test to make sure this rule does trigger with a document that
    contains a very long line within a fenced code block, even with
    an extended line length for code blocks.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_path = os.path.join(
        "test", "resources", "rules", "md013", "bad_fenced_code_block.md"
    )
    supplied_arguments = [
        "--set",
        "plugins.md013.code_block_line_length=$#100",
        "--strict-config",
        "scan",
        source_path,
    ]

    expected_return_code = 1
    expected_output = f"{source_path}:6:1: MD013: Line length [Expected: 100, Actual: 146] (line-length)"
    expected_error = ""

    # Act
    execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


@pytest.mark.rules
def test_md013_bad_fenced_code_block_with_config_active() -> None:
    """
    Test to make sure this rule does not trigger with a document that
    contains a long line within a fenced code block, but with the
    code_block value turned off.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_path = os.path.join(
        "test", "resources", "rules", "md013", "bad_fenced_code_block.md"
    )
    supplied_arguments = [
        "--set",
        "plugins.md013.code_blocks=$!False",
        "--strict-config",
        "scan",
        source_path,
    ]

    expected_return_code = 0
    expected_output = ""
    expected_error = ""

    # Act
    execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


@pytest.mark.rules
def test_md013_good_indented_code_block() -> None:
    """
    Test to make sure this rule does not trigger with a document that
    contains a long line within an indented code block, but with the
    code_block value turned off.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_path = os.path.join(
        "test", "resources", "rules", "md013", "good_indented_code_block.md"
    )
    supplied_arguments = [
        "scan",
        source_path,
    ]

    expected_return_code = 0
    expected_output = ""
    expected_error = ""

    # Act
    execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


@pytest.mark.rules
def test_md013_bad_indented_code_block() -> None:
    """
    Test to make sure this rule does trigger with a document that
    contains a long line within an indented code block.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_path = os.path.join(
        "test", "resources", "rules", "md013", "bad_indented_code_block.md"
    )
    supplied_arguments = [
        "scan",
        source_path,
    ]

    expected_return_code = 1
    expected_output = f"{source_path}:5:1: MD013: Line length [Expected: 80, Actual: 154] (line-length)"
    expected_error = ""

    # Act
    execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


@pytest.mark.rules
def test_md013_bad_indented_code_block_with_config() -> None:
    """
    Test to make sure this rule does not trigger with a document that
    contains a long line within an indented code block, but with the
    code_block_line_length set to 100.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_path = os.path.join(
        "test", "resources", "rules", "md013", "bad_indented_code_block.md"
    )
    supplied_arguments = [
        "--set",
        "plugins.md013.code_block_line_length=$#100",
        "--strict-config",
        "scan",
        source_path,
    ]

    expected_return_code = 1
    expected_output = f"{source_path}:5:1: MD013: Line length [Expected: 100, Actual: 154] (line-length)"
    expected_error = ""

    # Act
    execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


@pytest.mark.rules
def test_md013_bad_indented_code_block_with_config_active() -> None:
    """
    Test to make sure this rule does not trigger with a document that
    contains a long line within an indented code block, but with the
    code_blocks set to False.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_path = os.path.join(
        "test", "resources", "rules", "md013", "bad_indented_code_block.md"
    )
    supplied_arguments = [
        "--set",
        "plugins.md013.code_blocks=$!False",
        "--strict-config",
        "scan",
        source_path,
    ]

    expected_return_code = 0
    expected_output = ""
    expected_error = ""

    # Act
    execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


@pytest.mark.rules
def test_md013_good_thematic_break() -> None:
    """
    Test to make sure this rule does not trigger with a document that
    contains a normal line within a thematic break.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_path = os.path.join(
        "test", "resources", "rules", "md013", "good_thematic_break.md"
    )
    supplied_arguments = [
        "scan",
        source_path,
    ]

    expected_return_code = 0
    expected_output = ""
    expected_error = ""

    # Act
    execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


@pytest.mark.rules
def test_md013_bad_thematic_break() -> None:
    """
    Test to make sure this rule does trigger with a document that
    contains a long line within a thematic break.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_path = os.path.join(
        "test", "resources", "rules", "md013", "bad_thematic_break.md"
    )
    supplied_arguments = [
        "scan",
        source_path,
    ]

    expected_return_code = 1
    expected_output = f"{source_path}:1:1: MD013: Line length [Expected: 80, Actual: 87] (line-length)"
    expected_error = ""

    # Act
    execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


@pytest.mark.rules
def test_md013_bad_thematic_break_with_config() -> None:
    """
    Test to make sure this rule does not trigger with a document that
    contains a long line within a thematic break, but with a configuration
    to allow the long line.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_path = os.path.join(
        "test", "resources", "rules", "md013", "bad_thematic_break.md"
    )
    supplied_arguments = [
        "--set",
        "plugins.md013.line_length=$#100",
        "--strict-config",
        "scan",
        source_path,
    ]

    expected_return_code = 0
    expected_output = ""
    expected_error = ""

    # Act
    execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


@pytest.mark.rules
def test_md013_good_atx_heading() -> None:
    """
    Test to make sure this rule does not trigger with a document that
    contains a normal line within an Atx Heading.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_path = os.path.join(
        "test", "resources", "rules", "md013", "good_atx_heading.md"
    )
    supplied_arguments = [
        "scan",
        source_path,
    ]

    expected_return_code = 0
    expected_output = ""
    expected_error = ""

    # Act
    execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


@pytest.mark.rules
def test_md013_bad_atx_heading() -> None:
    """
    Test to make sure this rule does trigger with a document that
    contains a long line within an Atx Heading.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_path = os.path.join(
        "test", "resources", "rules", "md013", "bad_atx_heading.md"
    )
    supplied_arguments = [
        "scan",
        source_path,
    ]

    expected_return_code = 1
    expected_output = f"{source_path}:1:1: MD013: Line length [Expected: 80, Actual: 88] (line-length)"
    expected_error = ""

    # Act
    execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


@pytest.mark.rules
def test_md013_bad_atx_heading_with_config() -> None:
    """
    Test to make sure this rule does not trigger with a document that
    contains a long line within an Atx Heading, but with configuration
    to allow it.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_path = os.path.join(
        "test", "resources", "rules", "md013", "bad_atx_heading.md"
    )
    supplied_arguments = [
        "--set",
        "plugins.md013.heading_line_length=$#100",
        "--strict-config",
        "scan",
        source_path,
    ]

    expected_return_code = 0
    expected_output = ""
    expected_error = ""

    # Act
    execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


@pytest.mark.rules
def test_md013_bad_atx_heading_with_config_active() -> None:
    """
    Test to make sure this rule does not trigger with a document that
    contains a long line within an Atx Heading, but with configuration
    to exclude headings.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_path = os.path.join(
        "test", "resources", "rules", "md013", "bad_atx_heading.md"
    )
    supplied_arguments = [
        "--set",
        "plugins.md013.headings=$!False",
        "--strict-config",
        "scan",
        source_path,
    ]

    expected_return_code = 0
    expected_output = ""
    expected_error = ""

    # Act
    execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


@pytest.mark.rules
def test_md013_good_setext_heading() -> None:
    """
    Test to make sure this rule does not trigger with a document that
    contains a normal line within a SetExt Heading.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_path = os.path.join(
        "test", "resources", "rules", "md013", "good_setext_heading.md"
    )
    supplied_arguments = [
        "scan",
        source_path,
    ]

    expected_return_code = 0
    expected_output = ""
    expected_error = ""

    # Act
    execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


@pytest.mark.rules
def test_md013_bad_setext_heading() -> None:
    """
    Test to make sure this rule does trigger with a document that
    contains a long line within a SetExt Heading.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_path = os.path.join(
        "test", "resources", "rules", "md013", "bad_setext_heading.md"
    )
    supplied_arguments = [
        "scan",
        source_path,
    ]

    expected_return_code = 1
    expected_output = f"{source_path}:1:1: MD013: Line length [Expected: 80, Actual: 86] (line-length)"
    expected_error = ""

    # Act
    execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


@pytest.mark.rules
def test_md013_bad_setext_heading_with_config() -> None:
    """
    Test to make sure this rule does not trigger with a document that
    contains a long line within a SetExt Heading, but configuration to
    allow it.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_path = os.path.join(
        "test", "resources", "rules", "md013", "bad_setext_heading.md"
    )
    supplied_arguments = [
        "--set",
        "plugins.md013.heading_line_length=$#100",
        "--strict-config",
        "scan",
        source_path,
    ]

    expected_return_code = 0
    expected_output = ""
    expected_error = ""

    # Act
    execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


@pytest.mark.rules
def test_md013_bad_setext_heading_with_config_active() -> None:
    """
    Test to make sure this rule does not trigger with a document that
    contains a long line within a SetExt Heading, but with headings
    turned off.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_path = os.path.join(
        "test", "resources", "rules", "md013", "bad_setext_heading.md"
    )
    supplied_arguments = [
        "--set",
        "plugins.md013.headings=$!False",
        "--strict-config",
        "scan",
        source_path,
    ]

    expected_return_code = 0
    expected_output = ""
    expected_error = ""

    # Act
    execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


@pytest.mark.rules
def test_md013_good_html_block() -> None:
    """
    Test to make sure this rule does not trigger with a document that
    contains a normal line within a HTML block.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_path = os.path.join(
        "test", "resources", "rules", "md013", "good_html_block.md"
    )
    supplied_arguments = [
        "scan",
        source_path,
    ]

    expected_return_code = 0
    expected_output = ""
    expected_error = ""

    # Act
    execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


@pytest.mark.rules
def test_md013_bad_html_block() -> None:
    """
    Test to make sure this rule does trigger with a document that
    contains a long line within a HTML block.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_path = os.path.join(
        "test", "resources", "rules", "md013", "bad_html_block.md"
    )
    supplied_arguments = [
        "scan",
        "test/resources/rules/md013/bad_html_block.md",
    ]

    expected_return_code = 1
    expected_output = f"{source_path}:2:1: MD013: Line length [Expected: 80, Actual: 89] (line-length)"
    expected_error = ""

    # Act
    execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


@pytest.mark.rules
def test_md013_bad_html_block_with_config() -> None:
    """
    Test to make sure this rule does not trigger with a document that
    contains a long line within a HTML block, but configuration to allow
    it.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_path = os.path.join(
        "test", "resources", "rules", "md013", "bad_html_block.md"
    )
    supplied_arguments = [
        "--set",
        "plugins.md013.line_length=$#100",
        "--strict-config",
        "scan",
        source_path,
    ]

    expected_return_code = 0
    expected_output = ""
    expected_error = ""

    # Act
    execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


def test_md013_query_config() -> None:
    config_test = pluginQueryConfigTest(
        "md013",
        """
  ITEM               DESCRIPTION

  Id                 md013
  Name(s)            line-length
  Short Description  Line length
  Description Url    https://pymarkdown.readthedocs.io/en/latest/plugins/rule_
                     md013.md


  CONFIGURATION ITEM      TYPE     VALUE

  line_length             integer  80
  code_block_line_length  integer  80
  heading_line_length     integer  80
  code_blocks             boolean  True
  headings                boolean  True
  strict                  boolean  False
  stern                   boolean  False
""",
    )
    execute_query_configuration_test(config_test)
