Για το τρέξιμο της εφαρμογής τόσο του Πελάτη(CustomerUI) , όσο και για τον Admin (Admin Interface)
Σε περίπτωση που δεν υπάρχει η python 3 στο σύστημα σας εμπισκεφτείτε το
link : https://www.python.org/downloads/
και κατεβάστε την νεότερη έκδοση.
Το πρόγραμμα τρέχει και σε μερικές εκδόσεις της Python 2 (python 2.5 και μετά , αν και ενδέχεται να παρουσιαστούν προβλήματα ) 

Εκτελέστε στο  cmd τα ακόλουθα :
python -m pip install --upgrade pip
<<Αντιγράψτε το filepath στο οποίο εμπεριέχεται το αρχείο packages με τα απαραίτητα modules

>> cd  [File Path]
>>pip  install -r packages.txt

Το παραδοτέο περιλαμβάνει τα εξης αρχεία
"createDB.sql" - Αρχειο δημιουργίας βασης δεδομένων
"database.db" - Βαση δεδομένων
"insertAircrafts.py" - χρησιμοποιηθηκε για την εισαγωγη στοιχιων στο πινακα aircrafts
"travelAgentDiscountInsertion.py"  -""- -''- στον πίνακα travelAgentDiscount
"usefulFunctions.py" -  αρχειο με χρήσιμες συναρτησεις που χρησιμοποιηθηκαν πολλες φορες μέσα στον κωδικα
"journeyFinder.py" - περιέχει τη συνάρτηση getJourneys που χρησιμοποιείται για την ευρεση ταξιδιών βάσει των δοθέντων πληροφοριών
"handleDataBase.py" - περιέχει μεθοδους για έυκολο χειρισμό μίας βασης δεδομένων. όλες οι εντολες sql και γενικότερα η διαχείριση της βασης μεσω python έηινε καλώντας τις εθοδους αυτου του αρχειο
"flightSubmissionForm.py" - Αρχειο για τη δημιουργίας της φορμας εισαγωγής ταξιδιών
"adminPanel.py" - το αρχειο που μπορει να τρέχει ο admin της βασης

"Login.py "-το αρχείο για να συνδεθείτε στην εφαρμογή του πελάτη
"RegisterForm.py"-Η φόρμα δημιουργίας δικού σας profile.
"CustomerUI.py"- το Interface αφού συνδεθείτε.

Για να εξερευνήσετε την εφαρμογή για τον Customer τρέξτε το Login.py

GITHUB_REPOSITORY:
https://github.com/mariosstm/Database-Project.git