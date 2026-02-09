"""
Unit tests for Pong Game components
"""
import pygame
import sys
import os

# Set SDL to use dummy video driver for headless testing
os.environ['SDL_VIDEODRIVER'] = 'dummy'

# Import after setting environment variable
import pong_game

def test_paddle_creation():
    """Test that paddles can be created"""
    paddle = pong_game.Paddle(100, 200)
    assert paddle.rect.x == 100
    assert paddle.rect.y == 200
    assert paddle.rect.width == pong_game.PADDLE_WIDTH
    assert paddle.rect.height == pong_game.PADDLE_HEIGHT
    print("✓ Paddle creation test passed")

def test_paddle_movement():
    """Test that paddles move correctly"""
    paddle = pong_game.Paddle(100, 300)
    paddle.speed = 5
    initial_y = paddle.rect.y
    paddle.move()
    assert paddle.rect.y == initial_y + 5
    print("✓ Paddle movement test passed")

def test_paddle_boundaries():
    """Test that paddles stay within screen boundaries"""
    paddle = pong_game.Paddle(100, 0)
    paddle.speed = -10
    paddle.move()
    assert paddle.rect.top >= 0
    
    paddle = pong_game.Paddle(100, pong_game.HEIGHT)
    paddle.speed = 10
    paddle.move()
    assert paddle.rect.bottom <= pong_game.HEIGHT
    print("✓ Paddle boundary test passed")

def test_ball_creation():
    """Test that ball can be created"""
    ball = pong_game.Ball()
    assert ball.rect.width == pong_game.BALL_SIZE
    assert ball.rect.height == pong_game.BALL_SIZE
    assert ball.speed_x != 0
    assert ball.speed_y != 0
    print("✓ Ball creation test passed")

def test_ball_movement():
    """Test that ball moves"""
    ball = pong_game.Ball()
    initial_x = ball.rect.x
    initial_y = ball.rect.y
    ball.move()
    # Ball should have moved
    assert ball.rect.x != initial_x or ball.rect.y != initial_y
    print("✓ Ball movement test passed")

def test_ball_reset():
    """Test that ball reset works"""
    ball = pong_game.Ball()
    ball.rect.x = 100
    ball.rect.y = 100
    ball.reset()
    # Ball should be near center after reset
    assert abs(ball.rect.centerx - pong_game.WIDTH // 2) < 10
    assert abs(ball.rect.centery - pong_game.HEIGHT // 2) < 10
    print("✓ Ball reset test passed")

def test_game_initialization():
    """Test that game can be initialized"""
    pygame.init()
    game = pong_game.PongGame()
    assert game.player_score == 0
    assert game.computer_score == 0
    assert not game.game_over
    assert game.winner is None
    print("✓ Game initialization test passed")

def test_scoring():
    """Test that scoring works correctly"""
    pygame.init()
    game = pong_game.PongGame()
    
    # Simulate player scoring
    game.player_score = 0
    game.ball.rect.right = pong_game.WIDTH + 10
    game.check_scoring()
    assert game.player_score == 1
    print("✓ Player scoring test passed")
    
    # Simulate computer scoring
    game.computer_score = 0
    game.ball.rect.left = -10
    game.check_scoring()
    assert game.computer_score == 1
    print("✓ Computer scoring test passed")

def test_game_over():
    """Test that game over detection works"""
    pygame.init()
    game = pong_game.PongGame()
    
    # Test player winning
    game.player_score = pong_game.WINNING_SCORE
    game.check_game_over()
    assert game.game_over
    assert game.winner == "Player"
    print("✓ Player win detection test passed")
    
    # Test computer winning
    game.reset_game()
    game.computer_score = pong_game.WINNING_SCORE
    game.check_game_over()
    assert game.game_over
    assert game.winner == "Computer"
    print("✓ Computer win detection test passed")

def test_game_reset():
    """Test that game reset works"""
    pygame.init()
    game = pong_game.PongGame()
    game.player_score = 5
    game.computer_score = 3
    game.game_over = True
    game.winner = "Player"
    
    game.reset_game()
    
    assert game.player_score == 0
    assert game.computer_score == 0
    assert not game.game_over
    assert game.winner is None
    print("✓ Game reset test passed")

def run_all_tests():
    """Run all tests"""
    print("\n" + "="*50)
    print("Running Pong Game Tests")
    print("="*50 + "\n")
    
    try:
        test_paddle_creation()
        test_paddle_movement()
        test_paddle_boundaries()
        test_ball_creation()
        test_ball_movement()
        test_ball_reset()
        test_game_initialization()
        test_scoring()
        test_game_over()
        test_game_reset()
        
        print("\n" + "="*50)
        print("All tests passed! ✓")
        print("="*50 + "\n")
        return True
    except AssertionError as e:
        print(f"\n✗ Test failed: {e}")
        return False
    except Exception as e:
        print(f"\n✗ Error during testing: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)
