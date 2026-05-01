NEW_FILE_CODE
import json
import os
import glob


def fix_single_notebook(filepath):
    """修复单个 Notebook 文件"""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            nb = json.load(f)

        modified = False

        # 修复 language_info
        if 'metadata' in nb and 'language_info' in nb['metadata']:
            lang_info = nb['metadata']['language_info']

            if lang_info.get('version', '').startswith('2.'):
                lang_info['version'] = '3.x'
                lang_info['pygments_lexer'] = 'ipython3'

                if 'codemirror_mode' in lang_info:
                    lang_info['codemirror_mode']['version'] = 3

                modified = True

        # 确保 kernelspec 正确
        if 'metadata' in nb:
            if 'kernelspec' not in nb['metadata']:
                nb['metadata']['kernelspec'] = {}

            nb['metadata']['kernelspec'] = {
                "display_name": "Python 3",
                "language": "python",
                "name": "python3"
            }
            modified = True

        if modified:
            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(nb, f, ensure_ascii=False, indent=1)
            return True
        return False

    except Exception as e:
        print(f"✗ 处理失败 {filepath}: {e}")
        return False


def batch_fix_all_notebooks(directory):
    """批量修复目录下所有 Notebook"""
    pattern = os.path.join(directory, "**", "*.ipynb")
    files = glob.glob(pattern, recursive=True)

    print(f"找到 {len(files)} 个 .ipynb 文件\n")

    fixed_count = 0
    error_count = 0

    for filepath in files:
        rel_path = os.path.relpath(filepath, directory)
        try:
            if fix_single_notebook(filepath):
                print(f"✓ 已修复: {rel_path}")
                fixed_count += 1
            else:
                print(f"- 无需修复: {rel_path}")
        except Exception as e:
            print(f"✗ 错误: {rel_path} - {e}")
            error_count += 1

    print(f"\n{'=' * 50}")
    print(f"完成！")
    print(f"  修复: {fixed_count} 个文件")
    print(f"  错误: {error_count} 个文件")
    print(f"{'=' * 50}")


if __name__ == "__main__":
    target_dir = r"E:\《大模型--博学谷》"
    print(f"开始扫描目录: {target_dir}\n")
    batch_fix_all_notebooks(target_dir)
