# Instructions: in order to play the game, one should change the angle and velocity 
# with the arrows, press enter to launch the ball towards the target, and if delete key 
# is pressed the ball will be reset without changing the target location
# continue playing until time runs out

import Draw
import time
import random
import math

#Global variables
MAX_TIME = 60
ANGLE_CHANGE = 5 
VELOCITY_CHANGE = 10 
CANVAS_WIDTH = 700 
CANVAS_HEIGHT = 500

    
def drawScreen(dx,dy, angle, timeRemaining, velocity, score, targetY, animating):
    
    Draw.clear()
    
    #the screen statistics
    Draw.string("Angle: " + str(angle) + "°", CANVAS_WIDTH - 150, 10)
    Draw.string("Velocity: " + str(velocity), CANVAS_WIDTH - 150, 30)
    Draw.string("Time Remaining: " + str(int(timeRemaining)),CANVAS_WIDTH - 150, 50)
    Draw.string("Score: " + str(score),CANVAS_WIDTH - 150, 70)   
        
    #Draw the target 
    Draw.setColor(Draw.RED)
    Draw.filledRect(0,targetY,20,100)
    
    #Draw the ball
    Draw.setColor(Draw.BLACK)
    Draw.filledOval(dx,dy,20,20) #the ball being launched
    
    # Only show the line for angle when not moving (animating)
    if not animating:
        
        #create the line -> will increase and decrease with input velocity
        lineLength = (50 * (.005 * velocity))
        
        #start line at center of the ball
        lineStartX = dx + 10 
        lineStartY = dy + 10
        
        #end point of line using trig(find x and y point of end of line)
        lineEndX = lineStartX - lineLength * math.cos(math.radians(angle))
        lineEndY = lineStartY - lineLength * math.sin(math.radians(angle))
        
        
        # Draw line that represents the angle
        Draw.line(lineStartX, lineStartY, lineEndX, lineEndY)
    
    Draw.show()
    
    return dx, dy, angle, timeRemaining, velocity, score

def getTime(gameStart):
    
    #gamestart in the main
    elapsed = time.time() - gameStart #update elapsed time
    
    #count downwards (for the screen stat), can't go below 0
    remaining = max(0,MAX_TIME - elapsed) 
    
    return elapsed, remaining

    
def positionUpdate(velocity, angle, deltaT):
   
    #x(t) = xi + (vix * t) -> x component position
    # subtracting the initial position since going from greater position to smaller one
    dx = ( CANVAS_WIDTH - 30) - velocity* math.cos(math.radians(angle)) * deltaT
    
    #y(t) = yi + (viy * t) - (0.5 * g * t^2) -> y component position
    #gravity is negative
    dy = (CANVAS_HEIGHT - 30 - velocity * math.sin(math.radians(angle))\
        * deltaT) - ( 0.5 * -9.81 * deltaT ** 2)

    return dx,dy
    
    
def main():
    
    #create the canvas
    Draw.setCanvasSize(CANVAS_WIDTH,CANVAS_HEIGHT)
    
    #starting angle, velocity, score
    angle = 45 
    velocity = 180
    score = 0
    
    #set to false unless enter key pressed
    animating = False  
    #variable for when game has begun
    gameStart = time.time()
    
    #A new y point for the target
    #'CANVAS_HEIGHT-100' so wont go below
    targetY = random.uniform(0, CANVAS_HEIGHT-100) 
    
    dx = CANVAS_WIDTH - 30
    dy = CANVAS_HEIGHT - 30   
    
    elapsed, remaining = getTime(gameStart)
    
    #Animating: True if a projectile is in flight, False otherwise
    while elapsed < MAX_TIME:
        elapsed, remaining = getTime(gameStart)
        
        if Draw.hasNextKeyTyped():
            key = Draw.nextKeyTyped()
            if not animating: #only can adjust angle and velocity when not animating (cant adjust mid-animation)
                
                if key == "Left":    #left arrow = minus angle amount, cant go below 0
                    angle= max(0, angle - ANGLE_CHANGE)
                
                elif key == "Right":  #right arrow = plus angle amount, cant go above 90 degrees
                    angle = min(90, angle + ANGLE_CHANGE)
                
                elif key == "Up":       #up arrow = plus velocity amount
                        velocity+=VELOCITY_CHANGE
                    
                elif key =="Down":  #down arrow = minus velocity amount, cant be a negative
                        velocity = max(0,velocity - VELOCITY_CHANGE)
                        
                #allow enter and delete to run while animating    
            if key == "BackSpace": 
                #if hit delete key, shut off animation and reset ball position
                animating = False 
                dx, dy = CANVAS_WIDTH - 30, CANVAS_HEIGHT - 30
                
            
            #if hit enter key and animation hasnt started, turn on animation        
            elif key == "Return" and not animating: 
                animating = True 
                t0 = time.time()
                
        if animating:
            deltaT = time.time() - t0
            #update the position for every change in time (according to physics)
            dx, dy = positionUpdate(velocity, angle, deltaT)
            
                    
                    
            #if ball hit the target
            if 0 <= dx <= 20 and targetY <= dy <= targetY +100:
                score += 1
                 
                #change the target to random y point on the left side of screen  
                targetY = random.uniform(0, CANVAS_HEIGHT - 100) 
                dx, dy = CANVAS_WIDTH - 30, CANVAS_HEIGHT - 30  # Reset ball position                
                
                animating = False
                    
            #if ball didnt hit the target, and is going off canvas
            if dx <= 5 or dy > CANVAS_HEIGHT or dy <= 5 :
                    
                animating = False       
                dx, dy = CANVAS_WIDTH - 30, CANVAS_HEIGHT - 30  # Reset ball position                
                
                 
        drawScreen(dx,dy, angle, remaining, velocity, score, targetY, animating)
    

        #when times up turn animation off: display time done and final score
        if remaining <= 0:
            animating = False
            
            Draw.clear()  
            Draw.setFontSize(15)
            Draw.string("Time's up!", CANVAS_WIDTH/2 - 60, CANVAS_HEIGHT/2 - 50)
            Draw.string("Final Score: " + str(score), CANVAS_WIDTH/2 - 60, CANVAS_HEIGHT/2 - 30)  
            Draw.show()
    
main()
