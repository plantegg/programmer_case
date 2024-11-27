#!/bin/bash

# 将输入保存到临时文件
head -2 $1 > temp_input.txt

# 读取第一行的键名
keys=$(head -n 1 temp_input.txt | cut -d' ' -f2-)
# 读取第二行的值
values=$(tail -n 1 temp_input.txt | cut -d' ' -f2-)

# 将键名和值转换为数组
IFS=' ' read -r -a key_array <<< "$keys"
IFS=' ' read -r -a value_array <<< "$values"

# 遍历数组并打印对应关系
for i in "${!key_array[@]}"; do
    echo "${key_array[i]}: ${value_array[i]}"
done

# 删除临时文件
rm temp_input.txt

