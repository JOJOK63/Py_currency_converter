from PySide2 import QtWidgets
import currency_converter


# l'application hérite ici de la class QtWidgets.QWidget ,
# QWidget représente la fenetre et toute les manipulations possible dessus
class App(QtWidgets.QWidget):
    def __init__(self):
        # super permet de récupérer la méthode init de la class parent
        super().__init__()
        # ! à l'ordre d'appel des méthodes, on ne peut pas modifier les widgets si ils ne sont pas encore instanciés
        self.c = currency_converter.CurrencyConverter()
        self.setWindowTitle(" Convertisseur de devises")
        self.setup_ui()
        self.set_default_values()
        self.setup_connections()

    def setup_ui(self):
        # création d'un layout horizontal , le self de droite permet de préciser que le layout est lié a la fenetre principal
        self.layout = QtWidgets.QHBoxLayout(self)
        # cbb et un préfixe pour rendre le code plus compréhensible , ici Combobox
        # spn et un préfixe pour rendre le code plus compréhensible , ici SpinBox
        # btn et un préfixe pour rendre le code plus compréhensible , ici PushButton
        self.cbb_devisesFrom = QtWidgets.QComboBox()
        self.spn_montant = QtWidgets.QSpinBox()
        self.cbb_devisesTo = QtWidgets.QComboBox()
        self.spn_montantConverti = QtWidgets.QSpinBox()
        self.btn_inverser = QtWidgets.QPushButton("Inverser devises")
        #         ajout des widgets créer au layout
        self.layout.addWidget(self.cbb_devisesFrom)
        self.layout.addWidget(self.spn_montant)
        self.layout.addWidget(self.cbb_devisesTo)
        self.layout.addWidget(self.spn_montantConverti)
        self.layout.addWidget(self.btn_inverser)

    def set_default_values(self):
        # cbb prend en parametre seulement des list contenant des strings
        self.cbb_devisesFrom.addItems(sorted(list(self.c.currencies)))
        self.cbb_devisesTo.addItems(sorted(list(self.c.currencies)))
        self.cbb_devisesFrom.setCurrentText("EUR")
        self.cbb_devisesTo.setCurrentText("EUR")

        self.spn_montant.setRange(1, 1000000)
        self.spn_montantConverti.setRange(1, 1000000)

        self.spn_montant.setValue(100)
        self.spn_montantConverti.setValue(100)

    def setup_connections(self):
        # connection des méthodes aux layout , et utilisation des signaux
        self.cbb_devisesFrom.activated.connect(self.compute)
        self.cbb_devisesTo.activated.connect(self.compute)
        self.spn_montant.valueChanged.connect(self.compute)
        self.spn_montantConverti.valueChanged.connect(self.compute)
        self.btn_inverser.clicked.connect(self.inverser_devise)

    def compute(self):
        montant = self.spn_montant.value()
        devise_from = self.cbb_devisesFrom.currentText()
        devise_to = self.cbb_devisesTo.currentText()

        try:
            resultat = self.c.convert(montant, devise_from, devise_to)
        except currency_converter.RateNotFoundError:
            print("la conversion n'as pas fonctionné.")
        else:
            self.spn_montantConverti.setValue(resultat)

    def inverser_devise(self):
        devise_from = self.cbb_devisesFrom.currentText()
        devise_to = self.cbb_devisesTo.currentText()

        self.cbb_devisesFrom.setCurrentText(devise_to)
        self.cbb_devisesTo.setCurrentText(devise_from)
        self.compute()


# permet de créer l'application ou nous aurons accés a nos différentes fenetre ,   argument [] obligatoire
# ! différent de 'application de base
app = QtWidgets.QApplication([])
# création d'une fenetre pour l'application déja lancer
win = App()
# affichage du widget permettant d'afficher le contenu a l'utilisateur
win.show()

app.exec_()
