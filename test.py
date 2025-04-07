import json
# from pprint import pprint
from omni_split import OmniSplit

omni_spliter = OmniSplit(tokenizer_json_path="model/text_chunker_tokenizer/qwen_tokenizer.json", txt_chunk_size=512)
## note: test text split

with open("test/txt.txt", "r") as f:
    text_content = "".join(f.readlines())

res = omni_spliter.text_chunk_func(text_content)
for item in res:
    print(item)
    print("------------")
print("="*10)

with open("./test/c8d4614affc19ba92d7ba0671fd709803d0488a0c5a68bc237783a8af39fe32e/1c7fbb26-1012-4b03-894c-69ab2257985c_1743677710.4311144.md", "r") as f:
    md_content = f.read()
res = omni_spliter.markdown_chunk_func(md_content)
for item in res:
    print(item)
    print("------------")
print("="*10)

res = omni_spliter.markdown_chunk_func(md_content,clear_model=True)
for item in res:
    print(item)
    print("------------")
print("="*10)