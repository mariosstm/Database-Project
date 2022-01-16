CREATE TABLE Customer (
	ID string PRIMARY KEY NOT NULL	,
	Fname string NOT NULL,
	Mname string ,
	Lname string NOT NULL,
	USERNAME string NOT NULL,
	PASSWORD string NOT NULL,
	PostalCode varchar string ,
	Country string string,
	City string string,
	streetAddress string string,
	EMAIL string string,
	CellphoneNumber string
);

CREATE TABLE Ticket (
	ticketID string PRIMARY KEY NOT NULL,
	Date date ,
	NVA date ,
	NVB date ,
	TicketType string ,
	customerID string  ,
	JourneyID string  ,
	SeatNumber integer,
	Cost float,
	FOREIGN KEY (customerID) REFERENCES Customer(ID) ON DELETE CASCADE ON UPDATE CASCADE,
	FOREIGN KEY (JourneyID) REFERENCES Journey(JourneyID) ON DELETE CASCADE ON UPDATE CASCADE
);

CREATE TABLE Airport (
	AirportID string PRIMARY KEY  NOT NULL,
	City string,
	Country string,
	AirportName string
);


CREATE TABLE FlightLegs (
	legID string PRIMARY KEY  NOT NULL,
	travelDistance float,
	departureAirportID string,
	arrivalAirportID integer,
	departTime time,
	arrivalTime time,
	departDate date,
	arrivalDate date,
	departGate string,
	FOREIGN KEY (departureAirportID) REFERENCES Airport(AirportID) ON DELETE CASCADE ON UPDATE CASCADE,
	FOREIGN KEY (arrivalAirportID) REFERENCES Airport(AirportID)  ON DELETE CASCADE ON UPDATE CASCADE
);

CREATE TABLE Journey (
	journeyID string PRIMARY KEY NOT NULL,
	departureAirportID string,
	arrivalAirportID string,
	journeyDate date,
	FOREIGN KEY (departureAirportID) REFERENCES Airport(AirportID) ON DELETE CASCADE ON UPDATE CASCADE,
	FOREIGN KEY (arrivalAirportID) REFERENCES Airport(AirportID) ON DELETE CASCADE ON UPDATE CASCADE
);


CREATE TABLE journeysLegs (
	journeyID string,
	legID string,
	FOREIGN KEY (journeyID) REFERENCES Journey(journeyID) ON DELETE CASCADE ON UPDATE CASCADE, 
	FOREIGN KEY (legID) REFERENCES FlightLegs(legID) ON DELETE CASCADE ON UPDATE CASCADE
);


CREATE TABLE Aircraft (
	aircraftID string PRIMARY KEY  NOT NULL,
	aircraftType string ,
	numberOfSeats integer 
);

CREATE TABLE Pilot (
	pilotID string PRIMARY KEY  NOT NULL,
	VAT integer ,
	fullName string 
);

CREATE TABLE TravelAgent (
	travelAgentVAT string PRIMARY KEY  NOT NULL,
	Name string 
);

CREATE TABLE Controls (
	pilotID string,
	airplaneID string,
	legID string,
	FOREIGN KEY (pilotID) REFERENCES Pilot(pilotID) ON DELETE CASCADE ON UPDATE CASCADE,
	FOREIGN KEY (airplaneID) REFERENCES Aircraft(aircraftID) ON DELETE CASCADE ON UPDATE CASCADE,
	FOREIGN KEY (legID) REFERENCES FlightLegs(legID) ON DELETE CASCADE ON UPDATE CASCADE
);


CREATE TABLE BuyingVIATravelAgent (
	customerID string,
	travelAgentVAT string,
	ticketID string,
	FOREIGN KEY (customerID) REFERENCES Customer(ID) ON DELETE CASCADE ON UPDATE CASCADE,
	FOREIGN KEY (travelAgentVAT) REFERENCES TravelAgent(travelAgentVAT) ON DELETE CASCADE ON UPDATE CASCADE,
	FOREIGN KEY (ticketID) REFERENCES Ticket(ticketID) ON DELETE CASCADE ON UPDATE CASCADE
);


create table TravelAgentDiscount(
	travelAgentVAT string,
	journeyID string,
	discount float,
	FOREIGN key (travelAgentVAT) REFERENCES TravelAgent(travelAgentVAT) on DELETE CASCADE on UPDATE CASCADE,
	FOREIGN key (journeyID) REFERENCES Journey(journeyID) on DELETE cascade on update CASCADE
);

--DATA INERTION--


