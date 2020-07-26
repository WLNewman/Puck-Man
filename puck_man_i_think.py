import pygame
pygame.init()
pygame.font.init()
import math
import random
import time

startTime = time.time()
beginInvin = 0

screen_width = 500
screen_height = 500

win = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Puck-Man, I Think")

global lives
lives = 3
vel = 10
startX = 70
startY = 440
radius = 20
global points
points = 0
invincible = False

red = (255, 0, 0)
green = (0, 255, 0)
pink = (255, 0, 255)
yellow = [255, 255, 0]

uno = [50, 230]
dos = [50, 230]
tres = [50, 230]
velUno = [0, 0]
velDos = [0, 0]
velTres = [0, 0]



#coords for small pellets (probably should use loop to initialize these)

smallCoords = [(66, 70), (91, 70), (116, 70), (141, 70), (166, 70), (191, 70), (216, 70), (241, 70), (266, 70),
	(291, 70), (316, 70), (341, 70), (366, 70), (391, 70), (416, 70), (441, 70), (66, 250), (91, 250), (116, 250),
	(141, 250), (166, 250), (191, 250), (216, 250), (241, 250), (266, 250), (291, 250), (316, 250), (341, 250), (366, 250),
	(391, 250), (416, 250), (441, 250), (66, 430), (91, 430), (116, 430), (141, 430), (166, 430), (191, 430), (216, 430),
	(241, 430), (266, 430), (291, 430), (316, 430), (341, 430), (366, 430), (391, 430), (416, 430), (441, 430),
	(66, 95), (66, 120), (66, 145), (66, 170), (66, 195), (66, 220), (66, 275), (66, 300), (66, 325), (66, 350), (66, 375),
	(66, 400), (266, 95), (266, 120), (266, 145), (266, 170), (266, 195), (266, 220), (266, 275), (266, 300), (266, 325), 
	(266, 350), (266, 375), (266, 400), (441, 95), (441, 120), (441, 145), (441, 170), (441, 195), (441, 220), (441, 275), 
	(441, 300), (441, 325), (441, 350), (441, 375), (441, 400)]
bigCoords = [(160, 160), (160, 340), (355, 160), (355, 340)]

#ghost AI intersections u = up r = right l = left d = down
fourIntersec = [(48, 230), (240, 230), (420, 230)]  #+
ulr = [(140, 415), (240, 415), (335, 230)]          #_|_
uld = [(240, 140), (420, 320)]                      #-|
drl = [(140, 230), (240, 50), (335, 50)]            #T
udr = [(48, 140), (240, 320)]                       #|-
corners = [(48, 50), (420, 50), (48, 415), (420, 415)] #ロ

totalIntersec = [[50, 230], [240, 230], [420, 230], [140, 415], [240, 415], [335, 230], [240, 140], [420, 320], 
[140, 230], [240, 50], [335, 50], [50, 140], [240, 320], [50, 50], [420, 50], [50, 415], [420, 415]]

class Items:          
	#Makes pellets, power pellets, fruit
	def __init__(self, award, color, r, coordinates):
		self.award = award
		self.color = color
		self.r = r
		self.coordinates = coordinates


	def getPoints(self):
		#get the points and delete the pellets
		return self.award
	def drawPellets(self):
		#draw those pellets
		for pellet in range(len(self.coordinates)):
			pygame.draw.circle(win, self.color, self.coordinates[pellet], self.r)
		return self.coordinates


class Ghosts():
	#Ghosts!
	def __init__(self, intersec, color, side, initCoord):
		self.intersec = intersec
		self.color = color
		self.side = side
		self.initCoord = initCoord

	def drawGhost(self):
		#draw the ghost with looping options
		pygame.draw.rect(win, self.color, (self.initCoord[0], self.initCoord[1], self.side, self.side))
		if self.initCoord[0] < 0 - self.side:
			self.initCoord[0] = 500
		elif self.initCoord[0] > 500 + self.side:
			self.initCoord[0] = 0 - self.side
		if self.initCoord[1] < 50:
			self.initCoord[1] = 50
		elif self.initCoord[1] > 415:
			self.initCoord[1] = 415
		return (self.initCoord[0], self.initCoord[1])

	def hitGhost(self, x, y):
		#hit detection
		if math.sqrt(((x - (self.initCoord[0] + 20))**2)+(y - (self.initCoord[1] + 20))**2) <= 1.75 *radius:
			return x

	def moveGhost(self, vel):
		#messy. changes the velocity to move ghost
		right = [10, 0]
		up = [0, -10]
		left = [-10, 0]
		down = [0, 10]
		exception = [30, 30]

