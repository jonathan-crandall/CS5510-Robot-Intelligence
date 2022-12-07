class LocationTracker:
    def __init__(self, imageSizeX, imageSizeY):
        self.dimensions = (imageSizeX, imageSizeY)

    def fractionalLocation(self, location):
        return location / self.dimensions

    def getCenter(self, box):
        boxCenterY = (box[1] + box[3]) / 2
        boxCenterX = (box[0] + box[2]) / 2
        return self.fractionalLocation((boxCenterX, boxCenterY))

    def track(self, ballLocations, robotLocation): # Takes a list of xyxy ball locations (with the current and previous at the head of the list) and the xyxy robot location
        current = self.getCenter(ballLocations[0])
        previous = self.getCenter(ballLocations[1])

        m = (current[1] - previous[1]) / (current[0] - previous[0])

        robotCurrent = self.getCenter(robotLocation)

        b = current[1] - (current[0] * m)

        xTarget = (robotCurrent[1] - b) / m

        return robotCurrent[0] - xTarget # Returns a fractional distance for the robot to travel
