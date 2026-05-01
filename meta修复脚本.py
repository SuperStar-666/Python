"""
用记事本或其他文本编辑器打开这个 .ipynb 文件，将 metadata 部分修改为：
"metadata": {
  "kernelspec": {
   "display_name": "Python 3",
   "language": "python",
   "name": "python3"
  },
  "language_info": {
   "codemirror_mode": {
    "name": "ipython",
    "version": 3
   },
   "file_extension": ".py",
   "mimetype": "text/x-python",
   "name": "python",
   "nbconvert_exporter": "python",
   "pygments_lexer": "ipython3",
   "version": "3.12.4"
  }
 }


主要修改：
"version": "2.7.6" → "version": "3.x"
"ipython2" → "ipython3"
"version": 2 → "version": 3
保存后重新在 Jupyter 中打开即可

"""


NEW_FILE_CODE
import json
import sys
import os


def fix_notebook_python_version(filepath):
    """修复 Notebook 文件的 Python 版本配置"""

    # 读取文件
    with open(filepath, 'r', encoding='utf-8') as f:
        nb = json.load(f)

    # 修复 language_info
    if 'metadata' in nb and 'language_info' in nb['metadata']:
        lang_info = nb['metadata']['language_info']

        # 修改 Python 版本为 3.x
        if lang_info.get('version', '').startswith('2.'):
            print(f"检测到 Python 2 配置，正在修复...")
            lang_info['version'] = '3.x'
            lang_info['pygments_lexer'] = 'ipython3'

            if 'codemirror_mode' in lang_info:
                lang_info['codemirror_mode']['version'] = 3

            print(f"✓ 已修复: {filepath}")
        else:
            print(f"✓ 无需修复: {filepath}")

    # 保存文件
    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(nb, f, ensure_ascii=False, indent=1)


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("用法: python fix_python_version.py <notebook文件路径>")
    else:
        filepath = sys.argv[1]
        if os.path.exists(filepath):
            fix_notebook_python_version(filepath)
        else:
            print(f"文件不存在: {filepath}")
