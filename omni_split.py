from transformers import PreTrainedTokenizerFast
from sub_chunker.markdown_split import MarkdownChunker
from sub_chunker.text_split import SentenceChunker


class OmniSplit:
    def __init__(self, tokenizer_json_path="./model/qwen_tokenizer.json", txt_chunk_size=512):
        self.tokenizer_json_path = tokenizer_json_path
        self.txt_chunk_size = txt_chunk_size
        self.tokenizer = PreTrainedTokenizerFast(tokenizer_file=self.tokenizer_json_path)

    def get_text_len_func(self, text):
        """
        * @description: 获取文本长度
        * @param  self :
        * @param  text :
        * @return
        """
        if type(text) == str:
            return len(self.tokenizer.encode(text, add_special_tokens=False))
        else:
            raise ValueError("text must be str")

    def text_chunk_func(self, text, txt_chunk_size=None):
        """
        * @description: 纯文本的切割方法
        * @param  self :
        * @param  text :
        * @return
        """
        if txt_chunk_size is None:
            txt_chunk_size = self.txt_chunk_size
        text_chunker = SentenceChunker(tokenizer_or_token_counter=self.tokenizer, chunk_size=txt_chunk_size, delim=["!", "?", "\n", "。", ";", "；"], return_type="texts")
        ret_data = text_chunker.chunk(text)
        return ret_data

    def markdown_chunk_func(self, markdown_text, txt_chunk_size=None,clear_model=False):
        """
        * @description: markdown的切割方法
        * @param  self :
        * @param  text :
        * @return
        """
        if txt_chunk_size is None:
            txt_chunk_size = self.txt_chunk_size
        md_chunker = MarkdownChunker(max_chunk_words=txt_chunk_size,clear_model=clear_model)
        ret_data = md_chunker.chunk(markdown_text)
        return ret_data
