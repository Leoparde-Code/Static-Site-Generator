import sys

from copy_static import copy_static_to_public
from gen_content import generate_pages_recursive


def main():

    if len(sys.argv) >= 2:
        basepath = sys.argv[1]
    else:
        basepath = "/"



    copy_static_to_public("static", "docs")
    generate_pages_recursive("content", "template.html", "docs", basepath)

main()