--Airport
	insert into Airport (airportID, City, Country, AirportName) values ('ATH', 'Athens', 'Greece', 'Athens International Airport Eleftherios Venizelos');
	insert into Airport (airportID, City, Country, AirportName) values ('LHR', 'London', 'England', 'Heathrow Airport');
	insert into Airport (airportID, City, Country, AirportName) values ('MAN', 'Manchester', 'England', 'Manchester Airport');
	insert into Airport (airportID, City, Country, AirportName) values ('CDG', 'Paris', 'France', 'Paris Charles de Gaulle Airport');
	insert into Airport (airportID, City, Country, AirportName) values ('AMS', 'Amsterdam', 'Netherlands', 'Amsterdam Airport Schiphol');
	insert into Airport (airportID, City, Country, AirportName) values ('IST', 'Istanbul', 'Turkey', 'Istanbul Airport');
	insert into Airport (airportID, City, Country, AirportName) values ('FRA', 'Frankfurt', 'Germany', 'Frankfurt Airport');
	insert into Airport (airportID, City, Country, AirportName) values ('MUC', 'Munich', 'Germany', 'Munich International Airport');
	insert into Airport (airportID, City, Country, AirportName) values ('MAD', 'Madrid', 'Spain', 'Adolfo Suárez Madrid–Barajas Airport');
	insert into Airport (airportID, City, Country, AirportName) values ('BCN', 'Barcelona', 'Spain', 'Josep Tarradellas Barcelona-El Prat Airport');
	insert into Airport (airportID, City, Country, AirportName) values ('FCO', 'Rome', 'Italy', 'Leonardo da Vinci International Airport');
	insert into Airport (airportID, City, Country, AirportName) values ('ZRH', 'Zurich', 'Switzerland', 'Zurich Airport');
	insert into Airport (airportID, City, Country, AirportName) values ('BRU', 'Brussels', 'Belgium', 'Brussels Airport');
	insert into Airport (airportID, City, Country, AirportName) values ('DUB', 'Dublin', 'Ireland', 'Dublin Airport');
	insert into Airport (airportID, City, Country, AirportName) values ('DME', 'Moscow', 'Russia', 'Moscow Domodedovo Mikhail Lomonosov Airport');
	insert into Airport (airportID, City, Country, AirportName) values ('OSL', 'Oslo', 'Norwegia', 'Oslo Airport');
	insert into Airport (airportID, City, Country, AirportName) values ('VIE', 'Vienna', 'Austria', 'Vienna International Airport');
	insert into Airport (airportID, City, Country, AirportName) values ('JFK', 'New York City', 'USA', 'John F. Kennedy International Airport');
	insert into Airport (airportID, City, Country, AirportName) values ('LAX', 'Los Angeles', 'USA', 'Los Angeles International Airport');
	insert into Airport (airportID, City, Country, AirportName) values ('ORD', 'Chicago', 'USA', "O'Hare International Airport");

--Pilot
	insert into Pilot (pilotID, VAT, fullName) values (501673, 507, 'Joceline Paddington');
	insert into Pilot (pilotID, VAT, fullName) values (501521, 532, 'Ardath Benard');
	insert into Pilot (pilotID, VAT, fullName) values (501875, 921, 'Scott Lochran');
	insert into Pilot (pilotID, VAT, fullName) values (501537, 668, 'Hedi Mattersey');
	insert into Pilot (pilotID, VAT, fullName) values (501803, 748, 'Fulvia Gauche');
	insert into Pilot (pilotID, VAT, fullName) values (501808, 982, 'Saxon Marusic');
	insert into Pilot (pilotID, VAT, fullName) values (501298, 853, 'Ursala Bernardini');
	insert into Pilot (pilotID, VAT, fullName) values (501476, 870, 'Ariana Swatton');
	insert into Pilot (pilotID, VAT, fullName) values (501108, 856, 'Joannes Bickerstaff');
	insert into Pilot (pilotID, VAT, fullName) values (501644, 647, 'Aldis Copeland');
	insert into Pilot (pilotID, VAT, fullName) values (501406, 774, 'Clarette Crevagh');

