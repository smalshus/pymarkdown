"""
Extra tests for three level nesting with un/un.
"""

from test.utils import act_and_assert

import pytest

# pylint: disable=too-many-lines


@pytest.mark.gfm
def test_nested_three_ordered_unordered_block() -> None:
    """
    Verify that a nesting of ordered list, unordered list, block quote works
    properly.
    """

    # Arrange
    source_markdown = """1. + > list
     > item"""
    expected_tokens = [
        "[olist(1,1):.:1:3:]",
        "[ulist(1,4):+::5:   :]",
        "[block-quote(1,6):     :     > \n     > ]",
        "[para(1,8):\n]",
        "[text(1,8):list\nitem::\n]",
        "[end-para:::True]",
        "[end-block-quote:::True]",
        "[end-ulist:::True]",
        "[end-olist:::True]",
    ]
    expected_gfm = """<ol>
<li>
<ul>
<li>
<blockquote>
<p>list
item</p>
</blockquote>
</li>
</ul>
</li>
</ol>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_ordered_nl_unordered_nl_block() -> None:
    """
    Verify that a nesting of ordered list, new list, unordered list, new list, block quote works
    properly.
    """

    # Arrange
    source_markdown = """1.
   +
     > list
     > item"""
    expected_tokens = [
        "[olist(1,1):.:1:3:]",
        "[BLANK(1,3):]",
        "[ulist(2,4):+::5:   :\n]",
        "[BLANK(2,5):]",
        "[block-quote(3,6):     :     > \n     > ]",
        "[para(3,8):\n]",
        "[text(3,8):list\nitem::\n]",
        "[end-para:::True]",
        "[end-block-quote:::True]",
        "[end-ulist:::True]",
        "[end-olist:::True]",
    ]
    expected_gfm = """<ol>
<li>
<ul>
<li>
<blockquote>
<p>list
item</p>
</blockquote>
</li>
</ul>
</li>
</ol>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_ordered_text_nl_unordered_text_nl_block() -> None:
    """
    Verify that a nesting of ordered list, text, new list, unordered list, text, new list, block quote works
    properly.
    """

    # Arrange
    source_markdown = """1. abc
   + def
     > list
     > item"""
    expected_tokens = [
        "[olist(1,1):.:1:3:]",
        "[para(1,4):]",
        "[text(1,4):abc:]",
        "[end-para:::True]",
        "[ulist(2,4):+::5:   :\n]",
        "[para(2,6):]",
        "[text(2,6):def:]",
        "[end-para:::True]",
        "[block-quote(3,6):     :     > \n     > ]",
        "[para(3,8):\n]",
        "[text(3,8):list\nitem::\n]",
        "[end-para:::True]",
        "[end-block-quote:::True]",
        "[end-ulist:::True]",
        "[end-olist:::True]",
    ]
    expected_gfm = """<ol>
<li>abc
<ul>
<li>def
<blockquote>
<p>list
item</p>
</blockquote>
</li>
</ul>
</li>
</ol>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_ordered_unordered_block_skip() -> None:
    """
    Verify that a nesting of ordered list, unordered list, block quote works
    properly.
    """

    # Arrange
    source_markdown = """1. + > list
       item"""
    expected_tokens = [
        "[olist(1,1):.:1:3:]",
        "[ulist(1,4):+::5:   :     \n]",
        "[block-quote(1,6):     :     > \n]",
        "[para(1,8):\n  ]",
        "[text(1,8):list\nitem::\n]",
        "[end-para:::True]",
        "[end-block-quote:::True]",
        "[end-ulist:::True]",
        "[end-olist:::True]",
    ]
    expected_gfm = """<ol>
