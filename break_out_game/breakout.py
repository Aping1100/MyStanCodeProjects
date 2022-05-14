"""
stanCode Breakout Project
Adapted from Eric Roberts's Breakout by
Sonja Johnson-Yu, Kylie Jue, Nick Bowman,
and Jerry Liao.

YOUR DESCRIPTION HERE
"""

from campy.gui.events.timer import pause
from breakoutgraphics import BreakoutGraphics

FRAME_RATE = 1000 / 120  # 120 frames per second
NUM_LIVES = 3			 # Number of attempts



def main():
    """
    將class BreakoutGraphics() 匯入以使用其中的method
    以while迴圈進入程式，並以NUM_LIVES是否等於0為程式結束與否的條件
    以撞擊磚塊數量為method的啟用條件
    分別有bonus(),levelup(),gift() 三種情況

    """

    graphics = BreakoutGraphics()
    lives = NUM_LIVES

    graphics.set_ball_position()
    graphics.set_ball_velocity()
    graphics.set_paddle()

    while True:
        pause(FRAME_RATE)
        # 判別lives是否減一
        if graphics.death():
            lives -= 1
            if lives > 0:
                # 重新開始
                graphics.reset_ball()
            else:
                graphics.over()
                break
        # 啟動球的動作
        graphics.move_ball()
        graphics.check()

        if graphics.score == graphics.n:
            graphics.finish()
            break

        if graphics.score >= graphics.n//50:
            graphics.bonus()
            graphics.move_ball2()
            graphics.check2()

        if graphics.score >= graphics.n//4:
            graphics.levelup()

        if graphics.score >= graphics.n//2:
            graphics.gift()





















        '''
                if graphics.ball.x <= 0 or graphics.ball.x + graphics.ball.width > graphics.window.width:
            graphics.dx = -graphics.dx
        if graphics.ball.y <= graphics.brick.y <= graphics.brick.height or (graphics.brick.y >= graphics.paddle.y and graphics.paddle.x <= graphics.brick.x < graphics.paddle.x + graphics.paddle.width):
            graphics.dy = -graphics.dy
        '''












if __name__ == '__main__':
    main()
