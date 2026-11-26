# 跨租户去重对象的占量归属与退租

`examples/` 保存合成设备清册、二进制样本和两次各自从清册起步的记录。文件内容通过同名 `.bin` 样本给出，清册的 `payloads` 提供这些样本文件的实际长度和 SHA-256，可区分原件字节与不同的设备传输记录。

## 本地资料约定

`examples/catalog.json` 的 `inventory` 为已知设备、数据和合同。事件采用 JSON Lines，`time` 是到达记录端的时钟，同一时刻保持行顺序，`kind` 区分来源。字节位置从零起，起止范围左闭右开。操作请求、受理和实际设备结果是不同的来源事实。

logical_limit 是租户名下成功对象的逻辑正文容量，assigned 是分配给设备的实际容量。initial 同设备同 payload 的已核验副本可被允许共享。hint 仅是 SHA-256 首字节的十六进制，不能据此证明正文相同。share_pacts 的 valid_until 是允许创建新共享引用的截止点。remove_request 和 device removed 是不同时点。

## 检查及浏览

使用 Python 3.11 和标准库，在项目根目录运行。

```sh
python3 fixture_io.py examples/shift.jsonl
python3 fixture_io.py examples/comparison.jsonl
python3 -m unittest discover -s tests -v
```

读取工具检查样本完整性并原样显示对应事件。加 `--kind` 可只看一种记录。