<li>
<ul>
<li>
<blockquote>
<p>list
item</p>
</blockquote>
</li>
</ul>
</li>
</ol>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_ordered_nl_unordered_nl_block_skip() -> None:
    """
    Verify that a nesting of ordered list, new line, unordered list, new line, block quote works
    properly.
    """

    # Arrange
    source_markdown = """1.
   +
     > list
       item"""
    expected_tokens = [
        "[olist(1,1):.:1:3:]",
        "[BLANK(1,3):]",
        "[ulist(2,4):+::5:   :\n     \n]",
        "[BLANK(2,5):]",
        "[block-quote(3,6):     :     > \n]",
        "[para(3,8):\n  ]",
        "[text(3,8):list\nitem::\n]",
        "[end-para:::True]",
        "[end-block-quote:::True]",
        "[end-ulist:::True]",
        "[end-olist:::True]",
    ]
    expected_gfm = """<ol>
<li>
<ul>
<li>
<blockquote>
<p>list
item</p>
</blockquote>
</li>
</ul>
</li>
</ol>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_ordered_text_nl_unordered_text_nl_block_skip() -> None:
    """
    Verify that a nesting of ordered list, text, newline, unordered list, text, new line, block quote
    with a skipped block quote character works properly.
    """

    # Arrange
    source_markdown = """1. abc
   + def
     > list
       item"""
    expected_tokens = [
        "[olist(1,1):.:1:3:]",
        "[para(1,4):]",
        "[text(1,4):abc:]",
        "[end-para:::True]",
        "[ulist(2,4):+::5:   :\n     \n]",
        "[para(2,6):]",
        "[text(2,6):def:]",
        "[end-para:::True]",
        "[block-quote(3,6):     :     > \n]",
        "[para(3,8):\n  ]",
        "[text(3,8):list\nitem::\n]",
        "[end-para:::True]",
        "[end-block-quote:::True]",
        "[end-ulist:::True]",
        "[end-olist:::True]",
    ]
    expected_gfm = """<ol>
<li>abc
<ul>
<li>def
<blockquote>
<p>list
item</p>
</blockquote>
</li>
</ul>
</li>
</ol>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_ordered_max_unordered_max_block_max() -> None:
    """
    Verify that a nesting of ordered list, unordered list, block quote, with
    the maximum number of spaces allowed, works properly.
    """

    # Arrange
    source_markdown = """   1.    +    > list
              > item"""
    expected_tokens = [
        "[olist(1,4):.:1:9:   ]",
        "[ulist(1,10):+::14:         :]",
        "[block-quote(1,15):              :              > \n              > ]",
        "[para(1,17):\n]",
        "[text(1,17):list\nitem::\n]",
        "[end-para:::True]",
        "[end-block-quote:::True]",
        "[end-ulist:::True]",
        "[end-olist:::True]",
    ]
    expected_gfm = """<ol>
<li>
<ul>
<li>
<blockquote>
<p>list
item</p>
</blockquote>
</li>
</ul>
</li>
</ol>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_ordered_max_unordered_max_block_max_with_li1() -> None:
    """
    Verify that a nesting of ordered list, unordered list, block quote, with
    the maximum number of spaces allowed, works properly, with a list item.
    """

    # Arrange
    source_markdown = """   1.    +    > list
   1.         > item"""
    expected_tokens = [
        "[olist(1,4):.:1:9:   ]",
        "[ulist(1,10):+::14:         ]",
        "[block-quote(1,15):              :              > ]",
        "[para(1,17):]",
        "[text(1,17):list:]",
        "[end-para:::True]",
        "[end-block-quote:::True]",
        "[end-ulist:::True]",
        "[li(2,4):6:   :1]",
        "[icode-block(2,11):    :]",
        "[text(2,11):\a>\a&gt;\a item:    ]",
        "[end-icode-block:::True]",
        "[end-olist:::True]",
    ]
    expected_gfm = """<ol>
