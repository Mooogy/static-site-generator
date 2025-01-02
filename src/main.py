
from block_funcs import block_to_html_node

def main():
    block = """>I am quoting a famous person this quote is written over a couple of lines
>I am not sure how this might be handled but it should be contained in a single quoteblock
>despite however many lines I decide to **ABUSE**"""

    print(block_to_html_node(block).to_html())

if __name__ == "__main__":
    main()