############################################
		if self.initCoord in self.intersec: 
	
			choice = random.randrange(4)
			if choice == 1:
				return right
			elif choice == 2:
				return up
			elif choice == 3:
				return left
			else:
				return down

		#fixes bug (the one where at T intersection in middle-left if turn up get stuck on wall)
		elif self.initCoord[0] == 140 and self.initCoord[1] <= 50:
				return down

		else:
			return vel



#		pellets = []
"""		pelX = 66
		pelY = 70
		if pellets == []:
			while pelY < 435:
				if pelX <= 440:
					#Horizontal rows
					for coordinates in range(16):
						pellets.append((pelX, pelY))
						print((pelX,pelY))
						pelX += 3 * self.r + 1
					for pellet in range(len(pellets)):
						pygame.draw.circle(win, self.color, pellets[pellet], self.r)
				if pelX > 440:
					pelX = 66
					pelY += 180
		return pellets		"""


def drawChars(posx, posy):
	#draw all characters, Puck and Ghosts
	win.fill((0, 0, 0))
	pygame.draw.circle(win, yellow, (posx, posy), radius)
	pygame.display.update()

def drawItems(posx, posy):
	#draw the items pac man collects
	pellets = []
	pelX = 66
	pelY = 70
	pelR = 8

	for pellet in range(16):
		coordinates = (66, 70)
		pellets.append(coordinates)
		pelX += 3 * pelR
	for pellet in range(len(pellets)):
		pygame.draw.circle(win, (255, 255, 100), pellets[pellet], pelR)
		pelX += 3 * pelR
		if posx <= pelX + pelR and posy <= pelY + pelR:
			if posx >= pelX - pelR and posy >= pelY - pelR:
				pygame.draw.circle(win, (255, 0, 100), (80, 80), pelR)
				pellets.pop(pellet)

def drawMaze(rad, x, y, velC):
	#This is a mess, it draws the mazes walls, I'm sorry. I used radius as measuring stick.
	#Would update this to be single image, but I'm keeping it to remind me of my mistakes moving forward

	#Top and bottom
	pygame.draw.rect(win, (0, 26, 255), (2 * rad, 2 * rad, screen_width - (4 * rad), screen_height / 100))
	pygame.draw.rect(win, (0, 26, 255), (2 * rad, screen_height - (2 * rad), screen_width - (4 * rad), screen_height / 100))
	#Side and side (l,r,bl,br)
	pygame.draw.rect(win, (0, 26, 255), (2 * rad, 2 * rad, screen_height / 100, (screen_height /2) - (3 * rad)))
	pygame.draw.rect(win, (0, 26, 255), (screen_width - (2 * rad), 2 * rad, screen_height / 100, (screen_height /2) - (3 * rad)))
	pygame.draw.rect(win, (0, 26, 255), (2 * rad, (screen_height / 2) + (rad), screen_height / 100, (screen_height /2) - (3 * rad)))
	pygame.draw.rect(win, (0, 26, 255), (screen_width - (2 * rad), (screen_height / 2) + (rad), screen_height / 100, (screen_height /2) - (3 * rad) + 5))
	#Chunky squares (tl,tlb,trl,trb,bl,blb,br,brb)
	pygame.draw.rect(win, (0, 26, 255), (4.5 * rad, 4.5 * rad, 7.25 * rad, 2.25 * rad))
	pygame.draw.rect(win, (0, 26, 255), (4.5 * rad, 9.25 * rad, 7.25 * rad, 2.25 * rad))
	pygame.draw.rect(win, (0, 26, 255), (14.5 * rad, 4.5 * rad, 2 * rad, 7 * rad))
	pygame.draw.rect(win, (0, 26, 255), (19 * rad, 4.5 * rad, 2 * rad, 7 * rad))
	pygame.draw.rect(win, (0, 26, 255), (4.5 * rad, 13.5 * rad, 2.25 * rad, 7 * rad))
	pygame.draw.rect(win, (0, 26, 255), (9.25 * rad, 13.5 * rad, (2.3 * rad) + 3, 7 * rad))
	pygame.draw.rect(win, (0, 26, 255), (14.5 * rad, 13.5 * rad, 6.5 * rad, 2.25 * rad))
	pygame.draw.rect(win, (0, 26, 255), (14.5 * rad, 18.25 * rad, 6.5 * rad, 2.25 * rad))

	#Side tunnel (l,r,bl,br)
	pygame.draw.rect(win, (0, 26, 255), (0 - (3 * rad), (screen_height /2) - rad - 5, 5 * rad + 5, screen_height / 100))
	pygame.draw.rect(win, (0, 26, 255), (screen_width - (2 * rad), (screen_height /2) - rad - 5, 5 * rad + 5, screen_height / 100))
	pygame.draw.rect(win, (0, 26, 255), (0 - (3 * rad), (screen_height /2) + rad, 5 * rad, screen_height / 100))
	pygame.draw.rect(win, (0, 26, 255), (screen_width - (2* rad), (screen_height /2) + rad, 5 * rad, screen_height / 100))

	#Text at top
	textLives = pygame.font.SysFont('Tahoma', 30)
	textSurfaceLives = textLives.render(f'LIVES: {lives}', False, (255,255,255))
	win.blit(textSurfaceLives, (100, 5))

	textPoints = pygame.font.SysFont('Tahoma', 30)
	textSurfacePoints = textPoints.render(f'POINTS: {points}', False, (255,255,255))
	win.blit(textSurfacePoints, (290, 5))

	pygame.display.update()
	win.fill((0, 0, 0))


