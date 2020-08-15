###########################################
#
# Permet de créer un serveur web
#
# Author : Antoine-Alexis Bourdon
# Link : https://github.com/antoinealexisb/
# Version : 0.1.0
# Year : 7 july 2020
# Dependency : tkinter, http.server, socketserver, threading
#
###########################################

# Librairies
from tkinter import * 
import http.server
import socketserver
import threading

class ServerWeb:
	'''Classe qui permet de mettre en place un server HTTP.
	'''

	def __init__(self, PORT=8000):
		'''fonction qui initialise la classe ServerWeb
		Param : - ServerWeb (modif)
				- PORT (int) : numéro du port à utiliser
		Return : None
		'''
		self.lancer = False
		self.listButtons = None
		self.Handler = http.server.SimpleHTTPRequestHandler
		self.PORT = PORT
		
	def initialisationThread(self):
		'''Fonction qui initialise le threading et le server http.
		Param : - ServerWeb (modif)
		Return : None
		'''
		try:
			self.httpd = socketserver.TCPServer(("", self.PORT), self.Handler)
		except OSError:
			erreurPort="Erreur : le port "+str(self.PORT)+" est déjà utilisé."
			self.listButtons[4].config(text = erreurPort)
		else:
			self.listButtons[4].config(text = "")
			self.thread = threading.Thread(target = self.httpd.serve_forever)
			self.thread.daemon = True

	def startAndStop(self):
		'''Fontion qui met en place le serveur http ou non en fonction de l'état de celui-ci.
		Param : - ServerWeb (modif)
		Return : None
		'''
		if not self.lancer:
			self.start()
		else:
			self.stop()
		self.lancer = not self.lancer

	def setListButtons(self, listButtons):
		'''Fonction qui met la liste des boutons et des labels dans la variable associé et initialise le threading.
		Param : - ServerWeb (modif)
		Return : None
		'''
		self.listButtons = listButtons
		self.initialisationThread()

	def stop(self):
		'''Fonction qui arrete le serveur http et actualise les boutons et le status en cours.
		Param : - ServerWeb (modif)
		Return : None
		'''
		if self.lancer:
			self.httpd.shutdown()
			self.listButtons[0].config(text = "START")
			self.listButtons[3].config(text = "Status : Off", fg="blue")

	def start(self):
		'''Fonction qui met en route le serveur http.
		Param : - ServerWeb (modif)
		Return : None
		'''
		self.thread = threading.Thread(target = self.httpd.serve_forever)
		self.thread.start()
		self.listButtons[0].config(text = "STOP")
		self.listButtons[3].config(text = "Status : On \n sur http://127.0.0.1:"+str(self.PORT), fg="green")



def fenetre():
	'''Construit la fenetre principale "root"
	params : None
	Return : root (object tkinter)
	'''
	root = Tk()
	root.title('Formation')
	root.geometry("400x200")
	return root

def gestionnaireGrille(root):
	'''Configure la taille de la grille.
	Params : root (object tkinter) = la fenetre principale
	Return : None
	'''
	root.rowconfigure(5, weight=1)
	root.columnconfigure(2, weight=1)

def creationBoutons(root,server):
	'''Creer une liste de boutons et de labbels
	Params : root (object tkinter) = la fenetre principale
	Return : listButtons (list(Button))
	'''
	listButtons = []
	root.protocol("WM_DELETE_WINDOW", lambda:[server.stop(),root.destroy()])
	listButtons.append(Button(root, text='START', command= lambda: server.startAndStop()))
	listButtons.append(Button(root, text='Quitter', command= lambda:[server.stop(),root.destroy()]))
	listButtons.append(Label(root, text=""))
	listButtons.append(Label(root, text="Status : Off", fg="blue", font=("Helvetica", 10)))
	listButtons.append(Label(root, text="Erreur", fg="red", font=("Helvetica", 16)))
	return listButtons

def placementBoutons(listButtons):
	'''Placement des boutons dans la grille
	Params : listButtons (list(Button))
	Return : None
	'''
	listButtons[0].grid(row=0, column=2)
	listButtons[1].grid(row=1, column=2)
	listButtons[2].grid(row=3, column=0, columnspan=3, sticky='nesw')
	listButtons[3].grid(row=4, column=0, columnspan=3, sticky='ns')
	listButtons[4].grid(row=5, column=0, columnspan=3, sticky='ns')

def main(PORT=8000):
	'''Fonction principale
		Param : - PORT (int) : le port pour le serveur http.
		Return : None
	'''
	server = ServerWeb(PORT)
	root = fenetre()
	gestionnaireGrille(root)
	listButtons = creationBoutons(root,server)
	server.setListButtons(listButtons)
	placementBoutons(listButtons)
	root.mainloop()

if __name__ == "__main__":
	'''condition pour démarrer la fonction principale.
	verifie si l'utilisateur à mit le fichier port.
	'''
	try:
		tmp = int(open("port.txt","r").read())
	except (FileNotFoundError,ValueError):
		main()
	else:
		main((8000,tmp)[tmp>1])