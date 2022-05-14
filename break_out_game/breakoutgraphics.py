"""
stanCode Breakout Project
Adapted from Eric Roberts's Breakout by
Sonja Johnson-Yu, Kylie Jue, Nick Bowman, 
and Jerry Liao.

YOUR DESCRIPTION HERE
"""
from campy.graphics.gwindow import GWindow
from campy.graphics.gobjects import GOval, GRect, GLabel
from campy.gui.events.mouse import onmouseclicked, onmousemoved
import random

BRICK_SPACING = 5  # Space between bricks (in pixels). This space is used for horizontal and vertical spacing
BRICK_WIDTH = 40  # Height of a brick (in pixels)
BRICK_HEIGHT = 15  # Height of a brick (in pixels)
BRICK_ROWS = 10  # Number of rows of bricks
BRICK_COLS = 10  # Number of columns of bricks
BRICK_OFFSET = 50  # Vertical offset of the topmost brick from the window top (in pixels)
BALL_RADIUS = 10  # Radius of the ball (in pixels)
PADDLE_WIDTH = 75  # Width of the paddle (in pixels)
PADDLE_HEIGHT = 15  # Height of the paddle (in pixels)
PADDLE_OFFSET = 50  # Vertical offset of the paddle from the window bottom (in pixels)
INITIAL_Y_SPEED = 7  # Initial vertical speed for the ball
MAX_X_SPEED = 5  # Maximum initial horizontal speed for the ball

is_moving = False
go_to_bonus = False
shorten = False
give_bonus2 = False
enlarge = False
level_up = False


