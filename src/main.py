from copy_static import copy_static_to_public
from gen_content import generate_pages_recursive


def main():
    copy_static_to_public("static", "public")
    generate_pages_recursive("content", "template.html", "public")

main()
