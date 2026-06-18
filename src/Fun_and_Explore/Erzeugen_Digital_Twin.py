from PIL import Image,ImageDraw,ImageOps
import matplotlib.pyplot as plt
import numpy as np
import os

def Startpunkt(bild):
    '''
    Funktion zum bestimmen des Startpixel eines Bildes. Das entsprechende Bild muss angegeben werden.
    '''
    Breite,Höhe = bild.size
    Breite -=1
    Höhe -= 1
    Zwischenstück = Höhe-1                                           #durchsuchung der Reichen vom unteren 
    for i in range(Breite*Höhe):                                     #rechten Pixel nach dem ersten schwarzen
        aktuellesPixel = Breite,Höhe
        Pixelwert = bild.getpixel(aktuellesPixel)
        if Pixelwert <= 50:                                 #geändert
            if bild.getpixel((aktuellesPixel[0]-1,aktuellesPixel[1]+1)) <= 50:  #geändert
                Breite -= 1
                Höhe = Zwischenstück
                pass
            else:
                break
        else:
            if Höhe == 0:
                Breite = Breite-1
                Höhe = Zwischenstück
            else:
                Höhe = Höhe-1
    return Breite,Höhe

def Startpunkt_neu(bild):
    # In NumPy-Array umwandeln
    image_array = np.asarray(bild, dtype=np.uint8)

    # Alle schwarzen Pixel finden (Pixelwert 0)
    coords = np.column_stack(np.where(image_array == 0))

    if coords.size > 0:
        # Bildgröße holen (Höhe, Breite)
        height, width = image_array.shape

        # Rechte untere Ecke als Referenzpunkt
        bottom_right = np.array([height - 1, width - 1])

        # Pixel mit geringster euklidischer Distanz zur unteren rechten Ecke finden
        nearest_pixel = min(coords, key=lambda c: np.linalg.norm(c - bottom_right))

        # print("Schwarzer Pixel mit geringstem Abstand zur unteren rechten Ecke:", nearest_pixel)
        return int(nearest_pixel[1]), int(nearest_pixel[0])
    else:
        print("Kein schwarzer Pixel gefunden.")
        return 0, 0

def DickederLinie(bild, Breite,Höhe):
    Liniendicke = 0

    while True:
        pixel_value = bild.getpixel((Breite,Höhe))
        if pixel_value > 0: #and bild.getpixel((Breite-1,Höhe-1)) > 0:
            break

        Liniendicke += 1
        Breite -= 1
        Höhe -= 1
    
    #print("Liniendicke: ",Liniendicke)

    Liniendicke = Liniendicke // 2
    return Liniendicke

def zeichnen(bild, Eckenliste,Verbindungsliste, Liniendicke):
    image = Image.new('RGB', (bild.size), 'white')
    draw = ImageDraw.Draw(image)

    for element in Verbindungsliste:
        draw.line(element,fill = 'black', width=Liniendicke)

    for element in Eckenliste:
         #draw.point(element,fill = 'red')
         draw.rectangle((((element[0] - 0) - Liniendicke/2 , (element[1] - 0 )- Liniendicke/2),(element[0] + Liniendicke/2, element[1] + Liniendicke/2)),fill='red')
         #draw.line(((element[0] - 1) - Liniendicke/2, (element[1] -1),(element[0]+Liniendicke/2, element[1])), fill= 'red', width=Liniendicke)
         pass
    
    try:
        overlay = Image.open('logo_small.png')
        overlay = overlay.resize((200,150))

        image_w, image_h = image.size
        overlay_w, overlay_h = overlay.size

        x = (image_w - overlay_w) // 2
        y = 0

        image.paste(overlay, (x,y))
    except FileNotFoundError:
        pass

    image.save('Ausgegeben.png')

    plt.imshow(image)
    plt.axis('off')
    plt.show()

def Korrektur_Mitte_der_Linie(bild, Breite, Höhe, Code, Liniendicke):
    if Code == 0 or Code == 2:
        if Code == 0:
            tmp_Höhe = Höhe + Liniendicke
        elif Code == 2:
            tmp_Höhe = Höhe - Liniendicke

        tmpX = Breite
        maxX = Breite
        minX = Breite
        while True:
            if check_schwarz(bild, tmpX,tmp_Höhe):
                tmpX += 1
            else:
                maxX = tmpX - 1
                break
        tmpX = Breite
        while True:
            if check_schwarz(bild, tmpX,tmp_Höhe):
                tmpX -= 1
            else:
                minX = tmpX + 1
                break

        korrekte_Breite = (maxX - minX) // 2 + minX
        korrekte_Höhe = Höhe
    else:
        if Code == 1:
            tmp_Breite = Breite - Liniendicke
        elif Code == 3:
            tmp_Breite = Breite + Liniendicke

        tmpY = Höhe
        maxY = Höhe
        minY = Höhe
        while True:
            if check_schwarz(bild, tmp_Breite,tmpY):
                tmpY += 1
            else:
                maxY = tmpY - 1
                break
        tmpY = Höhe
        while True:
            if check_schwarz(bild, tmp_Breite,tmpY):
                tmpY -= 1
            else:
                minY = tmpY + 1
                break

        korrekte_Höhe = (maxY - minY) // 2 + minY
        korrekte_Breite = Breite

    return korrekte_Breite, korrekte_Höhe

