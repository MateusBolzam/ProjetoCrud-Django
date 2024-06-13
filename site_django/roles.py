from rolepermissions.roles import AbstractUserRole

class Gerente(AbstractUserRole):
    available_permissions = {'controle': True}

class Vendedor(AbstractUserRole):
    available_permissions = {'vendas': True}