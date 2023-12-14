
def DFS( maze , queue , visited , currCell , Path):
    for d in 'ESNW' :
        if maze[currCell][d]==True:
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
            Path[childCell]=currCell   