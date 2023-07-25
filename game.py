import pygame
import sys

from buttons.menu_button import MenuButton
import assets.colours as colours

# Initialize Pygame
pygame.init()

# Constants
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
TILE_SIZE = 32
FPS = 60


"""
beginner: 10 mines, 10x10
intermediate:  40 mines, 16x16
expert: 99 mines,  16 x 30
"""


class Game:
    def __init__(self):
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Minesweeper")
        self.clock = pygame.time.Clock()
        
        self.is_running = True
        self.show_menu = True
        self.handle_menu_buttons = True
        self.dissolve_buttons = False

        self.difficulty = None
        self.buttons = self.init_menu_buttons()

    def run(self):
        while self.is_running:
            self.handle_events()
            self.update()
            self.draw()
            self.clock.tick(FPS)

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.is_running = False

            if self.handle_menu_buttons:
                for button in self.buttons:
                    self.difficulty = selected = button.handle_event(event)
                    
                    if selected:
                        self.handle_menu_buttons = False
                        self.dissolve_buttons = True
                        self.start_time = pygame.time.get_ticks()
                        break
            
            
            
    def update(self):
        # Update game logic here
        pass

    def draw(self):
        self.screen.fill(colours.GREY)

        if self.show_menu: 
            self.blit_title()

            for button in self.buttons:  
                if self.dissolve_buttons:
   
                    dissolved = button.dissolve(self.start_time)  
                    if dissolved:
                        self.buttons = []
                        self.show_menu = False
                        break
                
                button.draw()



        # Draw game objects here
        pygame.display.flip()


    def init_menu_buttons(self):
        buttons = []
        for i, difficulty in enumerate(("Easy", "Medium", "Hard"), start=1):
            button = MenuButton(
                            self.screen, 
                            x = SCREEN_WIDTH // 2,
                            y = 120 + (i * 100), 
                            width = 250,
                            height = 60,
                            text = difficulty,
                            font_size = 30,
                            text_colour = colours.BLACK,
                            rect_colour = colours.DIM_GREY
                            )
            button.center_x()
            buttons.append(button)
        return buttons


    def blit_title(self):
           
        def draw_face_for_i():   
            happy_face = pygame.image.load("assets/images/happy_face.png")
            happy_face = pygame.transform.scale(happy_face, (25, 25))

            # Get the image dimensions
            width = happy_face.get_width()
            height = happy_face.get_height()

            # Calculate the position to center the image within the rectangle
            x = ((SCREEN_WIDTH - width) // 2 ) * 0.65
            y = ((SCREEN_HEIGHT - height) // 2 ) - 220

            self.screen.blit(happy_face, (x, y))


        def draw_title_text():
            # Set up font and text
            font = pygame.font.Font("assets/fonts/menu__title.ttf", 100)  # You can change the font and size here


            text_surface = font.render("Minesweeper", True, colours.BLACK)  # Render text with black color (0, 0, 0)

            # Get the dimensions of the text surface
            text_width, text_height = text_surface.get_size()

            # Calculate the position to center the text on the screen
            center_x = (SCREEN_WIDTH - text_width) // 2
            center_y = (SCREEN_WIDTH - text_height) // 2 - 270
            
            self.screen.blit(text_surface, (center_x, center_y))

        draw_face_for_i()
        draw_title_text()



