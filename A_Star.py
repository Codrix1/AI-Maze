from queue import PriorityQueue
import copy

def h(cell1, cell2):
    x1, y1 = cell1
    x2, y2 = cell2
    return (abs(x1 - x2) + abs(y1 - y2))

def A_star(height , width , start , goals , m):
    grid=[]
    expand =[]
    for row in range(height):
        for col in range(width):
            x = (row,col)   
            grid.append(x)      
    print(grid)
    open = PriorityQueue()
    open.put((min(h(start, goal) for goal in goals), h(start, min(goals, key=lambda goal: h(start, goal))), start))
    aPath = {}
    g_score = {cell:float("inf") for cell in grid}
    g_score[start] = 0
    f_score = {cell:float("inf") for cell in grid}
    f_score[start] = min(h(start, goal) for goal in goals)
    print(open)
    while not open.empty():
        currCell = open.get()[2]
        expand.append(currCell)
        if currCell in goals:
            end = copy.deepcopy(currCell)
            break        
        for d in 'ESNW':
            if m[currCell][d]==True:
                if d=='E':
                    childCell=(currCell[0],currCell[1]+1)
                elif d=='W':
                    childCell=(currCell[0],currCell[1]-1)
                elif d=='N':
                    childCell=(currCell[0]-1,currCell[1])
                elif d=='S':
                    childCell=(currCell[0]+1,currCell[1])

                temp_g_score = g_score[currCell] + 1
                temp_h_score = min(h(childCell, goal) for goal in goals)
                temp_f_score = temp_g_score + temp_h_score

                if temp_f_score < f_score[childCell]:   
                    aPath[childCell] = currCell
                    g_score[childCell] = temp_g_score
                    temp_h_score = min(h(childCell, goal) for goal in goals)
                    f_score[childCell] = temp_g_score + temp_h_score
                    open.put((f_score[childCell], min(h(childCell, goal) for goal in goals), childCell))        
    return  aPath , expand , end



