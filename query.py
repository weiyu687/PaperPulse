import json
from sentence_transformers import SentenceTransformer, util
from modelscope.hub.snapshot_download import snapshot_download

MODEL_ID = 'sentence-transformers/all-mpnet-base-v2'
LOCAL_MODEL_PATH = snapshot_download(MODEL_ID)
embedding_model = SentenceTransformer(LOCAL_MODEL_PATH)

def load_papers(json_path):
    with open(json_path, 'r', encoding='utf-8') as file:
        papers = json.load(file)
    return papers

def compute_similarity(query, text):
    query_embedding = embedding_model.encode(query, convert_to_tensor=True)
    text_embedding = embedding_model.encode(text, convert_to_tensor=True)
    similarity = util.cos_sim(query_embedding, text_embedding).item()
    return similarity

def search_papers(papers, user_queries, top_k=3):
    """
    根据用户查询和语义相似度返回最符合条件的论文。

    参数:
        papers (list): 论文列表。
        user_queries (dict): 用户查询，格式为 {"field_name": "query", "weight": float}。
        top_k (int): 返回的论文数量。

    返回:
        list: 排序后的论文列表。
    """
    scored_papers = []

    for paper in papers:
        total_score = 0.0

        for field, query_info in user_queries.items():
            query = query_info["query"]
            weight = query_info["weight"]

            if field == "innovations":
                innovation_texts = [
                    f"{innovation['name']} {innovation['implementation']}"
                    for innovation in paper.get("innovations", [])
                ]
                field_text = " ".join(innovation_texts)
            else:
                field_text = paper.get(field, "")

            similarity = compute_similarity(query, field_text)
            total_score += similarity * weight

        scored_papers.append((total_score, paper))

    scored_papers.sort(key=lambda x: x[0], reverse=True)
    return [paper for _, paper in scored_papers[:top_k]]


if __name__ == "__main__":
    PAPER_JSON = './paper.json'
    papers = load_papers(PAPER_JSON)

    user_queries = {
        "innovations": {"query": "捕捉边界上下文信息并提升分割性能", "weight": 1.0},
    }

    top_papers = search_papers(papers, user_queries, top_k=2)

    print("Top matching papers:")
    for i, paper in enumerate(top_papers, 1):
        print(f"Paper {i}:")
        print(json.dumps(paper, ensure_ascii=False, indent=4))