<li>
<ul>
<li>
<blockquote>
<p>list</p>
</blockquote>
</li>
</ul>
</li>
<li>
<pre><code>    &gt; item
</code></pre>
</li>
</ol>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_ordered_max_unordered_max_block_max_with_li2() -> None:
    """
    Verify that a nesting of ordered list, unordered list, block quote, with
    the maximum number of spaces allowed, works properly, with a list item.
    """

    # Arrange
    source_markdown = """   1.    +    > list
         +    > item"""
    expected_tokens = [
        "[olist(1,4):.:1:9:   ]",
        "[ulist(1,10):+::14:         :]",
        "[block-quote(1,15):              :              > ]",
        "[para(1,17):]",
        "[text(1,17):list:]",
        "[end-para:::True]",
        "[end-block-quote:::True]",
        "[li(2,10):14:         :]",
        "[block-quote(2,15):              :              > ]",
        "[para(2,17):]",
        "[text(2,17):item:]",
        "[end-para:::True]",
        "[end-block-quote:::True]",
        "[end-ulist:::True]",
        "[end-olist:::True]",
    ]
    expected_gfm = """<ol>
<li>
<ul>
<li>
<blockquote>
<p>list</p>
</blockquote>
</li>
<li>
<blockquote>
<p>item</p>
</blockquote>
</li>
</ul>
</li>
</ol>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_ordered_max_unordered_max_block_max_with_li3() -> None:
    """
    Verify that a nesting of ordered list, unordered list, block quote, with
    the maximum number of spaces allowed, works properly, with a list item.
    """

    # Arrange
    source_markdown = """   1.    +    > list
   1.    +    > item"""
    expected_tokens = [
        "[olist(1,4):.:1:9:   ]",
        "[ulist(1,10):+::14:         ]",
        "[block-quote(1,15):              :              > ]",
        "[para(1,17):]",
        "[text(1,17):list:]",
        "[end-para:::True]",
        "[end-block-quote:::True]",
        "[end-ulist:::True]",
        "[li(2,4):9:   :1]",
        "[ulist(2,10):+::14:         ]",
        "[block-quote(2,15):              :              > ]",
        "[para(2,17):]",
        "[text(2,17):item:]",
        "[end-para:::True]",
        "[end-block-quote:::True]",
        "[end-ulist:::True]",
        "[end-olist:::True]",
    ]
    expected_gfm = """<ol>
<li>
<ul>
<li>
<blockquote>
<p>list</p>
</blockquote>
</li>
</ul>
</li>
<li>
<ul>
<li>
<blockquote>
<p>item</p>
</blockquote>
</li>
</ul>
</li>
</ol>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_ordered_max_unordered_max_block_max_empty() -> None:
    """
    Verify that a nesting of ordered list, unordered list, block quote, with
    the maximum number of spaces allowed, and no text on the first line, works properly.
    """

    # Arrange
    source_markdown = """   1.    +    >
              > item"""
    expected_tokens = [
        "[olist(1,4):.:1:9:   ]",
        "[ulist(1,10):+::14:         :]",
        "[block-quote(1,15):              :              >\n              > ]",
        "[BLANK(1,16):]",
        "[para(2,17):]",
        "[text(2,17):item:]",
        "[end-para:::True]",
        "[end-block-quote:::True]",
        "[end-ulist:::True]",
        "[end-olist:::True]",
    ]
    expected_gfm = """<ol>
<li>
<ul>
<li>
<blockquote>
<p>item</p>
</blockquote>
</li>
</ul>
</li>
</ol>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_ordered_max_unordered_max_block_max_empty_with_li1() -> None:
    """
    Verify that a nesting of ordered list, unordered list, block quote, with
    the maximum number of spaces allowed, and no text on the first line, works properly, with a list item.
    """

    # Arrange
    source_markdown = """   1.    +    >
   1.         > item"""
    expected_tokens = [
        "[olist(1,4):.:1:9:   ]",
        "[ulist(1,10):+::14:         ]",
        "[block-quote(1,15):              :              >]",
        "[BLANK(1,16):]",
        "[end-block-quote:::True]",
        "[end-ulist:::True]",
        "[li(2,4):6:   :1]",
        "[icode-block(2,11):    :]",
        "[text(2,11):\a>\a&gt;\a item:    ]",
        "[end-icode-block:::True]",
        "[end-olist:::True]",
    ]
    expected_gfm = """<ol>
