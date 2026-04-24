from mcp.server.fastmcp import FastMCP
from pathlib import Path
import json

mcp = FastMCP("invoice-collection-mcp")

CUSTOMER_DATA_PATH = Path("customers.json")

def listar_clientes() -> list[dict]:
    """Load customer data from the JSON file.`"""

    if not CUSTOMER_DATA_PATH.exists():
        return []
    
    with open(CUSTOMER_DATA_PATH, "r", encoding="utf-8") as f:
        return json.load(f)


@mcp.tool()
def list_customers() -> list[dict]:
    """
        Lista todos os clientes cadastrados com plano, MRR e status de fatura.
        Use quando o usuário quiser uma visão geral da base de clientes.
    """

    return listar_clientes()


@mcp.tool()
def listar_faturas_vencidas() -> list[dict]:
    """"
        Lista clientes com fatura vencidas
        Use quando o usuario quiser saberm quem está inadimplente ou quais cobranças estão pendentes
    """
    customers = listar_clientes()
    
    overdue_customers = [
        customer
        for customer in customers
        if customer["invoice_status"] == "overdue"
    ]

    return overdue_customers

@mcp.tool()
def calcular_mrr_em_risco() -> dict:
    """
        Calcula o MRR em risco com base nos clientes com faturas vencidas.
        Use para avaliar o impacto financeiro potencial da inadimplência.
    """
    
    overdue_customers = listar_faturas_vencidas()

    total_mrr_at_risk = sum(
        customer["mrr"]
        for customer in overdue_customers
    )

    total_open_amount = sum(
        customer["open_invoice_amount"]
        for customer in overdue_customers
    )

    return {
        "overdue_customers_count": len(overdue_customers),
        "mrr_at_risk": round(total_mrr_at_risk, 2),
        "total_open_invoice_amount": round(total_open_amount, 2)
    }


@mcp.tool()
def priorizar_cobrancas() -> list[dict]:
    """
        Prioriza cobranças considerando valor em aberto, dias de atraso e plano.
        Use quando o usuário quiser saber quais clientes devem ser cobrados primeiro.
    """

    overdue_customers = listar_faturas_vencidas()

    plan_weight = {
        "Starter": 1,
        "Pro": 2,
        "Business": 3,
        "Enterprise": 4
    }

    prioritized = []

    for customer in overdue_customers:
        score = {
            customer["open_invoice_amount"] * 0.6
            + customer["days_overdue"] * 10
            + plan_weight.get(customer["plan"], 1) * 50
        }

        prioritized.append({
            "customer_id": customer["id"],
            "name": customer["name"],
            "plan": customer["plan"],
            "days_overdue": customer["days_overdue"],
            "open_invoice_amount": customer["open_invoice_amount"],
            "contact_email": customer["contact_email"],
            "priority_score": score
        })

    return sorted(
            prioritized,
            key=lambda item: item["priority_score"],
            reverse=True
        )


@mcp.tool()
def gerar_mensagem_cobranca(customer_id: str) -> dict:
    """
    Gera uma mensagem de cobrança educada para um cliente inadimplente.
    Use quando o usuário quiser preparar um email de cobrança para um cliente específico.
    """
    customers = list_customers()

    customer = next(
        (item for item in customers if item["id"] == customer_id),
        None
    )

    if customer is None:
        return {
            "error": True,
            "message": f"Cliente {customer_id} não encontrado."
        }

    if customer["invoice_status"] != "overdue":
        return {
            "error": True,
            "message": f"Cliente {customer['name']} não possui fatura vencida."
        }

    email_message = f"""
        Olá, equipe {customer["name"]}.

        Identificamos uma fatura em aberto no valor de ${customer["open_invoice_amount"]:.2f}, com {customer["days_overdue"]} dias de atraso.

        Poderiam verificar o pagamento ou nos informar caso precisem de ajuda?

        Obrigado,
        Equipe Financeira
        """.strip()

    return {
        "error": False,
        "customer_id": customer["id"],
        "customer_name": customer["name"],
        "contact_email": customer["contact_email"],
        "message": email_message
    }


if __name__ == "__main__":
    mcp.run()