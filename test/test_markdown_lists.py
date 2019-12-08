"""
https://github.github.com/gfm/#lists
"""
from pymarkdown.tokenized_markdown import TokenizedMarkdown

from .utils import assert_if_lists_different


def test_list_items_281():
    """
    Test case 281:  (part 1) Changing the bullet or ordered list delimiter starts a new list:
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    source_markdown = """- foo
- bar
+ baz"""
    expected_tokens = [
        "[block-quote:]",
        "[atx:1:Foo:: ::]",
        "[para:]",
        "[text:bar:]",
        "[text:baz:]",
        "[end-para]",
        "[end-block-quote]",
    ]

    # Act
    actual_tokens = tokenizer.transform(source_markdown)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)

def test_list_items_282():
    """
    Test case 282:  (part 2) Changing the bullet or ordered list delimiter starts a new list:
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    source_markdown = """1. foo
2. bar
3) baz"""
    expected_tokens = [
        "[block-quote:]",
        "[atx:1:Foo:: ::]",
        "[para:]",
        "[text:bar:]",
        "[text:baz:]",
        "[end-para]",
        "[end-block-quote]",
    ]

    # Act
    actual_tokens = tokenizer.transform(source_markdown)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)

def test_list_items_283():
    """
    Test case 283:  In CommonMark, a list can interrupt a paragraph. That is, no blank line is needed to separate a paragraph from a following list:
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    source_markdown = """Foo
- bar
- baz"""
    expected_tokens = [
        "[block-quote:]",
        "[atx:1:Foo:: ::]",
        "[para:]",
        "[text:bar:]",
        "[text:baz:]",
        "[end-para]",
        "[end-block-quote]",
    ]

    # Act
    actual_tokens = tokenizer.transform(source_markdown)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)

def test_list_items_284():
    """
    Test case 284:  In order to solve of unwanted lists in paragraphs with hard-wrapped numerals, we allow only lists starting with 1 to interrupt paragraphs. Thus,
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    source_markdown = """The number of windows in my house is
14.  The number of doors is 6."""
    expected_tokens = [
        "[block-quote:]",
        "[atx:1:Foo:: ::]",
        "[para:]",
        "[text:bar:]",
        "[text:baz:]",
        "[end-para]",
        "[end-block-quote]",
    ]

    # Act
    actual_tokens = tokenizer.transform(source_markdown)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)

def test_list_items_285():
    """
    Test case 285:  We may still get an unintended result in cases like
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    source_markdown = """The number of windows in my house is
1.  The number of doors is 6."""
    expected_tokens = [
        "[block-quote:]",
        "[atx:1:Foo:: ::]",
        "[para:]",
        "[text:bar:]",
        "[text:baz:]",
        "[end-para]",
        "[end-block-quote]",
    ]

    # Act
    actual_tokens = tokenizer.transform(source_markdown)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)

def test_list_items_286():
    """
    Test case 286:  (part 1) There can be any number of blank lines between items:
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    source_markdown = """- foo

- bar


- baz"""
    expected_tokens = [
        "[block-quote:]",
        "[atx:1:Foo:: ::]",
        "[para:]",
        "[text:bar:]",
        "[text:baz:]",
        "[end-para]",
        "[end-block-quote]",
    ]

    # Act
    actual_tokens = tokenizer.transform(source_markdown)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)

def test_list_items_287():
    """
    Test case 287:  (part 2) There can be any number of blank lines between items:
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    source_markdown = """- foo
  - bar
    - baz


      bim"""
    expected_tokens = [
        "[block-quote:]",
        "[atx:1:Foo:: ::]",
        "[para:]",
        "[text:bar:]",
        "[text:baz:]",
        "[end-para]",
        "[end-block-quote]",
    ]

    # Act
    actual_tokens = tokenizer.transform(source_markdown)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)

def test_list_items_288():
    """
    Test case 288:  (part 1) To separate consecutive lists of the same type, or to separate a list from an indented code block that would otherwise be parsed as a subparagraph of the final list item, you can insert a blank HTML comment:
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    source_markdown = """- foo
- bar

<!-- -->

- baz
- bim"""
    expected_tokens = [
        "[block-quote:]",
        "[atx:1:Foo:: ::]",
        "[para:]",
        "[text:bar:]",
        "[text:baz:]",
        "[end-para]",
        "[end-block-quote]",
    ]

    # Act
    actual_tokens = tokenizer.transform(source_markdown)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)

def test_list_items_289():
    """
    Test case 289:  (part 2) To separate consecutive lists of the same type, or to separate a list from an indented code block that would otherwise be parsed as a subparagraph of the final list item, you can insert a blank HTML comment:
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    source_markdown = """-   foo

    notcode