def MittederEcke(bild, Breite,Höhe,Code,Liniendicke):
    Breite, Höhe = Korrektur_Mitte_der_Linie(bild, Breite,Höhe,Code,Liniendicke)
    if Code == 0:
        if Check_ob_Sackgasse(bild, Breite,Höhe,Liniendicke) == True:
            pass
        else:
            Höhe -= Liniendicke
    elif Code == 1:
        if Check_ob_Sackgasse(bild, Breite,Höhe,Liniendicke) == True:
            pass
        else:
            Breite += Liniendicke
    elif Code == 2:
        if Check_ob_Sackgasse(bild, Breite,Höhe,Liniendicke) == True:
            pass
        else:
            Höhe += Liniendicke
    elif Code == 3:
        if Check_ob_Sackgasse(bild, Breite,Höhe,Liniendicke) == True:
            pass
        else:
            Breite -= Liniendicke
    return Breite, Höhe

def Check_ob_Sackgasse(bild, Breite,Höhe,Liniendicke):
    Seite_oben = check_ob_linie(bild, Breite,Höhe,Liniendicke,1,True)
    Seite_unten = check_ob_linie(bild, Breite,Höhe,Liniendicke,-1,True)
    Seite_links = check_ob_linie(bild, Breite,Höhe,Liniendicke,1,False)
    Seite_rechts = check_ob_linie(bild, Breite,Höhe,Liniendicke,-1,False)
    # print("Sackgasse: Seite_oben: ", Seite_oben, " Seite_unten: ", Seite_unten, " Seite_rechts: ", Seite_rechts, " Seite_links: ", Seite_links)

    counter = 0
    if Seite_oben:                                    #geändert
        counter +=1
    if Seite_unten:                                   #geändert
        counter +=1
    if Seite_links:                                    #geändert
        counter +=1
    if Seite_rechts:                                   #geändert
        counter +=1

    if counter == 1:
        return True
    else:
        return False

def Eckencheck(bild, Breite,Höhe,Liniendicke,zwischenliste):
    Seite_oben = check_ob_linie(bild, Breite,Höhe,Liniendicke,1,True)
    Seite_unten = check_ob_linie(bild, Breite,Höhe,Liniendicke,-1,True)
    Seite_links = check_ob_linie(bild, Breite,Höhe,Liniendicke,1,False)
    Seite_rechts = check_ob_linie(bild, Breite,Höhe,Liniendicke,-1,False)
    # print("Seite_oben: ", Seite_oben, " Seite_unten: ", Seite_unten, " Seite_rechts: ", Seite_rechts, " Seite_links: ", Seite_links)

    #print("br: ", Breite, "ld: ", Liniendicke)
    #print("h: ", Höhe)

    if Seite_oben:                                    #geändert
        zwischenliste.append((Breite,Höhe,0))
    if Seite_rechts:                                   #geändert
        zwischenliste.append((Breite,Höhe,1))
    if Seite_unten:                                   #geändert
        zwischenliste.append((Breite,Höhe,2))
    if Seite_links:                                    #geändert
        zwischenliste.append((Breite,Höhe,3))
    

def check_schwarz(bild, Breite, Höhe):
    tmpx, tmpy = bild.size
    if Breite < 0 or Höhe < 0 or Breite >= tmpx or Höhe >= tmpy:
        return False
    else:
        return bild.getpixel((Breite, Höhe)) == 0              #geändert

def Höhenbeweger(bild, Breite,Höhe,Liniendicke, negative = True):
    value = 1
    if negative:
        value = -1
    Höhe += value
    counter = 0
    while True:
        if check_schwarz(bild, Breite,Höhe):
            if counter == Liniendicke *4:
                Breite, Höhe = Korrektur_Mitte_der_Linie(bild, Breite, Höhe, 1 + value, Liniendicke)
                counter = 0
            Seite_links = check_ob_linie(bild, Breite,Höhe,Liniendicke,-1,False)
            Seite_rechts = check_ob_linie(bild, Breite,Höhe,Liniendicke,1,False)
            if Seite_links or Seite_rechts:
                # print("Seite gefunden Seite_links: ", Seite_links, " Seite_rechts: ", Seite_rechts)
                break

            Höhe += value
            counter += 1
        else:
            break
    
    return Breite ,Höhe

