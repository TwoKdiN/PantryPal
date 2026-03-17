#drop database if exists pantrypal;

#create database PantryPal;

#use PantryPal;

CREATE TABLE users(
    idUser INT AUTO_INCREMENT PRIMARY KEY,
    usernameUser VARCHAR(25) NOT NULL UNIQUE,
    passwordUser VARCHAR(25) NOT NULL,
    role ENUM('Manager', 'Waiter') NOT NULL
);


CREATE TABLE manager(
    usernameManager VARCHAR(25)  NOT NULL UNIQUE,
    passwordManager VARCHAR(25) NOT NULL,
    idManager INT auto_increment NOT NULL PRIMARY KEY
);

CREATE TABLE waiter(
    usernameWaiter VARCHAR(25) NOT NULL UNIQUE,
    passwordWaiter VARCHAR(25) NOT NULL,
    idWaiter INT auto_increment NOT NULL PRIMARY KEY
);

CREATE TABLE ingredient(
    idIngredient INT AUTO_INCREMENT NOT NULL PRIMARY KEY,
    nameIngredient VARCHAR(25) NOT NULL,
    quantityOfIngredient DOUBLE NOT NULL,
    threshold DOUBLE NOT NULL,
	category ENUM('Meat', 'Fish', 'Vegetable', 'Dairy Product'),
    idOfPlate INT NOT NULL
);

CREATE TABLE plate(
    idPlate INT AUTO_INCREMENT NOT NULL PRIMARY KEY ,
    namePlate VARCHAR(25) NOT NULL UNIQUE,
    price DOUBLE NOT NULL
);

CREATE TABLE tableNo(
    idTable INT NOT NULL PRIMARY KEY,
    status ENUM('Available', 'NOT Available') DEFAULT 'Available',
    orderId INT NOT NULL UNIQUE,
    idWaiter INT NOT NULL UNIQUE
);

CREATE TABLE Orders (
    order_id INT PRIMARY KEY AUTO_INCREMENT,
    table_id INT NOT NULL,
    waiter_id INT NOT NULL,
    order_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    status ENUM('Pending', 'Completed', 'Cancelled') NOT NULL DEFAULT 'Pending',
    FOREIGN KEY (table_id) REFERENCES tableNo(idTable),
    FOREIGN KEY (waiter_id) REFERENCES waiter(idWaiter)
);

CREATE TABLE OrderItems (
    order_item_id INT PRIMARY KEY AUTO_INCREMENT,
    order_id INT NOT NULL,
    menu_item_id INT NOT NULL,
    quantity INT NOT NULL,
    special_requests TEXT,
    FOREIGN KEY (order_id) REFERENCES Orders(order_id),
    FOREIGN KEY (menu_item_id) REFERENCES plate(idPlate)
);

CREATE TABLE Payments (
    payment_id INT PRIMARY KEY AUTO_INCREMENT,
    order_id INT NOT NULL,
    payment_method ENUM('cash', 'card') NOT NULL,
    amount DECIMAL(10, 2) NOT NULL,
    change_amount DECIMAL(10, 2) DEFAULT 0.00,
    payment_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (order_id) REFERENCES Orders(order_id)
);

CREATE TABLE sales(
	idSale INT AUTO_INCREMENT PRIMARY KEY,
	dateSale DATE NOT NULL,
	amount DOUBLE NOT NULL,
    paymentId INT NOT NULL,
    idOfWaiter INT NOT NULL UNIQUE,
    FOREIGN KEY (paymentId) REFERENCES Payments(payment_id),
    FOREIGN KEY (idOfWaiter) REFERENCES waiter(idWaiter)
);

/*
CREATE TABLE tableSale(
	idTableSale INT AUTO_INCREMENT PRIMARY KEY,
    tableAmount DOUBLE NOT NULL,
    idWaiter INT NOT NULL UNIQUE,
    idTable INT UNIQUE,
    dateAmount DATE NOT NULL 
);
*/

CREATE TABLE recipe (
    idRecipe INT AUTO_INCREMENT NOT NULL PRIMARY KEY,
    nameRecipe VARCHAR(50) NOT NULL,
    idPlate INT NOT NULL
);

CREATE TABLE recipe_ingredient (
    id INT AUTO_INCREMENT NOT NULL PRIMARY KEY,
    recipe_id INT NOT NULL,
    nameIngredient VARCHAR(50) NOT NULL,
    quantity DOUBLE NOT NULL,
    threshold DOUBLE NOT NULL
);

# Connection
ALTER TABLE manager ADD CONSTRAINT fk_managerUser FOREIGN KEY (idManager) REFERENCES users(idUser);
ALTER TABLE waiter ADD CONSTRAINT fk_waiterUser FOREIGN KEY (idWaiter) REFERENCES users(idUser);
ALTER TABLE ingredient ADD CONSTRAINT fk_plateIngedient FOREIGN KEY (idOfPlate) REFERENCES plate(idPlate) ON DELETE CASCADE ON UPDATE CASCADE;
#ALTER TABLE tableNo ADD CONSTRAINT fk_tableNoOrderNo FOREIGN KEY (idTable) REFERENCES orderNo(numberOfTable);
#ALTER TABLE orderNo ADD CONSTRAINT fk_orderNoTableNo FOREIGN KEY (idOrder) REFERENCES tableNo(orderId);
#ALTER TABLE waiter ADD CONSTRAINT fl_waiterOrderNo FOREIGN KEY (idWaiter) REFERENCES orderNo(idWaiter);
#ALTER TABLE orderNo ADD CONSTRAINT fk_orderNoPlate FOREIGN KEY (idOfPlate) REFERENCES plate(idPlate);
#LTER TABLE orderNo ADD CONSTRAINT fk_orderNotableSale FOREIGN KEY (idWaiter) REFERENCES tableSale(idWaiter);
#ALTER TABLE tableNo ADD CONSTRAINT fk_tableNotableSale FOREIGN KEY (idTable) REFERENCES tableSale(idTable);
ALTER TABLE recipe_ingredient ADD CONSTRAINT recipe_ingredient_ibfk_1 FOREIGN KEY (recipe_id) REFERENCES recipe(idRecipe) ON DELETE CASCADE ON UPDATE CASCADE;
ALTER TABLE recipe ADD CONSTRAINT recipe_ibfk_1 FOREIGN KEY (idPlate) REFERENCES plate(idPlate) ON DELETE CASCADE ON UPDATE CASCADE;
#ALTER TABLE ADD CONSTRAINT fk_ FOREIGN KEY () REFERENCES ();


#ALTER TABLE waiter DROP FOREIGN KEY fl_waiterOrderNo;

#DROP TABLE orderNo;
