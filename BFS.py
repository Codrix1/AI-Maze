
def BFS( maze , queue , visited , currCell , Path):
    for d in 'ESNW' :
        if maze[currCell][d]==True:
            if d=='E':
                childCell=(currCell[0],currCell[1]+1)
            elif d=='W':
                childCell=(currCell[0],currCell[1]-1)
            elif d=='N':
                childCell=(currCell[0]-1,currCell[1])
            elif d=='S':
                childCell=(currCell[0]+1,currCell[1])
            if childCell in visited:
                continue
            queue.append(childCell)
            visited.append(childCell)
            Path[childCell]=currCell   