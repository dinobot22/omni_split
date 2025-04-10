from io import BytesIO
from docx import Document
import os

def add_fix_before_extension(file_path):
    # 分割文件路径的目录、文件名和扩展名
    dir_name = os.path.dirname(file_path)
    base_name = os.path.basename(file_path)
    name, ext = os.path.splitext(base_name)
    
    # 在文件名和后缀之间添加 _fix
    new_name = f"{name}_fix{ext}"
    # 重新组合路径
    new_path = os.path.join(dir_name, new_name)
    return new_path



def delete_file(file_path):
    """删除指定路径的文件"""
    try:
        if os.path.exists(file_path):
            os.remove(file_path)
            # print(f"文件 {file_path} 已成功删除")
        else:
            pass
            # print(f"文件 {file_path} 不存在，无法删除")
    except Exception as e:
        print(f"删除文件 {file_path} 时出错: {e}")


def replace_hash_in_word_and_return_bytesIO(input_file):
    output_file = add_fix_before_extension(input_file)
    # 打开Word文档
    doc = Document(input_file)
    # 遍历文档中的所有段落
    for paragraph in doc.paragraphs:
        if '#' in paragraph.text:
            # 替换#为"!#"
            paragraph.text = paragraph.text.replace('#', r'\#')
    # 保存修改后的文档
    doc.save(output_file)
    with open(output_file, "rb") as f:
        doc_content = f.read()
        # 将bytes包装成BytesIO
        doc_content_io = BytesIO(doc_content)
    delete_file(output_file)
    return doc_content_io


import os
import re
import uuid
import base64
from typing import List, Dict

import os
import re
import uuid
import base64

def save_local_images_func(ret_data, image_save_path):
    """
    Process ret_data to extract Base64 images, save them locally, and update text references.
    
    Args:
        ret_data: List of dictionaries containing text with potential Base64 images
        image_save_path: Directory to save extracted images
        
    Returns:
        Modified ret_data with local image paths instead of Base64 strings
    """
    # Create directory if it doesn't exist
    if image_save_path and not os.path.exists(image_save_path):
        os.makedirs(image_save_path)
    
    # Regex pattern to match Base64 image strings
    base64_pattern = re.compile(r'!\[.*?\]\(data:image/(.*?);base64,(.*?)\)')
    
    for item in ret_data:
        if 'text' not in item:
            continue
            
        text = item['text']
        matches = base64_pattern.findall(text)
        
        if not matches:
            continue
            
        for match in matches:
            img_format, img_data = match
            try:
                # Generate unique filename
                filename = f"{uuid.uuid4()}.{img_format.split(';')[0]}"
                filepath = os.path.join(image_save_path, filename)
                
                # Decode and save image
                with open(filepath, 'wb') as f:
                    f.write(base64.b64decode(img_data))
                
                # Replace Base64 string with file path
                replacement = f"![](./{os.path.join(image_save_path, filename)})"
                text = text.replace(f"data:image/{img_format};base64,{img_data}", filepath)
                
            except Exception as e:
                print(f"Failed to process image: {e}")
                continue
                
        item['text'] = text
    
    return ret_data


def download_tokenizer_from_network(ms=True):
    if ms:
        qwen_tokenizer.json