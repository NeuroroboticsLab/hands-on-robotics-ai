from PIL import Image,ImageDraw
import math
import numpy as np
import matplotlib.pyplot as plt
import os

import argparse

# def minimaleStrecke(Längenliste : list) -> tuple:
#       '''
#       Funktion zum sortieren der zu überprüfenden Verbindungen und bestimmung des neuen Startwertes

#       Argumente:
#             Längenliste(list) : Liste mit den Verbindungen

#       Rückgabe:
#             tuple : neuen Knoten zum überprüfen
#       '''
#       Längenliste = sorted(Längenliste, key=lambda x: x[1])
#       Startwert = Längenliste[0][0]
#       return Startwert




def Dijkstra(Matrix : dict,Wahrheitsliste : dict,Kostenliste : dict,Wegliste : dict,Startknoten : tuple) -> tuple:
      '''
      Dijkstra-Algorithmus

      Argumente:
            Matrix(dict) : 
            Wahrheitsliste(dict) : 
            Kostenliste(dict) :
            Wegliste(dict):
            Startknoten(tuple) : 
            

      Rückgabe:
            tuple : gibt die vollständige Kostenliste und Wegliste zurück
      '''

      Längenliste = []
      
      Kostenliste[Startknoten] = 0
      Wegliste[Startknoten] = None
      for i in range(len(Matrix[Startknoten])):
            element1 = Matrix[Startknoten][i][0][2]
            element2 = Matrix[Startknoten][i][0][3]
            Kostenliste[(element1,element2)] = Kostenliste[Startknoten] + Matrix[Startknoten][i][1]
            Wegliste[(element1,element2)] = (Matrix[Startknoten][i][0][0],Matrix[Startknoten][i][0][1])
            Längenliste.append(((element1,element2),Matrix[Startknoten][i][1]))
      Wahrheitsliste[Startknoten] = True
      #Startknoten = minimaleStrecke(Längenliste)
      Startknoten = Längenliste[0][0]

      while len(Längenliste) != 0:
            if Wahrheitsliste[Startknoten] == False:
                  Längenliste.pop(0)
                  for i in range(len(Matrix[Startknoten])):
                        element1 = Matrix[Startknoten][i][0][2]
                        element2 = Matrix[Startknoten][i][0][3]
                        if Kostenliste[element1,element2] > Kostenliste[Startknoten] + Matrix[Startknoten][i][1]:
                              Kostenliste[(element1,element2)] = Kostenliste[Startknoten] + Matrix[Startknoten][i][1]
                              Wegliste[(element1,element2)] = (Matrix[Startknoten][i][0][0],Matrix[Startknoten][i][0][1])
                        Längenliste.append(((element1,element2),Matrix[Startknoten][i][1]))
                  Wahrheitsliste[Startknoten] = True
                  #Startknoten = minimaleStrecke(Längenliste)
                  Startknoten = Längenliste[0][0]
            else:
                  Längenliste.pop(0)
                  if len(Längenliste) != 0:
                        #Startknoten = minimaleStrecke(Längenliste)
                        Startknoten = Längenliste[0][0]
      
      return Kostenliste, Wegliste

def kürzesterWeg(Kostenliste : dict,Endknoten : tuple) -> None:
      print(Kostenliste[Endknoten])


      #finden der Anschließenden Punkte
      #kosten jedes Nachbar finden (kosten von Starpunkt zum ersten ANchbarpunkt,etc)
      #kosten eintragen
      #Startknoten als Abgearbeitet eintragen
      #Kosten in Liste eintragen und die kürzere finden
      #wieder Step 1-4
      #vergleichen ob der Weg zu angegebenen Punkt kleiner als Vorhandener Weg ist

def Wegbestimmung(Endknoten : tuple, Wegliste : dict) -> list:
      zwischenliste = []
      akpunkt = Endknoten
      zwischenliste.append(akpunkt)
      while Wegliste[akpunkt] != None:
            zwischenliste.append(Wegliste[akpunkt])
            akpunkt = Wegliste[akpunkt]
      return zwischenliste


