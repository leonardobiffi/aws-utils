# Preco AWS Ohio 02/2020
# https://aws.amazon.com/fargate/pricing/?nc1=h_ls

preco_vcpu_h = float(input("Preço CPU/hora -> "))
preco_gb_h = float(input("Preço Memória (GB)/hora -> "))
horas = int(input("Total de Horas [default=730hrs] -> ") or "730")
vcpu = float(input("vCPUs [default=0.25vCPU] -> ") or "0.25")
memoria = float(input("Memória (GB) [default=0.128GB] -> ") or "0.128")

print("====== Resultado ======")
preco = vcpu*preco_vcpu_h*horas + memoria*preco_gb_h*horas
print(f"vCPUs: {vcpu:5.2f}")
print(f"Memória GB: {memoria}")
print(f"Horas: {horas}\n")

print(f"Preço: ${preco:7.2f}")