-   foo

<!-- -->

    code"""
    expected_tokens = [
        "[block-quote:]",
        "[atx:1:Foo:: ::]",
        "[para:]",
        "[text:bar:]",
        "[text:baz:]",
        "[end-para]",
        "[end-block-quote]",
    ]

    # Act
    actual_tokens = tokenizer.transform(source_markdown)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)

def test_list_items_290():
    """
    Test case 290:  (part 1) List items need not be indented to the same level. The following list items will be treated as items at the same list level, since none is indented enough to belong to the previous list item:
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    source_markdown = """- a
 - b
  - c
   - d
  - e
 - f
- g"""
    expected_tokens = [
        "[block-quote:]",
        "[atx:1:Foo:: ::]",
        "[para:]",
        "[text:bar:]",
        "[text:baz:]",
        "[end-para]",
        "[end-block-quote]",
    ]

    # Act
    actual_tokens = tokenizer.transform(source_markdown)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)

def test_list_items_291():
    """
    Test case 291:  (part 2) List items need not be indented to the same level. The following list items will be treated as items at the same list level, since none is indented enough to belong to the previous list item:
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    source_markdown = """1. a

  2. b

   3. c"""
    expected_tokens = [
        "[block-quote:]",
        "[atx:1:Foo:: ::]",
        "[para:]",
        "[text:bar:]",
        "[text:baz:]",
        "[end-para]",
        "[end-block-quote]",
    ]

    # Act
    actual_tokens = tokenizer.transform(source_markdown)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)

def test_list_items_292():
    """
    Test case 292:  Note, however, that list items may not be indented more than three spaces. Here - e is treated as a paragraph continuation line, because it is indented more than three spaces:
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    source_markdown = """- a
 - b
  - c
   - d
    - e"""
    expected_tokens = [
        "[block-quote:]",
        "[atx:1:Foo:: ::]",
        "[para:]",
        "[text:bar:]",
        "[text:baz:]",
        "[end-para]",
        "[end-block-quote]",
    ]

    # Act
    actual_tokens = tokenizer.transform(source_markdown)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)

def test_list_items_293():
    """
    Test case 293:  And here, 3. c is treated as in indented code block, because it is indented four spaces and preceded by a blank line.
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    source_markdown = """1. a

  2. b

    3. c"""
    expected_tokens = [
        "[block-quote:]",
        "[atx:1:Foo:: ::]",
        "[para:]",
        "[text:bar:]",
        "[text:baz:]",
        "[end-para]",
        "[end-block-quote]",
    ]

    # Act
    actual_tokens = tokenizer.transform(source_markdown)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)

def test_list_items_294():
    """
    Test case 294:  This is a loose list, because there is a blank line between two of the list items:
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    source_markdown = """- a
- b

- c"""
    expected_tokens = [
        "[block-quote:]",
        "[atx:1:Foo:: ::]",
        "[para:]",
        "[text:bar:]",
        "[text:baz:]",
        "[end-para]",
        "[end-block-quote]",
    ]

    # Act
    actual_tokens = tokenizer.transform(source_markdown)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)

def test_list_items_295():
    """
    Test case 295:  So is this, with a empty second item:
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    source_markdown = """* a
*

* c"""
    expected_tokens = [
        "[block-quote:]",
        "[atx:1:Foo:: ::]",
        "[para:]",
        "[text:bar:]",
        "[text:baz:]",
        "[end-para]",
        "[end-block-quote]",
    ]

    # Act
    actual_tokens = tokenizer.transform(source_markdown)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)

def test_list_items_296():
    """
    Test case 296:  (part 1) These are loose lists, even though there is no space between the items, because one of the items directly contains two block-level elements with a blank line between them:
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    source_markdown = """- a
- b

  c
- d"""
    expected_tokens = [
        "[block-quote:]",
        "[atx:1:Foo:: ::]",
        "[para:]",
        "[text:bar:]",
        "[text:baz:]",
        "[end-para]",
        "[end-block-quote]",
    ]

    # Act
    actual_tokens = tokenizer.transform(source_markdown)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)

def test_list_items_297():
    """
    Test case 297:  (part 2) These are loose lists, even though there is no space between the items, because one of the items directly contains two block-level elements with a blank line between them:
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    source_markdown = """- a
- b

  [ref]: /url
