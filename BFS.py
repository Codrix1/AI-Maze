
def BFS(m,start , goal ):
    expand =[start]
    queue = [start]
    bfsPath = {}
    visited = [start]

    while len(queue)>0:
        currCell=queue.pop(0)
        expand.append(currCell)
        if currCell==goal:
            break
        for d in 'ESNW':
            if m[currCell][d]==True:
                if d=='E':
                    childCell=(currCell[0],currCell[1]+1)
                elif d=='W':
                    childCell=(currCell[0],currCell[1]-1)
                elif d=='S':
                    childCell=(currCell[0]+1,currCell[1])
                elif d=='N':
                    childCell=(currCell[0]-1,currCell[1])
                if childCell in visited:
                    continue
                queue.append(childCell)
                visited.append(childCell)
                bfsPath[childCell] = currCell
        
    return  bfsPath , expand