<li>
<ul>
<li>
<blockquote>
</blockquote>
</li>
</ul>
</li>
<li>
<pre><code>    &gt; item
</code></pre>
</li>
</ol>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_ordered_max_unordered_max_block_max_empty_with_li2() -> None:
    """
    Verify that a nesting of ordered list, unordered list, block quote, with
    the maximum number of spaces allowed, and no text on the first line, works properly, with a list item.
    """

    # Arrange
    source_markdown = """   1.    +    >
         +    > item"""
    expected_tokens = [
        "[olist(1,4):.:1:9:   ]",
        "[ulist(1,10):+::14:         :]",
        "[block-quote(1,15):              :              >]",
        "[BLANK(1,16):]",
        "[end-block-quote:::True]",
        "[li(2,10):14:         :]",
        "[block-quote(2,15):              :              > ]",
        "[para(2,17):]",
        "[text(2,17):item:]",
        "[end-para:::True]",
        "[end-block-quote:::True]",
        "[end-ulist:::True]",
        "[end-olist:::True]",
    ]
    expected_gfm = """<ol>
<li>
<ul>
<li>
<blockquote>
</blockquote>
</li>
<li>
<blockquote>
<p>item</p>
</blockquote>
</li>
</ul>
</li>
</ol>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_ordered_max_unordered_max_block_max_empty_with_li3() -> None:
    """
    Verify that a nesting of ordered list, unordered list, block quote, with
    the maximum number of spaces allowed, and no text on the first line, works properly, with a list item.
    """

    # Arrange
    source_markdown = """   1.    +    >
   1.    +    > item"""
    expected_tokens = [
        "[olist(1,4):.:1:9:   ]",
        "[ulist(1,10):+::14:         ]",
        "[block-quote(1,15):              :              >]",
        "[BLANK(1,16):]",
        "[end-block-quote:::True]",
        "[end-ulist:::True]",
        "[li(2,4):9:   :1]",
        "[ulist(2,10):+::14:         ]",
        "[block-quote(2,15):              :              > ]",
        "[para(2,17):]",
        "[text(2,17):item:]",
        "[end-para:::True]",
        "[end-block-quote:::True]",
        "[end-ulist:::True]",
        "[end-olist:::True]",
    ]
    expected_gfm = """<ol>
<li>
<ul>
<li>
<blockquote>
</blockquote>
</li>
</ul>
</li>
<li>
<ul>
<li>
<blockquote>
<p>item</p>
</blockquote>
</li>
</ul>
</li>
</ol>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_ordered_max_unordered_max_block_max_no_bq1() -> None:
    """
    Verify that a nesting of ordered list, unordered list, block quote, with
    the maximum number of spaces allowed, works properly,
    with no block quote characters on the second line.
    """

    # Arrange
    source_markdown = """   1.    +    > list
                item"""
    expected_tokens = [
        "[olist(1,4):.:1:9:   ]",
        "[ulist(1,10):+::14:         :              \n]",
        "[block-quote(1,15):              :              > \n]",
        "[para(1,17):\n  ]",
        "[text(1,17):list\nitem::\n]",
        "[end-para:::True]",
        "[end-block-quote:::True]",
        "[end-ulist:::True]",
        "[end-olist:::True]",
    ]
    expected_gfm = """<ol>
<li>
<ul>
<li>
<blockquote>
<p>list
item</p>
</blockquote>
</li>
</ul>
</li>
</ol>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_ordered_max_unordered_max_block_max_no_bq1_with_li1() -> None:
    """
    Verify that a nesting of ordered list, unordered list, block quote, with
    the maximum number of spaces allowed, works properly,
    with no block quote characters on the second line, with a list item.
    """

    # Arrange
    source_markdown = """   1.    +    > list
   1.           item"""
    expected_tokens = [
        "[olist(1,4):.:1:9:   ]",
        "[ulist(1,10):+::14:         ]",
        "[block-quote(1,15):              :              > ]",
        "[para(1,17):]",
        "[text(1,17):list:]",
        "[end-para:::True]",
        "[end-block-quote:::True]",
        "[end-ulist:::True]",
        "[li(2,4):6:   :1]",
        "[icode-block(2,11):    :]",
        "[text(2,11):item:      ]",
        "[end-icode-block:::True]",
        "[end-olist:::True]",
    ]
    expected_gfm = """<ol>
