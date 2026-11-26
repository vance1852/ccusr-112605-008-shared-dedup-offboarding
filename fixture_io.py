"""检查交换清单并浏览合成记录。"""

import argparse
import hashlib
import json
from pathlib import Path


def read_catalog(root):
    with (root / "catalog.json").open(encoding="utf-8") as handle:
        return json.load(handle)


def read_payload(root, manifest, name):
    if not name or name in {".", ".."} or Path(name).name != name or "\\" in name or ":" in name:
        raise ValueError("不合法的资料名")
    item = manifest["payloads"][name]
    value = (root / "payloads" / (name + ".bin")).read_bytes()
    if (len(value), hashlib.sha256(value).hexdigest()) != (item["bytes"], item["sha256"]):
        raise ValueError(f"资料长度或摘要不匹配：{name}")
    return value


def read_records(path):
    previous = 0
    with path.open(encoding="utf-8") as handle:
        for number, line in enumerate(handle, start=1):
            try:
                record = json.loads(line)
                if not isinstance(record, dict) or type(record.get("time")) is not int:
                    raise ValueError("事件应给出整数时钟")
                if record["time"] < previous or not isinstance(record.get("kind"), str) or not record["kind"]:
                    raise ValueError("事件缺少类型或时钟顺序错误")
            except ValueError as error:
                raise ValueError(f"{path.name}:{number} {error}") from error
            previous = record["time"]
            yield record


def main():
    parser = argparse.ArgumentParser(description="验证来源清单，显示原始记录")
    parser.add_argument("records", type=Path, help="来源记录路径")
    parser.add_argument("--kind", help="仅显示指定记录类型")
    args = parser.parse_args()
    root = args.records.parent
    try:
        manifest = read_catalog(root)
        for name in manifest["payloads"]:
            read_payload(root, manifest, name)
        for item in read_records(args.records):
            if args.kind is None or item["kind"] == args.kind:
                print(json.dumps(item, ensure_ascii=False))
    except (OSError, KeyError, ValueError) as error:
        parser.exit(2, f"资料检查失败：{error}\n")


if __name__ == "__main__":
    main()
