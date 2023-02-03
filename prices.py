# guarantee -> product -> product catalog

from typing import Dict, TypeVar, List

"""
typing library used for type checking, Dict[str, ] : restricts key as string , value can be string or float

"""
Guarantee_feature = TypeVar('Guarantee_feature', str, float)
Guarantee = Dict[str, Guarantee_feature ]

# Product Data Type 
Product = List[Guarantee]

# Clients Data type 

Client_feature = TypeVar('Client_feature', str, int, List)
Client = Dict[str, Client_feature]
ClientPtf = List[Client]

"""
Insurane products details & It's pricing 

"""
# Fire guarantee with type Guarantee 

# Property Product 

fire_guarantee: Guarantee = {
    'product_name': 'Fire', 
    'price': 10.1, 
}

# Earthquake guarantee with type Guarantee 

earthquake_guarantee: Guarantee = {
    
    'product_name': 'Earthquake',
    'price': 2.3,
}

"""
product property with type product i.e list 

"""
product_property: property = [fire_guarantee, earthquake_guarantee]


# Third party liability guarantee with type Guarantee 

# Motor Product

tpl_guarantee: Guarantee = {

    'name': 'Third Party Liability',
    'price': 200.3
}

# Own damage guarantee  with type Guarantee 

own_dmg_guarantee = {

    'name': 'Own damage cover',
    'price': 56.1
}

"""
Motor product defined as list through product type 

"""

motor_product: Product = [tpl_guarantee, own_dmg_guarantee]


"""
Agent will sell either Property product or a motor product 

"""

# Describing Client : Data Type =[Name, Age]

# Clients 

anna: Client = {
    'name': 'Anna',
    'age': 25,
}

john: Client= {
    'name': 'John',
    'age': 75, 
}

sarah: Client= {
    'name': 'Sarah',
    'age': 42,
}

"""
Describing Client Portfolio : Just collection of clients 

"""

clients_ptf: ClientPtf = [anna, john, sarah]


"""
Assigning products to clients and compute total price owned from the clients to the agents 

"""
# Consider age for different client products 

for client in clients_ptf:

    if client['age'] > 70:
        client['ins_products'] = product_property

    elif client['age'] > 40:
        client['ins_products'] = product_property + motor_product
    else:
        client['ins_products'] = motor_product

    print(client['name'], client['ins_products'], sep='\t')

    policy_cost = sum([
        guarantee['price'] for guarantee in client['ins_products']
        ])
    print(
        f'{client["name"]} has to pay (policy_cost:.2f) for {len(client["ins_product"])} guarantees.'
    )


potential_clients = clients_ptf
while  len(potential_clients) > 0:
    # 1st: potential_clients = [anna, john, sarah]
    # 2nd: potential_clients = [john, sarah]
    # 3rd: potential_clients = [sarah]
    client = potential_clients.pop(0)
    print(client['name'])