<li>
<ul>
<li>
<blockquote>
<p>list</p>
</blockquote>
</li>
</ul>
</li>
<li>
<pre><code>      item
</code></pre>
</li>
</ol>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_ordered_max_unordered_max_block_max_no_bq1_with_li2() -> None:
    """
    Verify that a nesting of ordered list, unordered list, block quote, with
    the maximum number of spaces allowed, works properly,
    with no block quote characters on the second line, with a list item.
    """

    # Arrange
    source_markdown = """   1.    +    > list
         +      item"""
    expected_tokens = [
        "[olist(1,4):.:1:9:   ]",
        "[ulist(1,10):+::14:         ]",
        "[block-quote(1,15):              :              > ]",
        "[para(1,17):]",
        "[text(1,17):list:]",
        "[end-para:::True]",
        "[end-block-quote:::True]",
        "[li(2,10):11:         :]",
        "[icode-block(2,16):    :]",
        "[text(2,16):item: ]",
        "[end-icode-block:::True]",
        "[end-ulist:::True]",
        "[end-olist:::True]",
    ]
    expected_gfm = """<ol>
<li>
<ul>
<li>
<blockquote>
<p>list</p>
</blockquote>
</li>
<li>
<pre><code> item
</code></pre>
</li>
</ul>
</li>
</ol>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_ordered_max_unordered_max_block_max_no_bq1_with_li3() -> None:
    """
    Verify that a nesting of ordered list, unordered list, block quote, with
    the maximum number of spaces allowed, works properly,
    with no block quote characters on the second line, with a list item.
    """

    # Arrange
    source_markdown = """   1.    +    > list
   1.    +      item"""
    expected_tokens = [
        "[olist(1,4):.:1:9:   ]",
        "[ulist(1,10):+::14:         ]",
        "[block-quote(1,15):              :              > ]",
        "[para(1,17):]",
        "[text(1,17):list:]",
        "[end-para:::True]",
        "[end-block-quote:::True]",
        "[end-ulist:::True]",
        "[li(2,4):9:   :1]",
        "[ulist(2,10):+::11:         ]",
        "[icode-block(2,16):    :]",
        "[text(2,16):item: ]",
        "[end-icode-block:::True]",
        "[end-ulist:::True]",
        "[end-olist:::True]",
    ]
    expected_gfm = """<ol>
<li>
<ul>
<li>
<blockquote>
<p>list</p>
</blockquote>
</li>
</ul>
</li>
<li>
<ul>
<li>
<pre><code> item
</code></pre>
</li>
</ul>
</li>
</ol>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_ordered_max_unordered_max_block_max_empty_no_bq1() -> None:
    """
    Verify that a nesting of ordered list, unordered list, block quote, with
    the maximum number of spaces allowed, and no text on the first line, works properly,
    with no block quote characters on the second line.
    """

    # Arrange
    source_markdown = """   1.    +    >
                item"""
    expected_tokens = [
        "[olist(1,4):.:1:9:   ]",
        "[ulist(1,10):+::14:         :              ]",
        "[block-quote(1,15):              :              >]",
        "[BLANK(1,16):]",
        "[end-block-quote:::False]",
        "[para(2,17):  ]",
        "[text(2,17):item:]",
        "[end-para:::True]",
        "[end-ulist:::True]",
        "[end-olist:::True]",
    ]
    expected_gfm = """<ol>
<li>
<ul>
<li>
<blockquote>
</blockquote>
item</li>
</ul>
</li>
</ol>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_ordered_max_unordered_max_block_max_empty_no_bq1_with_li1() -> (
    None
):
    """
    Verify that a nesting of ordered list, unordered list, block quote, with
    the maximum number of spaces allowed, and no text on the first line, works properly,
    with no block quote characters on the second line, with a list item.
    """

    # Arrange
    source_markdown = """   1.    +    >
   1.           item"""
    expected_tokens = [
        "[olist(1,4):.:1:9:   ]",
        "[ulist(1,10):+::14:         ]",
        "[block-quote(1,15):              :              >]",
        "[BLANK(1,16):]",
        "[end-block-quote:::True]",
        "[end-ulist:::True]",
        "[li(2,4):6:   :1]",
        "[icode-block(2,11):    :]",
        "[text(2,11):item:      ]",
        "[end-icode-block:::True]",
        "[end-olist:::True]",
    ]
    expected_gfm = """<ol>
