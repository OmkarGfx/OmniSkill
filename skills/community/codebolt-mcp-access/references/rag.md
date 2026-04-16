# codebolt.rag - Retrieval Augmented Generation Tools

## Tools

### `rag_create_index`
Creates a new RAG index for storing and retrieving documents.
| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| indexName | string | Yes | Unique name for the index |
| description | string | No | Description of index contents |

### `rag_add_documents`
Adds documents to an existing RAG index.
| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| indexName | string | Yes | Target index name |
| documents | array | Yes | Array of document objects |
| documents[].id | string | Yes | Unique document identifier |
| documents[].content | string | Yes | Document text content |
| documents[].metadata | object | No | Optional metadata |

### `rag_query`
Queries documents using natural language.
| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| indexName | string | Yes | Index to query |
| query | string | Yes | Natural language query |
| topK | number | No | Max results to return |

### `rag_delete_index`
Deletes an index and all its documents.
| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| indexName | string | Yes | Index to delete |

### `rag_update_document`
Updates an existing document in an index.
| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| indexName | string | Yes | Index containing document |
| documentId | string | Yes | Document to update |
| content | string | Yes | New content |
| metadata | object | No | Updated metadata |

### `rag_list_indexes`
Lists all available RAG indexes.
| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| *None* | - | - | No parameters required |

## Examples

```javascript
// Create index
const createResult = await codebolt.tools.executeTool(
  "codebolt.rag",
  "rag_create_index",
  { indexName: "project_docs", description: "API documentation" }
);

// Add documents
const addResult = await codebolt.tools.executeTool(
  "codebolt.rag",
  "rag_add_documents",
  {
    indexName: "project_docs",
    documents: [
      { id: "doc1", content: "Authentication API...", metadata: { type: "api" } }
    ]
  }
);

// Query index
const queryResult = await codebolt.tools.executeTool(
  "codebolt.rag",
  "rag_query",
  { indexName: "project_docs", query: "How to authenticate?", topK: 3 }
);

// List indexes
const indexes = await codebolt.tools.executeTool(
  "codebolt.rag",
  "rag_list_indexes",
  {}
);
```
