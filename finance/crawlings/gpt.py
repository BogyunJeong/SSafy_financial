from openai import OpenAI

def gpt_prompt(comment):
    client = OpenAI(api_key=OPENAI_API_KEY)

    response = client.responses.create(
    model="gpt-4o-mini",
    input=[
        {
        "role": "system",
        "content": [
            {
            "type": "input_text",
            "text": "당신은 증권사의 댓글을 분석하여 투자자들의 여론에 대해 분석하는 애널리스트야. 각 댓글들의 내용들을 취합하여 전체 의견들의 요약을 정리를 한 뒤, 마지막에 여론 분위기를 긍정적, 중립적, 부정적 중 하나로 분석할거야."
            }
        ]
        },
        {
        "role": "user",
        "content": [
            {
            "type": "input_text",
            "text": comment
                }
        ]
        }
    ],
    temperature=1,
    max_output_tokens=256
    )
    return response.output_text