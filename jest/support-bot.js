const { OpenAI } = require("openai")

const MODEL = "gpt-6-luna"
const PROMPT = "Classify the customer support message as billing, bug or other. Reply with that one word only."

/** Returns billing, bug or other for a customer support message. */
exports.classify = async (message) => {
  const client = new OpenAI() // created here, not on import, so the evals can skip without a key
  const reply = await client.chat.completions.create({
    model: MODEL,
    messages: [
      { role: "system", content: PROMPT },
      { role: "user", content: message },
    ],
  })
  return (reply.choices[0].message.content ?? "").trim().toLowerCase()
}
