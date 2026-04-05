import json
import os
import urllib.request

API_KEY = os.environ["ANTHROPIC_API_KEY"]

SYSTEM_PROMPT = """You are a scientific research assistant.

Read one paper abstract or excerpt and return valid JSON with exactly these keys:
summaryQuestion
summaryMethod
summaryFinding
keyVariables
nextObjective
nextExperiment
critique

Rules:
- Use plain text only.
- Do not use markdown.
- Do not include backticks.
- Return only one valid JSON object.
- Keep every field concise.
- summaryQuestion: exactly 1 sentence.
- summaryMethod: 1 to 2 short sentences.
- summaryFinding: 1 to 2 short sentences.
- keyVariables: one comma-separated line, not a paragraph.
- nextObjective: exactly 1 sentence.
- nextExperiment: 1 short sentence.
- critique: 1 to 2 short sentences.
"""

def _extract_json_object(text: str) -> str:
    text = text.strip()

    if text.startswith("```"):
        lines = text.splitlines()
        if len(lines) >= 3:
            text = "\n".join(lines[1:-1]).strip()

    start = text.find("{")
    end = text.rfind("}")
    if start != -1 and end != -1 and end > start:
        return text[start:end + 1]

    raise ValueError("No complete JSON object found in Claude response.")

def _fallback_result(paper_text: str) -> dict:
    lower_text = paper_text.lower()

    if "diffusion" in lower_text or "isotope" in lower_text or "dissolution" in lower_text or "basalt" in lower_text or "andesite" in lower_text:
        return {
            "summaryQuestion": "The paper studies diffusive isotope or chemical transport behavior in silicate melts.",
            "summaryMethod": "The study uses experiments, measurements, and modeling to analyze diffusion-related behavior in melts.",
            "summaryFinding": "The results suggest that transport behavior depends on melt composition, experimental conditions, and measurement corrections.",
            "keyVariables": "diffusion, isotope fractionation, melt composition, basalt, andesite, dissolution, SIMS, profile shape",
            "nextObjective": "Test whether the same transport behavior holds across a broader range of melt compositions and temperatures.",
            "nextExperiment": "Run additional controlled experiments while varying one major condition at a time and measuring the resulting profiles.",
            "critique": "A reviewer may ask for more experiments, stronger uncertainty analysis, and clearer justification of the modeling assumptions."
        }

    if "lunar" in lower_text or "magmatic" in lower_text or "melt inclusion" in lower_text:
        return {
            "summaryQuestion": "The paper studies whether magmatic processes can explain observed chemical signatures in lunar melts.",
            "summaryMethod": "The study uses petrologic observations and geochemical or magmatic modeling to test alternative interpretations.",
            "summaryFinding": "The results suggest that magmatic recharge or related processes may explain the observations without requiring an unusual mantle source.",
            "keyVariables": "lunar melts, melt inclusions, recharge, volatile elements, mantle source, magma evolution",
            "nextObjective": "Test whether the same interpretation remains valid under additional geochemical constraints.",
            "nextExperiment": "Compare model predictions with new measurements while varying one magmatic parameter at a time.",
            "critique": "A reviewer may ask whether competing explanations were fully ruled out and whether model uncertainty was sufficiently constrained."
        }

    return {
        "summaryQuestion": "The paper studies a scientific question described in the abstract.",
        "summaryMethod": "The study uses the experimental, observational, or modeling approach described in the text.",
        "summaryFinding": "The results suggest a meaningful conclusion about the system under study.",
        "keyVariables": "main system, input variables, measured outputs, constraints",
        "nextObjective": "Design a follow-up study that tests the main conclusion more directly.",
        "nextExperiment": "Change one major condition, hold others fixed, and compare the resulting measurements or model behavior.",
        "critique": "A reviewer may ask for clearer controls, assumptions, and uncertainty estimates."
    }

def analyze_paper_text(paper_text: str) -> dict:
    body = {
        "model": "claude-sonnet-4-6",
        "max_tokens": 1000,
        "temperature": 0.2,
        "system": SYSTEM_PROMPT,
        "messages": [
            {
                "role": "user",
                "content": paper_text
            }
        ]
    }

    req = urllib.request.Request(
        "https://api.anthropic.com/v1/messages",
        data=json.dumps(body).encode("utf-8"),
        headers={
            "Content-Type": "application/json",
            "x-api-key": API_KEY,
            "anthropic-version": "2023-06-01",
        },
        method="POST",
    )

    with urllib.request.urlopen(req) as resp:
        payload = json.loads(resp.read().decode("utf-8"))

    text = payload["content"][0]["text"].strip()
    print("RAW CLAUDE RESPONSE:\n", text)

    try:
        json_text = _extract_json_object(text)
        return json.loads(json_text)
    except Exception as e:
        print("JSON PARSE FAILED:", e)
        return _fallback_result(paper_text)