class BreakoutGraphics:

    def __init__(self, ball_radius=BALL_RADIUS, paddle_width=PADDLE_WIDTH, paddle_height=PADDLE_HEIGHT,
                 paddle_offset=PADDLE_OFFSET, brick_rows=BRICK_ROWS, brick_cols=BRICK_COLS, brick_width=BRICK_WIDTH,
                 brick_height=BRICK_HEIGHT, brick_offset=BRICK_OFFSET, brick_spacing=BRICK_SPACING, title='Breakout'):

        # Create a graphical window, with some extra space
        window_width = brick_cols * (brick_width + brick_spacing) - brick_spacing
        window_height = brick_offset + 3 * (brick_rows * (brick_height + brick_spacing) - brick_spacing)
        self.window = GWindow(width=window_width, height=window_height, title=title)

        # Create a paddle
        self.p_w = paddle_width
        self.p_h = paddle_height
        self.paddle = GRect(self.p_w, self.p_h)
        self.paddle.filled = True

        # Center a filled ball in the graphical window
        # 原本的球以及bonus
        self.ball = GOval(ball_radius * 2, ball_radius * 2)
        self.ball.filled = True

        self.ball2 = GOval(ball_radius * 2, ball_radius * 2)
        self.ball2.filled = True
        self.ball2.fill_color = 'red'

        # Default initial velocity for the ball
        # 原本的球以及bonus
        self.__dx = 0
        self.__dy = INITIAL_Y_SPEED
        self.__2dx = 2
        self.__2dy = -3

        # Initialize our mouse listeners
        onmousemoved(self.position)
        onmouseclicked(self.start)

        # Draw bricks
        self.n = 0
        for i in range(BRICK_COLS):
            for j in range(BRICK_ROWS):
                self.brick = GRect(BRICK_WIDTH, BRICK_HEIGHT)
                self.brick.filled = True
                self.brick.color = "white"
                if j < 2:
                    self.brick.fill_color = 'navy'
                elif 2 <= j < 4:
                    self.brick.fill_color = 'blue'
                elif 4 <= j < 6:
                    self.brick.fill_color = 'royalblue'
                elif 6 <= j < 8:
                    self.brick.fill_color = 'cornflowerblue'
                else:
                    self.brick.fill_color = 'lightsteelblue'
                self.window.add(self.brick, x=i * (brick_width + brick_spacing),
                                y=brick_offset + j * (brick_height + brick_spacing))
                self.n += 1

        # count score & lives
        self.score = 0
        self.label = GLabel('Score=' + str(self.score))
        self.label.font = '-20'
        self.window.add(self.label, x=0, y=self.label.height * 1.5)

        self.lives = 3
        self.l_lives = GLabel('LIVES: ' + str(self.lives))
        self.l_lives.font = '-15'
        self.window.add(self.l_lives, x=self.window.width-self.l_lives.width*1.2, y=self.label.height * 1.2)

        # levelup & gift
        self.rect = GRect(25, 25)
        self.rect.filled = True
        self.rect.color = 'white'

        self.rect2 = GRect(25, 25)
        self.rect2.filled = True
        self.rect2.color = 'white'

    def set_paddle(self):
        self.paddle = GRect(self.p_w, self.p_h)
        self.paddle.filled = True
        self.window.add(self.paddle, x=(self.window.width / 2 - self.paddle.width / 2),
                        y=self.window.height - PADDLE_OFFSET - self.paddle.height)

    def set_ball_velocity(self):
        self.__dx = random.randint(1, MAX_X_SPEED)
        self.__dy = INITIAL_Y_SPEED
        if random.random() > 0.5:
            self.__dx = -self.__dx

    # Getter
    def get_dx(self):
        return self.__dx

    def get_dy(self):
        return self.__dy

    def set_ball_position(self):
        self.window.add(self.ball, x=self.window.width / 2 - self.ball.width / 2, y=self.window.height / 2 - self.ball.height / 2)

    def reset_ball(self):
        global is_moving
        self.window.remove(self.ball2)
        self.set_ball_position()
        self.set_ball_velocity()
        is_moving = False
        self.lives -= 1
        self.l_lives.text = 'LIVES: ' + str(self.lives)

    def death(self):
        # 判別lives使否減一，球的高度低於paddle
        is_ball_under_paddle = self.ball.y + self.ball.height >= self.window.height - PADDLE_OFFSET / 2
        return is_ball_under_paddle

    def position(self, event):
        self.paddle.x = event.x - self.paddle.width / 2

    def move_ball(self):
        # 藉由開關將move_ball 啟動
        global is_moving
        onmouseclicked(self.start)
        if is_moving is True:
            self.ball.move(self.__dx, self.__dy)
            # 判別反彈條件
            if self.ball.x <= 0 or self.ball.x + self.ball.width >= self.window.width:
                self.__dx = -self.__dx
                self.ball.move(self.__dx, self.__dy)

            if self.ball.y <= 0 or self.ball.y + self.ball.height >= self.window.height:
                self.__dy = -self.__dy
                self.ball.move(self.__dx, self.__dy)

    def start(self, event):
        global is_moving
        is_moving = True

    def check(self):
        for i in range(2):
            for j in range(2):
                obj = self.window.get_object_at(self.ball.x + i * BALL_RADIUS * 2, self.ball.y + j * BALL_RADIUS * 2)
                if obj is not None:
                    # 由於只有最後一個建立的brick才會被辨識，因此已排除的方式將brick消除
                    if obj is not self.ball2 and obj is not self.label and obj is not self.l_lives and obj is not self.rect and obj is not self.rect2:
                        if obj is not self.paddle:
                            self.window.remove(obj)
                            self.score += 1
                            self.label.text = 'Score=' + str(self.score)
                        self.bouncing()

    def bouncing(self):
        self.__dy = -self.__dy
        self.ball.move(self.__dx, self.__dy)

    def bonus(self):
        global go_to_bonus
        if go_to_bonus is False:
            self.window.add(self.ball2, x=self.window.width / 2, y=self.window.height / 2)
            go_to_bonus = True

    def move_ball2(self):
        global go_to_bonus
        if go_to_bonus is True:
            self.ball2.move(self.__2dx, self.__2dy)
            if self.ball2.x <= 0 or self.ball2.x + self.ball2.width >= self.window.width:
                self.__2dx = -self.__2dx
            if self.ball2.y <= 0 or self.ball2.y + self.ball2.height >= self.window.height:
                self.__2dy = -self.__2dy
            if self.ball2.y+self.ball2.height >= self.window.height:
                self.__2dy = 0
                self.window.remove(self.ball2)

    def check2(self):
        for i in range(2):
            for j in range(2):
                obj2 = self.window.get_object_at(self.ball2.x + i * BALL_RADIUS * 2, self.ball2.y + j * BALL_RADIUS * 2)
                if obj2 is not None:
                    if obj2 is not self.ball and obj2 is not self.label and obj2 is not self.paddle and obj2 is not self.l_lives and obj2 is not self.rect and obj2 is not self.rect2:
                        # 與原本的球不同，碰到brick不會反彈
                        self.window.remove(obj2)
                        self.score += 1
                        self.label.text = 'Score=' + str(self.score)
                    if obj2 is self.paddle:
                        self.bouncing2()

    def bouncing2(self):
        self.__2dy = -self.__2dy
        self.ball2.move(self.__2dx, self.__2dy)

    def levelup(self):
        global level_up
        # 藉由開關啟動(將rect顯示)
        if level_up is True:
            self.rect2.move(0, 3)
            for i in range(self.paddle.width):
                # 因為用rect的四角去辨識是否有撞到paddle一直怪怪的，改用paddle表面去判釋，因為paddle的寬度不定，所以以1為單位去判別
                obj4 = self.window.get_object_at(self.paddle.x + i,
                                                 self.paddle.y)
                if obj4 is self.rect2:
                    # 撞到rect2
                    self.shorten()
                    self.window.remove(self.rect2)
                if self.rect2.y > self.window.height:
                    self.window.remove(self.rect2)
        else:
            self.rect2.fill_color = 'aqua'
            self.window.add(self.rect2, x=self.ball.x, y=self.window.height / 3)
            level_up = True

    def shorten(self):
        global shorten
        if shorten is False:
            # 移除原本的paddle，並建立一個縮短的paddle
            self.window.remove(self.paddle)
            self.p_w //= 2
            self.set_paddle()
            onmousemoved(self.position)
            shorten = True

    def gift(self):
        # 與levelup相似
        global give_bonus2
        if give_bonus2 is True:
            self.rect.move(0, 3)
            for i in range(self.paddle.width):
                obj4 = self.window.get_object_at(self.paddle.x+i, self.paddle.y)
                if obj4 is self.rect:
                    self.bonus2()
                    self.window.remove(self.rect)
                if self.rect.y > self.window.height:
                    self.window.remove(self.rect)
        else:
            self.rect.fill_color = 'pink'
            self.window.add(self.rect, x=self.ball.x, y=self.window.height/3)
            give_bonus2 = True

    def bonus2(self):
        global enlarge
        # 移除原本的paddle，並建立一個加長的paddle
        if enlarge is False:
            self.window.remove(self.paddle)
            self.p_w *= 4
            self.set_paddle()
            onmousemoved(self.position)
            enlarge = True

    def over(self):
        # NUM_LIVES為0時，遊戲結束的標籤
        self.lives -= 1
        self.l_lives.text = 'LIVES: ' + str(self.lives)
        self.l_over = GLabel('GAME OVER!')
        self.l_over.font = '-50'
        self.l_over.color = 'red'
        self.window.add(self.l_over, x=self.window.width/2-self.l_over.width/2, y=self.window.height/2+self.l_over.height/2)

    def finish(self):
        # score等於所有brick數時，遊戲成功破關的標籤
        self.l_finish = GLabel('CONGRATULATION!')
        self.l_finish.font = '-30'
        self.l_finish.color = 'GOLD'
        self.window.add(self.l_finish, x=self.window.width/2-self.l_finish.width/2, y=self.window.height/2+self.l_finish.height/2)








