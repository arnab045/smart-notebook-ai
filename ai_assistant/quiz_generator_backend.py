from core.gemini_config import model
import json

def generate_quiz(note_content, num_questions=10):

    prompt = f"""
    Create exactly {num_questions} multiple choice questions from this study note.

    Return ONLY valid JSON.

    Format:

    {{
      "questions": [
        {{
          "question": "Question text",
          "options": [
            "Option A",
            "Option B",
            "Option C",
            "Option D"
          ],
          "answer": 0,
          "explanation": "Short explanation of why the answer is correct"
        }}
      ]
    }}

    Rules:

    - Exactly {num_questions} questions
    - Exactly 4 options per question
    - answer must be option index (0,1,2,3)
    - No markdown
    - No explanation
    - Return JSON only
    - explanation must be 1-3 sentences
    - explanation should explain why the answer is correct

    Note:

    {note_content}
    """

    response = model.generate_content(prompt)

    return response.text