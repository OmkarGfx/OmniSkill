# codebolt.llm - LLM Inference Tools

Tools for interacting with Large Language Models and managing model configurations.

## Tools

### `llm_inference`
Sends an inference request to the LLM using OpenAI message format.
| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| messages | array | Yes | Array of messages with "role" (user/assistant/system) and "content" |
| tools | array | No | Array of tools available for the model to use |
| tool_choice | string | No | How to use tools: "auto", "none", or specific tool name |
| max_tokens | number | No | Maximum tokens to generate |
| temperature | number | No | Temperature (0-2), higher = more random |
| stream | boolean | No | Whether to stream the response |
| llmrole | string | No | Role to determine which model to use |

### `llm_get_config`
Gets the model configuration for a specific or default model.
| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| modelId | string | No | Model identifier (defaults to application model) |

## Examples

```javascript
// Basic inference request
await codebolt.tools.executeTool("codebolt.llm", "llm_inference", {
  messages: [
    { role: "system", content: "You are a helpful coding assistant." },
    { role: "user", content: "Explain async/await in JavaScript." }
  ],
  max_tokens: 1000,
  temperature: 0.7
});

// Inference with tools support
await codebolt.tools.executeTool("codebolt.llm", "llm_inference", {
  messages: [
    { role: "user", content: "What files are in the current directory?" }
  ],
  tools: [{
    type: "function",
    function: {
      name: "list_files",
      description: "Lists files in a directory",
      parameters: {
        type: "object",
        properties: {
          path: { type: "string", description: "Directory path" }
        },
        required: ["path"]
      }
    }
  }],
  tool_choice: "auto"
});

// Streaming inference
await codebolt.tools.executeTool("codebolt.llm", "llm_inference", {
  messages: [
    { role: "user", content: "Write a short story about a robot." }
  ],
  stream: true,
  llmrole: "creative"
});

// Get model configuration
await codebolt.tools.executeTool("codebolt.llm", "llm_get_config", {});

// Get specific model config
await codebolt.tools.executeTool("codebolt.llm", "llm_get_config", {
  modelId: "gpt-4"
});
```

## Notes

- Uses OpenAI message format for multi-turn conversations
- Supports function/tool calling for agent capabilities
- The `llmrole` parameter selects model configs for different use cases (coding, creative, analysis)