def zeichnen(zwischenliste : list, bild : Image, Liniendicke: int, Startknoten : tuple = (-1, -1), Endknoten : tuple = (-1,-1), color : str = ("green", "red", "orange", "purple"), erstes_zeichnen: bool = False) -> None:
      image = bild
      draw = ImageDraw.Draw(image)
      Zeichenliste = []
      for element in zwischenliste:
            if Wegliste[element] != None:
                  Zeichenliste.append((element[0],element[1],Wegliste[element][0],Wegliste[element][1]))
            else:
                  pass
      for element in Zeichenliste:
            draw.line(element,fill = color, width=Liniendicke)

      if not erstes_zeichnen:
            draw.rectangle((((Startknoten[0] - 0) - Liniendicke/2 , (Startknoten[1] - 0 )- Liniendicke/2),(Startknoten[0] + Liniendicke/2, Startknoten[1] + Liniendicke/2)),fill='yellow')
      else:
            draw.rectangle((((Startknoten[0] - 0) - Liniendicke/2 , (Startknoten[1] - 0 )- Liniendicke/2),(Startknoten[0] + Liniendicke/2, Startknoten[1] + Liniendicke/2)),fill='gold')
      draw.rectangle((((Endknoten[0] - 0) - Liniendicke/2 , (Endknoten[1] - 0 )- Liniendicke/2),(Endknoten[0] + Liniendicke/2, Endknoten[1] + Liniendicke/2)),fill='blue')

      image.save('AusgegebenDijkstra.png')

def berechne_distanz(punkt1, punkt2):
    return math.sqrt((punkt2[0] - punkt1[0]) ** 2 + (punkt2[1] - punkt1[1]) ** 2)

def Roboterwerte(zwischenliste : list) -> list:
      Roboterliste = []
      tmp = []
      for ecke in reversed(zwischenliste):
            tmp.append(ecke)
      
      for i in range(len(tmp)-1):
            tmpX = tmp[i][0] - tmp[i+1][0]
            tmpY = tmp[i][1] - tmp[i+1][1]

            if abs(tmpX) > abs(tmpY):
                  if tmpX > 0:
                        Roboterliste.append('3')
                  else:
                        Roboterliste.append('1')
            else:
                  if tmpY > 0:
                        Roboterliste.append('0')
                  else:
                        Roboterliste.append('2')

      return Roboterliste      

def get_point(pic, Eckenliste, titel = "Bild"):
      img = np.array(Image.open(pic))
      clicked_point = [(-1, -1)]
      red_clicked = [False]

      def on_click(event):
            if event.xdata is None or event.ydata is None:
                  return
            x, y = int(event.xdata), int(event.ydata)
            if img[y, x, 0] == 255 and img[y, x, 1] == 0 and img[y, x, 2] == 0:
                  clicked_point[0] = (x, y)
                  red_clicked[0] = True
                  plt.close()

      fig, ax = plt.subplots(figsize=(16, 9))
      fig.canvas.manager.set_window_title(titel)
      ax.imshow(img)
      ax.set_title(titel)
      fig.canvas.mpl_connect('button_press_event', on_click)
      plt.axis('off')
      plt.tight_layout()
      plt.show(block=True)

      min_distance = 1000000000
      korrekte_ecke = (-1, -1)
      for ecke in Eckenliste:
            distance = abs(ecke[0] - clicked_point[0][0]) + abs(ecke[1] - clicked_point[0][1])
            if distance < min_distance:
                  min_distance = distance
                  korrekte_ecke = ecke

      return korrekte_ecke

def reset_Matrizen(Eckenliste,Matrix,Wahrheitsliste,Kostenliste,Wegliste,reset_all=True):
      if reset_all:
            for ecke in Eckenliste:
                  Matrix[ecke] = []
                  Wahrheitsliste[ecke] = False
                  Kostenliste[ecke] = 100000000
                  Wegliste[ecke] = []
      else:
            for ecke in Eckenliste:
                  Wahrheitsliste[ecke] = False
                  Kostenliste[ecke] = 100000000
                  Wegliste[ecke] = []

      return Matrix,Wahrheitsliste,Kostenliste,Wegliste

