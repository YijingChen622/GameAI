**The Snowperson Puzzle Description:**

The puzzle is played on a grid board with N squares in the x-dimension and M squares in the y-dimension.
Each state contains the x and y coordinates for the robot, the snowballs, the destination point for the snowperson, and the obstacles.
Each board initially contains three snowballs: a small, medium, and large snowball.
From each state, the robot can move Up, Down, Left, or Right. If a robot moves to the location of an unobstructed snowball, the snowball will move one square in the same direction. Snowballs and the robot cannot pass through walls or obstacles, however.
The robot cannot push more than one snowball at a time. If two snowballs are in succession and the robot is adjacent to the smaller of the two, the robot may push the smaller snowball atop the larger one. However, the robot cannot push a large snowball atop a smaller one, nor can the robot move more than one snowball at a time. Movements that cause a snowball to travel more than one unit of the grid are also illegal.
Each movement is of equal cost. Whether or not the robot is pushing a snowball does not change the cost.
The goal is achieved when there is a stack of three snowballs on the game board and in the destination spot. This stack must have a large snowball on the bottom, a medium snowball in the middle, and a small snowball at the top.

**solution.py**
Where all of your heuristics and anytime algorithms will reside.

**search.py**
This contains default implementations of search algorithms discussed in class.

**snowman.py**
This specifies the search to the snowperson domain, specifically.

**test_problems.py**
This contains some example problems.
