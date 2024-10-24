import pygame

class Player:
    # State consts
    IDLE_STATE = 0
    MOVING_STATE = 1

    WALK_SPEED = 3

    DOWN = 0
    UP = 1
    LEFT = 2
    RIGHT = 3

    FRAME_SIZE = (100, 100)

    # Animations
    IDLE_ANIMATION = [(0, 60)]
    WALK_ANIMATION = [(0, 10), (1, 10), (0, 10), (2, 10)]


    # Variables
    pos_x = 100
    pos_y = 100

    current_state = IDLE_STATE
    current_direction = DOWN

    current_frame = 0
    current_animation = None

    current_duration = 0
    frame_counter = 0
    animation_index = 0

    # "Output"
    screen_rect = None
    # "Input"
    frame_rect = None

    spritesheet = None

    def __init__(self):
        self.spritesheet = pygame.image.load("farmer-big.png").convert_alpha()
        self.frame_rect = pygame.Rect(0,0, self.FRAME_SIZE[0], self.FRAME_SIZE[1])
        self.screen_rect = pygame.Rect(self.pos_x, self.pos_y, self.FRAME_SIZE[0], self.FRAME_SIZE[1])
        self.screen_rect.center = (self.pos_x, self.pos_y)
        self.set_animation(self.WALK_ANIMATION)

    def set_frame(self, frame):
        self.current_frame = frame
        cur_row = self.current_direction
        cur_col = self.current_frame

        self.frame_rect.topleft = (cur_col * self.FRAME_SIZE[0], cur_row * self.FRAME_SIZE[1])

    def next_frame(self):
        self.current_frame = self.current_animation[self.animation_index][0]
        self.current_duration = self.current_animation[self.animation_index][1]

    def set_animation(self, animation):
        self.current_animation = animation
        self.animation_index = 0

        self.frame_counter = 0
        self.next_frame()
        self.set_frame(self.current_frame)

    def update_animation(self):
        self.frame_counter += 1

        if self.frame_counter >= self.current_duration:
            self.frame_counter = 0
            self.animation_index += 1
            if self.animation_index >= len(self.current_animation):
                self.animation_index = 0
            self.next_frame()
            self.set_frame(self.current_frame)

    def move(self, direction):
        self.current_state = self.MOVING_STATE

        if direction == self.DOWN:
            self.pos_y += self.WALK_SPEED
            self.current_direction = self.DOWN
        if direction == self.UP:
            self.pos_y -= self.WALK_SPEED
            self.current_direction = self.UP
        if direction == self.RIGHT:
            self.pos_x += self.WALK_SPEED
            self.current_direction = self.RIGHT
        if direction == self.LEFT:
            self.pos_x -= self.WALK_SPEED
            self.current_direction = self.LEFT

        self.screen_rect.center = (self.pos_x, self.pos_y)

    def stop_move(self):
        pass

    def update(self):
        self.update_animation()

    def draw(self, screen):
        screen.blit(self.spritesheet, self.screen_rect, self.frame_rect)
