
def DFS(m,start , goal ):
    expand =[]
    queue = [start]
    dfsPath = {}
    visited = [start]

    while len(queue)>0:
        currCell=queue.pop()
        expand.append(currCell)
        if currCell==goal:
            break
        for d in 'ESNW':
            if m[currCell][d]==True:
                if d=='E':
                    childCell=(currCell[0],currCell[1]+1)
                if d=='W':
                    childCell=(currCell[0],currCell[1]-1)
                if d=='S':
                    childCell=(currCell[0]+1,currCell[1])
                if d=='N':
                    childCell=(currCell[0]-1,currCell[1])
                if childCell in visited:
                    continue
                queue.append(childCell)
                visited.append(childCell)
                dfsPath[childCell] = currCell
        
    return  dfsPath , expand