Project 1: Search
=============================

## Question 1:
+ Mục tiêu: Xây dựng hàm tìm kiếm 1 food ở vị trí cố dịnh cho pacman bằng thuật toán DFS
+ Cách làm:
  + Khởi tạo 1 Stack lưu lại nút (state) và chuỗi hành động (actions) dẫn tới nút đó
  
    ```python
    path = util.Stack()
    visited = []
    path.push((startNode, startActions))
    ```
  + Tại mỗi vòng lặp, lấy ra phần tử ở đầu Stack
  + Kiểm tra nút đó đã được thăm hay chưa, nếu thăm rồi thì không làm gì
  + Nếu nút đó chưa được thăm, đưa nút này vào danh sách đã thăm
  + Nếu nút đó là đích (là food) thì trả về chuỗi hành động và dừng vòng lặp
  + Nếu không, duyệt qua các nút con (SuccessorState) của nút này và đưa lần lượt vào Stack
  + Lặp lại cho đén khi Stack rỗng
  
    ```python
    while not path.isEmpty():
        curNode, curActions = path.pop()
        if curNode not in visited:
            visited.append(curNode)
            if (problem.isGoalState(curNode)):
                return curActions

            for nxtNode, action, stepCost in problem.getSuccessors(curNode):
                path.push((nxtNode, curActions + [action]))
    ```

## Question 2:
+ Mục tiêu: Xây dựng hàm tìm kiếm 1 food ở vị trí cố dịnh cho pacman bằng thuật toán BFS
+ Cách làm:
  + Khởi tạo 1 Queue lưu lại nút (state) và chuỗi hành động (actions) dẫn tới nút đó
  
    ```python
    path = util.Queue()
    visited = []
    path.push((startNode, startActions))
    ```
  + Tại mỗi vòng lặp, lấy ra phần tử ở đầu Queue
  + Kiểm tra nút đó đã được thăm hay chưa, nếu thăm rồi thì không làm gì
  + Nếu nút đó chưa được thăm, đưa nút này vào danh sách đã thăm
  + Nếu nút đó là đích (là food) thì trả về chuỗi hành động và dừng vòng lặp
  + Nếu không, duyệt qua các nút con (SuccessorState) của nút này và đưa lần lượt vào Queue
  + Lặp lại cho đén khi Queue rỗng
  
    ```python
    while not path.isEmpty():
        curNode, curActions = path.pop()
        if curNode not in visited:
            visited.append(curNode)
            if (problem.isGoalState(curNode)):
                return curActions

            for nxtNode, action, stepCost in problem.getSuccessors(curNode):
                path.push((nxtNode, curActions + [action]))
    ```

## Question 3:
+ Mục tiêu: Áp dụng thuật toán Uniform-Cost Graph Search cho Pacman
+ Cách làm:
  + Khởi tạo 1 Priority Queue với priority tăng dần, lưu lại nút (state), chuỗi hành động (actions), tổng cost dẫn tới nút đó
  
    ```python
    path = util.PriorityQueue()
    visited = []
    path.push((startNode, startActions, startCost), priority)
    ```
  + Tại mỗi vòng lặp, lấy ra phần tử ở đầu Priority Queue
  + Kiểm tra nút đó đã được thăm hay chưa, nếu thăm rồi thì không làm gì
  + Nếu nút đó chưa được thăm, đưa nút này vào danh sách đã thăm
  + Nếu nút đó là đích (là food) thì trả về chuỗi hành động và dừng vòng lặp
  + Nếu không, duyệt qua các nút con (SuccessorState) của nút này và đưa lần lượt vào Priority Queue
  + Đặt priority của nút con chính bằng cost tới nút đó, để những nút có cost nhỏ hơn được đưa lên đầu Priority Queue
  + Lặp lại cho đén khi Priority Queue rỗng
  
    ```python
    while not path.isEmpty():
        curNode, curActions, curCost = path.pop()
        if curNode not in visited:
            visited.append(curNode)
            if (problem.isGoalState(curNode)):
                return curActions

            for nxtNode, action, stepCost in problem.getSuccessors(curNode):
                priority = curCost + stepCost
                path.push((nxtNode, curActions + [action], curCost + stepCost), priority)
    ```

## Question 4:
+ Mục tiêu: Áp dụng thuật toán A* cho pacman.
+ Cách làm:
  + Tương tự như thuật toán Uniform-Cost ở Q3
  + Tuy nhiên, priority của nút con được tính bằng cost tới nút đó công thêm giá trị heuristic của nó
  
  ```python
  for nxtNode, action, stepCost in problem.getSuccessors(curNode):
      priority = curCost + stepCost + heuristic(nxtNode, problem)
      path.push((nxtNode, curActions + [action], curCost + stepCost), priority)
  ```
## Question 5:
+ Mục tiêu: Xây dựng thuật toán giúp pacman tìm đường ngắn nhất đi qua 4 góc của mê cung 
+ Cách làm:


[![asciicast](https://asciinema.org/a/1VPrz7M9avVfN8Vt98E6ipAaB.svg)](https://asciinema.org/a/1VPrz7M9avVfN8Vt98E6ipAaB?speed=0.25)

