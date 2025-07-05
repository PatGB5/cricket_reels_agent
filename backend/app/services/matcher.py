from difflib import SequenceMatcher

async def match_facts_to_segments(facts, segments):
    matched = []
    for fact in facts:
        best_match = None
        best_score = 0
        for segment in segments:
            score = SequenceMatcher(None, fact["fact"], segment["text"]).ratio()
            if score > best_score:
                best_match = segment
                best_score = score
        matched.append({
            "fact": fact["fact"],
            "image_path": fact.get("image_path", None),
            "start": best_match["start"],
            "end": best_match["end"]
        })
    return matched
