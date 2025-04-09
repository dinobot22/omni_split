import json
from io import BytesIO

# from pprint import pprint
from omni_split import OmniSplit
import docx

from utils.base_utils import replace_hash_in_word_and_return_bytesIO

omni_spliter = OmniSplit(tokenizer_json_path="model/text_chunker_tokenizer/qwen_tokenizer.json", txt_chunk_size=1000)
## note: test text split
test_text = False
if test_text:
    with open("test/txt.txt", "r") as f:
        text_content = "".join(f.readlines())
    res = omni_spliter.text_chunk_func(text_content)
    for item in res:
        print(item)
        print("------------")
    print("=" * 10)

## note: test markdown json split
test_markdown = False
if test_markdown:
    with open("./test/c8d4614affc19ba92d7ba0671fd709803d0488a0c5a68bc237783a8af39fe32e/1c7fbb26-1012-4b03-894c-69ab2257985c_1743677710.4311144_content_list.json", "r") as f:
        md_content_json = json.load(f)
    res = omni_spliter.markdown_json_chunk_func(md_content_json)
    for item in res:
        print(item)
        print("------------")
    print("=" * 10)
    
    res = omni_spliter.markdown_json_chunk_func(md_content_json,clear_model=True)
    for item in res:
        print(item)
        print("------------")
    print("=" * 10)

## note: test markdown split
test_markdown = False
if test_markdown:
    with open("./test/c8d4614affc19ba92d7ba0671fd709803d0488a0c5a68bc237783a8af39fe32e/1c7fbb26-1012-4b03-894c-69ab2257985c_1743677710.4311144.md", "r") as f:
        md_content = f.read()
    res = omni_spliter.markdown_chunk_func(md_content)
    for item in res:
        print(item)
        print("------------")
    print("=" * 10)


    res = omni_spliter.markdown_chunk_func(md_content, clear_model=True)
    for item in res:
        print(item)
        print("------------")
    print("=" * 10)




    # res = omni_spliter.markdown_json_chunk_func(md_content_json, clear_model=True)
    # for item in res:
    #     print(item)
    #     print("------------")
    # print("=" * 10)


## note: test word split
test_document = True
if test_document:

    new_doc_io = replace_hash_in_word_and_return_bytesIO("./test/图谱效率构建(增加知识融合).docx")
    res = omni_spliter.document_chunk_func(new_doc_io, txt_chunk_size=1000, clear_model=False)
    for item in res:
        print(item)
        print("------------")
    print("=" * 10)


    new_doc_io = replace_hash_in_word_and_return_bytesIO("./test/图谱效率构建(增加知识融合).docx")
    res = omni_spliter.document_chunk_func(new_doc_io, txt_chunk_size=1000, clear_model=False,save_local_images_dir="./images")
    for item in res:
        print(item)
        print("------------")
    print("=" * 10)

    res = omni_spliter.document_chunk_func(new_doc_io, txt_chunk_size=1000, clear_model=True)
    for item in res:
        print(item)
        print("------------")
    print("=" * 10)