def Breitenbeweger(bild, Breite,Höhe,Liniendicke,negative = True):
    value = 1
    if negative:
        value = -1
    Breite += value
    counter = 0
    while True:
        if check_schwarz(bild, Breite,Höhe):
            if counter == Liniendicke *4:
                Breite, Höhe = Korrektur_Mitte_der_Linie(bild, Breite, Höhe, 2 + (-value), Liniendicke)
                counter = 0
            Seite_oben = check_ob_linie(bild, Breite,Höhe,Liniendicke,1,True)
            Seite_unten = check_ob_linie(bild, Breite,Höhe,Liniendicke,-1,True)
            if Seite_oben or Seite_unten:
                # print("Seite gefunden Seite_oben: ", Seite_oben, " Seite_unten: ", Seite_unten)
                break

            Breite += value
            counter += 1
        else:
            break

    return Breite, Höhe

def check_ob_linie(bild, Breite, Höhe, Liniendicke, value, oben_oder_unten):
    for i in range(1, Liniendicke*2):
        if oben_oder_unten:
            if not check_schwarz(bild, Breite,Höhe-(i*value)):
                return False
        else:
            if not check_schwarz(bild, Breite-(i*value),Höhe):
                return False
    return True

def Verbindung(bild, Breite,Höhe,Code,Liniendicke):
    if Code == 0:
        Höhe -= Liniendicke*2
        Breite_neu, Höhe_neu = Höhenbeweger(bild, Breite, Höhe, Liniendicke, True)
    if Code == 1:
        Breite += Liniendicke*2
        Breite_neu, Höhe_neu = Breitenbeweger(bild, Breite, Höhe, Liniendicke, False)
    if Code == 2:
        Höhe += Liniendicke*2
        Breite_neu, Höhe_neu = Höhenbeweger(bild, Breite, Höhe, Liniendicke, False)
    if Code == 3:
        Breite -= Liniendicke*2
        Breite_neu, Höhe_neu = Breitenbeweger(bild, Breite, Höhe, Liniendicke, True)
    return Breite_neu, Höhe_neu

def Selbe_Ecke(ecke1, ecke2, Liniendicke):
    # print("Ecke 1: ", ecke1," Ecke 2:" , ecke2)
    if abs(ecke1[0] - ecke2[0]) < Liniendicke - 3 and abs(ecke1[1] - ecke2[1]) < Liniendicke - 3:
        return True
    else:

        return False
    
def Selbe_Verbindung(Verbindung1, Verbindung2, Liniendicke):
    # print("Verbindung 1: ", Verbindung1, " Verbindung 2: ", Verbindung2)
    if Selbe_Ecke((Verbindung1[0], Verbindung1[1]), (Verbindung2[0], Verbindung2[1]), Liniendicke) and Selbe_Ecke((Verbindung1[2], Verbindung1[3]), (Verbindung2[2], Verbindung2[3]), Liniendicke):
        return True
    else:
        return False

def listenprüfer(Original_Breite, Original_Höhe, Breite, Höhe, Liniendicke, Eckenliste, Probeliste, Verbindungsliste):
    ecke_existiert = False
    for ecke in Eckenliste:
        if Selbe_Ecke(ecke, (Breite, Höhe), Liniendicke):
            ecke_existiert = True

    if not ecke_existiert:
        # print("Ecke gespeichert")
        Eckenliste.append((Breite,Höhe))
        Probeliste.append((Breite,Höhe))

    if len(Verbindungsliste) == 0:
        Verbindungsliste.append((Original_Breite,Original_Höhe,Breite,Höhe))
    else:
        verbindung_existiert = False
        for verbindung in Verbindungsliste:
            if Selbe_Verbindung(verbindung, (Original_Breite,Original_Höhe,Breite,Höhe), Liniendicke) or Selbe_Verbindung(verbindung, (Breite,Höhe,Original_Breite,Original_Höhe), Liniendicke):
                verbindung_existiert = True

        if not verbindung_existiert:
            # print("Verbindung gespeichert")
            Verbindungsliste.append((Original_Breite,Original_Höhe,Breite,Höhe))

    return Eckenliste, Probeliste, Verbindungsliste

