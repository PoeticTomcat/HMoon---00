import pygame
from field import Field

class Player:
    # State consts
    IDLE_STATE = 0
    MOVING_STATE = 1
    USING_STATE = 2

    WALK_SPEED = 3
    RUN_SPEED = 5

    DOWN = 0
    UP = 1
    LEFT = 2
    RIGHT = 3

    FRAME_SIZE = (100, 100)
    TILE_SIZE = 32

    #Tool constants
    HOE = 0
    WATERING_CAN = 1
    TURNIP_SEED = 2

    # Tool variables
    cur_tool = 0
    tools = [HOE, WATERING_CAN, TURNIP_SEED]

    # Animations
    IDLE_ANIMATION = [(0, 60)]
    WALK_ANIMATION = [(0, 10), (1, 10), (0, 10), (2, 10)]
    RUN_ANIMATION = [(0, 8), (3, 8), (0, 8), (4, 8)]
    TILLING_ANIMATION = [(12, 15), (13, 4), (14, 8), (15, 30)]
    TOOL_SWITCH = [(11, 45)]

    TILLING_FRAME = 14


    # Variables

    screen = None
    field = None

    pos_x = 100
    pos_y = 100

    current_state = IDLE_STATE
    current_direction = DOWN

    current_frame = 0
    current_animation = None

    current_duration = 0
    frame_counter = 0
    animation_index = 0

    tile_x = 0
    tile_y = 0
    reticle_x = 0
    reticle_y = 0

    running = False

    # "Output"
    screen_rect = None
    # "Input"
    frame_rect = None

    spritesheet = None
    tool_sheet = None

    def __init__(self, f, s):
        self.field = f
        self.screen = s
        self.spritesheet = pygame.image.load("farmer-big.png").convert_alpha()
        self.tool_sheet = pygame.image.load("tools-big.png").convert_alpha()
        self.frame_rect = pygame.Rect(0,0, self.FRAME_SIZE[0], self.FRAME_SIZE[1])
        self.screen_rect = pygame.Rect(self.pos_x, self.pos_y, self.FRAME_SIZE[0], self.FRAME_SIZE[1])
        self.screen_rect.center = (self.pos_x, self.pos_y)
        self.set_animation(self.IDLE_ANIMATION)

    def set_frame(self, frame):
        self.current_frame = frame
        cur_row = self.current_direction
        cur_col = self.current_frame

        self.frame_rect.topleft = (cur_col * self.FRAME_SIZE[0], cur_row * self.FRAME_SIZE[1])

    def next_frame(self):
        self.current_frame = self.current_animation[self.animation_index][0]
        self.current_duration = self.current_animation[self.animation_index][1]
        self.on_frame()

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
                if self.current_state == self.USING_STATE:
                    self.current_state = self.IDLE_STATE
                    self.set_animation(self.IDLE_ANIMATION)
                    return
            self.next_frame()
            self.set_frame(self.current_frame)

    def use_tool(self):
        self.current_state = self.USING_STATE
        self.set_animation(self.TILLING_ANIMATION)

    def move(self, direction):
        if self.current_state != self.IDLE_STATE and self.current_state != self.MOVING_STATE:
            return
        if self.current_state != self.MOVING_STATE:
            if self.running:
                self.set_animation(self.RUN_ANIMATION)
            else:
                self.set_animation(self.WALK_ANIMATION)
            self.current_state = self.MOVING_STATE

        if self.running == True:
            if direction == self.DOWN:
                self.pos_y += self.RUN_SPEED
                self.current_direction = self.DOWN
            if direction == self.UP:
                self.pos_y -= self.RUN_SPEED
                self.current_direction = self.UP
            if direction == self.RIGHT:
                self.pos_x += self.RUN_SPEED
                self.current_direction = self.RIGHT
            if direction == self.LEFT:
                self.pos_x -= self.RUN_SPEED
                self.current_direction = self.LEFT

        else:

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
        self.update_tile_position()
        self.field.set_reticle_pos(self.reticle_x, self.reticle_y)

    def stop_move(self):
        if self.current_state == self.MOVING_STATE:
            self.current_state = self.IDLE_STATE
            self.set_animation(self.IDLE_ANIMATION)

    def start_running(self):
        self.running = True
        if self.current_animation != self.RUN_ANIMATION:
            self.set_animation(self.RUN_ANIMATION)
    
    def stop_running(self):
        self.running = False
        if self.current_state == self.MOVING_STATE:
            self.set_animation(self.WALK_ANIMATION)

    def update_tile_position(self):
        self.tile_x  = self.pos_x // self.TILE_SIZE
        self.reticle_x = self.tile_x
        if self.current_direction == self.LEFT:
            self.reticle_x -= 1
        elif self.current_direction == self.RIGHT:
            self.reticle_x += 1
        
        self.tile_y = self.pos_y // self.TILE_SIZE
        self.reticle_y = self.tile_y
        if self.current_direction == self.DOWN:
            self.reticle_y += 1
        elif self.current_direction == self.UP:
            self.reticle_y -= 1

    def on_frame(self):
        if self.current_frame == self.TILLING_FRAME:
            self.field.till_tile(self.reticle_x, self.reticle_y)

    def update(self):
        self.update_animation()

    def draw(self):
        self.screen.blit(self.spritesheet, self.screen_rect, self.frame_rect)
