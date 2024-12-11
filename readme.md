## Reading

You may need to increase the size of the csv reader buffer.

```python
import csv
import sys

csv.field_size_limit(sys.maxsize)

entries_read = []
with open(data_dir / f"{monthly_file}.csv", "r") as f:
    reader = csv.reader(f)
    for row in reader:
        entries_read.append(row)
```
