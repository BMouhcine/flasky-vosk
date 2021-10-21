##Setup: 
> pip install -r requirements.txt

##Lancer l'app:
> python app.py

##Lancer l'indexation:
Il suffit d'envoyer une requête HTTP POST vers l'endpoint suivant:  `localhost:5000/`.  
La requête HTTP POST doit contenir le fichier media (mp3, wav, etc.)  
une simulation de la requête est comme suit (curl):
> curl --location --request POST '127.0.0.1:5000' --form 'data=@"/C:/Users/asus/Desktop/flasky-vosk-main/flasky-vosk-main/test.wav"'  

cette requête curl doit être construite par analogie dans le front, et tout passera bien :D.