- d"""
    expected_tokens = [
        "[block-quote:]",
        "[atx:1:Foo:: ::]",
        "[para:]",
        "[text:bar:]",
        "[text:baz:]",
        "[end-para]",
        "[end-block-quote]",
    ]

    # Act
    actual_tokens = tokenizer.transform(source_markdown)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)

def test_list_items_298():
    """
    Test case 298:  This is a tight list, because the blank lines are in a code block:
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    source_markdown = """- a
- ```
  b


  ```
- c"""
    expected_tokens = [
        "[block-quote:]",
        "[atx:1:Foo:: ::]",
        "[para:]",
        "[text:bar:]",
        "[text:baz:]",
        "[end-para]",
        "[end-block-quote]",
    ]

    # Act
    actual_tokens = tokenizer.transform(source_markdown)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)

def test_list_items_299():
    """
    Test case 299:  This is a tight list, because the blank line is between two paragraphs of a sublist. So the sublist is loose while the outer list is tight:
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    source_markdown = """- a
  - b

    c
- d"""
    expected_tokens = [
        "[block-quote:]",
        "[atx:1:Foo:: ::]",
        "[para:]",
        "[text:bar:]",
        "[text:baz:]",
        "[end-para]",
        "[end-block-quote]",
    ]

    # Act
    actual_tokens = tokenizer.transform(source_markdown)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)

def test_list_items_300():
    """
    Test case 300:  This is a tight list, because the blank line is inside the block quote:
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    source_markdown = """* a
  > b
  >
* c"""
    expected_tokens = [
        "[block-quote:]",
        "[atx:1:Foo:: ::]",
        "[para:]",
        "[text:bar:]",
        "[text:baz:]",
        "[end-para]",
        "[end-block-quote]",
    ]

    # Act
    actual_tokens = tokenizer.transform(source_markdown)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)

def test_list_items_301():
    """
    Test case 301:  This list is tight, because the consecutive block elements are not separated by blank lines:
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    source_markdown = """- a
  > b
  ```
  c
  ```
- d"""
    expected_tokens = [
        "[block-quote:]",
        "[atx:1:Foo:: ::]",
        "[para:]",
        "[text:bar:]",
        "[text:baz:]",
        "[end-para]",
        "[end-block-quote]",
    ]

    # Act
    actual_tokens = tokenizer.transform(source_markdown)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)

def test_list_items_302():
    """
    Test case 302:  (part 1) A single-paragraph list is tight:
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    source_markdown = """- a"""
    expected_tokens = [
        "[block-quote:]",
        "[atx:1:Foo:: ::]",
        "[para:]",
        "[text:bar:]",
        "[text:baz:]",
        "[end-para]",
        "[end-block-quote]",
    ]

    # Act
    actual_tokens = tokenizer.transform(source_markdown)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)

def test_list_items_303():
    """
    Test case 303:  (part 2) A single-paragraph list is tight:
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    source_markdown = """- a
  - b"""
    expected_tokens = [
        "[block-quote:]",
        "[atx:1:Foo:: ::]",
        "[para:]",
        "[text:bar:]",
        "[text:baz:]",
        "[end-para]",
        "[end-block-quote]",
    ]

    # Act
    actual_tokens = tokenizer.transform(source_markdown)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)

def test_list_items_304():
    """
    Test case 304:  This list is loose, because of the blank line between the two block elements in the list item:
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    source_markdown = """1. ```
   foo
   ```

   bar"""
    expected_tokens = [
        "[block-quote:]",
        "[atx:1:Foo:: ::]",
        "[para:]",
        "[text:bar:]",
        "[text:baz:]",
        "[end-para]",
        "[end-block-quote]",
    ]

    # Act
    actual_tokens = tokenizer.transform(source_markdown)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)

def test_list_items_305():
    """
    Test case 305:  (part 1) Here the outer list is loose, the inner list tight:
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    source_markdown = """* foo
  * bar

  baz"""
    expected_tokens = [
        "[block-quote:]",
        "[atx:1:Foo:: ::]",
        "[para:]",
        "[text:bar:]",
        "[text:baz:]",
        "[end-para]",
        "[end-block-quote]",
    ]

    # Act
    actual_tokens = tokenizer.transform(source_markdown)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)

def test_list_items_306():
    """
    Test case 306:  (part 2) Here the outer list is loose, the inner list tight:
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    source_markdown = """- a
  - b
  - c

- d
  - e
  - f"""
    expected_tokens = [
        "[block-quote:]",
        "[atx:1:Foo:: ::]",
        "[para:]",
        "[text:bar:]",
        "[text:baz:]",
        "[end-para]",
        "[end-block-quote]",
    ]

    # Act
    actual_tokens = tokenizer.transform(source_markdown)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)