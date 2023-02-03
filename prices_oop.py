from typing import List

from ins_types import Guarantee, Client

# Guarantees definition
fire_guarantee = Guarantee('Fire', -10.1)
earthquake_guarantee = Guarantee('Earthquake', 2.3)
tpl_guarantee = Guarantee('Third party liablity', 200.3)
own_dmg_guarantee = Guarantee('Own damage cover', 56.1)

# Products definition
Product = List[Guarantee]
property_product: Product = [fire_guarantee, earthquake_guarantee]
motor_product: Product = [tpl_guarantee, own_dmg_guarantee]

# Clients definition
anna = Client('Anna', 1995)
john = Client('John', 1945)
sarah = Client('Sarah', 1975)
ClientPtf = List[Client]
clients_ptf: ClientPtf = [anna, john, sarah]


def find_best_products(client: Client) -> List[Guarantee]:
    if client.age > 70:
        return property_product
    elif client.age > 40:
        return property_product + motor_product
    else:
        return motor_product

Guarantee.tax_ratio = 0.5

# Premium evaluation per client
for client in clients_ptf:
    client.ins_products = find_best_products(client)

    try:
        policy_cost = client.eval_premium()
        print(
            f'{client.name} has to pay {policy_cost:.2f} dollars for {len(client.ins_products)} guarantees.'
        )
    except Exception as e:
        print(e)