#Time for the main event!
while lives >= 0:
	startTime = time.time()

	autorun = True
	pygame.time.delay(100)

	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			lives = -1

	keys = pygame.key.get_pressed()

	#Hit detection
	if keys[pygame.K_ESCAPE]:
		lives = -1

	if keys[pygame.K_LEFT]:
		startX -= vel
		if startX <= 0 - radius:
			#loop around
			startX += screen_width + (2 * radius)
		if startX == (2 * radius) + 20 and startY < (screen_height /2):
			#detect left side top
			startX += vel
		if startX == (2 * radius) + 20 and startY > (screen_height /2):
			#detect left side bottom
			startX += vel
		if startX <= 250 and startX > 236 and startY >= (4 * radius) and startY <= (7.5 * radius):
			#tlt
			startX += vel
		if startX <= 250 and startX > 70 and startY >= (8.5 * radius) and startY <= (12 * radius):
			#tlb
			startX += vel
		if startX > 250 and startY >= 260 and startY <= 330:
			#brt
			startX += vel
		if startX > 250 and startY >= 345 and startY <= 435:
			#brb
			startX += vel
		if startX < 260 and startX > 100 and startY > 250 and startY <= 435:
			#bll,blr square
			startX += vel
		if startX > 260 and startX < 440 and startY > 70 and startY < 250:
			#trt,trb square
			startX += vel

		
	if keys[pygame.K_RIGHT]:
		startX += vel
		if startX >= screen_width + radius:
			startX = 0 - (2 * radius)
		if startX == screen_width - (2 * radius) - 10 and startY < (screen_height /2):
			#detect right side top
			startX -= vel
		if startX == screen_width - (2 * radius) - 10 and startY > (screen_height /2):
			#detect right side bottom
			startX -= vel
		if startX <= (4 * radius) and startY >= (4 * radius) and startY <= (7.5 * radius):
			#tlt
			startX -= vel
		if startX <= (4 * radius) and startY >= (8.5 * radius) and startY <= (12 * radius):
			#tlb
			startX -= vel
		if startX > 260  and startX < 300 and startY >= 260 and startY <= 330:
			#brt
			startX -= vel
		if startX > 260 and startX < 300 and startY >= 345 and startY <= 435:
			#brb
			startX -= vel
		if startX < 260 and startX > 70 and startY > 250 and startY <= 435:
			#bll,blr square
			startX -= vel
		if startX > 260 and startX < 440 and startY > 70 and startY < 250:
			#trt,trb square
			startX -= vel


	if keys[pygame.K_UP] and startY > (3 * radius) + 12:
		startY -= vel
		if startX < (3 * radius) + 5 and startY > (screen_height / 2) - radius:
			#detect left tunnel top
			startY += vel
		if startX > screen_width - (3 * radius) and startY < (screen_height / 2) + radius:
			#detect right tunnel top
			startY += vel
		if startX > (2.75 * radius) + 20 and startX <= (11.75 * radius) + 20 and startY < 241:
			#tlt,ltb square
			startY += vel
		if startX > (12.75 * radius) + 20 and startX <= (20.75 * radius) + 20 and startY >= 315 and startY <= 500:
			#brt,brb square
			startY += vel
		if startX > 75 and startX < 160 and startY > 260 :
			#bll square
			startY += vel
		if startX > 160 and startX < 260 and startY > 260 :
			#blr square
			startY += vel
		if startX > 275 and startX < 350 and startY < 250:
			#tll square
			startY += vel
		if startX > 360 and startX < 440 and startY < 250:
			#tlr square
			startY += vel


	if keys[pygame.K_DOWN] and startY < screen_height - (3 * radius):
		startY += vel
		if startX < (3 * radius) + 5 and startY < (screen_height / 2) + radius:
			#detect left tunnel bottom
			startY -= vel
		if startX > screen_width - (3 * radius) and startY < (screen_height / 2) + radius:
			#detect right tunnel bottom
			startY -= vel
		if startX > (2.75 * radius) + 20 and startX <= (11.75 * radius) + 20 and startY < (9 * radius) + 13:
			#tlt,tlb square
			startY -= vel
		if startX > (12.75 * radius) + 20 and startX <= (20.75 * radius) + 20 and startY >= 260 and startY <= 400:
			#brt square NOTE THE 260 ABOVE MAY CAUSE ERRORS IF MAP CHANGED
			startY -= vel
		if startX > 70 and startX < 160 and startY >= 250:
			#blr square
			startY -= vel
		if startX > 160 and startX < 260 and startY >= 250:
			#blr square
			startY -= vel
		if startX > 275 and startX < 350 and startY < 100:
			#tll square
			startY -= vel
		if startX > 360 and startX < 440 and startY < 100:
			#tlr square
			startY -= vel


	drawChars(startX, startY)