if __name__ == '__main__':
    base_name = "Maze"
    formats = ["jpg", "jpeg", "png", "bmp", "gif", "tiff", "webp"]

    bild = None
    for ext in formats:
        file_name = f"{base_name}.{ext}"
        if os.path.exists(file_name):
            try:
                bild = Image.open(file_name)
                print(f"Opened {file_name}")
                break
            except Exception as e:
                print(f"Failed to open {file_name}: {e}")

    if bild is None:
        print("Fehler: Keine Bilddatei gefunden (Maze.jpg/png/...)")
        exit(1)

    plt.imshow(bild)
    plt.axis('off')
    plt.show()
    bild = bild.convert('L')
    bild = ImageOps.expand(bild, border=(50, 200, 50, 50), fill=255)

    Eckenliste = []
    Probeliste = []
    Verbindungsliste = []
    zwischenliste = []
    Verbindungsliste = []

    Breite, Höhe = bild.size
    for x in range(Breite-1):
        for y in range(Höhe-1):
            if bild.getpixel((x,y)) > 140:
                bild.putpixel((x,y),255)
            else:
                bild.putpixel((x,y),0) 
        
    # bild.show()

    #Breite, Höhe = Startpunkt(bild)
    Breite, Höhe = Startpunkt_neu(bild)
    # print((Breite,Höhe))
    Liniendicke = DickederLinie(bild, Breite,Höhe)
    Breite -= Liniendicke
    Höhe -= Liniendicke
    # print((Breite,Höhe))
    
    #Breite = 79
    #Höhe = 44
    #Liniendicke = 2
    
    Eckencheck(bild, Breite,Höhe,Liniendicke, zwischenliste)
    Eckenliste.append((Breite,Höhe))

    print("Start Eckensuche")
    
    while len(zwischenliste) != 0:
        if len(zwischenliste) > 50:
            print(zwischenliste)
            break
        # print("zw: ",zwischenliste)
        Breite,Höhe,Code = zwischenliste[0]
        zwischenliste.pop(0)
        # print("zw: ",zwischenliste)
        Breite_neu, Höhe_neu = Verbindung(bild, Breite,Höhe,Code,Liniendicke)
        Breite_neu, Höhe_neu = MittederEcke(bild, Breite_neu, Höhe_neu, Code, Liniendicke)

        Eckenliste, Probeliste, Verbindungsliste = listenprüfer(Breite, Höhe, Breite_neu, Höhe_neu, Liniendicke, Eckenliste, Probeliste, Verbindungsliste)
        # print("CL: ",Verbindungsliste, "EL: ", Eckenliste, "PL: ", Probeliste)
        if len(Probeliste) != 0:
            Breite, Höhe = Probeliste[0]
            #print(Probeliste,":pb")
            Probeliste.pop(0)
            
            Eckencheck(bild, Breite, Höhe, Liniendicke, zwischenliste)
        else:
            pass

        #zeichnen(Eckenliste,Verbindungsliste, Liniendicke)
        #input("Drücke Enter, um fortzufahren...")


    print(Eckenliste) 
    print(Verbindungsliste)

    korrigierte_Verbindungsliste = []

    for verbindung in Verbindungsliste:
        erste_ecke = False
        zweite_ecke = False
        for i, ecke in enumerate(Eckenliste):
            if abs(ecke[0] - verbindung[0]) == 0 and abs(ecke[1] - verbindung[1]) == 0:
                erste_ecke = True
            if abs(ecke[0] - verbindung[2]) == 0 and abs(ecke[1] - verbindung[3]) == 0:
                zweite_ecke = True

        if not erste_ecke or not zweite_ecke:
            print("Fehler bei Verbindung: ", verbindung)
            tmp_ecke1 = None
            tmp_ecke2 = None
            for ecke in Eckenliste:
                if abs(ecke[0] - verbindung[0]) < Liniendicke - 3 and abs(ecke[1] - verbindung[1]) < Liniendicke - 3:
                    tmp_ecke1 = ecke
                    print("Ecke: ", tmp_ecke1)
                if abs(ecke[0] - verbindung[2]) < Liniendicke - 3 and abs(ecke[1] - verbindung[3]) < Liniendicke - 3:
                    tmp_ecke2 = ecke
                    print("Ecke: ", tmp_ecke2)

            if tmp_ecke1 is not None and tmp_ecke2 is not None:
                korrigierte_Verbindungsliste.append((tmp_ecke1[0], tmp_ecke1[1], tmp_ecke2[0], tmp_ecke2[1]))
                print("Korrigierte Verbindung: ", korrigierte_Verbindungsliste[-1])
            else:
                print("Warnung: Verbindung konnte nicht korrigiert werden: ", verbindung)
        else:
            korrigierte_Verbindungsliste.append(verbindung)

    Verbindungsliste = korrigierte_Verbindungsliste
    
    zeichnen(bild, Eckenliste,Verbindungsliste, Liniendicke)

    datei = open('DijkstraWerteEcke.txt','w')
    for tuple in Eckenliste:
        datei.write(str(tuple) + '\n')
    datei.close()
    datei2 = open('DijkstraWerte.txt','w')
    for tuple in Verbindungsliste:
        datei2.write(str(tuple) + '\n')
    datei2.close()

    datei3 = open('Liniendicke.txt','w')
    datei3.write(str(Liniendicke*2))
    datei3.close()

