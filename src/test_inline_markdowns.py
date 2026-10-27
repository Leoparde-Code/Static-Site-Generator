import unittest
from inline_markdown import *

class TestInlineMarkdown(unittest.TestCase):

    def test_basic(self):
        node = TextNode("This is text with a `code block` word", TextType.TEXT)
        split_node = split_nodes_delimiter([node], "`", TextType.CODE)

        self.assertEqual(split_node, [
            TextNode("This is text with a ", TextType.TEXT),
            TextNode("code block", TextType.CODE),
            TextNode(" word", TextType.TEXT),
        ])

    def test_non_TextNode(self):
        node = TextNode("already bold", TextType.BOLD)
        split_text = split_nodes_delimiter([node], "**", TextType.BOLD)

        self.assertEqual(split_text, [TextNode("already bold", TextType.BOLD)])

    def test_unbalanced_delimiter(self):
        node = TextNode("This has an unclosed `code block", TextType.TEXT)

        with self.assertRaises(Exception):
            split_nodes_delimiter([node], "`", TextType.CODE)

    def test_multiple_delimited_sections(self):
        node = TextNode("Some `code` and more `code` here", TextType.TEXT)
        split_text = split_nodes_delimiter([node], "`", TextType.CODE)

        self.assertEqual(split_text, [TextNode("Some ", TextType.TEXT), TextNode("code", TextType.CODE), TextNode(" and more ", TextType.TEXT), TextNode("code", TextType.CODE), TextNode(" here", TextType.TEXT)])

    def test_text_to_textnodes_bold(self):
        text = "This is **bold** text"
        nodes = text_to_textnodes(text)
        expected = [
            TextNode("This is ", TextType.TEXT),
            TextNode("bold", TextType.BOLD),
            TextNode(" text", TextType.TEXT),
        ]
        self.assertListEqual(nodes, expected)

    def test_text_to_textnodes_italic(self):
        text = "This is _italic_ text"
        nodes = text_to_textnodes(text)
        expected = [
            TextNode("This is ", TextType.TEXT),
            TextNode("italic", TextType.ITALIC),
            TextNode(" text", TextType.TEXT),
        ]
        self.assertListEqual(nodes, expected)

    def test_text_to_textnodes_all(self):
        text = "This is **bold** text and _italic_`code`![alt text](boot.dev.image)[anchor text](boot.dev)"
        nodes = text_to_textnodes(text)
        expected = [
            TextNode("This is ", TextType.TEXT),
            TextNode("bold", TextType.BOLD),
            TextNode(" text and ", TextType.TEXT),
            TextNode("italic", TextType.ITALIC),
            TextNode("code", TextType.CODE),
            TextNode("alt text", TextType.IMAGE, "boot.dev.image", ),
            TextNode("anchor text", TextType.LINK, "boot.dev", )
        ]
        self.assertListEqual(nodes, expected)

    def test_split_images(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.TEXT),
                TextNode("second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"),
            ],
            new_nodes,
        )

    def test_split_no_images(self):
        node = TextNode(
            "This is text with an and another",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with an and another", TextType.TEXT),
            ],
            new_nodes,
        )

    def test_split_image_at_start(self):
        node = TextNode(
            "![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.TEXT),
                TextNode("second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"),
            ],
            new_nodes,
        )

    def test_split_image_at_end(self):
        node = TextNode(
            "This is text with an and another ![second image](https://i.imgur.com/3elNhQu.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with an and another ", TextType.TEXT),
                TextNode("second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"),
            ],
            new_nodes,
        )

    def test_split_links(self):
        node = TextNode(
            "This is text with an [link](https://i.imgur.com/zjjcJKZ.png) and another [second link](https://i.imgur.com/3elNhQu.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("link", TextType.LINK, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.TEXT),
                TextNode("second link", TextType.LINK, "https://i.imgur.com/3elNhQu.png"),
            ],
            new_nodes,
        )

    def test_split_no_links(self):
        node = TextNode(
            "This is text with an and another",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("This is text with an and another", TextType.TEXT),
            ],
            new_nodes,
        )

    def test_split_link_at_start(self):
        node = TextNode(
            "[link](https://i.imgur.com/zjjcJKZ.png) and another [second link](https://i.imgur.com/3elNhQu.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("link", TextType.LINK, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.TEXT),
                TextNode("second link", TextType.LINK, "https://i.imgur.com/3elNhQu.png"),
            ],
            new_nodes,
        )

    def test_split_link_at_end(self):
        node = TextNode(
            "This is text with an and another [second link](https://i.imgur.com/3elNhQu.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("This is text with an and another ", TextType.TEXT),
                TextNode("second link", TextType.LINK, "https://i.imgur.com/3elNhQu.png"),
            ],
            new_nodes,
        )

    def test_extract_markdown_images(self):
        matches = extract_markdown_images(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)"
        )
        self.assertListEqual([("image", "https://i.imgur.com/zjjcJKZ.png")], matches)

    def test_extract_markdown_two_images(self):
        matches = extract_markdown_images(
            "![image](https://i.imgur.com/zjjc.png)This is text with two ![image](https://i.imgur.com/zjjcJKZ.png)"
        )
        self.assertListEqual([("image", "https://i.imgur.com/zjjc.png"), ("image", "https://i.imgur.com/zjjcJKZ.png"), ], matches)

    def test_extract_markdown_link(self):
        matches = extract_markdown_links(
            "This is text with an [anchor text](https://i.imgur.com/zjjcJKZ.png)"
        )
        self.assertListEqual([("anchor text", "https://i.imgur.com/zjjcJKZ.png")], matches)

    def test_extract_markdown_two_links(self):
        matches = extract_markdown_links(
            "[anchor text](https://i.imgur.com/zjjc.png)This is text with two [anchor text 2](https://i.imgur.com/zjjcJKZ.png)"
        )
        self.assertListEqual([("anchor text", "https://i.imgur.com/zjjc.png"), ("anchor text 2", "https://i.imgur.com/zjjcJKZ.png"), ], matches)

    def test_extract_markdown_both_image_and_link(self):
        matches = extract_markdown_links(
            "![image](https://i.imgur.com/zjjc.png)This is text with two [anchor text](https://i.imgur.com/zjjcJKZ.png)"
        )
        self.assertListEqual([("anchor text", "https://i.imgur.com/zjjcJKZ.png"), ], matches)




if __name__ == "__main__":
    unittest.main()



if __name__ == "__main__":
    unittest.main()
