import os
import json
import fitz
from datetime import datetime
from sentence_transformers import SentenceTransformer, util

def extract_text(pdf_path):
    doc = fitz.open(pdf_path)
    blocks = []
    for page_num, page in enumerate(doc):
        text = page.get_text("blocks")
        for block in text:
            content = block[4].strip()
            if len(content) > 40:
                blocks.append({
                    "page": page_num + 1,
                    "text": content
                })
    return blocks

def main():
    input_dir = "/app/input"
    output_dir = "/app/output"

    with open(os.path.join(input_dir, "persona.json")) as f:
        config = json.load(f)

    persona = config["persona"]
    job = config["job"]
    documents = config["documents"]

    query = f"You are reviewing a document for a {persona}. Task: {job}"
    model = SentenceTransformer("./cached_model")
    query_vec = model.encode(query, convert_to_tensor=True)

    best_blocks_per_doc = []
    all_other_blocks = []

    for doc in documents:
        path = os.path.join(input_dir, doc)
        print(f"\n📄 Processing document: {doc}")
        if not os.path.exists(path):
            print(f"❌ File {doc} not found!")
            continue

        texts = extract_text(path)
        if not texts:
            print(f"⚠️ No suitable text found in {doc}")
            continue

        doc_scores = []
        for block in texts:
            vec = model.encode(block["text"], convert_to_tensor=True)
            score = util.pytorch_cos_sim(query_vec, vec).item()
            print(f"📝 {doc} - Page {block['page']} - Score: {score:.4f}")
            doc_scores.append({
                "document": doc,
                "page": block["page"],
                "text": block["text"],
                "score": score
            })

        doc_scores.sort(key=lambda x: -x["score"])
        if doc_scores:
            best_blocks_per_doc.append(doc_scores[0])
            all_other_blocks.extend(doc_scores[1:])

    all_other_blocks.sort(key=lambda x: -x["score"])

    # Pick top 5 relevant sections
    needed = 5 - len(best_blocks_per_doc)
    top_blocks = best_blocks_per_doc + all_other_blocks[:needed]

    output = {
        "metadata": {
            "input_documents": documents,
            "persona": persona,
            "job": job,
            "timestamp": datetime.now().isoformat()
        },
        "extracted_sections": [],
        "subsection_analysis": []
    }

    for rank, item in enumerate(top_blocks, start=1):
        output["extracted_sections"].append({
            "document": item["document"],
            "page": item["page"],
            "section_title": f"{item['document']} - Pg {item['page']}: {item['text'][:60]}...",
            "importance_rank": rank
        })
        output["subsection_analysis"].append({
            "document": item["document"],
            "page": item["page"],
            "refined_text": item["text"]
        })

    with open(os.path.join(output_dir, "persona_output.json"), "w") as f:
        json.dump(output, f, indent=2)

if __name__ == "__main__":
    main()
