import pygame, sys, time, random
from pygame.locals import *

# Initialize pygame
pygame.init()

###### C L A S S E S ######
# Make a class full of all variables (for easy importation)
class Variables:
    def __init__(self):
        # Make the colors
        self.WHITE = (255,255,255)
        self.RED = (255, 0, 0)
        self.GREEN = (0, 255, 0)
        self.BLUE = (0, 0, 255)
        self.BLACK = (0,0,0)
        
        # Make a window
        self.WINDOW_WIDTH = 620
        self.WINDOW_HEIGHT = 620
        self.window_surface = pygame.display.set_mode((self.WINDOW_WIDTH, self.WINDOW_HEIGHT),0, 32)
        pygame.display.set_caption('Snake')

        # Set up direction variables
        self.DOWN = 'down'
        self.UP = 'up'
        self.LEFT = 'left'
        self.RIGHT = 'right'

        self.MOVE_SPEED = 20

        # Make the calock and FPS
        self.clock = pygame.time.Clock()
        self.FPS = 5

        # Snake length starts at 100 pixels, but move speed streches it out
        self.length = 100
        self.length = self.length//self.MOVE_SPEED

        # Count (for list purposes)
        self.count = 0

        # Make x and y lists
        self.x_list = []
        self.y_list = []


# Make an apple class
class Apple:
    def __init__(self, variables):
        # Make an attribute to contain all of the variables
        self.variables = variables

        # Make the actual apple object (at 0,0 temporarily)
        self.apple = pygame.Rect(0, 0, 20, 20)

        # Give the apple a color
        self.color = self.variables.RED

        # Randomize the coordinates of the apple
        self.get_new_coordinates()

    # Change the coordinates of the apple to a new random location
    def get_new_coordinates(self):
        # Get a random number 1-30 (When multiplied by 20, it will be on the grid, and between 20 and 60)
        random_number_for_x = random.randint(1, 30)

        # Multiply it by 20 so that it is on the grid
        # Apply the random number to the apple's x coordinate
        self.apple.x = ((random_number_for_x) * 20)

        # Get a new random number for the apple's y coordinate
        random_number_for_y = random.randint(1, 30)

        # Fit it into the grid, and apply it to apple.y
        self.apple.y = ((random_number_for_y) * 20)

    # Draw the apple onto the screen
    def draw_apple(self):
        pygame.draw.rect(self.variables.window_surface, self.color, self.apple)
    
    # Make a method to easily randomize the coordinates and draw the apple simultaneous
    def make_apple(self):
        self.get_new_coordinates()
        self.draw_apple()
    

class PlayerHead:
    def __init__(self, variables):
        # Make an attribute to contain all of the variables and constants
        self.variables = variables

        # Make the head object
        self.head = pygame.Rect(20, 20, 20, 20)

        # Give the head a color
        self.color = self.variables.GREEN

        # Make an attribute containing the direction the head is going
        self.direction = self.variables.RIGHT

    # Make a method to move the head
    def move(self):
        # If the head's direction is up
        if self.direction == self.variables.UP:
            # Move the head up
            self.head.y -= self.variables.MOVE_SPEED

        # If the head's direction is down
        elif self.direction == self.variables.DOWN:
            # Move the head down
            self.head.y += self.variables.MOVE_SPEED

        # If the head's direction is right
        elif self.direction == self.variables.RIGHT:
            # Move the head to the right
            self.head.x += self.variables.MOVE_SPEED

        # If the head's direction is left
        elif self.direction == self.variables.LEFT:
            # Move the head to the left
            self.head.x -= self.variables.MOVE_SPEED
        
        # Add the player's coordinates to a running list, for the tail to follow
        self.variables.x_list.append(self.head.x)
        self.variables.y_list.append(self.head.y)

    # Draw the head onto the screen
    def draw(self):
        pygame.draw.rect(self.variables.window_surface, self.color, self.head)
    
    # Check if the head is off of the screen
    def check_if_off_screen(self):
        if (self.head.x < 0) or (self.head.y < 0) or (self.head.x > self.variables.WINDOW_WIDTH) or (self.head.y > self.variables.WINDOW_HEIGHT):
            self.die()
    
    # Kill the player
    def die(self):
        pygame.quit()
        sys.exit()
    

# Make the Tail object
class PlayerTail:
    def __init__(self, variables):
        # Make an attribute containing all variables and constants
        self.variables = variables

        # Make the tail (width and height are 20 to stay on the grid)
        self.tail = pygame.Rect(0, 0, 20, 20)

        # Give the tail a color
        self.color = self.variables.BLACK

    # Move the tail to follow the head
    def move(self):
        # Check if the snake is long enough for the tail to move without deleting the head
        if self.variables.count >= self.variables.length:
            # Find where the head was, exactly one snake length ago
            index = (self.variables.count - self.variables.length)

            # Change the tail's x position to the place that the head used to be in
            self.tail.x = self.variables.x_list[index]

            # Change the tail's y position to the place that the head used to be in
            self.tail.y = self.variables.y_list[index] 
    
    # Draw the tail onto the screen
    def draw(self):
        pygame.draw.rect(self.variables.window_surface, self.color, self.tail)
    


###### D E F I N I T I O N S ######
# Make an object with all of the variables inside of it
variables = Variables()

# Make an apple
apple = Apple(variables)

# Make the player's head
head = PlayerHead(variables)

# Make the player's tail
tail = PlayerTail(variables)

# Put an apple on the screen
apple.make_apple()


###### M A I N  L O O P ######
# Create a sentinal to contain the status of the player
dead = False
while not dead:

    # Pygame events loop
    for event in pygame.event.get():
        # If someone clicks on the 'x' in the top corner
        if event.type == QUIT:
            # End the game
            pygame.quit()
            sys.exit()

        # Take keyboard input
        if event.type == KEYDOWN:

            # If the player presses the left key
            if event.key == K_LEFT or event.key == K_a:
                # Move the head to the left
                head.direction = variables.LEFT

            # If the player presses the right key 
            if event.key == K_RIGHT or event.key == K_d:
                # Move the head to the right
                head.direction = variables.RIGHT

            # If the player presses the up key
            if event.key == K_UP or event.key == K_w:
                # Move the head upwards
                head.direction = variables.UP

            # If the player presses the down key
            if event.key == K_DOWN or event.key == K_s:
                # Move the head downwards
                head.direction = variables.DOWN

            # If the player uses the cheat key
            if event.key == K_g:
                # Make the snake longer
                variables.length += 1
    
    # This is where I would blank out the screen, but I won't

    # Move the head
    head.move()

    # Move the tail
    tail.move()

    # Draw the head
    head.draw()

    # Draw the tail
    tail.draw()

     # Check if the snake has eaten the apple
    if head.head.x == apple.apple.x and head.head.y == apple.apple.y:
        variables.length += 1
        apple.make_apple()
    
    # Check if the snake is off the screen
    head.check_if_off_screen()

    # Increase the count by one
    variables.count += 1

    # Update the display
    pygame.display.update()

    # Wait until the next frame
    variables.clock.tick(variables.FPS)
