import google.generativeai as genai

GEMINI_API_KEY = "AIzaSyAd-5uzCtjfOkSwl9A73gDnxFYdWtBvBSs"

genai.configure(api_key=GEMINI_API_KEY)

model = genai.GenerativeModel("gemini-3.5-flash")