def berechne_Matrizen(Eckenliste):
      Matrix = {}
      Wahrheitsliste = {}
      Kostenliste = {}
      Wegliste = {}

      Matrix,Wahrheitsliste,Kostenliste,Wegliste = reset_Matrizen(Eckenliste,Matrix,Wahrheitsliste,Kostenliste,Wegliste)

      for verbindung in Verbindungsliste:
            Längey = max(verbindung[1],verbindung[3]) - min(verbindung[1],verbindung[3])
            Längex = max(verbindung[0],verbindung[2]) - min(verbindung[0],verbindung[2])
            if Längey >= Längex:
                  distanzen = {key: berechne_distanz(key, (verbindung[0], verbindung[1])) for key in Matrix.keys()}
                  naechster_key = min(distanzen, key=distanzen.get)
                  if naechster_key in Matrix:
                        Matrix[naechster_key].append((verbindung,Längey))

                  distanzen = {key: berechne_distanz(key, (verbindung[2], verbindung[3])) for key in Matrix.keys()}
                  naechster_key = min(distanzen, key=distanzen.get)
                  if naechster_key in Matrix:
                        Matrix[naechster_key].append(((verbindung[2], verbindung[3], verbindung[0], verbindung[1]),Längey)) 
            else:
                  distanzen = {key: berechne_distanz(key, (verbindung[0], verbindung[1])) for key in Matrix.keys()}
                  naechster_key = min(distanzen, key=distanzen.get)
                  if naechster_key in Matrix:
                        Matrix[naechster_key].append((verbindung,Längex))

                  distanzen = {key: berechne_distanz(key, (verbindung[2], verbindung[3])) for key in Matrix.keys()}
                  naechster_key = min(distanzen, key=distanzen.get)
                  if naechster_key in Matrix:
                        Matrix[naechster_key].append(((verbindung[2], verbindung[3], verbindung[0], verbindung[1]),Längex)) 

      for key, value in Matrix.items():
            Matrix[key] = [((key[0], key[1], tupel[0][2], tupel[0][3]), tupel[1]) for tupel in value]

      return Matrix,Wahrheitsliste,Kostenliste,Wegliste
      