#	drawItems(startX, startY)
	smallPellets = Items(10, (255, 255, 100), 8, smallCoords)
	smallCoords = smallPellets.drawPellets()
	powerPellets = Items(20, (255, 255, 100), 14, bigCoords)
	bigCoords = powerPellets.drawPellets()


	ghostUno = Ghosts(totalIntersec, red, 40, uno)
	ghostDos = Ghosts(totalIntersec, green, 40, dos)
	ghostTres = Ghosts(totalIntersec, pink, 40, tres)

	ghostOne = ghostUno.drawGhost()
	ghostTwo = ghostDos.drawGhost()
	ghostThree = ghostTres.drawGhost()

	velUno = ghostUno.moveGhost(velUno)
	uno[0] += velUno[0]
	uno[1] += velUno[1]
	velDos = ghostDos.moveGhost(velDos)
	dos[0] += velDos[0]
	dos[1] += velDos[1]
	velTres = ghostTres.moveGhost(velTres)
	tres[0] += velTres[0]
	tres[1] += velTres[1]

	drawMaze(radius, startX, startY, vel)
	

	for coords in smallCoords:
		#Hit detections small pellets
		if math.sqrt(((startX - coords[0])**2)+(startY - coords[1])**2) <= radius:
			points += smallPellets.getPoints()
			smallCoords.remove((coords))
	for coords in bigCoords:
		#Hit detections big pellets
		if math.sqrt(((startX - coords[0])**2)+(startY - coords[1])**2) <= radius:
			points += powerPellets.getPoints()
			bigCoords.remove((coords))
			invincible = True
			beginInvin = startTime


	if smallCoords == [] and bigCoords == []:
		#kill program
		lives = -5

	#Ghost hit detection. + 20 because sides = 20 and it's drawn from top left
	if not invincible:
		if ghostUno.hitGhost(startX, startY):
			startX = 70
			startY = 440
			lives -= 1
		if ghostDos.hitGhost(startX, startY):
			startX = 70
			startY = 440
			lives -= 1
		if ghostTres.hitGhost(startX, startY):
			startX = 70
			startY = 440
			lives -= 1	

	if invincible:
		yellow = green      #visual aid
		if ghostUno.hitGhost(startX, startY):
			uno[0] = 50
			uno[1] = 230
			points += 50
		if ghostDos.hitGhost(startX, startY):
			dos[0] = 50
			dos[1] = 230
			points += 50
		if ghostTres.hitGhost(startX, startY):
			tres[0] = 50
			tres[1] = 230
			points += 50


		if startTime - beginInvin >= 5:
			invincible = False
			yellow = (255, 255, 0)
			print("ENDED")

pygame.quit()