<li>
<ul>
<li>
<blockquote>
</blockquote>
</li>
</ul>
</li>
<li>
<pre><code>      item
</code></pre>
</li>
</ol>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_ordered_max_unordered_max_block_max_empty_no_bq1_with_li2() -> (
    None
):
    """
    Verify that a nesting of ordered list, unordered list, block quote, with
    the maximum number of spaces allowed, and no text on the first line, works properly,
    with no block quote characters on the second line, with a list item.
    """

    # Arrange
    source_markdown = """   1.    +    >
         +      item"""
    expected_tokens = [
        "[olist(1,4):.:1:9:   ]",
        "[ulist(1,10):+::14:         ]",
        "[block-quote(1,15):              :              >]",
        "[BLANK(1,16):]",
        "[end-block-quote:::True]",
        "[li(2,10):11:         :]",
        "[icode-block(2,16):    :]",
        "[text(2,16):item: ]",
        "[end-icode-block:::True]",
        "[end-ulist:::True]",
        "[end-olist:::True]",
    ]
    expected_gfm = """<ol>
<li>
<ul>
<li>
<blockquote>
</blockquote>
</li>
<li>
<pre><code> item
</code></pre>
</li>
</ul>
</li>
</ol>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_ordered_max_unordered_max_block_max_empty_no_bq1_with_li3() -> (
    None
):
    """
    Verify that a nesting of ordered list, unordered list, block quote, with
    the maximum number of spaces allowed, and no text on the first line, works properly,
    with no block quote characters on the second line, with a list item.
    """

    # Arrange
    source_markdown = """   1.    +    >
   1.    +      item"""
    expected_tokens = [
        "[olist(1,4):.:1:9:   ]",
        "[ulist(1,10):+::14:         ]",
        "[block-quote(1,15):              :              >]",
        "[BLANK(1,16):]",
        "[end-block-quote:::True]",
        "[end-ulist:::True]",
        "[li(2,4):9:   :1]",
        "[ulist(2,10):+::11:         ]",
        "[icode-block(2,16):    :]",
        "[text(2,16):item: ]",
        "[end-icode-block:::True]",
        "[end-ulist:::True]",
        "[end-olist:::True]",
    ]
    expected_gfm = """<ol>
<li>
<ul>
<li>
<blockquote>
</blockquote>
</li>
</ul>
</li>
<li>
<ul>
<li>
<pre><code> item
</code></pre>
</li>
</ul>
</li>
</ol>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_ordered_max_plus_one_unordered_max_block_max() -> None:
    """
    Verify that a nesting of ordered list, unordered list, block quote, with
    the maximum number of spaces (plus one for the first) allowed, works properly.
    """

    # Arrange
    source_markdown = """    1.    +    > list
               > item"""
    expected_tokens = [
        "[icode-block(1,5):    :\n    ]",
        "[text(1,5):1.    +    \a>\a&gt;\a list\n           \a>\a&gt;\a item:]",
        "[end-icode-block:::True]",
    ]
    expected_gfm = """<pre><code>1.    +    &gt; list
           &gt; item
</code></pre>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_ordered_max_plus_one_unordered_max_block_max_no_bq1() -> None:
    """
    Verify that a nesting of ordered list, unordered list, block quote, with
    the maximum number of spaces (plus one for the first) allowed, works properly,
    with no block quote characters on the second line.
    """

    # Arrange
    source_markdown = """    1.    +    > list
                 item"""
    expected_tokens = [
        "[icode-block(1,5):    :\n    ]",
        "[text(1,5):1.    +    \a>\a&gt;\a list\n             item:]",
        "[end-icode-block:::True]",
    ]
    expected_gfm = """<pre><code>1.    +    &gt; list
             item