--Customer
	insert into Customer (ID, Fname, Mname, Lname, USERNAME, PASSWORD, PostalCode, Country, City, streetAddress, EMAIL,cellphonenumber,discount) values ('55239', 'Trent', 'Elise', 'Downing', 'edowning0', 'iFvZixs83K', '35203 CEDEX 2', 'France', 'Rennes', '09151 Division Point', 'edowning0@jimdo.com','263-959-5992',0.0);
	insert into Customer (ID, Fname, Mname, Lname, USERNAME, PASSWORD, PostalCode, Country, City, streetAddress, EMAIL,cellphonenumber,discount) values ('55467', 'Karon', 'Dewie', 'Garrard', 'dgarrard0', 'uP5qZU', null, 'Greece', 'Magoúla', '06 Eagan Way', 'dgarrard0@google.cn','549-484-7830',0.0);
	insert into Customer (ID, Fname, Mname, Lname, USERNAME, PASSWORD, PostalCode, Country, City, streetAddress, EMAIL,cellphonenumber,discount) values ('55227', 'Jaymie', 'Scott', 'Moxon', 'smoxon1', 'yB8wL3AIdYRF', null, 'Greece', 'Neochórion', '38 Talmadge Drive', 'smoxon1@studiopress.com','219-492-3804',0.0);
	insert into Customer (ID, Fname, Mname, Lname, USERNAME, PASSWORD, PostalCode, Country, City, streetAddress, EMAIL,cellphonenumber,discount) values ('55007', 'Chrysa', 'Jilleen', 'Barnewall', 'jbarnewall2', 'cFHxqq8', '30942 CEDEX 9', 'France', 'Nîmes', '099 Monica Center', 'jbarnewall2@gravatar.com','753-736-7623',0.0);
	insert into Customer (ID, Fname, Mname, Lname, USERNAME, PASSWORD, PostalCode, Country, City, streetAddress, EMAIL,cellphonenumber,discount) values ('55699', 'Raymond', 'Horace', 'Lindholm', 'hlindholm3', 'dmDx1Dhf', '57704 CEDEX', 'France', 'Hayange', '306 Mendota Court', 'hlindholm3@gmpg.org','372-366-1124',0.0);
	insert into Customer (ID, Fname, Mname, Lname, USERNAME, PASSWORD, PostalCode, Country, City, streetAddress, EMAIL,cellphonenumber,discount) values ('55496', 'Alyce', 'Inigo', 'Moyse', 'imoyse4', 'tiVxEagBJK', '78067 CEDEX', 'France', 'Saint-Quentin-en-Yvelines', '2737 Eagan Street', 'imoyse4@tmall.com','971-526-5528',0.0);
	insert into Customer (ID, Fname, Mname, Lname, USERNAME, PASSWORD, PostalCode, Country, City, streetAddress, EMAIL,cellphonenumber,discount) values ('55792', 'Philippa', 'Julienne', 'Tokley', 'jtokley5', 'MAJgnGr', '43071', 'Spain', 'Tarragona', '08619 New Castle Circle', 'jtokley5@cbc.ca','197-493-7211',0.0);
	insert into Customer (ID, Fname, Mname, Lname, USERNAME, PASSWORD, PostalCode, Country, City, streetAddress, EMAIL,cellphonenumber,discount) values ('55789', 'Frederik', 'Kassi', 'Domnick', 'kdomnick6', '4MwdvH8oBKb', '78165 CEDEX', 'France', 'Marly-le-Roi', '827 Sage Point', 'kdomnick6@blogtalkradio.com','755-746-9264',0.0);
	insert into Customer (ID, Fname, Mname, Lname, USERNAME, PASSWORD, PostalCode, Country, City, streetAddress, EMAIL,cellphonenumber,discount) values ('55097', 'Tony', 'Gertie', 'Nicklen', 'gnicklen7', '7ZHIxCNkA', null, 'Greece', 'Aíyira', '4 Corben Trail', 'gnicklen7@tinyurl.com','755-746-9264',0.0);
	insert into Customer (ID, Fname, Mname, Lname, USERNAME, PASSWORD, PostalCode, Country, City, streetAddress, EMAIL,cellphonenumber,discount) values ('55447', 'Dmitri', 'Virgie', 'Sandever', 'vsandever8', 'oeIIl46t', '70004 CEDEX', 'France', 'Vesoul', '10 Grasskamp Plaza', 'vsandever8@e-recht24.de','668-711-6972',0.0);
	insert into Customer (ID, Fname, Mname, Lname, USERNAME, PASSWORD, PostalCode, Country, City, streetAddress, EMAIL,cellphonenumber,discount) values ('55506', 'Kele', 'Flossi', 'Ridde', 'fridde9', 'Ki2TBlqFu2', '80146 CEDEX', 'France', 'Abbeville', '593 Maple Point', 'fridde9@wunderground.com','454-408-5615',0.0);


