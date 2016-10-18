# Change Log
All notable changes to this project will be documented in this file.

## 1.1 - 2016-10-18
### Changed
- No more boundary, birds wrap on edge of screen
- Improved flock dispersal
- Tweaked display
- Tweaked flocking parameters

### Removed
- Mouse avoidance, as it was not particularly interesting

## 1.0 - 2016-09-04
### Added
- Graphical 2d flocking simulation
- Circular boundary
- Birds follow these rules:
 - Avoid getting too close to neighbors (separation)
 - Steer towards neighbors' heading (alignment)
 - Steer towards neighbors' position (cohesion)
 - Avoid the boundary
 - Avoid the mouse
- Space disperses the flock


