# Use cases

Talk-to-Data can use Router, Schema, SQL, Python, Visualization, Business Analyst, and Reviewer agents. Put connections and dataframes in `SharedState`, keep schema/results in `Context`, use swarm for exploration, workflow for governed reports, and graph for parallel analysis.

OCR can use Router, OCR, Layout Parser, JSON Formatter, and Reviewer. Store clients and temporary artifacts in shared state; use a workflow for predictable stages or a graph for page-level parallelism.

RAG can use Retriever, Searcher, Summarizer, and Reviewer. Keep vector stores in shared state and citations/findings in context. Swarm supports adaptive retrieval; workflow is simple; graph parallelizes retrieval and joins before review.

Coding assistants can use Architect, Coder, Tester, and Reviewer. Inject filesystem and test tools, preserve plans and results in context, and isolate credentials in shared state. Use workflow for a fixed delivery pipeline, swarm for iterative repair, and graph for parallel tests/reviews.