if __name__ == '__main__':  

      parser = argparse.ArgumentParser(description="Maze Solver with Dijkstra for Multiple Midwaypoints")
      parser.add_argument("-p","--points", default=1, help="Number of Midwaypoints the robot should take (1-3)", type=int)
      parser.add_argument("-r","--return_home", default=False, help="Bool for letting the robot return to home position", type=bool)
      parser.add_argument("-e","--endless", default=False, help="Bool for letting the robot move endlessly on the given path", type=bool)

      args = parser.parse_args()

      MengeEndpunkte = args.points
      if MengeEndpunkte < 1:
            MengeEndpunkte = 1
      elif MengeEndpunkte > 3:
            MengeEndpunkte = 3
      
      zurueckZumStart = args.return_home
      
      endless = args.endless
      if endless:
            zurueckZumStart = True

      Eckenliste = []
      Verbindungsliste = []

      zwischenliste = []
      Roboterliste = []
      ListeStrecken = []

      bild = Image.open('Ausgegeben.png')
      datei = open('DijkstraWerteEcke.txt','r')
      for Zeile in datei:
            Eckenliste.append(eval(Zeile.strip()))
      datei.close()

      datei2 = open('DijkstraWerte.txt','r')
      for Zeile in datei2:
            Verbindungsliste.append(eval(Zeile.strip()))
      datei2.close()

      datei3 = open('Liniendicke.txt','r')
      for Zeile in datei3:
            Liniendicke = eval(Zeile.strip())
      datei3.close()

      Startknoten = get_point("Ausgegeben.png", Eckenliste, "Klicke auf den Startpunkt")
      
      bild2 = Image.open("Ausgegeben.png")
      draw2 = ImageDraw.Draw(bild2)
      draw2.rectangle((((Startknoten[0] - 0) - Liniendicke/2 , (Startknoten[1] - 0 )- Liniendicke/2),(Startknoten[0] + Liniendicke/2, Startknoten[1] + Liniendicke/2)),fill='gold')
      bild2.save("AusgegebenDijkstra.png")
      
      # Multiple_Points_Dijkstra
      ListeEndpunkte = []
      for i in range(MengeEndpunkte):
            ListeEndpunkte.append(get_point("AusgegebenDijkstra.png", Eckenliste, "Klicke auf den Endpunkt"))
            # print("Liste Endpunkte: ", ListeEndpunkte)
            bild3 = Image.open("AusgegebenDijkstra.png")
            draw3 = ImageDraw.Draw(bild3)
            draw3.rectangle((((ListeEndpunkte[i][0] - 0) - Liniendicke/2 , (ListeEndpunkte[i][1] - 0 )- Liniendicke/2),(ListeEndpunkte[i][0] + Liniendicke/2, ListeEndpunkte[i][1] + Liniendicke/2)),fill='blue')
            bild3.save("AusgegebenDijkstra.png")

      Matrix,Wahrheitsliste,Kostenliste,Wegliste = berechne_Matrizen(Eckenliste)

      if zurueckZumStart:
            MengeEndpunkte += 1
            ListeEndpunkte.append(Startknoten)

      for i in range(MengeEndpunkte):
            if i == 0:
                  Endpunkt = ListeEndpunkte[i]
            else:
                  Startknoten = ListeEndpunkte[i-1]
                  Endpunkt = ListeEndpunkte[i]

            Matrix,Wahrheitsliste,Kostenliste,Wegliste = reset_Matrizen(Eckenliste, Matrix,Wahrheitsliste,Kostenliste,Wegliste, False)
            Kostenliste, Wegliste = Dijkstra(Matrix,Wahrheitsliste,Kostenliste,Wegliste,Startknoten)
            zwischenliste = Wegbestimmung(Endpunkt,Wegliste)

            if i == 0:
                  zeichnen(zwischenliste, bild, Liniendicke, Startknoten, Endpunkt, "green", True)
            elif i == 1:
                  zeichnen(zwischenliste, bild, Liniendicke, Startknoten, Endpunkt, "red")
            elif i == 2:
                  zeichnen(zwischenliste, bild, Liniendicke, Startknoten, Endpunkt, "orange")
            elif i == 3:
                  zeichnen(zwischenliste, bild, Liniendicke, Startknoten, Endpunkt, "purple")

            Roboterliste = Roboterwerte(zwischenliste)
            ListeStrecken.append(Roboterliste)

      datei3 = open('Roboterwerte.txt','w')
      LaengeListeStrecken = len(ListeStrecken)
      for i in range(LaengeListeStrecken):
            if i < LaengeListeStrecken - 1:
                  datei3.write(', '.join(ListeStrecken[i]) + "\n")
            else:
                  datei3.write(', '.join(ListeStrecken[i]))
      datei3.close()

      Roboterliste = [x for Zeile in ListeStrecken for x in Zeile]
      print("Roboterliste:")
      print(Roboterliste)

      ZeilenBegin = []
      Zaehler = 0
      for Zeile in ListeStrecken:
          ZeilenBegin.append(Zaehler)   
          Zaehler += len(Zeile)

      ZeilenBegin = list(map(str, ZeilenBegin))

      print("Beginn neuer Abschnitt:")
      print(ZeilenBegin)

      datei4_name = 'maze.c'
      datei5_name = 'tmp.c'

      datei4 = open(datei4_name,'r')
      datei5 = open(datei5_name,'w')

      for Zeile in datei4:
            if "int int_richtungen" in Zeile:
                  Zeilenteile = Zeile.split('=')
                  Endzeile = Zeilenteile[0] + '= {' + ', '.join(Roboterliste) + '};\n'
                  datei5.write(Endzeile)
            elif "int middle_indices[]" in Zeile:
                  Zeilenteile = Zeile.split('=')
                  Endzeile = Zeilenteile[0] + '= {' + ', '.join(ZeilenBegin[1:]) + '};\n'
                  datei5.write(Endzeile)
            elif "int endless_loop" in Zeile:
                  Zeilenteile = Zeile.split('=')
                  Endzeile = Zeilenteile[0] + '= ' + str(int(endless)) + ';\n'
                  datei5.write(Endzeile)
            else:
                  datei5.write(Zeile)

      datei4.close()
      datei5.close()

      os.remove(datei4_name)
      os.rename(datei5_name, datei4_name)

      image = Image.open("AusgegebenDijkstra.png")
      fig, ax = plt.subplots(figsize=(16, 9))
      ax.imshow(np.array(image))
      ax.set_title("Dijkstra Ergebnis")
      ax.axis('off')
      plt.tight_layout()
      plt.show()
