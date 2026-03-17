from Order import Order

class Waiter:
    def __init__(self, tables):
        self.tables = tables

    def viewTables(self):
        for table in self.tables:
            print("Τραπέζι:", table.tableNumber, "- Κατάσταση:", table.getStatus())

    def createOrder(self, table):
        new_order = Order(len(table.getCurrentOrder()) + 1, table) if table.getCurrentOrder() else Order(1, table)
        table.setCurrentOrder(new_order)
        print("Δημιουργήθηκε νέα παραγγελία για το τραπέζι:", table.tableNumber)
        return new_order

    def sendOrder(self, order):
        order.sendOrder()
        print("Η παραγγελία απεστάλη.")

    def processPayment(self, table, paymentMethod):
        if table.getCurrentOrder():
            total_price = table.getCurrentOrder().getTotalPrice()
            print("Συνολική τιμή παραγγελίας:", total_price)
            print("Η πληρωμή πραγματοποιήθηκε με επιτυχία μέσω:", paymentMethod)
            table.setCurrentOrder(None)
        else:
            print("Δεν υπάρχει παραγγελία για αυτό το τραπέζι.")
