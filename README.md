# PaperPulse

### 项目通过大模型提取paper创新点并保存
### 保存的内容示例如下：
```json
{
  "paper_title": "Sample Paper Title",
  "authors": ["Author A", "Author B"],
  "publication_date": "2025-04-20",
  "innovations": [
    {
      "name": "Novel Algorithm for Data Processing",
      "implementation": "This involves using a new approach to...",
      "problem_solved": "It addresses the inefficiency in existing algorithms..."
    }
  ]
}
```

### 基于语义相似度计算返回论文信息，支持选定字段


### 将项目拉取到本地后，将paper保存到paper文件夹下，然后从[KIMi](https://platform.moonshot.cn/)获取API_KEY并填入main.py中
### 运行main.py即可自动提取创新点，保存到paper.json文件中


### 运行query.py，设置查询字段、关键词和权重，返回查询到的指定数量的论文