import pygame
from .button import Button
import assets.colours as colours
import game
import time

class MenuButton(Button):
    
    def __init__(self, screen, x=0, y=0, width=0, height=0, text=None, font=None):
        super().__init__(screen, x, y, width, height, text, font)


        self.font = pygame.font.Font("assets/fonts/menu_buttons.ttf", 30)
        self.default_text_colour = self.text_colour = colours.BLACK,
        self.default_rect_colour = self.rect_colour = colours.DIM_GREY
        
        self.cool_face_image = pygame.image.load("assets/images/faces/cool_face.png")
        self.cool_face_image = pygame.transform.scale(self.cool_face_image, (25, 25))

        self.dead_face_image = pygame.image.load("assets/images/faces/dead_face.png")
        self.dead_face_image = pygame.transform.scale(self.dead_face_image, (25, 25))

        self.happy_face_image = pygame.image.load("assets/images/faces/happy_face.png")
        self.happy_face_image = pygame.transform.scale(self.happy_face_image, (25, 25))
        
        self.scared_face_image = pygame.image.load("assets/images/faces/scared_face.png")
        self.scared_face_image = pygame.transform.scale(self.scared_face_image, (25, 25))

        self.face_image = self.happy_face_image
        

    def __str__(self):
        return str(self.hover)


    def draw(self):
        
        if self.hover:
            self.rect_colour = colours.GREY_60
            self.text_colour = colours.WHITE

            if self.text == "Easy":
                self.face_image = self.cool_face_image 
            if self.text == "Medium":
                self.face_image = self.scared_face_image
            elif self.text == "Hard": 
                self.face_image = self.dead_face_image
        else:
            self.rect_colour = self.default_rect_colour
            self.text_colour = self.default_text_colour
            
        if self.clicked:
            self.face_image = self.cool_face_image
            
        self._draw_base_rectangle()
        self._draw_text()

        if self.hover:
            self._draw_flag()
            self._draw_face_for_i()
    
        self.screen.blit(self.surface, (self.rect.x , self.rect.y))      

    def _draw_base_rectangle(self):
        rounded_rect_rect = pygame.Rect(0, 0, self.width, self.height)
        pygame.draw.rect(self.surface, self.rect_colour, rounded_rect_rect, border_radius=20)

    def _draw_text(self):
        text = self.font.render(self.text, True, self.text_colour)
        text_x = (self.width  - text.get_width()) // 2
        text_y = (self.height - text.get_height()) // 2
        self.surface.blit(text, (text_x, text_y))
         
    def _draw_flag(self):
        flag = pygame.image.load("assets/images/flag.png")
        flag = pygame.transform.scale(flag, (50, 50))

        image_x = ((self.width - flag.get_width()) // 2 ) + 90
        image_y = (self.height - flag.get_height()) // 2 

        self.surface.blit(flag, (image_x, image_y))

    def _draw_face_for_i(self):   
        width = self.face_image.get_width()
        height = self.face_image.get_height()

        # Calculate the position to center the image within the rectangle
        x = ((game.SCREEN_WIDTH - width) // 2 ) * 0.65
        y = ((game.SCREEN_HEIGHT - height) // 2 ) - 220

        self.screen.blit(self.face_image, (x, y))


    def dissolve(self, start_time):
        # Calculate the time elapsed since the start of the loop
        elapsed_time = pygame.time.get_ticks() - start_time

        # Calculate the current alpha value based on elapsed time
        current_alpha = max(0, 255 - (255 * elapsed_time / 1000))

        # Set the new alpha value for the rectangle
        self.surface.set_alpha(int(current_alpha))

        if current_alpha == 0: 
            game.start_time = time.time()
            return True
        
