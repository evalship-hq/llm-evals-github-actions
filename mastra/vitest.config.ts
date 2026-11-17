import { defineConfig } from "vitest/config"

export default defineConfig({
  test: { setupFiles: ["@mastra/evals/vitest/setup"] },
})
