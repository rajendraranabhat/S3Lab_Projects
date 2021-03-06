package com.rajendra.pkg2

object Lab08 {
  case class Point(x: Double, y: Double)

  abstract class Shape()
  case class Circle(center: Point, radius: Double) extends Shape()
  case class Rectangle(lowerLeft: Point, height: Double, width: Double) extends Shape()
  case class Square(lowerLeft: Point, height: Double) extends Shape()
  case class SomeOtherShape(lowerLeft: Point) extends Shape()
  
  class ShapeStretcher {
    def stretch(s: Shape): Shape = s match {
      // FIXME
      case Circle(c,r) => Circle(Point(1,2),3)
      case Rectangle(_,_,_) => Rectangle(Point(2,3),4,5)
      case Square(_,_) => Square(Point(2,3),4)
      case SomeOtherShape(_) => SomeOtherShape(Point(2,3))
      case _ => SomeOtherShape(Point(2,3))
      }
    }
}