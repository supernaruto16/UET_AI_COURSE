Project 5: Classification
=============================

[![asciicast](https://asciinema.org/a/rKzFnRyuI4D3jIwJ2pBowDw4K.png)](https://asciinema.org/a/rKzFnRyuI4D3jIwJ2pBowDw4K?speed=10)

## Question 1:
+ Mục tiêu: Xây dựng mô hình Perceptron cho bài toán nhận diện chữ số
+ Cách làm:
  + Với mỗi bộ traingdata, ta có vector feature(f) và `true_label` (y)
  + Tính số điểm dự đoán `predicted_score` của f với từng label và chọn ra `max_label` (y') là label cho số điểm lớn nhất
  + 
    ```python
    predicted_score = util.Counter()
    for label in self.legalLabels:
        predicted_score[label] = trainingData[i] * self.weights[label]

    max_label = predicted_score.argMax()
    true_label = trainingLabels[i]
    ```
  + Nếu `max_label == true_label` thì không cần làm gì
  + Nếu không, cập nhật weight lại weight của 2 label trên theo công thức:
  + 
    ```python
    if max_label != true_label:
        self.weights[max_label] = self.weights[max_label] - trainingData[i]
        self.weights[true_label] = self.weights[true_label] + trainingData[i]
    ```

## Question 2:
+ Mục tiêu: Với mỗi label trả về top 100 features có trọng số (weight) lớn nhất
+ Cách làm:
  + sắp xếp lại vector weights của mỗi label theo thứ tự giảm dần giá trị của chúng (đã được tính từ Q1)
  + Trả về 100 phần từ đầu tiên
  + 
    ```python
    featuresWeights = self.weights[label].sortedKeys()[:100]
    ```
  + Từ kết quả visualize thu được, có thể trả lời cho câu hỏi phụ là phương án a gần giống nhất với kết quả của mô hình Perceptron.

## Question 3:
+ Mục tiêu: Xây dựng mô hình MIRA cho bài toán nhận diện chữ số
+ Cách làm:
  + Với mỗi `C` từ `Cgrid` cho trước, làm tương tự với mô hình Perceptron ở Q1, tính được số điểm dự đoán của f với từng label
  + Tuy nhiên, khi `max_label != true_label` tìm tham số `t` thỏa mãn công thức:
  + 
    ```python
    t = ((self.weights[max_label] - self.weights[true_label]) * (trainingData[i]) + 1.0) / (trainingData[i] * trainingData[i] * 2)
    t = min(t, C)
    ```
  + Cập nhật lại weight của từng label theo công thức:
  + 
    ```python
    tf = util.Counter()
    for feature in self.features:
        tf[feature] = trainingData[i][feature] * t
    self.weights[max_label] = self.weights[max_label] - tf
    self.weights[true_label] = self.weights[true_label] + tf
    ```

## Question 4:
+ Mục tiêu: Xây dựng các feature mở rộng cho dataClassifier của bài toán nhận diện chữ số
+ Cách làm:
  + với từng datum, đếm số thành phần liên thông của các pixel có màu trắng (có giá trị = 0) bằng thuật toán DFS
  + 
    ```python
    connected_component = 0
    visited = util.Counter()
    def visit(cell):
        visited[cell] = 1
        directions = [(0, 1), (0, -1), (1, 0), (-1, 0), (1, 1), (-1, -1), (-1, 1), (1, -1)]
        for d in directions:
            next_cell = (cell[0] + d[0], cell[1] + d[1])
            if next_cell[0] < 0 or next_cell[1] < 0:
                continue 
            if next_cell[0] >= DIGIT_DATUM_WIDTH or next_cell[1] >= DIGIT_DATUM_HEIGHT:
                continue
            if  visited[next_cell] or datum.getPixel(next_cell[0], next_cell[1]):
                continue
            visit(next_cell)
    for i in xrange(DIGIT_DATUM_WIDTH):
        for j in xrange(DIGIT_DATUM_HEIGHT):
            if visited[(i, j)] or datum.getPixel(i, j):
                continue
            connected_component += 1
            visit((i, j))
    ```
  + Thêm 3 feature mới là:
  + 
    ```python
    features['has_gt1_connected_com'] = connected_component > 1
    features['has_gt3_connected_com'] = connected_component > 3
    features['has_gt5_connected_com'] = connected_component > 5
    ```

## Question 5:
+ Mục tiêu: Xây dựng mô hình Perceptron cho Pacman
+ Cách làm:
  + Tương tự như mô hình Perceptron ở Q1, tuy nhiên ở đây trainingData sẽ là các state, và các label là các legalAction của state. Các label đều đã có sẵn weight của riêng mình. Ta sẽ phải xây dựng 1 weight chung
  + 
    ```python
    for data, true_label in zip(trainingData, trainingLabels):
        predicted_score = util.Counter()    
        for move in data[1]:
            predicted_score[move] = self.weights * data[0][move]
        max_label = predicted_score.argMax()
        if max_label == true_label:
            continue
        self.weights = self.weights + data[0][true_label]
        self.weights = self.weights - data[0][max_label]
    ```

## Question 6:
+ Mục tiêu: Xây dựng các feature mở rộng cho dataClassfier cho pacman dựa trên hành vi của StopAgent, FoodAgent, SuicideAgent, ContestAgent
+ Cách làm:
  + với StopAgent, ta có `feature['stop']` mô phỏng hành vi dừng:
  + 
    ```python
    features['stop'] = (action == 'Stop')
    ```
  + với FoodAgent, ta có `feature['min_food_distance']` cho biết khoảng cách thức ăn gần nhất
  + 
    ```python
    foods_distance = [util.manhattanDistance(food, pacman_pos) for food in foods]
    features['min_food_distance'] = min(foods_distance)
    ```
  + với ContestAgent và SuicideAgent, ta có các feature sau:
    + `zoned_ghost_cnt`: sô lượng ghost trong vùng bán kính < 2 của pacman
    + `scared_ghost_cnt`: số lượng ghost đang trong trạng thái sợ hãi
    + `min_ghost_distance`: khoảng cách tới ghost gần nhất
    + `hunter_mode`: bằng 1 khi pacman có thể chạy tới capsule gần nhất và quay về tấn công ghost
  + 
    ```python
    features['zoned_ghost_cnt'] = sum([1 if util.manhattanDistance(ghost.getPosition(), pacman_pos) < 2 else 0 for ghost in ghost_states])
    features['scared_ghost_cnt'] = sum([1 if ghost.scaredTimer > 0 else 0 for ghost in ghost_states])
    features['min_ghost_distance'] = min_ghost_distance
    nearest_capsule = capsules_distance[0]
        for ghost in ghost_states:
            if util.manhattanDistance(nearest_capsule[1], ghost.getPosition()) + nearest_capsule[0] <= ghost.scaredTimer:
                features['hunter_mode'] = 1
    ```