</code></pre>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_ordered_max_unordered_max_plus_one_block_max() -> None:
    """
    Verify that a nesting of ordered list, unordered list, block quote, with
    the maximum number of spaces (plus one for the second) allowed, works properly.
    """

    # Arrange
    source_markdown = """   1.     +    > list
                 item"""
    expected_tokens = [
        "[olist(1,4):.:1:6:   :      ]",
        "[icode-block(1,11):    :\n    ]",
        "[text(1,11):+    \a>\a&gt;\a list\n       item:]",
        "[end-icode-block:::True]",
        "[end-olist:::True]",
    ]
    expected_gfm = """<ol>
<li>
<pre><code>+    &gt; list
       item
</code></pre>
</li>
</ol>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_ordered_max_unordered_max_plus_one_block_max_no_bq1() -> None:
    """
    Verify that a nesting of ordered list, unordered list, block quote, with
    the maximum number of spaces (plus one for the second) allowed, works properly,
    with no block quote characters on the second line.
    """

    # Arrange
    source_markdown = """   1.     +    > list
               > item"""
    expected_tokens = [
        "[olist(1,4):.:1:6:   :      ]",
        "[icode-block(1,11):    :\n    ]",
        "[text(1,11):+    \a>\a&gt;\a list\n     \a>\a&gt;\a item:]",
        "[end-icode-block:::True]",
        "[end-olist:::True]",
    ]
    expected_gfm = """<ol>
<li>
<pre><code>+    &gt; list
     &gt; item
</code></pre>
</li>
</ol>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_ordered_max_unordered_max_block_max_plus_one() -> None:
    """
    Verify that a nesting of ordered list, unordered list, block quote, with
    the maximum number of spaces (plus one for the third) allowed, works properly.
    """

    # Arrange
    source_markdown = """   1.    +     > list
               > item"""
    expected_tokens = [
        "[olist(1,4):.:1:9:   ]",
        "[ulist(1,10):+::11:         :           ]",
        "[icode-block(1,16):    :\n    ]",
        "[text(1,16):\a>\a&gt;\a list\n\a>\a&gt;\a item:]",
        "[end-icode-block:::True]",
        "[end-ulist:::True]",
        "[end-olist:::True]",
    ]
    expected_gfm = """<ol>
<li>
<ul>
<li>
<pre><code>&gt; list
&gt; item
</code></pre>
</li>
</ul>
</li>
</ol>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_ordered_max_unordered_max_block_max_plus_one_no_bq1() -> None:
    """
    Verify that a nesting of ordered list, unordered list, block quote, with
    the maximum number of spaces (plus one for the third) allowed, works properly,
    with no block quote characters on the second line.
    """

    # Arrange
    source_markdown = """   1.    +     > list
                 item"""
    expected_tokens = [
        "[olist(1,4):.:1:9:   ]",
        "[ulist(1,10):+::11:         :           ]",
        "[icode-block(1,16):    :\n    ]",
        "[text(1,16):\a>\a&gt;\a list\n  item:]",
        "[end-icode-block:::True]",
        "[end-ulist:::True]",
        "[end-olist:::True]",
    ]
    expected_gfm = """<ol>
<li>
<ul>
<li>
<pre><code>&gt; list
  item
</code></pre>
</li>
</ul>
</li>
</ol>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)
