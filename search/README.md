Project 1: Search
=============================

## Question 1 (3/3):
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

## Question 2 (3/3):
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

## Question 3 (3/3):
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

## Question 4 (3/3):
+ Mục tiêu: Áp dụng thuật toán A* cho pacman.
+ Cách làm:
  + Tương tự như thuật toán Uniform-Cost ở Q3
  + Tuy nhiên, priority của nút con được tính bằng cost tới nút đó công thêm giá trị heuristic của nó
  
    ```python
    for nxtNode, action, stepCost in problem.getSuccessors(curNode):
        priority = curCost + stepCost + heuristic(nxtNode, problem)
        path.push((nxtNode, curActions + [action], curCost + stepCost), priority)
    ```
## Question 5 (3/3):
+ Mục tiêu: Thêm các hàm bài toán CornersProblem giúp pacman tìm đường ngắn nhất đi qua 4 góc của mê cung 
+ Cách làm:
  + Hàm getStartState cho biết trang thái bắt đầu bao gồm vị trí của pacman và trang thái chưa thăm của 4 góc
    
    ```python
    visitedCorners = [False] * 4
    return (self.startingPosition, visitedCorners)
    ```
  + Hàm isGoalState cho biết trò chơi kết thúc khi cả 4 góc đều được thăm
  
    ```python
    visitedCorners = state[1]
    if False not in visitedCorners:
        return True
    return False
    ```
  + Hàm getSuccessors cho biết các trạng thái tiếp theo mà pacman có thể đi (loại bỏ trạng thái đi vào tường hoặc ra ngoài mê cung)

    ```python
    x, y = currentPosition
    dx, dy = Actions.directionToVector(action)
    nextx, nexty = int(x + dx), int(y + dy)
    nextVisitedCorners = visitedCorners[:]

    hitsWall = self.walls[nextx][nexty]
    if not hitsWall:
        cornerIdx = -1
        for i in xrange(len(self.corners)):
            if (self.corners[i] == (nextx, nexty)):
                cornerIdx = i

        if (cornerIdx != -1):
            nextVisitedCorners[cornerIdx] = True
        nextState = ((nextx, nexty), nextVisitedCorners)
        successors.append((nextState, action, 1))
    ```

## Question 6 (3/3):
+ Mục tiêu: Xây dựng thuật toán cornersHeuristic
+ Cách làm:
  + Duyệt qua tất cả cá tổ hợp mà pacman có thể đi qua các góc còn lại
  + Với mỗi tổ họp, ước tính tổng bước pacman phải đi bằng hàm manhattanDistance
  + Chọn ra tổ hợp có tổng bước đi nhỏ nhất
    
    ```python
    from itertools import permutations 
    orders = list(permutations(order))
    for order in orders:
        sumManhattanDistance = util.manhattanDistance(curPos, corners[order[0]])
        for i in xrange(1, len(order)):
            sumManhattanDistance += util.manhattanDistance(corners[order[i-1]], corners[order[i]])
        res = min(res, sumManhattanDistance)
    ```

## Question 7 (4/4):
+ Mục tiêu: Xây dựng thuật toán foodHeuristic giúp pacman ăn hết food
+ Cách làm:
  + Tình đường đi thực tế (mazeDistance) từ pacman tới tất cả các food còn lại

    ```python
    dist = []
    for i in xrange(len(foodList)):
        dist.append(mazeDistance(position, foodList[i], problem.startingGameState))
    ```
  + Duyệt qua tất cả các cặp food, chọn cặp mà đường pacman lần lượt đi qua chúng là lớn nhất trong tất cả các cặp
    ```python
    for i in xrange(len(foodList)-1):
        for j in xrange(i + 1, len(foodList)):
            u, v = foodList[i], foodList[j]
            du, dv = dist[i], dist[j]
            sumDistance = min(du, dv) + problem.heuristicInfo[(u, v)]
            res = max(res, sumDistance)
    ```

## Question 8 (3/3):
+ Mục tiêu: Xây dựng thuật toán giúp pacman ưu tiên ăn các food ở gần nhất
+ Cách làm:
  + Trong hàm findPathToClosestDot, trả về search.aStarSearch(problem) để sử dụng thuật toán A* ở Q4
  + Trong hàm isGoalState của class AnyFoodSearchProblem trả về đúng nếu có food ở ô (x, y)
    ```python
    class AStarFoodSearchAgent(SearchAgent):
        def findPathToClosestDot(self, gameState):
            return search.aStarSearch(problem)
    
    class AnyFoodSearchProblem(PositionSearchProblem):
        def isGoalState(self, state):
            return self.food[x][y]
    ```

[![asciicast](https://asciinema.org/a/1VPrz7M9avVfN8Vt98E6ipAaB.svg)](https://asciinema.org/a/1VPrz7M9avVfN8Vt98E6ipAaB?speed=0.25)

