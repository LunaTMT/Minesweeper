import pygame
import sys

from buttons.menu_button import MenuButton
from buttons.return_button import ReturnButton
from board.board import Board
import assets.colours as colours
import game


class Minesweeper:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((game.SCREEN_WIDTH, game.SCREEN_HEIGHT))
        pygame.display.set_caption("Minesweeper")
        self.clock = pygame.time.Clock()
        
        self.is_running = True

        self.show_menu = True
        self.handle_menu_buttons = True
        self.dissolve_buttons = False

        self.play_game = False
        self.bombs_shown = False

        self.difficulty = None
        
        self.buttons = []
        self.init_menu_buttons()

    def run(self):
        while self.is_running:
            self.handle_events()
            self.update()
            self.draw()
            self.clock.tick(game.FPS)

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.is_running = False

            if self.handle_menu_buttons:
                for button in self.buttons:
                    """
                    When the user has pressed a button the value of the button, i.e. the difficulty, is returned.
                    This difficult is used to correctly instantiate the correct board parameters below
                    """
                    self.difficulty = pressed = button.handle_event(event)
    

                    if pressed: 
                        """
                        now the button has been pressed we want to initialise the board 
                        with the correct parameters based upon the selected difficulty above        
                            - beginner:     10 mines, 10x10
                            - intermediate: 40 mines, 16x16
                            - expert:       99 mines, 16x30  
                        """              
                
                        match self.difficulty:
                            case "Easy":
                                self.board = Board(self, rows=10, columns=10, bombs=10)
                            case "Medium":
                                self.board = Board(self, rows=16, columns=16, bombs=40)
                            case "Hard":
                                self.board = Board(self, rows=16, columns=30, bombs=99)
                        self.return_button = ReturnButton(self, x=10, y=10)

                        """
                        Gamestate change
                        we no longer want to show the menu or allow anymore handling of the buttons
                        in addition we want them to fade away in the dissolve function
                        """
                        self.handle_menu_buttons = False
                        self.dissolve_buttons = True
                        self.start_time = pygame.time.get_ticks()
                        break
            
            if self.play_game:
                self.board.handle_event(event)
                self.return_button.handle_event(event)
            
    def update(self):
        # Update game logic here
        pass

    def draw(self):
        self.screen.fill(colours.GREY)
        
        if self.show_menu: 
            self.blit_title()

            for button in self.buttons:  
                if self.dissolve_buttons:
                    has_dissolved = button.dissolve(self.start_time)  #have the buttons fully disolved? (Bool)
                    #Gamestate change
                    if has_dissolved:
                        # When the buttons have fully disolved we no longer want to show the buttons and we want the game to begin
                        self.buttons = []
                        self.show_menu = False
                        self.play_game = True
                        self.dissolve_buttons = False
                        break
                button.draw()

        if self.play_game:
            self.board.draw()
            self.return_button.draw()

        pygame.display.flip()


    def init_menu_buttons(self):
        """
        This function initialised 3 MenuButton objects each centered along the x axis and beneath the other
        They denote the difficulty of the game to be played
        """
        buttons = []
        for i, difficulty in enumerate(("Easy", "Medium", "Hard"), start=1):
            button = MenuButton(
                            self.screen, 
                            y = 120 + (i * 100), 
                            width = 250,
                            height = 60,
                            text = difficulty)
            button.center_x()
            buttons.append(button)
        self.buttons = buttons

    def blit_title(self):
        
        def draw_face_for_i():  
            """
            This function blits a smiley face above the 'i' in the title
            """
            happy_face = pygame.image.load("assets/images/faces/happy_face.png")
            happy_face = pygame.transform.scale(happy_face, (25, 25))

            # Get the image dimensions
            width = happy_face.get_width()
            height = happy_face.get_height()

            # Calculate the position to center the image within the rectangle
            x = ((game.SCREEN_WIDTH - width) // 2 ) * 0.65
            y = ((game.SCREEN_HEIGHT - height) // 2 ) - 220

            self.screen.blit(happy_face, (x, y))
        
        def draw_title_text():
            """
            This funciton simply blits the title text 
            """
            # Set up font and text
            font = pygame.font.Font("assets/fonts/menu_title.ttf", 100)  # You can change the font and size here

            text_surface = font.render("Minesweeper", True, colours.BLACK)  # Render text with black color (0, 0, 0)

            # Get the dimensions of the text surface
            text_width, text_height = text_surface.get_size()

            # Calculate the position to center the text on the screen
            center_x = (game.SCREEN_WIDTH - text_width) // 2
            center_y = (game.SCREEN_WIDTH - text_height) // 2 - 270
            
            self.screen.blit(text_surface, (center_x, center_y))
        
        draw_face_for_i()
        draw_title_text()



