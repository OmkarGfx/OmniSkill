# Tokenizer

Text tokenization operations.

| Tool | Description | Key Parameters |
|------|-------------|----------------|
| `tokenizer_encode` | Encode text into tokens | text (req) |
| `tokenizer_decode` | Decode tokens into text | tokens (req) |

```javascript
await codebolt.tools.executeTool("codebolt.tokenizer", "tokenizer_encode", {
  text: "Hello world"
});
```
