from explainer.gemini_explainer import generate_celestial_explanation

text = "The international space startion reaches maximum elevation of 63 degrees during twilight"

result = generate_celestial_explanation(text,"ISS Flyover")

print(result)