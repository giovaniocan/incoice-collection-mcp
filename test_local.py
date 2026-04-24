from server import calcular_mrr_em_risco, gerar_mensagem_cobranca, listar_clientes, listar_faturas_vencidas, priorizar_cobrancas

clientes = listar_clientes()
vencidas = listar_faturas_vencidas()

print("Clientes encontrados:", len(clientes))
print("Faturas vencidas:", len(vencidas))
print("MRR em risco:", calcular_mrr_em_risco())

for cliente in vencidas:
    print(
        cliente["id"],
        cliente["name"],
        "dias em atraso:",
        cliente["days_overdue"],
        "valor:",
        cliente["open_invoice_amount"]
    )

print("Prioridade de cobranças:")
for item in priorizar_cobrancas():
    print(item["customer_id"], item["name"], item["priority_score"])


    
print(gerar_mensagem_cobranca("CUS-004"))