--TravelAgent
	insert into TravelAgent (travelAgentVAT, Name) values ('166677', 'Nolan, McLaughlin and Koepp');
	insert into TravelAgent (travelAgentVAT, Name) values ('166264', 'Howell, Schmeler and Ryan');
	insert into TravelAgent (travelAgentVAT, Name) values ('166689', 'Trantow LLC');
	insert into TravelAgent (travelAgentVAT, Name) values ('166318', 'Muller-Kirlin');
	insert into TravelAgent (travelAgentVAT, Name) values ('166457', 'Oberbrunner, Wilkinson and Roberts');
	insert into TravelAgent (travelAgentVAT, Name) values ('166816', 'Carter-Gibson');
	insert into TravelAgent (travelAgentVAT, Name) values ('166614', 'Hand, Mayer and Adams');
	insert into TravelAgent (travelAgentVAT, Name) values ('166248', 'Crist-Lind');
	insert into TravelAgent (travelAgentVAT, Name) values ('166033', 'Cremin, Satterfield and Witting');
	insert into TravelAgent (travelAgentVAT, Name) values ('166032', 'Smitham, Lakin and Block');
	insert into TravelAgent (travelAgentVAT, Name) values ('166436', 'Ortiz Inc');


--FlightLegs
--ATH - MAD
	insert into FlightLegs (legID, travelDistance, departTime, arrivalTime, departDate, arrivalDate, departGate, departureAirportID, arrivalAirportID) values ('3103', 1, '10:00', '14:00', '2022-03-15', '2022-03-15', 18, 'ATH', 'MAD');
--ATH - MAD περασμενη ημρομηνια
	insert into FlightLegs (legID, travelDistance, departTime, arrivalTime, departDate, arrivalDate, departGate, departureAirportID, arrivalAirportID) values ('3104', 1, '08:00', '12:00', '2021-12-10', '2021-12-10', 51, 'ATH', 'MAD');
--ATH - FCO - MAD
	insert into FlightLegs (legID, travelDistance, departTime, arrivalTime, departDate, arrivalDate, departGate, departureAirportID, arrivalAirportID) values ('3105', 1, '14:00', '17:00', '2022-02-05', '2022-02-05', 18, 'ATH', 'FCO');
	insert into FlightLegs (legID, travelDistance, departTime, arrivalTime, departDate, arrivalDate, departGate, departureAirportID, arrivalAirportID) values ('3106', 1, '18:00', '21:00', '2022-02-05', '2022-02-05', 18, 'FCO', 'MAD');
--ATH - CDG - ZRH - MAD
	insert into FlightLegs (legID, travelDistance, departTime, arrivalTime, departDate, arrivalDate, departGate, departureAirportID, arrivalAirportID) values ('3107', 1, '14:00', '16:00', '2022-02-05', '2022-02-05', 18, 'ATH', 'CDG');
	insert into FlightLegs (legID, travelDistance, departTime, arrivalTime, departDate, arrivalDate, departGate, departureAirportID, arrivalAirportID) values ('3108', 1, '17:00', '19:00', '2022-02-05', '2022-02-05', 18, 'CDG', 'ZRH');
	insert into FlightLegs (legID, travelDistance, departTime, arrivalTime, departDate, arrivalDate, departGate, departureAirportID, arrivalAirportID) values ('3109', 1, '20:00', '22:00', '2022-02-05', '2022-02-05', 18, 'ZRH', 'MAD');	
-- CDG-MAD, απότελει το δευτερο σκέλος του ταξιδιού no8, ATH-MAD, το πώτο σκέλος του είναι το ATH-CDG με αριθμό Leg 3107 που ανηκει και στο ταξίδι 4 
	insert into FlightLegs (legID, travelDistance, departTime, arrivalTime, departDate, arrivalDate, departGate, departureAirportID, arrivalAirportID) values ('3110', 1, '18:00', '21:00', '2022-02-05', '2022-02-05', 18 , 'CDG', 'MAD');	
--Journey
	INSERT INTO journey (journeyID,departureAirportID, arrivalAirportID) values ('1','ATH','MAD');
	INSERT INTO journey (journeyID,departureAirportID, arrivalAirportID) values ('2','ATH','MAD');
	INSERT INTO journey (journeyID,departureAirportID, arrivalAirportID) values ('3','ATH','MAD');
	INSERT INTO journey (journeyID,departureAirportID, arrivalAirportID) values ('4','ATH','MAD');
	INSERT INTO journey (journeyID,departureAirportID, arrivalAirportID) values ('5','ATH','FCO');
	INSERT INTO journey (journeyID,departureAirportID, arrivalAirportID) values ('6','FCO','MAD');
	INSERT INTO journey (journeyID,departureAirportID, arrivalAirportID) values ('7','LHR','MAD');
	INSERT INTO journey (journeyID,departureAirportID, arrivalAirportID) values ('8','ATH','MAD');










