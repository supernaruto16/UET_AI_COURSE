Project 2: Multi-Agent Search
=============================

## Question 1:
+ Mục tiêu: Tối ưu cho Reflex Agent.
+ Cách làm:
  + Viết lại hàm `evaluateFunction` để cải tiến phương thức đánh giá số điểm của game state sau khi chọn 1 action của Pacman.
  + Thêm biến `bonus` là số lượng điểm cộng thêm vào số điểm mặc định của currentGameState
  + Theo từng trường hợp mà bonus được tính như sau:
    + Nếu ghosts đang sợ hãi và số lượng nước đi còn lại > 2:
      + Pacman ưu tiên việc đuổi và ăn ghosts hơn ăn food.
      + Nếu khoảng cách từ pacman tới ghost gần nhất <= 1. Pacman sẽ ăn ghost.
      + Nếu không, duyệt lần lượt vị trí của từng food, tính tỉ lệ giữa khoảng cách từ pacman tới ghost ở xa nhất với khoảng cách từ pacman tới food gần nhất
      + Bonus bằng giả trị lớn nhất của tỉ lệ nêu trên
    ```python
    bonus = max([manhattanDistance(food, next_pacman_pos) / max_ghost_dist for food in next_food_list])
    ```
    + Nếu không:
      + Pacman ưu tiên việc ăn food ở xa hơn so với food ở gần ghost
      + Nếu khoảng cách từ pacman tới ghost gần nhất <= 1. Pacman sẽ chọn action khác.
      + Nếu không, duyệt lần lượt vị trí của từng food, tính tỉ lệ giữa khoảng cách từ pacman tới food gần nhất với khoảng cách giữa pacman với ghost ở gần nhất
      + Bonus bằng giả trị lớn nhất của tỉ lệ nêu trên
      ```python
      bonus = max([min_ghost_dist / manhattanDistance(food, next_pacman_pos) for food in next_food_list])
      ``` 

## Question 2:
+ Mục tiêu: Áp dụng thuật toán Minimax cho pacman.
+ Cách làm:
  + Tạo hàm `minimax_value` nhận các tham số:
    + game_state: game state hiện tại
    + cur_depth: độ sâu cây minimax hiện tại
    + cur_agent: agent hiện tại
  + Nếu agent là Pacman và độ sâu hiện tại bằng 1,hàm sẽ trả lại action tối ưu nhất.
  + Nếu agent là pacman, hàm sẽ trả lại giá trị lớn nhất trong cấc nút con.
    ```python
    best_score = max([self.minimax_value(next_game_state, next_depth, next_agent) for next_game_state in successor_game_state])
    ```
  + Nếu agent là ghost, hàm sẽ trả lại giá trị nhỏ nhất trong các nút con.
    ```python
    best_score = min([self.minimax_value(next_game_state, next_depth, next_agent) for next_game_state in successor_game_state])
    ```

## Question 3:
+ Mục tiêu: Áp dụng thuật toán Alpha Beta Pruning cho pacman.
+ Cách làm:
  + Tương tự `Question 2`. Tuy nhiên hàm `minimax_value` nhận 2 tham số:
    + alpha: Giá trị lớn nhất của các nút Max, khởi tạo = -INF
    + beta: Giá trị lớn nhất của các nút Min, khởi tạo = INF
  + Nếu agent là pacman:
    + Duyệt tất cả các giá trị của game state tiếp theo
    + Nếu xuất hiện 1 giá trị lớn hơn beta, dừng lại và trả về giá trị này
    + Cập nhật `alpha = max(alpha, best_score)`
    + Sau khi duyệt hết, trả về giá trị lớn nhất
  + Nếu agent là ghost:
    + Duyệt tất cả các giá trị của game state tiếp theo
    + Nếu xuất hiện 1 giá trị nhỏ hơn alpha, dừng lại và trả về giá trị này
    + Cập nhật `beta = min(beta, best_score)`
    + Sau khi duyệt hết, trả về giá trị nhỏ nhất

## Question 4:
+ Mục tiêu: Áp dụng thuật toán Expectimax cho pacman.
+ Cách làm:
  + Tạo hàm `expectimax_value` tương tự hàm `minimax_value` ở `Question 2`.
  + Tuy nhiên, nếu agent là ghost, giá trị trả về sẽ là expected value score của tất cả các trạng thái tiếp theo.
    ```python
    next_scores = [self.expectimax_value(next_game_state, next_depth, next_agent) for next_game_state in successor_game_state]
    best_score = sum(next_scores) / len(next_scores)
    ```

## Question 5:
+ Mục tiêu: Thiết kế hàm `evaluateFunction` để cải tiến phương thức đánh giá số điểm của game state hiện tại.
+ Sử dụng thuật toán tương tự hàm `evaluteFunction` ở `Question 1`.