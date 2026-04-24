# Invoice Collection MCP

Simple MCP server for a fake SaaS invoice collection workflow.

It helps an AI assistant answer questions like:

- Which customers are overdue?
- How much revenue is at risk?
- Who should be contacted first?
- What collection message should be sent?

## What It Does

This project reads mock customer data from `customers.json` and exposes it as MCP tools.

Current tools:

- `list_customers()`
- `listar_faturas_vencidas()`
- `calcular_mrr_em_risco()`
- `priorizar_cobrancas()`
- `gerar_mensagem_cobranca(customer_id)`

## Why It Exists

This is a learning project to practice building MCP servers with a more realistic business case.

Instead of generic demo tools, it simulates a simple finance workflow for a SaaS company.

## Project Files

```text
invoice-collection-mcp/
├── customers.json
├── server.py
├── test_local.py
└── README.md
```

## Run Locally

Create a virtual environment:

```bash
python -m venv .venv
source .venv/bin/activate
```

Install dependencies:

```bash
pip install mcp
```

Run the MCP Inspector:

```bash
mcp dev server.py
```

## Local Test

```bash
python test_local.py
```

## Example Use Case

A founder could ask:

> Which customers are overdue and how much MRR is at risk?

An MCP host can then call the server tools and return the answer using your business data.

## Next Step

The next improvement is turning this into a more realistic product flow by adding task creation for the finance team and connecting the server to a real MCP host like Cursor, Claude Desktop, or VS Code.
