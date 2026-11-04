import Anthropic from "@anthropic-ai/sdk"

export const MODEL = "claude-haiku-5-5"
const PROMPT = "Classify the customer support message as billing, bug or other. Reply with that one word only."

/** Returns billing, bug or other for a customer support message. */
export async function classify(message: string): Promise<string> {
  const client = new Anthropic() // created here, not on import, so the evals can skip without a key
  const reply = await client.messages.create({
    model: MODEL,
    max_tokens: 4096,
    system: PROMPT,
    messages: [{ role: "user", content: message }],
  })
  // The model thinks first by default, so the answer is in the text blocks after its thinking block.
  return reply.content.map((block) => (block.type === "text" ? block.text : "")).join("").trim().toLowerCase()
}
